# -*- encoding: utf-8-*-
'''
    @File        File Handle
    @Author      tx
    @CreatedDate 2018-04-02
    @UpdatedDate 2018-04-13
'''
# py3 = True if sys.version > '3' else False
import os
import sys
import time
pwd = os.path.dirname(os.path.realpath(__file__))       #pwd2 = sys.path[0]
pardir = os.path.abspath(os.path.join(pwd, os.pardir))
sys.path.append(pardir)

reload(sys)
sys.setdefaultencoding('utf8')

g_iDEBUG = 1
def DEBUG(*value):
    if g_iDEBUG == 1:
        t = time.strftime("%Y-%m-%d %H:%M:%S")
        # filename = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
        filename = os.path.splitext(os.path.basename(__file__))[0]
        print "[python2.7][%s,%s]:" % (filename, t),
        for i in value:
            print i,
        print ""

# get_fileList
def get_files(path, tail=None):
    try:
        files=[]
        if not os.path.exists(path):
            return None
        for dirpath, dirnames, filenames in os.walk(path):
            if len(filenames)==0:
                continue
            for file in filenames:
                if tail:
                    if tail != os.path.splitext(file)[1]:
                        continue
                fullpath = os.path.join(dirpath, file)
                files.append(fullpath)
        return files
    except Exception as e:
        DEBUG(e)
        return None

def isExsit(path, fname):
    try:
        fullpath = os.path.join(path, fname)
        if not os.path.isfile(fullpath):
            return False
        return True
    except Exception as e:
        print(e)
        return False

def rmfile(path, fname):
    try:
        fullpath = os.path.join(path, fname)
        os.remove(fullpath)
        return True
    except Exception as e:
        print(e)
        return False

def cpfile(srcfpath, tarfpath):
    try:
        import shutil
        shutil.copy(srcfpath, tarfpath)
        # os.system("cp -f {} {}".format(srcfpath, tarfpath))
        return True
    except Exception as e:
        print(e)
        return False

# get_file
def get_file_data(path, fname, mode="rb"):
    try:
        fullpath = os.path.join(path, fname)
        with open(fullpath, mode) as fp:
            fbuf = fp.read()
        return fbuf
    except Exception as e:
        print(e)
        return False


def _while_read_write_test(srcfpath, tarfpath):
    try:
        fsize = get_file_size()
        with open(srcfpath, 'rb') as f_in, open(tarfpath, 'wb') as f_out:
            for x in range(1, fsize, 1):
                content = f_in.read(1024)
                f_out.write(content)
        return True
    except Exception as e:
        print(e)
        return False


def get_file_md5(path, fname, mode='1'):
    try:
        # 需要使用二进制格式读取文件内容
        buf = get_file_data(path, fname, mode="rb")
        if not buf:
            print("File[%s] open failed."%fname)
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


def write_date_2file(path, fname, buf):
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        fullpath = os.path.join(path, fname)
        with open(fullpath, "wb") as fp:
            fp.write(buf)
        return fullpath
    except Exception as e:
        return None


# get_data
def get_symbol_value(buf, head_sym='', tail_sym=''):
    value = ''
    try:
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


# get_fileSize
def get_file_size(spath, unit='B'):
    try:
        # spath = os.path.join(path, fname)
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
            print("Please Input Correct File Size Unit, include: B, KB, MB, G")
            return None
        return round(fsize, 3)
    except Exception as e:
        print(e)
        return None

def get_file_time(spath, tattr='C'):
    try:
        # spath = os.path.join(path, fname)
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


def test():
    fileList = get_files("../", '.py')
    for file in fileList:
        DEBUG("file path: ", file)

if __name__ == '__main__':
    test()
