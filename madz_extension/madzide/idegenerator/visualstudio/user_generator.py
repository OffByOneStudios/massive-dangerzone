"""madzide:madzide/idegenerator/visualstudio/user_generator.py
@OffbyOne Studios 2014
Generator for .vcxproj.user files
"""

import os
import sys
import madz.module as module
from madz.bootstrap import *

def generate(client_script):

    path = os.path.split(client_script)

    body= ""
    python_loc = get_python_location()
    fragments = {
        "namespace" : "",
        "script_name" : path[1],
        "working" : path[0],
        "python" : get_python_location(),

    }

    plugins = list(map(module.EcsModules.current, module.EcsModules.current[module.Old].entities()))
    for plugin in plugins:
        if plugin.old.executable:
            fragments["namespace"] = plugin.id.namespace

            body += body_template.format(**fragments)


    return user_file_template.format(body)


def get_python_location():
    return sys.executable

user_file_template = \
"""<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
{}
</Project>
"""

body_template = \
"""
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='{namespace}|Win32'">
    <LocalDebuggerCommand>{python}</LocalDebuggerCommand>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='{namespace}|Win32'">
    <LocalDebuggerCommandArguments>{script_name} execute {namespace}</LocalDebuggerCommandArguments>
    <DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>
    <LocalDebuggerWorkingDirectory>{working}</LocalDebuggerWorkingDirectory>
  </PropertyGroup>
"""
