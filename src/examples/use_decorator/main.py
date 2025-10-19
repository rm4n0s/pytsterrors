import json
from pytsterrors import TSTError, tst_decorator

@tst_decorator
def example1(a:int) -> None: 
    raise json.loads(";")

def example2(b:int) -> None:
    example1(b)
    
def example3(c:int) -> None:
    example2(c)

def main() -> None:
    try:
        example3(1)
    except TSTError as err:
        print(err.func_trace())
        if err.routes('main', 'example3', 'example2', 'example1.JSONDecodeError'):
            print("exception from a specific route of calls and tag "+err.tag()+" is the name of the exception's class that raised by json.loads")

if __name__ == "__main__":
    main()