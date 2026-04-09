try:
    number=int(input("enter number:"))
    result = 100/number
    print(f"result of division:{result}")
except ValueError:
    print("error, thats not number")
except ZeroDivisionError:
    print(" this number can not division of zero")
finally:
    print("ended cod")