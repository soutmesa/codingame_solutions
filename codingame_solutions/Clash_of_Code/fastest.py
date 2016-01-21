__author__ = 'Amin'

import sys
import math


def dna(s):
    nuclobases = ["A", "T", "C", "G"]
    nuclobases_complementary = ["T", "A", "G", "C"]

    r = ""
    for c in s:
        if c in nuclobases:
            index = nuclobases.index(c)
            r += nuclobases_complementary[index]

    return r


def dna_if(s):
    r = ""
    for c in s:
        if c == "A":
            r += "T"
        elif c == "T":
            r += "A"
        elif c == "C":
            r += "G"
        elif c == "G":
            r += "C"
        else:
            r += c

    return r


def l33t(s):
    normal_speach = "EeAaOo"
    l33t_speach = "334400a"

    for ns, ls in zip(normal_speach, l33t_speach):
        s = s.replace(ns, ls)

    return s


def count_letters(s):
    count = 0
    for c in s:
        if c.islower() or c.isupper():
            count += 1

    return count


def only_capital(s):
    r = ""
    for c in s:
        if c.isalpha():
            if c.isupper():
                r += c


def sum_of_letters_values(s):
    sum_of_letters = 0
    for c in s:
        sum_of_letters += ord(c)

    return sum_of_letters


def sort_tuples():
    n = int(input())

    elements = []
    for i in range(n):
        item, distance = input().split()
        distance = float(distance)
        elements.append((item, distance))

    elements_sorted = sorted(elements, key=lambda tup: tup[1])
    r = ""
    for x, y in reversed(elements_sorted):
        r += x + " "

    print(r[:-1])


# you are provided with a and b coefficients and then for each calc you have to calculate y=a*x+b
# and print each y in separate line
def linear_function():
    a, b = [int(i) for i in input().split()]
    n = int(input())

    for i in range(n):
        x = int(input())
        y = a * x + b
        print(y)


# you are provided with n numbers and should print them from lowest to highest
def sort_numbers():
    n = int(input())
    l = []
    for i in range(n):
        x = int(input())
        l.append(x)

    l.sort()

    r = ""
    for v in reversed(l):
        r += str(v) + " "

    print(r[:-1])


if __name__ == "__main__":
    #a = [int(x) for x in input().split()]
    #print(a[1])

    sort_tuples()

    linear_function()

    sort_numbers()

    s = input()
    print(dna(s))
    print(dna_if(s))
    print(l33t(s))
    print(count_letters(s))
