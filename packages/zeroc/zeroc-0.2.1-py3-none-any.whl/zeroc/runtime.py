import subprocess
from .compiler import compile

def run(code, input_data=None):
    exe = None
    try:
        exe = compile(code)
        result = subprocess.run(
            [exe],
            input=input_data,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Runtime error: {result.stderr}")
            
        return result.stdout
    finally:
        if exe:
            try: os.unlink(exe)
            except: pass