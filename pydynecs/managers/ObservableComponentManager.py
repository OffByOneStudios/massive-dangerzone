"""pydynecs/manager/ObservableComponentManager.py
@OffbyOne Studios 2014
Provides a mutator for applying the observable interfaces to any class.
"""
import abc

import pyext

from .. import abstract

class ObservableComponentManager(abstract.IObservableEntityManager, abstract.IComponentManager):
    event_type=pyext.Event
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_mod = self.event_type()
        self._on_des = self.event_type()

    def on_mod(self): return self._on_mod
    def on_des(self): return self._on_des
    
    def set(self, key, value):
        isnew = True
        expired = None
        if self.has(key):
            isnew = False
            expired = self.get(key)
        super().set(key, value)
        self._on_mod(self, key, isnew, expired)

    def des(self, key):
        self._on_des(self, key)
        super().des(key)