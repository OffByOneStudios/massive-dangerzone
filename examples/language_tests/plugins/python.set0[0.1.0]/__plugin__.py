from madz.stub import *
from madz.languages.python.config import *
from madz.plugin_config import *

plugin = Plugin(
    name="python.set0",
    version="0.1.0",

    language="python",

    config=PluginConfig([
        OptionLanguageConfig(
            Config([
                OptionHeaderSearchPaths(["/usr/include/python2.7/"])
            ])),
    ]),

    description=[
        VariableDefinition("test0_i64", TypeInt64),     # Value 1
        VariableDefinition("test0_i32", TypeInt32),     # Value 2
        VariableDefinition("test0_i16", TypeInt16),     # Value 3
        VariableDefinition("test0_i8", TypeInt8),       # Value 4

        VariableDefinition("test0_u64", TypeUInt64),    # Value 5
        VariableDefinition("test0_u32", TypeUInt32),    # Value 6
        VariableDefinition("test0_u16", TypeUInt16),    # Value 7
        VariableDefinition("test0_u8", TypeUInt8),      # Value 8

        VariableDefinition("test0_f64", TypeFloat64),   # Value .1
        VariableDefinition("test0_f32", TypeFloat32),   # Value .2

        VariableDefinition("test0_vp", TypePointer(TypeNone)), # Value 0 (null pointer)

        VariableDefinition("test1_var", TypeFloat32),   # Value 0.0
        VariableDefinition("test1_func",                # Sets test1_var to 16.0
            TypeFunction(
                TypeNone, [])),

        VariableDefinition("test2_func0",                # Returns Value 9
            TypeFunction(
                TypeInt32, [])),

        VariableDefinition("test2_func1",                # Returns Addition of Arguments
            TypeFunction(
                TypeInt32, [
                TypeFunctionArgument("A", TypeInt32),
                TypeFunctionArgument("B", TypeInt32)
            ])),

        VariableDefinition("test3_var0", TypeFloat32),  # Value 0.0
        VariableDefinition("test3_var1", TypeFloat32),  # Value 1.0
        VariableDefinition("test3_var_pointer", TypeFloat32.Pointer()), # Points to test3_var0
        VariableDefinition("test3_func",                # Points test3_var_pointer to test3_var1
            TypeFunction(
                TypeNone, [])),

        TypeDeclaration("test4_type_simple", TypeInt32),
        VariableDefinition("test4_var_simple", NamedType("test4_type_simple")), # Value 1
        TypeDeclaration("test4_type_struct",
            TypeStruct({
                "var": TypeInt32,
                "varp": TypeInt32.Pointer(),
            })),
        VariableDefinition("test4_var_struct", "test4_type_struct"), # var Value = 1, varp points to var
        TypeDeclaration("test4_type_array", TypeArray(TypeInt32, 16)),
        VariableDefinition("test4_var_array", "test4_type_array"), # Array Value 1-16

        TypeDeclaration("test5_struct",
            TypeStruct({
                "a": TypeArray(TypeInt32, 32),
                "b": TypeUInt8,
            })),
        VariableDefinition("test5_func",
            TypeFunction(
                "test5_struct", [
                TypeFunctionArgument("a", TypeArray(TypeInt32, 32)),
                TypeFunctionArgument("b", TypeUInt8)
            ])),
    ]
)
