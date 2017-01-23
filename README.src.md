[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikDynamicClosure
Enable dynamic binding of closure variables.

Dynamic binding resolves closure variables in a function using the function's
caller function's context, instead of the function's creator function's
context.

Tested working with:
- Python 2.7, 3.5

## Table of Contents
[:toc(beg='next', indent=-1)]

## Setup
[:tod()]

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikDynamicClosure
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikDynamicClosure

cd AoikDynamicClosure

python setup.py install
```

## Usage
Code:
```
# coding: utf-8
from aoikdynamicclosure import dynamic_closure


@dynamic_closure
def get_closure_variable():
    """
    Get closure variable `CLOSURE_VARIABLE` defined in the caller's context.
    """
    # Return the closure variable
    return CLOSURE_VARIABLE


def main():
    """
    Main function.
    """
    # Define a variable to be accessed in function `get_closure_variable`
    CLOSURE_VARIABLE = 12345

    # Verify it works
    assert(get_closure_variable() == CLOSURE_VARIABLE)


# If is run as main module
if __name__ == '__main__':
    # Call main function
    exit(main())
```

## License
This project is licensed under MIT.

The dependency libraries byteplay and byteplay3 are licensed under LGPL.
