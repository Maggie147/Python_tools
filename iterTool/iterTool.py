#!/usr/bin/python
#-*-coding:utf-8-*- 
import itertools


def combinations_itertools(string, n):
    """
    combinations_itertools, use itertools.combinations
    """
    newlist = []
    for i in range(1, len(string)+1):
        iter = itertools.combinations(string, i)
        newlist.append(list(iter))
    # print newlist
    return newlist[n-1]


def permutationsAll_itertools(string):
    """
    permutationsAll_itertools, use itertools.permutations
    """
    newlist = []
    for n in range(1, len(string)+1):
        perNList = []
        for per in itertools.permutations(string, n):
            # print per
            perNList.append("".join(per))
        newlist.append(perNList)
    return newlist


def permutationsN_itertools(string, n):
    """
    permutationsN_itertools, use itertools.permutations
    """
    newlist = []
    for i in itertools.permutations(string, n):
        newlist.append("".join(i))
    return newlist


def main():

    list1 = "abc"
    # list1 = ['a', 'b', 'c']

    list2 = []
    n = 3           # n <= len(list1)
    # list2 = combinations_itertools(list1, n)
    # list2 = permutationsAll_itertools(list1)
    list2 = permutationsN_itertools(list1, n)
    print list2

if __name__ == '__main__':
    main()