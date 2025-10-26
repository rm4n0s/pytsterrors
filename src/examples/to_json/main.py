# this is a simulation passing exceptions between microservices


from pytsterrors import TSTError, json_to_tst_error


def internal_microservice():
    raise TSTError("error-from-microservice", "an error that raised from inside microservice")

# get_restapi_microservice simulates an HTTP handler that returns the exception in JSON format 
def get_restapi_microservice() -> str:
    try:
        internal_microservice()
    except TSTError as err:
        return err.to_json()
    
    return ""


def main() -> None:
    # here we simulate the user taking the error as json from microservice or even from the logs of the microservice
    err_json = get_restapi_microservice()
    err = json_to_tst_error(err_json)
    print(err.func_trace())
    if err.sub_routes('get_restapi_microservice', 'internal_microservice.error-from-microservice'):
        print("exception from a specific route of calls")

if __name__ == "__main__":
    main()