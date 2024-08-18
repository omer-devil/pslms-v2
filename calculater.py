# accepting input from users
n1 = input("Enter the first number: ")
n2 = input("Enter the second number: ")
opration = input("Enter an oprater: ")

# converting string into float number
num1 = float(n1)
num2 = float(n2)

# logical opration(>,<,<=,>=,==,!=)
if opration == "+":
    print(num1 + num2)
elif opration == "-":
    print(num1 - num2)
elif opration == "*":
    print(num1 * num2)
elif opration == "/":
    if num2 != 0:
        print(num1 / num2)
    else:
        print("can not divide by zero!")