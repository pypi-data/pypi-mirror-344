import os
import subprocess
import math
import sys
from typing import Union, List, Tuple

class Utils:
    def __init__(self):
        self.PATH_TO_THONNYPYTHON = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Programs\Thonny\python.exe')
        self.PATH_TO_THONNYLIBFOLDER = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Programs\Thonny\Lib\site-packages')
        
        if self.PATH_TO_THONNYLIBFOLDER not in sys.path:
            sys.path.append(self.PATH_TO_THONNYLIBFOLDER)
            
    def Check(self, library: str, install: bool, args: Union[List[Union[str, Tuple[str, str]]], str]) -> bool:
        i_s = ""
        try:
            if isinstance(args, list):
                imports = []
                for i in args:
                    if isinstance(i, tuple):
                        imports.append(f"{i[0]} as {i[1]}")
                    else:
                        imports.append(i)
                i_s = f"from {library} import {', '.join(imports)}"
            elif isinstance(args, str):
                arg = f" as {args}" if args else ""
                i_s = f"import {library}{arg}"
            else:
                raise ValueError("Invalid type of values")
            print(i_s)
            exec(i_s, globals())
            
            if not ImportError or Exception:
                return True

        except ImportError:
            print("The library is not installed, if you choosed True in second argument, then it will install the package or library automatically")
            if install:
                print("INSTALLING IN THONNY...")
                result = subprocess.run([self.PATH_TO_THONNYPYTHON, '-m', 'pip', 'install', '--target', self.PATH_TO_THONNYLIBFOLDER, library],
                               capture_output=True,
                               text=True)
                if result.returncode != 0:
                    print(f"Installation failed. Error: {result.stderr}")
                    return False
                print("Installation successful. Re-attempting import...")
            
            try:
                exec(i_s, globals())
                return True
            except:
                print("The installation of library failed, exiting the program...")
                return False
        
util = Utils()
a = util.Check("colorama", True, [("init", "c_init"), "Fore", "Style"])
b = util.Check("pygame", True, "p")
print(a, b)

c_init()
print(f"{Fore.RED}hi")