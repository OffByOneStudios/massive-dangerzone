"""pydynecs/synchronization/ondemand/SyncOnDemandClientSystem.py
@OffbyOne Studios 2014
This provides on demand access to a remote ECS by pretending to be the system in question.
"""
import threading

import zmq
import pyext

from ... import abstract
from . import *

class SyncOnDemandClientSystem(abstract.ISystem):
    def __init__(self, sys_class, query_bind_str=None, sub_bind_str=None):
        self._sysclass = sys_class
    
        self._query_bind_str = query_bind_str
        self._sub_bind_str = sub_bind_str
        
        self._serializer = PyObjFakeSerializer(self)
        
        self._manager_cache = {}
        self._component_cache = {}
        self._index_cache = {}
        
    def start(self):
        if not (self._context is None):
            raise Exception("Server already started")
            
        self._context = zmq.Context()
        
        self._socket_query = self._context.socket(zmq.REQ)
        self._socket_query.connect(self._sub_bind_str)
        
        self._query_thread = self.SubscriberThread(self)
        
        self._network_build_managers(force=True)
    
    def stop(self):
        self._stopped = True
    
    class SubscriberThread(threading.Thread):
        def __init__(self, server):
            super().__init__()
            self._server = server

        def start(self):
            self._context = zmq.Context()
            self._socket_sub = self._context.socket(zmq.SUB)
            self._socket_sub.connect(self._query_bind_str)
            
        def run(self):
            while not self._server._stopped:
                request = pyext.zmq_busy(
                    lambda: self._socket_sub.recv_pyobj(zmq.NOBLOCK),
                    lambda: self._server._stopped)
                result = self._server._sub_invoke(*request)
                self._server.send_pyobj(result)
    
    def _outbound_manager(self, manager):
        return abstract.manager_key(manager)
        
    def _inbound_manager(self, manager):
        return self._manager_cache[manager]
        
    def _outbound_entity(self, entity):
        return entity
        
    def _inbound_entity(self, entity):
        return entity
    
    ### START ISystem
    def get_manager(self, key):
        return self._manager_cache[key]
    
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
            manager_class = self._sysclass.get_manager_class
        except:
            pass
        
        manager_netclass = {
            "index": SyncOnDemandIndexManager,
            "entity": SyncOnDemandEntityManager,
            "component": SyncOnDemandComponentManager,
        }[meta["manager_classification"].split("-")[0]]
        
        if not (manager_class is None):
            class ActualOverrideNetManager(manager_netclass, manager_class):
                _meta = meta
            instance = ActualOverrideNetManager(self, key)
        else:
            class ActualNetManager(manager_netclass):
                _meta = meta
            instance = ActualNetManager(self, key)
            
        self._manager_cache[key] = instance
    
    def _network_build_managers(self, force=False):
        if not (force or len(_manager_cache) == 0):
            return
        
        self._manager_cache = {}
        self._component_cache = {}
        self._index_cache = {}
    
        meta_managers = self._query(("meta-managers",))
        for key, manager, meta in meta_managers:
            self._network_build_manager(key, meta)
    
    _sub_invoke = pyext.multimethod(pyext.ArgMatchStrategy(True))
    
    def _query(self, query):
        self._query_socket.send_pyobj(query)
        result = pyext.zmq_busy(lambda: self._query_socket.recv_pyobj(zmq.NOBLOCK))
        return result
        
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
        
    