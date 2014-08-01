"""madzide:madzide/idegenerator/visualstudio/VisualStudioGenerator.py
@OffbyOne Studios 2014
Generates .vcxproj files
"""
import os
import madz.module as module
from madz.config import *
from madz.bootstrap import *


def generate(user_config, project_name, project_guid):
    fragments = {
        "project_name" : project_name,
        "project_guid" : project_guid,
        "project_configuration" : "",
        "project_configuration_type" : "",
        "extension_settings" : "",
        "nmake_configuration" : "",
        "none_include" : "",
        "cl_include" : "",
        "cl_compile" : "",
    }

    external_includes = gen_external_include(user_config)
    plugins = list(map(module.EcsModules.current, module.EcsModules.current[module.Old].entities()))
    for plugin in plugins:
        if plugin.old.executable:
            executable = plugin.id.namespace

            fragments["project_configuration"] += gen_project_configuration(executable)
            fragments["project_configuration_type"] += gen_project_configuration_type(executable)
            fragments["extension_settings"] += gen_extension_settings(executable)
            fragments["nmake_configuration"] += gen_nmake_configuration(executable, external_includes)

        # Sort files
        for f in os.listdir(str(plugin.old.directory.path)):
            if not os.path.isdir(f):
                file_path = os.path.abspath(os.path.join(str(plugin.old.directory.path), f))
                ext = os.path.splitext(file_path)[1]
                if ext in [".h", ".hpp"]:
                    fragments["cl_include"] += gen_cl_include(file_path)
                elif ext in ["c", ".cpp"]:
                    fragments["cl_compile"] += gen_cl_compile(file_path)
                else:
                    fragments["none_include"] += gen_none_include(file_path)

    return template.format(**fragments)

def gen_external_include(user_config):
    res = ""
    for conf in user_config.get_options():
        if isinstance(conf, LanguageConfig):
            for opt in conf.get_options():
                print(opt)
                if isinstance(opt, OptionHeaderSearchPaths):
                    res += ";".join(opt.get_value())
                    res += ";"

        if isinstance(conf, LibraryConfig):
            for opt in conf.get_options():
                if isinstance(opt, OptionHeaderSearchPaths):
                    res += ";".join(opt.get_value())
                    res += ";"

    return res

def gen_project_configuration(namespace):
    return \
"""
    <ProjectConfiguration Include="{0}|Win32">
      <Configuration>{0}</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
""".format(namespace)

def gen_project_configuration_type(namespace):
    return \
"""
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='{}|Win32'" Label="Configuration">
    <ConfigurationType>Makefile</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v120</PlatformToolset>
  </PropertyGroup>
""".format(namespace)

def gen_extension_settings(namespace):
    return \
"""
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='{}|Win32'">
    <Import Project="$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
""".format(namespace)

def gen_nmake_configuration(namespace, include_search_path):
    return \
"""  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='{}|Win32'">
    <NMakeBuildCommandLine>$(SolutionDir)\\build.bat</NMakeBuildCommandLine>
    <NMakeCleanCommandLine>$(SolutionDir)\\clean.bat</NMakeCleanCommandLine>
    <NMakeReBuildCommandLine>$(SolutionDir)\\rebuild.bat</NMakeReBuildCommandLine>
    <NMakePreprocessorDefinitions>WIN32;_DEBUG;$(NMakePreprocessorDefinitions)</NMakePreprocessorDefinitions>
    <IncludePath>$(VC_IncludePath);$(WindowsSDK_IncludePath);</IncludePath>
    <NMakeIncludeSearchPath>{}</NMakeIncludeSearchPath>
  </PropertyGroup>
""".format(namespace, include_search_path)



def gen_none_include(file_path):
    return \
"""    <None Include="{}" />
""".format(file_path)

def gen_cl_include(file_path):
    return \
"""    <ClInclude Include="{}" />
""".format(file_path)

def gen_cl_compile(file_path):
        return \
"""    <ClCompile Include="{}" />
""".format(file_path)

## Project Template
template = \
"""<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="12.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup Label="ProjectConfigurations">
{project_configuration}
  </ItemGroup>
  <PropertyGroup Label="Globals">
    <ProjectGuid>{{{project_guid}}}</ProjectGuid>
    <Keyword>MakeFileProj</Keyword>
    <ProjectName>{project_name}</ProjectName>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
{project_configuration_type}

  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>
{extension_settings}
  <PropertyGroup Label="UserMacros" />
{nmake_configuration}
  <ItemDefinitionGroup>
  </ItemDefinitionGroup>
  <ItemGroup>
  <None Include="build.bat" />
  <None Include="clean.bat" />
  <None Include="rebuild.bat" />
{none_include}
  </ItemGroup>
  <ItemGroup>
{cl_include}
  </ItemGroup>
  <ItemGroup>
{cl_compile}
  </ItemGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
  <ImportGroup Label="ExtensionTargets">
  </ImportGroup>
</Project>
"""
