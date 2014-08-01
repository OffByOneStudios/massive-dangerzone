"""madzide:madzide/idegenerator/visualstudio/filter_generator.py
@OffbyOne Studios 2014
Generator for .vcxproj.filters files
"""

import msilib

import madz.module as module
from madz.bootstrap import *

class GuidGenerator(object):

    def __init__(self):
        self.guid = msilib.UuidCreate()

    @property
    def next_guid(self):
        self.guid = msilib.UuidCreate()
        return self.guid


def cache_namespace(collection, namespace):
    for i in range(len(namespace) + 1):
        collection.add("\\".join(namespace[0:i]))

def generate():
    namespace_cache = set()

    fragments = {
        "filters" : "",
        "none_include" : "",
        "cl_include" : "",
        "cl_compile" : "",
    }

    plugins = list(map(module.EcsModules.current, module.EcsModules.current[module.Old].entities()))
    for plugin in plugins:

        namespace = plugin.id.namespace.split(".")
        if not (plugin.id.implementation is None):
            namespace.append("%28{}%29".format(plugin.id.implementation))

        if not (plugin.id.version is None):
            namespace.append("[{!s}]".format(plugin.id.version))

        plugin_filter = "\\".join(namespace)
        cache_namespace(namespace_cache, namespace)



        for f in os.listdir(str(plugin.old.directory.path)):
            if not os.path.isdir(f):
                file_path = os.path.abspath(os.path.join(str(plugin.old.directory.path), f))
                ext = os.path.splitext(file_path)[1]

                if ext in [".h", ".hpp"]:
                    fragments["cl_include"] += gen_cl_include(file_path, plugin_filter)
                elif ext in ["c", ".cpp"]:
                    fragments["cl_compile"] += gen_cl_compile(file_path, plugin_filter)
                else:
                    fragments["none_include"] += gen_none_include(file_path, plugin_filter)

    guid_generator = GuidGenerator()
    for name in namespace_cache:
        if not name == "":
            fragments["filters"] += gen_filter_entry(name, guid_generator)

    return filter_template.format(**fragments)



def gen_none_include(file_path, filter_name):
    return \
"""    <None Include="{}">
      <Filter>{}</Filter>
    </None>
""".format(file_path, filter_name)

def gen_cl_include(file_path, filter_name):
    return \
"""    <ClInclude Include="{}">
      <Filter>{}</Filter>
    </ClInclude>
""".format(file_path, filter_name)

def gen_cl_compile(file_path, filter_name):
    return \
"""    <ClCompile Include="{}">
      <Filter>{}</Filter>
    </ClCompile>
""".format(file_path, filter_name)


def gen_filter_entry(filter_name, guid_generator):
    return \
"""
<Filter Include="{0}">
      <UniqueIdentifier>{{{1.next_guid}}}</UniqueIdentifier>
</Filter>""".format(filter_name, guid_generator)



filter_template = \
"""<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="12.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
{filters}
  </ItemGroup>
  <ItemGroup>
{none_include}
  </ItemGroup>
  <ItemGroup>
{cl_include}
  </ItemGroup>
  <ItemGroup>
{cl_compile}
  </ItemGroup>
</Project>
"""
