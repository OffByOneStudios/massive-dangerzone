"""madzide:madzide/idegenerator/visualstudio/batch_generator.py
@OffbyOne Studios 2014
Interface for generating batch files to bridge to nmake project.
"""


def generate(client_script):
    build = "python {} command make\n".format(client_script)
    clean = "python {} command clean\n".format(client_script)
    rebuild = "python {} command clean make\n".format(client_script)

    return [build, clean, rebuild]
