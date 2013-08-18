from madz.plugin_stub import *

plugin = Plugin(
    #### PluginId attributes:
    ## These describe the PluginId object provided by this plugin. They are
    ## all optional. But if provided they must match the path of the plugin.

    # Fully qualified plugin namespace.
    name            = "feature0_simple_plugin.basic_plugin",
    # SemanticVersion parseable string. May also be a SemanticVersion object
    version         = "0.1.0",
    # Implementation name. Used to differentiate otherwise matching plugins.
    # Can be any string.
    implementation  = "example",

    #### Language:
    ## This just chooses the language. The language can be configured by
    ## the plugins configuration object.
    # The string representing the language to use:
    language="c",
    # The list of libraries to use, the math library is configured in the system_config:
    libraries=["math"],

    #### Configuration:
    ## This describes the configuration to take effect while processing this
    ## plugin. For example, library configuration, compiler prefrence, ect.
    config=PluginConfig([
        
    ]),

    #### Description:
    ## This describes the plugin description used by madz to communicate with
    ## the plugin. It is currently a raw AST.
    description=[
        # A globaly accessible unsgined 32 bit integer
        VariableDefinition("a_global", TypeUInt32),

        # A function provided by the plugin that prints the global.
        VariableDefinition("print_global", 
            # The function doesn't return anything or take any arguments.
            TypeFunction(TypeNone, [])),

        # A function provided by the plugin that preturns a float.
        VariableDefinition("do_math_on_global", 
            # The function returns a 32 bit float.
            TypeFunction(TypeFloat32, [])),
    ],
)
