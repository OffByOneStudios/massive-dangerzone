"""pydynecs/synchronization/ondemand/SyncOnDemandServer.py
@OffbyOne Studios 2014
This provides the server for on demand access to an ECS.
"""

import threading

import zmq
import pyext

from ... import abstract

class SyncOnDemandServer(object):
    def __init__(self, system, query_bind=pyext.ZmqBind(), sub_bind=pyext.ZmqBind()):
        self.query_binding = query_bind
        self.sub_binding = sub_bind
        
        self.system = system.current
        
        self._context = None
        self._serializer = PyObjFakeSerializer(self)
        
        self._stopped = False
        
    def start(self):
        if not (self._context is None):
            raise Exception("Server already started")
            
        self._context = zmq.Context()
        
        self._socket_sub = self._context.socket(zmq.PUB)
        self._socket_sub.bind(self.sub_bind)
        
        self._query_thread = self.QueryThread(self)
    
    def stop(self):
        self._stopped = True
    
    class QueryThread(threading.Thread):
        def __init__(self, server):
            super().__init__()
            self._server = server

        def start(self):
            self._context = zmq.Context()
            self._socket_query = self._context.socket(zmq.REP)
            self._server.query_bind.bind(self._socket_query)
            
        def run(self):
            while not self._server._stopped:
                request = pyext.zmq_busy(
                    lambda: self._socket_query.recv_pyobj(zmq.NOBLOCK),
                    lambda: self._server._stopped)
                result = self._server.invoke(*request)
                self._server.send_pyobj(result)
    
    def _outbound_manager(self, manager):
        return abstract.manager_key(manager)
        
    def _inbound_manager(self, manager):
        return self._system[manager]
        
    def _outbound_entity(self, entity):
        return entity
        
    def _inbound_entity(self, entity):
        return entity
    
    ## Invoke Methods
    
    invoke = pyext.multimethod(pyext.ArgMatchStrategy(True))
    
    @invoke.method("meta-managers")
    def invoke_meta_managers(self, cmd):
        """Returns manager listing information."""
        def expand(kvp, self=self):
            key, value = kvp
            return (key, self._outbound_manager(value), value.meta())
            
        return list(map(expand, self.system.items()))
    
    @invoke.method("manager-entities")
    def invoke_manager_entities(self, cmd, manager):
        """Returns a list entities."""
        manager = self._inbound_manager(manager)
        
        return list(map(self._outbound_entity, manager.entities()))
    
    @invoke.method("manager-component")
    def invoke_manager_component(self, cmd, manager, entity):
        """Returns a component for a given entity/manager."""
        manager = self._inbound_manager(manager)
        entity = self._inbound_entity(entity)
        
        return self._serializer.pack(manager[entity])
    
    @invoke.method("entity-components")
    def invoke_entity_components(self, cmd, entity):
        """Returns all components for a given entity."""
        entity = self._inbound_entity(entity)
    
        return list(map(lambda co: self._serializer.pack(*co), self._system.components_of(entity)))
    
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
    