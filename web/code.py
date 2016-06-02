#!/bin/env python3
#coding:utf-8
#代码操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Team,Host,Status,Code,NginxHost,Relat
from .base import encode,decode
import paramiko,random
import time
import os
import xlrd
from multiprocessing import Pool

class update:
    def __init__(self,hostip,port,username,password):
        self.t=paramiko.Transport(hostip,port)
        self.t.connect(username=username,password=password)
        self.sftp=paramiko.SFTPClient.from_transport(self.t)
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostip,port,username,password)
    def update(self,updatefile,filename):
        try:
            self.sftp.mkdir('/update',mode=0o755)
        except:
            pass
        self.sftp.put(updatefile,'{0}/{1}'.format('/update',filename),)
        self.t.close()
    #备份
    def backup(self,dir,filename):
        t=time.strftime("%Y-%m-%d",time.localtime())
        try:
            self.sftp.mkdir('/backup',mode=0o755)
        except:
            pass
        command='cp -rf {0}/{1} /backup/{2}'.format(dir,filename,filename+t)
        print(command)
        self.ssh.exec_command(command)
        self.replace(dir,filename)
    #替换文件
    def replace(self,dir,filename):
        command='cp -rf {0}/{1} {2}/{3}'.format("/update",filename,dir,filename)
        self.ssh.exec_command(command)
    #重启JAVA服务
    def reload(self):
        stopcommand="kill -9 `ps -ef|grep {0}|grep -v grep |awk '{print $2}'`".format()
        self.ssh.exec_command(stopcommand)
        time.sleep(5)
        startcommand='sh {0}/bin/startup.sh'.format()
    #回滚
    def goback(self,updatefile,filename):
        pass

class nginx:
    def __init__(self,host,upstream,nginxconf,code):
        self.upstream=upstream
        self.nginxconf=nginxconf
        self.code=code
        self.ssh=paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=host.hostip,port=host.port,username=host.user,password=decode(host.hostpwd))
    def downteam(self):
        command=r"sed -i 's/\({0}.*;\)'/#\1/g {1}".format(self.upstream,self.nginxconf)
        #command="touch /tmp/a.txt"
        self.ssh.exec_command(command)
        self.reloadnginx()
        #
    def upteam(self):
        command=r"sed -i 's/\(#{0}.*;\)'/\1/g {1}".format(self.upstream,self.nginxconf)
        self.ssh.exec_command(command)
        self.reloadnginx()
    def reloadnginx(self):
        command="/usr/local/tengine-2.1.2/sbin/nginx -c {0} -s reload".format(self.nginxconf)
        #command="/usr/sbin/nginx -c /etc/nginx/nginx.conf -s reload"
        self.ssh.exec_command(command)
        status=Status.objects.get(status="灰度发布中")
        self.code.status=status
        self.code.save()
        self.ssh.close()
def curl(url,status,code):
    import urllib.request
    try:
        urllib.request.urlopen(url)
        if status ==1:
            status=Status.objects.get(status="测试通过")
        else:
            status=Status.objects.get(status="发布成功")
        code.status=status
        code.save()
        return True
    except:
        return False
@login_required(login_url=reverse_lazy('login'))
def code(request):
    userid=User.objects.get(username=request.user)
    teamall=Team.objects.filter(userid=userid).all()
    if request.method =="POST":
        list=[]
        filename=request.FILES.getlist('files[]')
        teamname=request.POST.get('teamname')
        teamhost=Team.objects.get(id=teamname)
        path='{0}/{1}/{2}/{3}'.format('/opt',teamhost.groupname,request.user,time.strftime("%Y-%m-%d-%H-%M",time.localtime()),)
        if not os.path.exists(path):
            os.makedirs(path)
        for file in filename:
            pathname='{0}/{1}'.format(path,file.name)
            with open(pathname,'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            if file.name != "readme.xls":
                list.append(file.name)
            p=Pool(5)
            for host in teamhost.host.all():
                u=update(host.hostip,host.port,host.user,decode(host.hostpwd))
                p.apply_async(u.update(pathname,file.name))
            p.close()
            p.join()
        status=Status.objects.get(status='等待更新')
        t=time.time()
        Code.objects.get_or_create(team=teamhost,path=list,status=status,user=userid,date=t,dir=path)
        code=Code.objects.get(team=teamhost,path=list,status=status,user=userid,date=t)
        for host in teamhost.host.all():
            Relat.objects.create(code=code,host=host,status=status)
        return render(request,'upload.html',{"msg":"已经上传成功，请前往发布列表页进行发布","teamall":teamall})
    return render(request,'upload.html',{"teamall":teamall})


@login_required(login_url=reverse_lazy('login'))
def status(request):

    return render(request, 'status.html')

@login_required(login_url=reverse_lazy('login'))
def updateall(request):
    user=User.objects.get(username=request.user)
    if user.is_superuser:
        updateall=Code.objects.all()
        return render(request,'updateall.html',{'updateall':updateall})
    else:
        updateall=Code.objects.filter(user=user)
        return render(request,'updateall.html',{'updateall':updateall})


@login_required(login_url=reverse_lazy('login'))
def backall(request):
    status=Status.objects.get(status="回退")
    backall=Code.objects.filter(status=status)
    return render(request,'backall.html',{"backall":backall})

@login_required(login_url=reverse_lazy('login'))
def tree(request):
    return render(request,'phptree.html')

@login_required(login_url=reverse_lazy('login'))
def release(request):
    if request.method=="POST":
        id=request.POST.get("id")
        code=Code.objects.get(id=id)
        status=Status.objects.get(status="正在发布")
        code.status=status
        code.save()
        #涉及灰度发布
        #摘nginx
        nginxhosts=code.team.nginxhost.all()#所有nginx
        nginxconf=code.team.nginxconf #nginx的配置文件
        nginxupstream=code.team.nginxupstream #nginx的upstream
        status=Status.objects.get(status="等待更新")
        waitupdate=Relat.objects.filter(code=code,status=status) #项目所有在等待更新状态的主机
        rd=random.randint(0,int(waitupdate.count())-1)#任选一台
        w=waitupdate[rd]
        upstream='{0}:{1}'.format(w.host.hostip,code.team.teamport)
        p=Pool(5)
        for nginxhost in nginxhosts:
            ng=nginx(nginxhost,upstream,nginxconf,code)
            p.apply_async(ng.downteam())
        p.close()
        p.join()
        #上面摘除了一台机器
        #下面进行升级替换
        p=Pool(5)
        up=update(w.host.hostip,w.host.port,w.host.user,decode(w.host.hostpwd))
        data=xlrd.open_workbook("{0}/{1}".format(code.dir,"readme.xls"))
        table=data.sheets()[0]
        nrows=table.nrows
        ncols=table.ncols
        for r in range(nrows):
            for c in range(ncols):
                p.apply_async(up.backup(code.team.path,table.cell(r,1).value))
        p.close()
        p.join()
                #用到进程通信
        #重启
        #备份
        #测试
        #回退
        #重启
        return HttpResponse('OK')