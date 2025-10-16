import json
import inspect
import copy
import typing


class TSTError(Exception):
    _func_trace: list[str]
    _message: str
    _tag: str
    _params_per_function: list[typing.Dict[str, typing.Any]]

    def __init__(
        self,
        tag: str,
        message: str,
        copy_params=False,
        can_inspect=True,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._func_trace = []
        self._message = message
        self._params_per_function = []
        self._tag = tag

        if can_inspect:
            for frame_info in inspect.stack()[1:]:
                func_name = frame_info.function
                if func_name == "<module>":
                    continue

                frame = frame_info.frame
                if "self" in frame.f_locals:
                    class_name = frame.f_locals["self"].__class__.__name__
                    self._func_trace.append(f"{class_name}.{func_name}")
                else:
                    self._func_trace.append(func_name)

                if copy_params:
                    arg_info = inspect.getargvalues(frame)
                    params = {}
                    for name in arg_info.args:
                        if name == "self":
                            params[name] = True
                        else:
                            params[name] = copy.deepcopy(arg_info.locals[name])

                    self._params_per_function.append(
                        {"function": func_name, "params": params}
                    )

            self._func_trace[0] = f"{self._func_trace[0]}.{tag}"
            self._func_trace.reverse()

    def __str__(self) -> str:
        if self._message:
            return self._message
        else:
            return super().__str__()

    def dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "func_trace": self._func_trace,
            "message": self._message,
            "tag": self._tag,
            "params_per_function": self._params_per_function,
        }

    def func_trace(self) -> list[str]:
        return self._func_trace
    
    def message(self) -> str:
        return self._message
    
    def tag(self) -> str:
        return self._tag 
    
    def params_per_function(self) -> list[typing.Dict[str, typing.Any]]:
        return self._params_per_function

    def to_json(self) -> str:
        return json.dumps(self.dict())

    def set_attrs(
        self, func_trace: list[str], params_metadata: list[typing.Dict[str, typing.Any]]
    ) -> None:
        self._func_trace = func_trace
        self._params_per_function = params_metadata
