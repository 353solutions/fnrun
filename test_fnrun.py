from tempfile import NamedTemporaryFile
from fnrun import run_func

code = '''
factor = 2.3


def norm(val):
    print(f'normalizing {val}')
    return val / factor
'''


def test_fnrun():
    tmp = NamedTemporaryFile(suffix='.py')
    tmp.write(code.encode('utf-8'))
    tmp.flush()
    val, factor = 3, 10
    args, ctx = [val], {'factor': factor}

    retval, stdout = run_func(tmp.name, 'norm', args, ctx=ctx)
    assert round(retval, 6) == round(val / factor, 6), 'bad return value'
    expected_out = f'normalizing {val}'
    assert expected_out == stdout.strip(), 'bad stdout'
