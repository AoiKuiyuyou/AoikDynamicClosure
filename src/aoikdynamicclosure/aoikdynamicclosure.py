# coding: utf-8
"""
Implement decorator `dynamic_closure`.
"""
from __future__ import absolute_import

# Standard imports
from functools import wraps
import inspect
import opcode


try:
    # Python 3
    import byteplay3 as byteplay
except ImportError:
    # Python 2
    import byteplay


# Export attributes
__all__ = ('__version__', 'dynamic_closure')

# Version
__version__ = '0.1.0'


def dynamic_closure(func):
    """
    Decorator that enables dynamic binding of closure variables in given \
        function.

    Dynamic binding resolves closure variables in a function using the \
        function's caller function's context, instead of the function's \
        creator function's context.

    :param func:
        Function to be decorated.

    :return:
        A wrapper function that implements the dynamic binding.
    """
    # Store original code object
    orig_code_obj = func.__code__

    # Create code play object
    codeplay = byteplay.Code.from_code(func.__code__)

    # VM instruction `LOAD_DEREF`'s opcode
    opcode_load_deref = opcode.opmap['LOAD_DEREF']

    # VM instruction `LOAD_GLOBAL`'s opcode
    opcode_load_global = opcode.opmap['LOAD_GLOBAL']

    # Binding infos list.
    # Items are tuples. Tuple format is:
    # (
    #     _CODE_ITEM_INDEX,     # Index into `codeplay.code`.
    #     _VARIABLE_NAME,       # Closure variable name.
    # )
    binding_info_s = []

    # For each code item
    for code_item_index, (opcode_obj, oparg) in enumerate(codeplay.code):
        # If the opcode object has `real` attribute
        if hasattr(opcode_obj, 'real'):
            # If the opcode is `LOAD_DEREF` or `LOAD_GLOBAL`.
            # It means the instruction is to load the closure variable's value
            # to the stack.
            if opcode_obj.real in [opcode_load_deref, opcode_load_global]:
                # Create binding info.
                # 1st element: Index into `codeplay.code`.
                # 2nd element: Closure variable name.
                binding_info = (code_item_index, oparg)

                # Add to binding infos list
                binding_info_s.append(binding_info)

    # Create the wrapper function
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        """
        Wrapper function that implements the dynamic binding.
        """
        # Get the caller's frame
        caller_frame = inspect.currentframe().f_back

        # Get the caller's locals dict
        caller_locals = caller_frame.f_locals

        # Get the caller's globals dict
        caller_globals = caller_frame.f_globals

        # If the `__builtins__` key exists in the caller's globals dict
        if '__builtins__' in caller_globals:
            # Get the caller's `builtins` module
            caller_builtins = caller_globals['__builtins__']
        # If the `__builtins__` key not exists in the caller's globals dict
        else:
            # No `builtins` module
            caller_builtins = None

        # For each binding info
        for index, variable_name in binding_info_s:
            # If the variable name is in the caller's locals dict
            if variable_name in caller_locals:
                # Get the variable value from there
                variable_value = caller_locals[variable_name]
            # If the variable name is in the caller's globals dict
            elif variable_name in caller_globals:
                # Get the variable value from there
                variable_value = caller_globals[variable_name]
            # If the variable name is in the caller's `builtins` module
            elif caller_builtins and hasattr(caller_builtins, variable_name):
                # Get the variable value from there
                variable_value = getattr(caller_builtins, variable_name)
            # If the variable name is in none of above
            else:
                # Get error message
                error_msg = "name '{}' is not defined".format(variable_name)

                # Raise error
                raise NameError(error_msg)

            # Modify the load instruction to load the variable value resolved
            # using the function's caller function's context, instead of the
            # function's creator function's context.
            #
            # pylint: disable=no-member
            codeplay.code[index] = (byteplay.LOAD_CONST, variable_value)
            # pylint: enable=no-member

        # Replace the original function's code object
        func.__code__ = codeplay.to_code()

        # Call the original function
        result = func(*args, **kwargs)

        # Restore the original code object
        func.__code__ = orig_code_obj

        # Return the call result
        return result

    # Return the wrapper function
    return wrapper_func
