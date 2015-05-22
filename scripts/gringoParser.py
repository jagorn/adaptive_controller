#! /usr/bin/env python
import gringo


def string2fun(string):
    parenthesis = string.find("(")
    if string.isdigit():
        return int(string)
    elif parenthesis == -1:
        return gringo.Fun(string, [])
    elif parenthesis == 0:
        fun_tuple = ()
        for element in _string2list(string[1:-1]):
            fun_tuple = fun_tuple + (string2fun(element),)
        return fun_tuple
    else:
        return gringo.Fun(string[0:parenthesis], map(string2fun, _string2list(string[parenthesis + 1:-1])))


def _string2list(string):
    list = []
    open = 1
    last = 0
    for index in xrange(len(string)):
        if string[index] == "(":
            open += 1
        elif string[index] == ")":
            open -= 1
        elif string[index] == "," and open == 1:
            list.append(string[last:index])
            last = index + 1
    list.append(string[last:])
    return list
