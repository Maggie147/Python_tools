#!/sur/bin/python
# -*- coding: utf-8 -*-

'makeTextFile.py -- creat text file'

import codecs
import sys
import urllib


def main():
	if len(sys.argv) > 1:
		str = sys.argv[1]
		str = str.decode('utf-8')  			# utf8 2 unicode
	else:
		str = u"中文"

	print str
	params = {}

	params['name'] = str.encode('utf-8')    # unicode 2 utf8
	print urllib.urlencode(params)

'''
    strings = '\xe5\x91\xb5\xe5\x91\xb5\xe5\x93\x92'
    # strings = '\xe4\xb8\xad\xe5\x9b\xbd'
    # deSting = strings.decode('gbk').encode('utf-8')
    deSting = strings.decode('utf-8').encode('gbk', 'ignore')
    deSting = strings.decode('utf-8')
    print deSting
 '''

if __name__ == "__main__":
    main()
