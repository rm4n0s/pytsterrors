from pytsterrors import TSTError, json_to_tst_error

class A:
    def __init__(self) -> None:
        raise TSTError("error-class-A", " error from class A", copy_params=True)


class B:
    def something1(self, a:int) -> None:
        ab = A()

class C:
    def something2(self, b:int) -> None:
        c = B()
        c.something1(b)


def main() -> None:
    try:
        c = C()
        c.something2(1)
    except TSTError as err:
        json_string = err.to_json()

        tst = json_to_tst_error(json_string)
        print("from json ", tst.dict())


if __name__ == "__main__":
    main()
