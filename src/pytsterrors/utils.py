from pytsterrors.exception import TSTError
import json

def json_to_tst_error(json_string: str | bytes) -> TSTError:
    data = json.loads(json_string)
    if not isinstance(data, dict):
        raise TSTError("not-instance-of-dict", "JSON must represent a dictionary")

    tag = data.get("tag")
    message = data.get("message")
    func_trace = data.get("func_trace")
    params_metadata = data.get("params_per_function")
    if not tag or not message or not func_trace or not params_metadata:
        raise TSTError("not-correct-json", "JSON is not from TSTError")
    
    tst = TSTError(tag, message=message, can_inspect=False)
    tst.set_attrs(func_trace=func_trace, params_metadata=params_metadata)

    return tst
        
   

