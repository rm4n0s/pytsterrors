import json
from pytsterrors import TSTError, json_to_tst_error


def test_tst_error():
    def fn1():
        raise TSTError("fn1-failed", "failed fn1")

    def fn2():
        fn1()

    def fn3():
        fn2()

    def fn4() -> TSTError | None:
        try:
            fn3()
        except TSTError as err:
            return err

    err = fn4()
    assert err != None
    all_trace = ['<module>', 'console_main', 'main', 'HookCaller.__call__', 'PytestPluginManager._hookexec', '_multicall',
                 'pytest_cmdline_main', 'wrap_session', '_main', 'HookCaller.__call__', 'PytestPluginManager._hookexec',
                 '_multicall', 'pytest_runtestloop', 'HookCaller.__call__', 'PytestPluginManager._hookexec', '_multicall',
                 'pytest_runtest_protocol', 'runtestprotocol', 'call_and_report', 'from_call', '<lambda>', 'HookCaller.__call__',
                 'PytestPluginManager._hookexec', '_multicall', 'pytest_runtest_call', 'Function.runtest', 'HookCaller.__call__',
                 'PytestPluginManager._hookexec', '_multicall', 'pytest_pyfunc_call',
                 'test_tst_error', 'fn4', 'fn3', 'fn2', 'fn1.fn1-failed']
    assert err.func_trace() == all_trace
    assert err.routes(*all_trace)
    assert err.sub_routes('fn3', 'fn2', 'fn1.fn1-failed')
    assert err.sub_routes('test_tst_error', 'fn4',
                          'fn3', 'fn2', 'fn1.fn1-failed')
    expected_msg = "failed fn1"
    assert err.message() == expected_msg
    assert err.__str__() == expected_msg
    expected_tag = 'fn1-failed'
    assert err.tag() == expected_tag
    expected_dict = {
        "func_trace": all_trace,
        "message": expected_msg,
        "tag": expected_tag
    }
    assert err.to_dict() == expected_dict
    expected_json = json.dumps(expected_dict)
    assert err.to_json() == expected_json
    assert json_to_tst_error(err.to_json()) == err


def test_tst_error_creation():
    err = TSTError("fn1-failed", "failed fn1", can_inspect=False)
    assert err != None
    assert err.func_trace() == []
    expected_msg = "failed fn1"
    assert err.message() == expected_msg
    assert err.__str__() == expected_msg
    expected_tag = 'fn1-failed'
    assert err.tag() == expected_tag
    all_funcs = ['test_tst_error', 'fn4', 'fn3', 'fn2', 'fn1.fn1-failed']
    err.set_func_trace(all_funcs)
    assert err.routes(*all_funcs)
    assert err.sub_routes('fn3', 'fn2', 'fn1.fn1-failed')
    assert err.sub_routes('fn1.fn1-failed')
    expected_dict = {
        "func_trace": all_funcs,
        "message": expected_msg,
        "tag": expected_tag
    }
    assert err.to_dict() == expected_dict
    expected_json = json.dumps(expected_dict)
    assert err.to_json() == expected_json
    assert json_to_tst_error(err.to_json()) == err


def test_tst_error_with_params():
    from collections import Counter
    expected_cnt = Counter('aaa')

    def fn1(a: int):
        raise TSTError("fn1-failed", "failed fn1")

    def fn2(b: int, c: str):
        fn1(b)

    def fn3(d: int, e: str, cnt: Counter):
        fn2(d, e)

    def fn4() -> TSTError | None:
        try:
            fn3(3, 'haha', expected_cnt)
        except TSTError as err:
            return err

    err = fn4()
    assert err != None
    all_trace = ['<module>', 'console_main', 'main', 'HookCaller.__call__', 'PytestPluginManager._hookexec', '_multicall',
                 'pytest_cmdline_main', 'wrap_session', '_main', 'HookCaller.__call__', 'PytestPluginManager._hookexec',
                 '_multicall', 'pytest_runtestloop', 'HookCaller.__call__', 'PytestPluginManager._hookexec', '_multicall',
                 'pytest_runtest_protocol', 'runtestprotocol', 'call_and_report', 'from_call', '<lambda>', 'HookCaller.__call__',
                 'PytestPluginManager._hookexec', '_multicall', 'pytest_runtest_call', 'Function.runtest', 'HookCaller.__call__',
                 'PytestPluginManager._hookexec', '_multicall', 'pytest_pyfunc_call',
                 'test_tst_error_with_params', 'fn4', 'fn3', 'fn2', 'fn1.fn1-failed']
    assert err.func_trace() == all_trace
    assert err.routes(*all_trace)
    assert err.sub_routes('fn3', 'fn2', 'fn1.fn1-failed')
    expected_msg = "failed fn1"
    assert err.message() == expected_msg
    assert err.__str__() == expected_msg
    expected_tag = 'fn1-failed'
    assert err.tag() == expected_tag
    expected_dict = {
        "func_trace": all_trace,
        "message": expected_msg,
        "tag": expected_tag
    }
    assert err.to_dict() == expected_dict


def test_tst_error_threading():
    import threading
    err: TSTError | None = None

    def fn1():
        raise TSTError("fn1-failed", "failed fn1")

    def fn2():
        fn1()

    def fn3():
        fn2()

    def fn4():
        try:
            fn3()
        except TSTError as e:
            nonlocal err
            err = e

    t1 = threading.Thread(target=fn4)
    try:
        t1.start()
        t1.join()
    except TSTError as e:
        err = e

    assert err != None
    all_trace = ['Thread._bootstrap', 'Thread._bootstrap_inner',
                 'Thread.run', 'fn4', 'fn3', 'fn2', 'fn1.fn1-failed']
    assert err.func_trace() == all_trace
    assert err.routes(*all_trace)
    assert err.sub_routes('fn3', 'fn2', 'fn1.fn1-failed')
    assert err.sub_routes('fn1.fn1-failed')
    expected_msg = "failed fn1"
    assert err.message() == expected_msg
    assert err.__str__() == expected_msg
    expected_tag = 'fn1-failed'
    assert err.tag() == expected_tag
    expected_dict = {
        "func_trace": all_trace,
        "message": expected_msg,
        "tag": expected_tag
    }
    assert err.to_dict() == expected_dict
    expected_json = json.dumps(expected_dict)
    assert err.to_json() == expected_json
    assert json_to_tst_error(err.to_json()) == err



def test_tst_error_fuzzy_routes():
    def fn1():
        raise TSTError("fn1-failed", "failed fn1")

    def fn2():
        fn1()

    def fn3():
        fn2()

    def fn4() -> TSTError | None:
        try:
            fn3()
        except TSTError as err:
            return err

    err = fn4()
    assert err != None
    all_trace = ['<module>', 'console_main', 'main', 'HookCaller.__call__', 'PytestPluginManager._hookexec', '_multicall',
                 'pytest_cmdline_main', 'wrap_session', '_main', 'HookCaller.__call__', 'PytestPluginManager._hookexec',
                 '_multicall', 'pytest_runtestloop', 'HookCaller.__call__', 'PytestPluginManager._hookexec', '_multicall',
                 'pytest_runtest_protocol', 'runtestprotocol', 'call_and_report', 'from_call', '<lambda>', 'HookCaller.__call__',
                 'PytestPluginManager._hookexec', '_multicall', 'pytest_runtest_call', 'Function.runtest', 'HookCaller.__call__',
                 'PytestPluginManager._hookexec', '_multicall', 'pytest_pyfunc_call',
                 'test_tst_error_fuzzy_routes', 'fn4', 'fn3', 'fn2', 'fn1.fn1-failed']
    assert err.func_trace() == all_trace
    assert err.routes(*all_trace)
    assert err.fuzzy_routes('<module>',  'runtestprotocol', 'pytest_pyfunc_call', 'fn3', 'fn1.fn1-failed')
    assert not err.fuzzy_routes('<module>',  'runtestprotocol', 'fn3', 'pytest_pyfunc_call', 'fn1.fn1-failed')
    assert err.fuzzy_routes('_main',  'runtestprotocol', 'pytest_pyfunc_call', 'fn3')
    assert not err.fuzzy_routes('_main',   'runtestprotocol', 'fn3', 'pytest_pyfunc_call')