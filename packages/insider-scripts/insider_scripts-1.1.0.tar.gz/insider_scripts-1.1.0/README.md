# Insider Scripts

## Purpose

Run python scripts from inside a package without relative import error.

Often when working on a project, one might want scripts to be callable from anywhere within the tree of the project.

For instance with the following layout:

```
your_package/
|── scriptX.py
|── A_folder/
|   ├── A.py
|   ├── C.py
|   └── scriptA.py
|── B_folder/
|   └── B.py
```

The following import in **C.py** will fail if the **scriptA.py** imports **C** and is run from inside the package:
```python
from .A import A # relative import with no known parent package.
from ..B_folder.B import B # relative import with no known parent package.
```

Absolute import of A would work:
```python
import A.A
```
but it would the fail if **scriptX.py** imports **C**.

Using the trick of adding a path to sys.path will work most of the time, however if you have the following situation:

**C.py**
```python
import sys
from importlib import Path
sys.path.append(Path(__file__).parent.parent)
from B import B

def make_B() -> B:
  return B()
```

**scriptX.py**
```python
from A_folder.C import make_B
from B_folder.B import B
b = make_B()
print(isinstance(b, B)) # prints False
```

**scriptX.py** will print False because *make_B* produces an instance of *B.B* while the imported *B* is an instance of *B_folder.B.B*.

The best solution I found to solve those issue resulted in the creation of the **insider_scripts** package.


## Installation

```
pip install insider_scripts
```

## Usage

Import the function define script from the insider_scripts and call it with either the depth of the script in the package, or the path of the package root.

### Example layout

```
your_package/
|── A_folder/
|   ├── A.py
|   └── script.py
|── B_folder/
|   └── B.py
```

### Example script:\n"

```python
from pathlib import Path
from insider_scripts import define_script
define_script(1) # or define_script(Path(__file__).parent.parent) or define_script(-1)

from .A import A
from ..B_folder.B import B
```