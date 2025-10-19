from pytsterrors import TSTError


def example1(a:int) -> None: 
    raise TSTError("error-from-examle1","error from example1")

def example2(b:int) -> None:
    example1(b)
    
def example3(c:int) -> None:
    example2(c)

class A:
    def __init__(self) -> None:
        raise TSTError("error-class-A", " error from class A")
    
class B:
    def something1(self, a:int) -> None:
        ab = A()

class C:
    def something2(self, b:int) -> None:
        c = B()
        c.something1(b)



def main() -> None:
    try:
        example3(1)
    except TSTError as err:
        if err.routes('main', 'example3', 'example2', 'example1.error-from-examle1'):
            print("exception from specific route of calls")

    try:
        C().something2(2)
    except TSTError as err:
        if err.sub_routes('B.something1', 'A.__init__.error-class-A'):
            print("exception from a part of route of calls")

if __name__ == "__main__":
    main()