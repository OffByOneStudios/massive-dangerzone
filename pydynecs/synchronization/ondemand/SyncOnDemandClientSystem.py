"""pydynecs/synchronization/ondemand/SyncOnDemandClientSystem.py
@OffbyOne Studios 2014
This provides on demand access to a remote ECS by pretending to be the system in question.
"""
import threading

import zmq
import pyext

from ... import abstract, serialization
from . import *

class SyncOnDemandClientSystem(abstract.ISystem):
    def __init__(self, sys_class, query_bind=None, sub_bind=None):
        self._sysclass = sys_class
    
        self._query_bind = query_bind
        self._sub_bind = sub_bind
        
        self._serializer = serialization.PyObjFakeSerializer(self)
        
        self._context = None
        self._stopped = False
        self._manager_cache = {}
        self._manager_class_cache = {}
        self._component_cache = {}
        self._index_cache = {}
        
    def start(self):
        if not (self._context is None):
            raise Exception("Client already started")
            
        self._context = zmq.Context()
        
        self._socket_query = self._context.socket(zmq.REQ)
        self._socket_query.connect(str(self._query_bind))
        
        self._sub_thread = self.SubscriberThread(self)
        self._sub_thread.start()
        
        self._sysid = self._query(("meta-id",))
        abstract.system_instances[self._sysid] = self
        self._network_build_managers(force=True)
    
    def stop(self):
        self._stopped = True
    
    class SubscriberThread(threading.Thread):
        def __init__(self, server):
            super().__init__()
            self._server = server

        def _run_start(self):
            self._context = zmq.Context()
            self._socket_sub = self._context.socket(zmq.SUB)
            self._socket_sub.connect(str(self._server._sub_bind))
            
        def run(self):
            self._run_start()
            while not self._server._stopped:
                request = pyext.zmq_busy(
                    lambda: self._socket_sub.recv_pyobj(zmq.NOBLOCK),
                    lambda: self._server._stopped)
                if request is None: continue
                
                result = self._server._sub_invoke(*request)
                self._server.send_pyobj(result)
    
    def _outbound_manager(self, manager):
        return abstract.manager_key(manager)
        
    def _inbound_manager(self, manager):
        return self._manager_cache[manager]
        
    def _outbound_entity(self, entity):
        e = abstract.entity(entity)
        tup = (e.system, e.id, e.group)
        return tup
        
    def _inbound_entity(self, entity):
        return abstract.Entity(*entity)
    
    ### START ISystem
    def pydynecs_system_id(self):
        return self._sysid
        
    def last_entity(self, *args, **kwargs): raise NotImplementedError()
    def new_entity(self, *args, **kwargs): raise NotImplementedError()
    def reclaim_entity(self, *args, **kwargs): raise NotImplementedError()
    def valid_entity(self, *args, **kwargs): raise NotImplementedError()
    
    def get_manager_class(self, key):
        return self._manager_class_cache[abstract.manager_key(key)]
        
    def get_manager(self, key):
        return self._manager_cache[abstract.manager_key(key)]
    
    @classmethod
    def add_manager(self, key, manager_class):
        raise NotImplementedError("Cannot add managers to remote systems.")
    
    def managers(self):
        """Returns key-value-pairs of (key, IComponentManager instance)."""
        return self._manager_cache.items()
    ### END ISystem
    
    ### Networking
    def _network_build_manager(self, key, meta):
        manager_class = None
        try:
            manager_class = self._sysclass.get_manager_class()
        except:
            pass
        
        manager_netclass = {
            "index": SyncOnDemandIndexManager,
            "entity": SyncOnDemandEntityManager,
            "component": SyncOnDemandReadableComponentManager,
        }[meta["manager_classification"].split("-")[0]]
        
        actualclass = None
        if not (manager_class is None):
            class ActualOverrideNetManager(manager_netclass, manager_class):
                _net_meta = meta
                _key = key
            actualclass = ActualOverrideNetManager
        else:
            class ActualNetManager(manager_netclass):
                _net_meta = meta
                _key = key
            actualclass = ActualNetManager
        
        instance = actualclass(self)
        self._manager_class_cache[key] = actualclass
        self._manager_cache[key] = instance
    
    def _network_build_managers(self, force=False):
        if not (force or len(_manager_cache) == 0):
            return
        
        self._manager_cache = {}
        self._entities_cache = {}
        self._component_cache = {}
        self._index_cache = {}
    
        meta_managers = self._query(("meta-managers",))
        for key, manager, meta in meta_managers:
            self._network_build_manager(key, meta)
    
    _sub_invoke = pyext.multimethod(pyext.ArgMatchStrategy(True))
    
    def _query(self, query):
        self._socket_query.send_pyobj(query)
        result = self._socket_query.recv_pyobj()
        return result
    
    def _query_entities(self, manager):
        manager = abstract.manager_key(manager)
        if not manager in self._entities_cache:
            entities = self._query(("manager-entities", self._outbound_manager(manager)))
            self._entities_cache[manager] = set(map(self._inbound_entity, entities))
        return self._entities_cache[manager]
    
    def _query_has(self, manager, entity):
        return entity in self._query_entities(manager)
    
    def _query_component(self, manager, entity):
        mankey = abstract.manager_key(manager)
        key = (mankey, entity)
        if not (key in self._component_cache):
            self._component_cache[key] = self._serializer.unpack(mankey,
                self._query((
                    "manager-component",
                    self._outbound_manager(manager),
                    self._outbound_entity(entity))))
        return self._component_cache[key]
    
    def _query_index(self, manager, index):
        mankey = abstract.manager_key(manager)
        key = (mankey, entity)
        if not (key in self._index_cache):
            self._index_cache[key] = self._inbound_entity(
                self._query((
                    "manager-index",
                    self._outbound_manager(manager),
                    self._serializer.pack(mankey, index))))
        return self._index_cache[key]
    
    @_sub_invoke.method("meta-managers-changed")
    def _sub_invoke_meta_managers_changed(self, cmd):
        self._network_build_managers(force=True)
    
    @_sub_invoke.method("manager-entity-component")
    def _sub_invoke_manager_entity_component(self, cmd, manager, entity, component):
        manager = self._inbound_manager(manager)
        entity = self._inbound_entity(entity)
        
        component = self._serializer.unpack(abstract.manager_key(manager), component)
        
        if isinstance(manager, abstract.IIndexManager):
            self._index_cache[(manager, component)] = entity
        else:
            self._component_cache[(manager, entity)] = component
        
    def _sub_invoke_missing(*args):
        print("WARNING: CLIENT PROTOCOL out of date, malformed publish: ", args[0], args[1])
    _sub_invoke.default=_sub_invoke_missing
        
    