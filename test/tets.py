import re,time
'''
a="""upstream new{
      server1:1  wq
      server1:2  qeqw
      server1:3  wqewq
      server1:4  eqw;
}

upstream old{
    server2:1 adsa
    server2:2 asdadsaaa
    server2:4 back;
}

upstream oldd{
   server3:1 adsa
   server3:2 asdadsa;
  server3:3  ck;
  server3:4  back;
}

    """
b=re.findall('upstream\s*%s\s*\{.*?;\n\}\n'%'oldd',a,re.S)
print(b[0])
c=re.sub('(.*back)',lambda m:"#"+m.group(0),b[0])
print(c)

import os
os.path.exists('/opt/admin/2016-5-26/')'''
"""
from multiprocessing import Pool
import os,time,random
def long_time_task(name):
    print('run task {0} ({1})'.format(name,os.getpid()))
    start=time.time()
    time.sleep(random.random()*3)
    end=time.time()
    print('task {0} run {1}s'.format(name,(end-start)))
def a(name):
    print('run a {0} ({1})'.format(name,os.getpid()))
    print(1)
if __name__ == '__main__':
    print('Parent process {0}'.format(os.getpid()))
    p=Pool(4)
    for i in range(5):
        p.apply_async(long_time_task,args=(i,))
        p.apply_async(a,args=(i,))
    print('waiting for all sub done')
    p.close()
    p.join()
    print('all sub done')"""
import paramiko
import os
"""
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.10.0.53',22,'root',)
stdin,stdout,stderr=ssh.exec_command('ls')
for i in stdout.readlines():
    if os.path.isdir(i):
        print('daa')
    else:
        print('da')
"""
"""
t=paramiko.Transport('10.10.0.53',22)
t.connect(username='root',password='51credit.com')
sftp=paramiko.SFTPClient.from_transport(t)
sftp.put('/opt/admin/1/test.jpg',"/root/abc.jpg")
"""
import urllib.request
try:
    urllib.request.urlopen("http://www.w2qweqweq.com")
except:
    print("jje")