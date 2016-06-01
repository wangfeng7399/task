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
''''''
import os
os.path.exists('/opt/admin/2016-5-26/')
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
import paramiko,re
import os
"""
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.10.0.53',22,'root','51credit.com')
command=r"sed -i 's/\({0}.*\)/#\1/g' {1}".format("In","/root/a.txt")
stdin,stdout,stderr=ssh.exec_command(command)
print(stdout)
"""
"""

t=paramiko.Transport('10.10.0.53',22)
t.connect(username='root',password='51credit.com')
sftp=paramiko.SFTPClient.from_transport(t)
stdout=sftp.file("/root/a.txt",mode="r+")
print(stdout.read())
b=re.findall('na',stdout.read(),re.S)
print(b)
c=re.sub('na','NA',str(stdout.read()))
print(c)
#stdout.write(c)
'''
'''
import urllib.request
try:
    urllib.request.urlopen("http://www.w2qweqweq.com")
except:
    print("jje")
'''
'''
import  paramiko
t=paramiko.Transport('10.10.0.53',22)
t.connect(username='root',password='51credit.com')
sftp=paramiko.SFTPClient.from_transport(t)
#sftp.get("/root/a.txt","/tmp/a.txt")
stdout=sftp.file("/root/a.txt",mode="r+")
print(stdout.read())
#b=re.findall('na',stdout.read(),re.S)
#print(b)
c=re.sub('(.*na.*)',lambda m:"#"+m.group(0),str(stdout.read()))
print(c)
#stdout.write(c)
'''
'''

with open("/tmp/a.txt","r+")as f:
    c=re.sub('(.*na.*)',lambda m:"#"+m.group(0),f.read())
with open("/tmp/a.txt","w+") as f:
    f.write(c)
'''
'''
with open("/tmp/a.txt","r+")as f:
    c=re.sub('#(.*)',lambda m:m.group(0),f.read())
    print(c)
'''
'''
import paramiko
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.10.0.53',22,'root','51credit.com')
#command=r"sed -i 's/\({0}.*\)/#\1/g' {1}".format("In","/root/a.txt")
stdin,stdout,stderr=ssh.exec_command("/usr/sbin/nginx -c /etc/nginx/nginx.conf -s reload")
'''
'''
import xlwt
style0=xlwt.easyxf("font: name  Time New Roman, color-index red")
style1=xlwt.easyxf(num_format_str="D-MMMM-YY")
wb=xlwt.Workbook()
ws=wb.add_sheet("A Test Sheet")
ws.write(0,0,123,style0)
ws.write(1,0,"b",style1)
ws.write(2,0,1)
ws.write(2,1,1)
ws.write(2,2,xlwt.Formula("A3+B3"))
wb.save("test.xls")
'''
import xlrd
data=xlrd.open_workbook("test.xls")
table=data.sheets()[0]
nrows=table.nrows
ncols=table.ncols
for r in range(nrows):
    for c in range(ncols):
        print("{0}行{1}列的数据为{2},值的类型{3} ".format(r+1,c+1,table.cell(r,c).value,type(table.cell(r,c).value)))