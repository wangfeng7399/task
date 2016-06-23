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
'''
import xlrd
data=xlrd.open_workbook("test.xls")
table=data.sheets()[0]
nrows=table.nrows
ncols=table.ncols
for r in range(nrows):
    for c in range(ncols):
        print("{0}行{1}列的数据为{2},值的类型{3} ".format(r+1,c+1,table.cell(r,c).value,type(table.cell(r,c).value)))
'''
import  os,json
list=[]
print(list)
for i in os.listdir('/data/pycharm/django/task'):
    print(i,os.path.isdir('{0}/{1}'.format("/data/pycharm/django/task",i)))
    if not os.path.isdir('{0}/{1}'.format("/data/pycharm/django/task",i)):
        list.append({"text":i})
print(json.dumps(list))


[{'text': 'rc6.d'}, {'text': 'autofs.conf'}, {'text': 'csh.login'}, {'text': 'cron.hourly'}, {'text': 'xinetd.d'}, {'text': 'pkcs11'}, {'text': 'login.defs'}, {'text': 'postfix'}, {'text': 'latrace.d'}, {'text': 'bluetooth'}, {'text': 'NetworkManager'}, {'text': 'hosts.deny'}, {'text': 'udev'}, {'text': 'xinetd.conf'}, {'text': '.java'}, {'text': 'avahi'}, {'text': 'gnupg'}, {'text': 'nanorc'}, {'text': 'pm-utils-hd-apm-restore.conf'}, {'text': 'X11'}, {'text': 'system-release'}, {'text': 'wgetrc'}, {'text': 'auto.misc'}, {'text': 'ltrace.conf'}, {'text': 'sudo.conf'}, {'text': 'ld.so.cache'}, {'text': 'virc'}, {'text': 'dhcp'}, {'text': 'dbus-1'}, {'text': 'sestatus.conf'}, {'text': 'crypttab'}, {'text': 'inputrc'}, {'text': 'DIR_COLORS.256color'}, {'text': 'passwd-'}, {'text': 'rpm'}, {'text': 'pango'}, {'text': 'purple'}, {'text': 'auto.smb'}, {'text': 'protocols'}, {'text': 'cron.deny'}, {'text': 'libuser.conf'}, {'text': 'maven'}, {'text': 'samba'}, {'text': 'firefox'}, {'text': 'alternatives'}, {'text': 'smartd.conf'}, {'text': 'xdg'}, {'text': 'ssh'}, {'text': 'portreserve'}, {'text': 'kdump-adv-conf'}, {'text': 'latrace.conf'}, {'text': 'rsyslog.d'}, {'text': 'init.d'}, {'text': 'audisp'}, {'text': 'anacrontab'}, {'text': 'oddjob'}, {'text': 'aliases'}, {'text': 'GeoIP.conf'}, {'text': 'enscript.cfg'}, {'text': 'dnsmasq.d'}, {'text': 'hosts'}, {'text': 'wpa_supplicant'}, {'text': 'mime.types'}, {'text': 'group'}, {'text': 'cgrules.conf'}, {'text': 'lxc'}, {'text': 'ntp'}, {'text': 'ld.so.conf.d'}, {'text': 'festival'}, {'text': 'rc3.d'}, {'text': 'favicon.png'}, {'text': 'updatedb.conf'}, {'text': 'inittab'}, {'text': 'lsb-release'}, {'text': 'statetab.d'}, {'text': 'mtab'}, {'text': 'bash_completion.d'}, {'text': 'pam.d'}, {'text': 'passwd'}, {'text': 'rc2.d'}, {'text': 'centos-release'}, {'text': 'request-key.conf'}, {'text': 'ld.so.conf'}, {'text': 'hp'}, {'text': 'hosts.allow'}, {'text': 'profile.d'}, {'text': 'prelink.cache'}, {'text': 'gdm'}, {'text': 'sasl2'}, {'text': 'ghostscript'}, {'text': 'magic'}, {'text': 'gshadow-'}, {'text': 'jvm'}, {'text': 'oddjobd.conf'}, {'text': 'rc1.d'}, {'text': 'mailcap'}, {'text': 'rc0.d'}, {'text': 'Trolltech.conf'}, {'text': 'motd'}, {'text': 'idmapd.conf'}, {'text': 'sysconfig'}, {'text': 'dracut.conf'}, {'text': 'event.d'}, {'text': 'ethers'}, {'text': 'at.deny'}, {'text': 'logrotate.conf'}, {'text': 'cron.daily'}, {'text': 'gssapi_mech.conf'}, {'text': 'rwtab'}, {'text': 'default'}, {'text': 'issue'}, {'text': 'cups'}, {'text': 'yp.conf'}, {'text': 'gnome-vfs-2.0'}, {'text': 'bashrc'}, {'text': 'openldap'}, {'text': 'rc.d'}, {'text': 'docker'}, {'text': 'chkconfig.d'}, {'text': 'pulse'}, {'text': 'kdump.conf'}, {'text': 'popt.d'}, {'text': 'libaudit.conf'}, {'text': 'xml'}, {'text': 'dracut.conf.d'}, {'text': 'request-key.d'}, {'text': 'sssd'}, {'text': 'krb5.conf'}, {'text': 'sudo-ldap.conf'}, {'text': 'plymouth'}, {'text': 'issue.net'}, {'text': 'ConsoleKit'}, {'text': 'shadow-'}, {'text': 'scl'}, {'text': 'pbm2ppa.conf'}, {'text': 'abrt'}, {'text': 'cron.monthly'}, {'text': 'audit'}, {'text': 'alsa'}, {'text': 'sgml'}, {'text': 'quotagrpadmins'}, {'text': 'fstab'}, {'text': 'ssl'}, {'text': 'system-release-cpe'}, {'text': 'environment'}, {'text': 'man.config'}, {'text': 'sos.conf'}, {'text': 'rc'}, {'text': 'rpc'}, {'text': 'sudoers'}, {'text': 'obex-data-server'}, {'text': 'PackageKit'}, {'text': 'logrotate.d'}, {'text': 'cgsnapshot_blacklist.conf'}, {'text': 'lvm'}, {'text': 'mtools.conf'}, {'text': 'pnm2ppa.conf'}, {'text': 'libreport'}, {'text': 'pm'}, {'text': 'mail.rc'}, {'text': 'setuptool.d'}, {'text': 'sound'}, {'text': 'anthy-conf'}, {'text': 'gcrypt'}, {'text': 'services'}, {'text': 'rc.sysinit'}, {'text': 'gconf'}, {'text': 'depmod.d'}, {'text': 'filesystems'}, {'text': 'shells'}, {'text': 'terminfo'}, {'text': 'gtk-2.0'}, {'text': 'ntp.conf'}, {'text': 'nsswitch.conf'}, {'text': 'ipa'}, {'text': 'selinux'}, {'text': 'redhat-lsb'}, {'text': 'skel'}, {'text': 'yum'}, {'text': 'ppp'}, {'text': 'quotatab'}, {'text': 'statetab'}, {'text': 'grub.conf'}, {'text': 'sysctl.conf'}, {'text': 'securetty'}, {'text': 'rc4.d'}, {'text': 'asound.conf'}, {'text': 'yum.repos.d'}, {'text': 'foomatic'}, {'text': 'nginx'}, {'text': 'opt'}, {'text': 'aliases.db'}, {'text': 'auto.net'}, {'text': 'redhat-release'}, {'text': 'cron.d'}, {'text': 'adjtime'}, {'text': 'modprobe.d'}, {'text': 'blkid'}, {'text': 'auto.master'}, {'text': 'bonobo-activation'}, {'text': 'jvm-commmon'}, {'text': 'exports'}, {'text': 'java'}, {'text': 'oddjobd.conf.d'}, {'text': 'my.cnf'}, {'text': 'group-'}, {'text': 'init'}, {'text': 'sudoers.d'}, {'text': 'mke2fs.conf'}, {'text': 'cas.conf'}, {'text': 'fprintd.conf'}, {'text': 'warnquota.conf'}, {'text': 'rsyslog.conf'}, {'text': 'netconfig'}, {'text': 'yum.conf'}, {'text': 'dnsmasq.conf'}, {'text': 'csh.cshrc'}, {'text': 'hal'}, {'text': 'readahead.conf'}, {'text': 'prelink.conf'}, {'text': 'crontab'}, {'text': 'snmp'}, {'text': 'DIR_COLORS'}, {'text': 'cgconfig.conf'}, {'text': 'gshadow'}, {'text': 'drirc'}, {'text': 'rwtab.d'}, {'text': 'pinforc'}, {'text': 'fonts'}, {'text': 'polkit-1'}, {'text': 'pcmcia'}, {'text': 'iproute2'}, {'text': 'printcap'}, {'text': 'httpd'}, {'text': 'rc.local'}, {'text': 'resolv.conf'}, {'text': 'cgconfig.d'}, {'text': 'security'}, {'text': '.pwd.lock'}, {'text': 'prelink.conf.d'}, {'text': 'gai.conf'}, {'text': 'lsb-release.d'}, {'text': 'rc5.d'}, {'text': 'host.conf'}, {'text': 'localtime'}, {'text': 'makedev.d'}, {'text': 'nfsmount.conf'}, {'text': 'networks'}, {'text': 'acpi'}, {'text': 'autofs_ldap_auth.conf'}, {'text': 'profile'}, {'text': 'pki'}, {'text': 'certmonger'}, {'text': 'vimrc'}, {'text': 'shadow'}, {'text': 'DIR_COLORS.lightbgcolor'}, {'text': 'kde'}, {'text': 'cron.weekly'}, {'text': 'sane.d'}]
