#coding:utf-8
'''
    @File        FileHandle.py
    @Author
    @CreatedDate 2018-04-02
    @UpdatedDate 2018-04-13
'''
# py3 = True if sys.version > '3' else False

import os
import sys
import time
import json
pwd = os.path.dirname(os.path.realpath(__file__))       #pwd2 = sys.path[0]
pardir = os.path.abspath(os.path.join(pwd, os.pardir))
sys.path.append(pardir)

reload(sys)
sys.setdefaultencoding('utf8')


g_iDEBUG = 0
def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        print "[python2.7][%s, %s]:" % (filename, t),
        for i in value:
            print i,
        print ""


class ManyFilesHandle(object):
    def __init__(self, path, tail=None):
        self.path = path
        self.tail = tail
        if not os.path.exists(path):
            print("Path Not exists!")
            sys.exit()

    def get_files(self):
        try:
            files = []
            for dirpath, dirnames, filenames in os.walk(self.path):
                if len(filenames) == 0:
                    continue
                for file in filenames:
                    if self.tail:
                        if self.tail != os.path.splitext(file)[1]:
                            continue
                    fullpath = os.path.join(dirpath, file)
                    files.append(fullpath)
            return files
        except Exception as e:
            print(e)
            return None


class FileHandle(object):
    def __init__(self, path):
        self.path = path

    def _isExsit(self, fname):
        try:
            fullpath = os.path.join(self.path, fname)
            if not os.path.isfile(fullpath):
                return False
            return True
        except Exception as e:
            print(e)
            return False


    def rmfile(self, fname):
        try:
            fullpath = os.path.join(self.path, fname)
            os.remove(fullpath)
            return True
        except Exception as e:
            print(e)
            return False


    def cpfile(self, fname, tarfpath):
        try:
            import shutil
            fullpath = os.path.join(self.path, fname)
            shutil.copy(fullpath, tarfpath)
            # os.system("cp -f {} {}".format(fullpath, tarfpath))
            return True
        except Exception as e:
            print(e)
            return False

    def get_file_data(self, fname, mode="rb"):
        try:
            fullpath = os.path.join(self.path, fname)
            with open(fullpath, mode) as fp:
                fbuf = fp.read()
            return fbuf
        except Exception as e:
            print(e)
            return None

    def get_file_md5(self, fname, mode='1'):
        try:
            buf = self.get_file_data(fname)
            if not buf:
                print("File[%s] open failed."%spath)
                return None
            if mode == '1':
                import md5
                md5Obj = md5.new()
                md5Obj.update(buf)
            else:
                import hashlib
                md5Obj = hashlib.md5()
                md5Obj.update(buf)
            return md5Obj.hexdigest()
        except Exception as e:
            print(e)
            return None

    def writ_data_2file(self, path, fname, buf):
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            fullpath = os.path.join(self.path, fname)
            with open(fullpath, 'wb') as fp:
                fp.write(buf)
            return fullpath
        except Exception as e:
            print(e)
            return None


    def get_symbol_value(self, fname, head_sym='', tail_sym=''):
        value = ''
        try:
            buf = self.get_file_data(fname)

            begin = buf.rfind(head_sym)
            if begin:
                if tail_sym:
                    end = buf[begin+len(head_sym):].find(tail_sym)
                    if end:
                        value = buf[begin+len(head_sym): begin+len(head_sym)+end]
                    else:
                        value = buf[begin+len(head_sym): ]
                else:
                    value = buf[begin+len(head_sym):]
            else:
                print("Not Found head symbol")
        except Exception as e:
            print(e)
        return value


    def get_file_size(self, fname, unit='B'):
    try:
        spath = os.path.join(self.path, fname)
        # spath = unicode(spath, 'utf8')
        unit = unit.upper()
        fsize = os.path.getsize(spath)      # get file size, unit is B
        if unit == 'B':
            return fsize
        elif unit == 'KB':
            fsize = fsize/float(1024)
        elif unit == 'MB':
            fsize = fsize/float(1024*1024)
        elif unit == 'G':
            fsize = fsize/float(1024*1024*1024)
        else:
            print("Please Input Correct Size Unit, include: B, KB, MB, G")
            return None
        return round(fsize, 3)
    except Exception as e:
        print(e)
        return None

    def get_file_time(self, fname, tattr='C'):
        try:
            spath = os.path.join(self.path, fname)
            # spath = unicode(spath,'utf8')
            tattr = tattr.upper()
            if tattr == 'C':
                ftime = os.path.getctime(spath)
            elif tattr == 'M':
                ftime = os.path.getmtime(spath)
            elif tattr == 'A':
                ftime = os.path.getatime(spath)
            else:
                print("Please Input Correct File Time Attr, include: C, M , A")
                return None
            return ftime
        except Exception as e:
            print(e)
            return None


if __name__=='__main__':
    filesObj = ManyFilesHandle('./')

    fobj= FileHandle('./')