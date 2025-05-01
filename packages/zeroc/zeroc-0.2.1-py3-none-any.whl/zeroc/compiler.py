import subprocess
import tempfile
import os
import shutil

def _check_gcc():
    if not shutil.which('gcc'):
        raise RuntimeError("gcc not found. Install it first")

def compile(code, optimize=False):
    _check_gcc()
    
    with tempfile.NamedTemporaryFile(suffix='.c', delete=False) as f:
        f.write(code.encode('utf-8'))
        src = f.name
    
    exe = tempfile.mktemp()
    
    try:
        cmd = ['gcc', src, '-o', exe]
        if optimize:
            cmd.insert(1, '-O3')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Compilation failed: {result.stderr}")
        
        return exe
    finally:
        os.unlink(src)