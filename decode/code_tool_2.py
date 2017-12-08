#!/sur/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys


def main():

    if len(sys.argv) > 1:
        str = sys.argv[1]
        # str = str.decode('utf-8')           # utf8 2 unicode
        # str = str.replace('x', '\x')
    else:
        str = '\xe5\x91\xb5\xe5\x91\xb5\xe5\x93\x92'
 
    print str
    print str.decode('utf-8')


    # strings = '\xe5\x91\xb5\xe5\x91\xb5\xe5\x93\x92'
    # # strings = '\xe4\xb8\xad\xe5\x9b\xbd'
    # # deSting = strings.decode('gbk').encode('utf-8')
    # deSting = strings.decode('utf-8').encode('gbk', 'ignore')
    # print deSting
    # deSting = strings.decode('utf-8')
    # print deSting


if __name__ == "__main__":
    main()
