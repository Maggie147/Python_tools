# -*- encoding: utf-8-*-
#================================================
#  __title__ = 'file_test'
#  __author__ = 'tx'
#  __mtime__ = '2018-01-16'
#=================================================
import os
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')


def tar_pack(targetfile, sourcefile):
    try:
        if targetfile.find('.tgz'):
            tar_command = "tar -zcvpf %s %s" % (targetfile, sourcefile)
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S")
            tar_command = "tar -zcvpf %s_%s.tgz %s" % (targetfile, t, sourcefile)

        print "cp Command: " + cpy_command

        if os.system(cpy_command) == 0:
            print "tar pack success"
            return True
        else:
            return False
    except Exception as e:
        print e
        return False

def tar_uppack(targetfile, sourcefile):
    try:

        tar_command = "tar -zxvf %s -C %s" % (sourcefile, targetfile)

        print "cp Command: " + cpy_command

        if os.system(cpy_command) == 0:
            return True
        else:
            return False
    except Exception as e:
        return False


def get_sysArgv():
    argv1 = ''
    argv2 = ''
    try:
        if len(sys.argv) != 3:
            print "can shu not true"
            sys.exit()
        else:
            argv1 = sys.argv[1]
            argv2 = sys.argv[2]
            return (argv1, argv2)
    except Exception as e:
        print e
        return (None, None)

def main():
    argvs = get_sysArgv()
    out = tar_pack(argvs[0], argvs[1])


if __name__ == '__main__':
    main()