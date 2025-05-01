import os
import subprocess
import sys
import importlib
from typing import Union, List, Tuple

class Utils:
    def __init__(self):
        self.PATH_TO_THONNYPYTHON = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Programs\Thonny\python.exe')
        self.PATH_TO_THONNYLIBFOLDER = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Programs\Thonny\Lib\site-packages')
        
        if self.PATH_TO_THONNYLIBFOLDER not in sys.path:
            sys.path.append(self.PATH_TO_THONNYLIBFOLDER)
            
    def Check(self, library: str, install: bool, args: Union[List[Union[str, Tuple[str, str]]], str]) -> bool:
        try:
            # First attempt to import
            if isinstance(args, list):
                imports = []
                for i in args:
                    if isinstance(i, tuple):
                        imports.append(f"{i[0]} as {i[1]}")
                    else:
                        imports.append(i)
                import_statement = f"from {library} import {', '.join(imports)}"
            elif isinstance(args, str):
                import_statement = f"import {library} as {args}" if args else f"import {library}"
            else:
                raise ValueError("Invalid args type")
            
            print(f"Import attempt: {import_statement}")
            exec(import_statement, globals())
            return True

        except ImportError as e:
            print(f"Import failed: {str(e)}")
            if install:
                print(f"Installing {library}...")
                result = subprocess.run(
                    [self.PATH_TO_THONNYPYTHON, '-m', 'pip', 'install', '--target', self.PATH_TO_THONNYLIBFOLDER, library],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"Install failed: {result.stderr}")
                    return False
                    
                # Clear module cache and re-import
                sys.modules.pop(library, None)
                importlib.invalidate_caches()
                
                try:
                    print("Re-attempting import...")
                    exec(import_statement, globals())
                    return True
                except Exception as e:
                    print(f"Final import failed: {str(e)}")
                    return False
            return False