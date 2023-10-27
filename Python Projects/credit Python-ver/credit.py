# TODO


def int2list(n):  # Converting an integer into a list
    return [int(d) for d in str(n)]


def luhn_algorithm(cc_number):
    cc_number = int2list(cc_number)
    s2l = cc_number[-2::-2]  # A list of second-to-last number for multiplication
    f1l = cc_number[-1::-2]
    cc_number_sum = sum(f1l)
    for i in s2l:
        cc_number_sum += sum(int2list(i * 2))
    return cc_number_sum % 10


def cc_type(cc_number):
    digits = len(str(cc_number))
    first2d = int(str(cc_number)[:2])
    first1d = int(str(cc_number)[0])
    if digits == 15 and first2d in [34, 37]:
        return print("AMEX")
    elif digits == 16 and first2d in [51, 52, 53, 54, 55]:
        return print("MASTERCARD")
    elif digits in [13, 16] and first1d == 4:
        return print("VISA")
    else:
        return print("INVALID")


def main():
    while True:
        cc_number = input("Number: ")
        if cc_number.isnumeric():
            cc_number = int(cc_number)
            break

    if luhn_algorithm(cc_number) == 0:
        cc_type(cc_number)
    else:
        print("INVALID")


main()
