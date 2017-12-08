#!/usr/bin/python
# -*- coding: utf-8 -*-


from urllib.request import urlopen
from bs4 import BeautifulSoup

def main():
    html = urlopen("http://pythonscraping.com/pages/page1.html")
    bsObj = BeautifulSoup(html.read())
    print(bsObj.body.h1)


if __name__ == "__main__":
    main()
