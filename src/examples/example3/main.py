from pytsterrors import tst_decorator

@tst_decorator
def example1(a:int) -> None: 
    raise ValueError("error from example1")

def example2(b:int) -> None:
    example1(b)
    
def example3(c:int) -> None:
    example2(c)

def main() -> None:
    example3(1)
    
    # Your main logic here
    print("Hello from the main function!")
    # Add more code, e.g., call other functions, process data, etc.

if __name__ == "__main__":
    main()