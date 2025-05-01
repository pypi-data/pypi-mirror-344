# ZeroC - Simple C Runner

Run C code directly from Python with seamless integration.

## Installation

```bash
pip install zeroc
```

## Basic Usage

```python
from zeroc import run

# Simple C program execution
output = run("""
#include <stdio.h>
int main() {
    printf("Hello from C!\\n");
    return 0;
}
""")

print(output)  # "Hello from C!"
```

### Advanced Usage

#### With Input/Output

```python
# Pass input to C program
result = run("""
#include <stdio.h>
int main() {
    char name[100];
    scanf("%s", name);
    printf("Hello, %s!\\n", name);
    return 0;
}
""", input_data="World")

print(result)  # "Hello, World!"
```

### Web Framework Integrations

#### Flask Example

```python
from flask import Flask, request, jsonify
from zeroc import run

app = Flask(__name__)

@app.route('/run-c', methods=['POST'])
def execute_c():
    try:
        code = request.json.get('code')
        input_data = request.json.get('input', '')
        output = run(code, input_data=input_data)
        return jsonify({"output": output})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()
```

### Django Example

```python
# views.py
from django.http import JsonResponse
from zeroc import run

def run_c_code(request):
    if request.method == 'POST':
        try:
            code = request.POST.get('code')
            input_data = request.POST.get('input', '')
            output = run(code, input_data=input_data)
            return JsonResponse({'output': output})
        except RuntimeError as e:
            return JsonResponse({'error': str(e)}, status=400)
```

### FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from zeroc import run

app = FastAPI()

@app.post("/execute")
async def execute(code: str, input_data: str = ""):
    try:
        output = run(code, input_data=input_data)
        return {"output": output}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Performance Optimization

```python
# Enable compiler optimizations (-O3 flag)
from zeroc.compiler import compile
from subprocess import run as subprocess_run

exe_path = compile("""
#include <stdio.h>
int main() {
    // Performance-critical code
    for(int i=0; i<1000000; i++) {
        printf("%d\\n", i);
    }
    return 0;
}
""", optimize=True)

# Run the optimized executable
result = subprocess_run([exe_path], capture_output=True, text=True)
print(result.stdout)
```

### Jupyter Notebook Usage

```python
from IPython.display import display, Markdown
from zeroc import run

def run_c_in_notebook(code):
    try:
        output = run(code)
        display(Markdown(f"```\\n{output}\\n```"))
    except RuntimeError as e:
        display(Markdown(f"**Error:** {e}"))

run_c_in_notebook("""
#include <stdio.h>
int main() {
    printf("Notebook integration works!\\n");
    return 0;
}
""")
```

### Requirements

#### GCC compiler must be installed:

- Linux: *sudo apt-get install gcc*

- Mac: *xcode-select --install*

- Windows: *Install MinGW* or use *WSL*

License

MIT

**Author**: [Fidal PalamParambil](https://github.com/mrfidal)


