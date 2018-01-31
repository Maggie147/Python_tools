#!/usr/bin python  
# coding=utf-8  
# filename : backup_ver3.py  
import os  
import time  
  
source='/home/grace/python/'  
  
target_dir='/home/grace/test/'  
  
today=target_dir+time.strftime('%Y%m%d')  
  
now = time.strftime("%H%M")  
  
comment=raw_input('Enter comment->')  
  
if(len(comment)==0):  
    target=today+os.sep+now+'.zip'  
else:  
    target = today + os.sep+now +'_'+\  
            comment.replace(' ','_')+'.zip'  
  
if not os.path.exists(today):  
    os.mkdir(today)  
    print 'Sucessfully create directory',today  
  
zip_command="zip -qr '%s' %s" %(target,''.join(source))  
  
if os.system(zip_command)==0:  
    print 'Sucessfully backup to',target  
else:  
    print 'Backup Failed!'