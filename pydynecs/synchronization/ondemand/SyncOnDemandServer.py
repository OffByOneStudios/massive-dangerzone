"""pydynecs/synchronization/ondemand/SyncOnDemandServer.py
@OffbyOne Studios 2014
This provides the server for on demand access to an ECS.
"""

import threading

import zmq
import pyext

from ... import abstract, serialization

class SyncOnDemandServer(object):
    def __init__(self, system, query_bind=None, sub_bind=None):
        self.query_bind = query_bind or pyext.ZmqBind()
        self.sub_bind = sub_bind or pyext.ZmqBind()
        
        self.system = system.current
        
        self._serializer = serialization.PyObjFakeSerializer(self)
        
        self._context = None
        self._stopped = False
        
    def start(self):
        if not (self._context is None):
            raise Exception("Server already started")
            
        self._context = zmq.Context()
        
        self._socket_sub = self._context.socket(zmq.PUB)
        self.sub_bind.bind(self._socket_sub)
        
        self._query_thread = self.QueryThread(self)
        self._query_thread.start()
    
    def stop(self):
        self._stopped = True
    
    class QueryThread(threading.Thread):
        def __init__(self, server):
            super().__init__()
            self._server = server

        def _run_start(self):
            self._context = zmq.Context()
            self._socket_query = self._context.socket(zmq.REP)
            self._server.query_bind.bind(self._socket_query)
            
        def run(self):
            self._run_start()
            while not self._server._stopped:
                request = pyext.zmq_busy(
                    lambda: self._socket_query.recv_pyobj(zmq.NOBLOCK),
                    lambda: self._server._stopped,
                    sleep_time=0.001)
                if request is None: continue
                
                result = self._server.invoke(self._server, *request)
                self._socket_query.send_pyobj(result)
    
    def _outbound_manager(self, manager):
        return abstract.manager_key(manager)
        
    def _inbound_manager(self, manager):
        return self.system[manager]
        
    def _outbound_entity(self, entity):
        e = abstract.entity(entity)
        tup = (e.system, e.id, e.group)
        return tup
        
    def _inbound_entity(self, entity):
        return abstract.Entity(*entity)
    
    ## Invoke Methods
    
    invoke = pyext.multimethod(pyext.ArgMatchStrategy(True))
    
    @invoke.method("meta-id")
    def invoke_meta_id(self, cmd):
        """Returns system id."""
        return self.system.pydynecs_system_id()
    
    @invoke.method("meta-managers")
    def invoke_meta_managers(self, cmd):
        """Returns manager listing information."""
        def expand(kvp, self=self):
            key, value = kvp
            return (key, self._outbound_manager(value), value.meta())
            
        return list(map(expand, self.system.managers()))
    
    @invoke.method("manager-entities")
    def invoke_manager_entities(self, cmd, manager):
        """Returns a list entities."""
        manager = self._inbound_manager(manager)
        
        return list(map(self._outbound_entity, manager.entities()))
    
    @invoke.method("manager-component")
    def invoke_manager_component(self, cmd, manager, entity):
        """Returns a component for a given entity/manager."""
        key = abstract.manager_key(manager)
        manager = self._inbound_manager(manager)
        entity = self._inbound_entity(entity)
        
        return self._serializer.pack(key, manager[entity])
    
    @invoke.method("manager-index")
    def invoke_manager_index(self, cmd, manager, index):
        """Returns a component for a given entity/manager."""
        index = self._serializer.unpack(abstract.manager_key(manager), index)
        manager = self._inbound_manager(manager)
        
        if not (index in manager):
            return None
        
        return self._outbound_entity(manager[index])
    
    @invoke.method("entity-components")
    def invoke_entity_components(self, cmd, entity):
        """Returns all components for a given entity."""
        entity = self._inbound_entity(entity)
    
        return list(map(lambda co: self._serializer.pack(*co), self.system.components_of(entity)))
    
    ## Publish Methods
    
    def pub_meta_managers_changed(self):
        """Publish a manger list modified notification."""
        self._socket_sub.send_pyobj(("meta-managers-changed",))
    
    def pub_manager_entity_changed(self, manager, entity, components):
        """Publish a manager/entity/component modified tuple."""
        self._socket_sub.send_pyobj(("manager-entity-component", 
            self._outbound_manager(manager),
            self.outbound_entity(entity),
            self.serializer.pack(abstract.manager_key(manager), component)))
    