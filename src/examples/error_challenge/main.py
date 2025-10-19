from pytsterrors import TSTError
import random
err_bank_account_empty = "AccountIsEmpty"
err_investment_lost = "InvestmentLost"

def fn1():
    n = random.randint(1, 10)
    print("fn1 random num " + str(n))
    if n%2 == 0 :
        raise TSTError(err_bank_account_empty, "account is empty")
	
    raise TSTError(err_investment_lost, "investment is lost")

def fn2():
    fn1()

def fn3():
    fn1()

def fn4():
    n = random.randint(1, 10)
    print("fn4 random num " + str(n))
    if n%2 == 0 :
        fn3()
    else:
        fn2()



def main() -> None:
    print("Error handling challenge")
    try:
        fn4()
    except TSTError as err:
        print(err.func_trace())
        if err.sub_routes("fn4","fn3","fn1.InvestmentLost"):
            print("The money in your account didn't do well")
        elif err.sub_routes("fn4","fn2","fn1.AccountIsEmpty"):
            print("Aand it's gone")
        else:
            print("This line is for bank members only")
    

if __name__ == "__main__":
    main()