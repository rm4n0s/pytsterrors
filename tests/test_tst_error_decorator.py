import json
from pytsterrors import TSTError, json_to_tst_error, tst_decorator


def test_tst_error_decorator_on_function_of_the_exception():
    @tst_decorator
    def fn1():
        raise ValueError("failed fn1")

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
                 'test_tst_error_decorator_on_function_of_the_exception', 'fn4', 'fn3', 'fn2', 'fn1.ValueError']
    assert err.func_trace() == all_trace
    assert err.routes(*all_trace)
    assert err.sub_routes('fn3', 'fn2', 'fn1.ValueError')
    assert err.sub_routes('test_tst_error_decorator_on_function_of_the_exception', 'fn4',
                          'fn3', 'fn2', 'fn1.ValueError')
    expected_msg = "failed fn1"
    assert err.message() == expected_msg
    assert err.__str__() == expected_msg
    expected_tag = 'ValueError'
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


def test_tst_error_decorator_as_function():
    def fn1():
        tst_decorator(json.loads)(";")

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
                 'test_tst_error_decorator_as_function', 'fn4', 'fn3', 'fn2', 'fn1', 'loads', 'JSONDecoder.decode', 'JSONDecoder.raw_decode.JSONDecodeError']
    assert err.func_trace() == all_trace
    assert err.routes(*all_trace)
    assert err.sub_routes('fn3', 'fn2', 'fn1','loads', 'JSONDecoder.decode', 'JSONDecoder.raw_decode.JSONDecodeError')
    assert err.sub_routes('test_tst_error_decorator_as_function', 'fn4',
                          'fn3', 'fn2', 'fn1', 'loads', 'JSONDecoder.decode', 'JSONDecoder.raw_decode.JSONDecodeError')
    expected_msg = "Expecting value: line 1 column 1 (char 0)"
    assert err.message() == expected_msg
    assert err.__str__() == expected_msg
    expected_tag = 'JSONDecodeError'
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




def test_tst_error_decorator_on_upper_function():
    def fn1():
        raise ValueError("failed fn1")

    def fn2():
        fn1()

    @tst_decorator
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
                 'test_tst_error_decorator_on_upper_function', 'fn4', 'fn3', 'fn2', 'fn1.ValueError']
    assert err.func_trace() == all_trace
    assert err.routes(*all_trace)
    assert err.sub_routes('fn3', 'fn2', 'fn1.ValueError')
    assert err.sub_routes('test_tst_error_decorator_on_upper_function', 'fn4',
                          'fn3', 'fn2', 'fn1.ValueError')
    expected_msg = "failed fn1"
    assert err.message() == expected_msg
    assert err.__str__() == expected_msg
    expected_tag = 'ValueError'
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




def test_multiple_tst_error_decorators():
    @tst_decorator
    def fn1():
        raise ValueError("failed fn1")
    
    @tst_decorator
    def fn2():
        fn1()

    @tst_decorator
    def fn3():
        fn2()

    def fn4() -> TSTError | None:
        try:
            fn3()
        except TSTError as err:
            return err

    err = fn4()
    assert err != None
    print(err.func_trace())
    all_trace = ['<module>', 'console_main', 'main', 'HookCaller.__call__', 'PytestPluginManager._hookexec', '_multicall',
                 'pytest_cmdline_main', 'wrap_session', '_main', 'HookCaller.__call__', 'PytestPluginManager._hookexec',
                 '_multicall', 'pytest_runtestloop', 'HookCaller.__call__', 'PytestPluginManager._hookexec', '_multicall',
                 'pytest_runtest_protocol', 'runtestprotocol', 'call_and_report', 'from_call', '<lambda>', 'HookCaller.__call__',
                 'PytestPluginManager._hookexec', '_multicall', 'pytest_runtest_call', 'Function.runtest', 'HookCaller.__call__',
                 'PytestPluginManager._hookexec', '_multicall', 'pytest_pyfunc_call',
                 'test_multiple_tst_error_decorators', 'fn4', 'fn3', 'fn2', 'fn1.ValueError']
    assert err.func_trace() == all_trace
    assert err.routes(*all_trace)
    assert err.sub_routes('fn3', 'fn2', 'fn1.ValueError')
    assert err.sub_routes('test_multiple_tst_error_decorators', 'fn4',
                          'fn3', 'fn2', 'fn1.ValueError')
    expected_msg = "failed fn1"
    assert err.message() == expected_msg
    assert err.__str__() == expected_msg
    expected_tag = 'ValueError'
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
