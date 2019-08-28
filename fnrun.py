import importlib.util as imputil
from io import StringIO
from contextlib import redirect_stdout
from pathlib import Path


def file_module_name(file_name):
    """
    >>> file_module_name('/path/to/tok.py')
    'tok'
    """
    path = Path(file_name)
    mod_name = path.name
    if path.suffix:
        mod_name = mod_name[:-len(path.suffix)]
    return mod_name


def load_module(file_name):
    mod_name = file_module_name(file_name)
    spec = imputil.spec_from_file_location(mod_name, file_name)
    mod = imputil.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_func(file_name, name='main', args=None, kw=None, ctx=None):
    """Run a function from file with args and kw.

    ctx values are injected to module during function run time.
    """
    mod = load_module(file_name)
    fn = getattr(mod, name)  # Might raise if name not found

    if ctx is not None:
        for attr, value in ctx.items():
            setattr(mod, attr, value)

    args = [] if args is None else args
    kw = {} if kw is None else kw

    stdout = StringIO()
    with redirect_stdout(stdout):
        val = fn(*args, **kw)

    return val, stdout.getvalue()
