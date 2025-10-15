from pytsterrors import TSTError

def example1(a:int) -> None: 
    raise TSTError("error-from-examle1","error from example1", copy_params= True)

def example2(b:int) -> None:
    example1(b)
    
def example3(c:int) -> None:
    example2(c)

def main() -> None:
    try:
        example3(1)
    except TSTError as err:
        print(err.dict())
    # Your main logic here
    print("Hello from the main function!")
    # Add more code, e.g., call other functions, process data, etc.

if __name__ == "__main__":
    main()