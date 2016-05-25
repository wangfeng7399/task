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
'''
import os
os.path.isdir()