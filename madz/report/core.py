"""madz/report/core.py
@OffbyOne Studios 2014
Core features of report subsystem.
"""

from pydynecs import *
import pyext

## Ecs System
@system_syntax
class EcsReport(System): pass
EcsReport.current = EcsReport()
manager = manager_decorator_for(EcsReport)

## Core Components:

@manager
class Active(CoercingComponentManager, BasicComponentManager):
    coerce = bool

@manager
class Children(CoercingComponentManager, BasicComponentManager):
    coerce = list

@manager
class Parent(CheckedComponentManager, BasicComponentManager):
    def check(self, value):
        return EcsReport.current.valid_entity(value)

## Core Meta Components:

@manager
class Time(BasicComponentManager):
    pass

@manager
class ModifiedTime(BasicComponentManager):
    pass

@manager
class ReportLevel(CheckedComponentManager, BasicComponentManager):
    def check(self, value):
        return self.DEBUG <= value <= self.CRITICAL
    DEBUG=0
    INFO=1
    NOTICE=2
    WARNING=3
    ERROR=4
    CRITICAL=5

@manager
class ReportingModule(BasicComponentManager):
    # Tuple of (True, entity)
    pass

## Simple Report Data Components:

@manager
class Message(CoercingComponentManager, BasicComponentManager):
    coerce = str

## Polymorphic Functions:

