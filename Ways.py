import sys
def print_departure():
    print("------------------------------------------")
###输入检查
def input_check(prompt: str)->str:
    x= input(prompt)
    if x == "exit":
        sys.exit()
    return x

