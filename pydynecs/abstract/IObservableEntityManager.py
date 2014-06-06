"""pydynecs/abstract/IObservableEntityManager.py
@OffbyOne Studios 2014
Abstract class for providing entity subscription objects.
"""
import abc

from .IEntityManager import IEntityManager

class IObservableEntityManager(IEntityManager):
    @abc.abstractmethod
    def on_des(self):
        """An object for attaching a callback for when an entity is removed from the manager.
        
        Contains an 'event' object for subscribing to. Has the following signature:
            (manager, entity)
        """
        pass
    
    @abc.abstractmethod
    def on_mod(self):
        """An object for attaching a callback for when an entity is modified on the manager.
        
        Contains an 'event' object for subscribing to. Has the following signature:
            (manager, entity, isnew, expired=None)
        `isnew` is an argument which informs the handler if this entity is new.
        `expired` is an optional argument which represents the expired value,
            for example on component managers it is the value which was just overwritten.
        """
        pass