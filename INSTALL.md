
## Requirements
=========
In all cases, the following are required:
* Python3.3 or later: https://www.python.org/downloads/
* pyzmq: https://github.com/zeromq/pyzmq
* watchdog : https://pypi.python.org/pypi/watchdog

One of the following c/c++ toolchains/runtimes is required

#### Windows
Madz supports development on windows using both MinGW and MSVC. A few caveats:
* OffByOne Studios makes heavy use of C++11 features. Therefore the MSVC runtime in VisualStudio-2010 Express or later is recommended

#### Linux
Madz supports development on linux using GCC and Clang/LLVM. As with windows Ob1's projects make use of C++11 features, so recent versions of the toolchain are recomended.'

## Configuring the Example
Before the example can be run in /examples/simple_example the user config must be configured for you system. Fill in the requisite information for
* user_os_choice
* user_compiler_preference
* user_runtime_python

for your system

```python
from madz.user_config import *

# This is an example of a user config file. These are used to provide
# machine specific information to madz.

# Choose operating system
user_os_choice = { "windows" : 0, "linux" : 1, "macosx" : 2}["windows"]
# Prefered compiler. Options cl, mingw, gcc, clang
user_compiler_preference = "mingw"

# The Python3 installation used to run madz
user_runtime_python = ["C:\\Python33", "/usr/bin/python34"][user_os_choice]
```

## Building the Example:
Using two terminals, of whom the former has access to your compiler toolchain from it's path (ie run vcvarsall or use the developer console for MSVC)
* Launch the daemon in the former:

```python main.py daemon```

* Perform a build command in the latter:

```python main.py command make```

## Running the example:
Again with the daemon running execute in your client shell the execute command:

```python main.py execute "target"```

Target is the name of the executable's namespace in the executables folder.
