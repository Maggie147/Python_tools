#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import base64


def get_file(filepath, rmflag=0):
    filebuf = None
    try:
        with open(filepath, "rb+") as fp:
            filebuf = fp.read()
        try:
            if rmflag == 1:
                os.remove(filepath)
        except Exception as e:
            print e
    except Exception as e:
        DEBUGE("Open file [%s] failed!!!" % filepath)
    return filebuf


def write_data_toFile(tarPath, tarName, data):
    if not os.path.exists(tarPath):
        os.makedirs(tarPath)
    try:
        with open(tarPath+tarName, "wb") as fp:
            fp.write(data)
        return True
    except:
        return False


def decode_base64(sdata):
    """Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """
    try:
        missing_padding = 4 - len(sdata) % 4
        if missing_padding:
            sdata += b'='* missing_padding
        return base64.decodestring(sdata)
    except Exception as e:
        print e
        return None


def test():
    s_path = "./test_file/picture.txt"

    s_buf = get_file(s_path, 0)

    decode_data = decode_base64(s_buf)
    if decode_data:
        ret = write_data_toFile('./test_file/', 'picture.bmp', decode_data)
        if not ret:
            print "save decode data failed!!!"
        else:
            print "decode success"
    else:
        print "decode failed!!!"



def main():

    test()


if __name__ == '__main__':
    main()