import ast
import inspect
import textwrap
import sys
from functools import wraps
from .patterns import PatternMatcher


def fix_missing_locations(node):
    """
    Recursively set line numbers and column offsets for AST nodes
    that are missing them.
    """
    for child in ast.walk(node):
        if not hasattr(child, 'lineno'):
            child.lineno = 1
        if not hasattr(child, 'col_offset'):
            child.col_offset = 0
    return node


def match(fn=None, *, source=None):
    """
    Decorator that enables pattern matching syntax in Python functions.

    This can be used in two ways:
    1. As a simple decorator: @match
    2. With explicit source code: @match(source="match x: case 1: ...")

    When used in string-based evaluation, always use the second form to provide the source.
    """
    if fn is None:
        # Called as @match(source="...")
        return lambda f: match(f, source=source)

    if source is None:
        # Called as @match with a real function
        try:
            source = inspect.getsource(fn)
            source = textwrap.dedent(source)
        except (OSError, IOError):
            raise ValueError(
                "Could not get source code. When using with exec() or eval(), "
                "you must provide the source code explicitly: @match(source='...')"
            )
    else:
        # Make sure the source code is dedented
        source = textwrap.dedent(source)

    # Parse the source code
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        if sys.version_info < (3, 10) and "match" in source:
            raise SyntaxError(
                "match/case syntax requires Python 3.10+ or the patterna library. "
                "Make sure your function is decorated with @match."
            ) from e
        raise

    # Find the function definition node
    fn_def = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and (fn.__name__ == node.name):
            fn_def = node
            break

    if fn_def is None:
        raise ValueError(f"Could not find function definition for {fn.__name__} in source code")

    # Find all match statements in the function
    match_stmts = [n for n in ast.walk(fn_def) if isinstance(n, ast.Match)]

    if not match_stmts:
        # No match statements found
        return fn

    # Store the AST for later use
    fn._patterna_match_stmts = match_stmts

    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Call the function and get the locals
        result = fn(*args, **kwargs)

        # Get the locals from the last frame
        frame = sys._getframe().f_back
        while frame:
            if frame.f_code is fn.__code__:
                break
            frame = frame.f_back

        if frame is None:
            # Could not find the frame, just return the result
            return result

        locals_dict = frame.f_locals.copy()
        globals_dict = frame.f_globals.copy()

        # Process each match statement
        for match_stmt in fn._patterna_match_stmts:
            # Evaluate the subject expression
            subject_expr = compile(
                ast.Expression(match_stmt.subject),
                "<match_subject>",
                "eval"
            )
            subject_value = eval(subject_expr, globals_dict, locals_dict)

            # Try each case
            for case in match_stmt.cases:
                matcher = PatternMatcher(subject_value)
                bindings = matcher.match(case.pattern)

                if bindings is not None:
                    # We have a match, check guard if present
                    if case.guard:
                        guard_env = globals_dict.copy()
                        guard_env.update(locals_dict)
                        guard_env.update(bindings)

                        guard_expr = ast.Expression(case.guard)
                        compiled_guard = compile(guard_expr, "<guard>", "eval")

                        try:
                            guard_result = eval(compiled_guard, guard_env)
                        except Exception as e:
                            raise RuntimeError(f"Error evaluating guard: {e}")

                        if not guard_result:
                            continue  # Guard failed

                    # Prepare environment for case body
                    exec_env = globals_dict.copy()
                    exec_env.update(locals_dict)
                    exec_env.update(bindings)

                    # Execute the body
                    case_fn_name = "_pattern_case_handler"
                    return_node = ast.Return(
                        value=ast.Name(id="result", ctx=ast.Load())
                    )

                    fake_fn = ast.FunctionDef(
                        name=case_fn_name,
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                            vararg=None,
                            kwarg=None
                        ),
                        body=case.body + [return_node],
                        decorator_list=[],
                        returns=None
                    )

                    mod = ast.Module(body=[fake_fn], type_ignores=[])
                    fix_missing_locations(mod)

                    try:
                        compiled = compile(mod, "<ast>", "exec")
                    except SyntaxError as e:
                        raise SyntaxError(f"Error compiling case body: {e}")

                    try:
                        exec(compiled, exec_env)
                        case_result = exec_env[case_fn_name]()
                        return case_result
                    except Exception as e:
                        raise RuntimeError(f"Error executing case body: {e}")

            # No matches found, continue to next match statement

        # If no match statements were matched, return the original result
        return result

    return wrapper