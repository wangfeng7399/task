#!/bin/env python3
#coding:utf-8
#代码操作
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.models import User
from .models import Team,Status,Code,Relat,Host,HostStatus
from .base import dc,send_mail
import paramiko,random
import time
import os,shutil
import xlrd
from multiprocessing import Pool

class update:
    def __init__(self,hostip,port,username,datapath,path,code,host):
        key_file='/root/.ssh/id_rsa'
        key=paramiko.RSAKey.from_private_key_file(key_file)
        self.datapath=datapath
        self.code=code
        self.path=path
        self.host=host #relat表中的数据
        self.t=paramiko.Transport(hostip,port)
        #self.t.load_system_host_keys()
        #self.t.connect(username=username,password=password)
        self.t.connect(username=username,pkey=key)
        self.sftp=paramiko.SFTPClient.from_transport(self.t)
        self.ssh=paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self.ssh.connect(hostip,port,username,password)
        self.ssh.connect(hostip,port,username,pkey=key)
    def update(self,updatefile,filename):
        try:
            self.sftp.mkdir('/update',mode=0o777)
        except:
            pass
        self.sftp.put(updatefile,'{0}/{1}'.format('/update',filename),)
        self.t.close()

    #重启JAVA服务
    def reload(self):
        if self.code.team.language_id.language=="java":
            stopcommand="/etc/init.d/resin stop"
            self.ssh.exec_command(stopcommand)
            time.sleep(5)
            startcommand='/etc/init.d/resin start'
            print(startcommand)
            self.ssh.exec_command(startcommand)
        status=Status.objects.get(status="灰度发布中")
        self.code.status=status
        self.code.save()
        hstatus=Status.objects.get(status="等待测试")
        self.host.status=hstatus
        self.host.save()
    #替换文件
    def replace(self,update,filename):
        command='cp -rf {0}/{1} {2}{3}'.format("/update",update,self.datapath,filename)
        print(command)
        self.ssh.exec_command(command)
        self.reload()
    #备份
    def backup(self,update,filename):
        t=time.strftime("%Y-%m-%d",time.localtime())
        try:
            self.sftp.mkdir('/backup',mode=0o777)
        except:
            pass
        command=r'\cp -rf {0}{1} /backup/{2}'.format(self.datapath,filename,update+t)
        self.ssh.exec_command(command)
        self.replace(update,filename)
    #回滚
    def goback(self,updatefile,filename):
        t=time.strftime("%Y-%m-%d",time.localtime())
        command='\cp -rf {0}{1} {2}{3}'.format('/backup/',updatefile+t,self.datapath,filename)
        print(command)
        self.ssh.exec_command(command)
    #取日志
    def log(self,id):
        command='tail -50 /data/logs/resin/s0/jvm-app-0.log >/tmp/{0}.log'.format(id)
        self.ssh.exec_command(command)
        self.sftp.get('/tmp/{0}.log'.format(id),'/usr/local/task/logs/{0}.log'.format(id))
    #取目录
    def tree(self):
        #self.sftp.put('/data/pycharm/django/task/web/tree.py','/opt/tree.py')
        self.sftp.put('/usr/local/task/web/tree.py','/opt/tree.py')
        self.ssh.exec_command('python /opt/tree.py {0}'.format(self.path))
        time.sleep(3)
        #self.sftp.get('/opt/json.json','/data/pycharm/django/task/static/json/json.json')
        self.sftp.get('/opt/json.json','/usr/local/task/static/json/json.json')
    def delfile(self,filename):
        command='rm -rf {0}/{1}'.format("/update",filename)
        print(command)
        self.ssh.exec_command(command)
class nginx:
    def __init__(self,host,upstream,nginxconf,code):
        key_file='/root/.ssh/id_rsa'
        key=paramiko.RSAKey.from_private_key_file(key_file)
        self.upstream=upstream
        self.nginxconf=nginxconf
        self.code=code
        self.ssh=paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self.ssh.connect(hostname=host.hostip,port=host.port,username=host.user,password=dc(host.hostpwd))
        self.ssh.connect(hostname=host.hostip,port=host.port,username=host.user,pkey=key)
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
        command="/usr/local/tengine-2.1.2/sbin/nginx -s reload"
        #command="/usr/sbin/nginx -c /etc/nginx/nginx.conf -s reload"
        self.ssh.exec_command(command)
        status=Status.objects.get(status="灰度发布中")
        self.code.status=status
        self.code.save()
        self.ssh.close()
def curl(code,ip,port,url):
    import os
    if port=="":
       port=80
    try:
        req=os.system('curl {0}:{1}{2}'.format(ip,port,url))
        if req==0:
            status=Status.objects.get(status="等待测试")
            code.status=status
            code.save()
            return True
        else:
            return False
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
        url=request.POST.get('url')
        teamhost=Team.objects.get(id=teamname)
        datetime=time.strftime("%Y-%m-%d-%H-%M",time.localtime())
        path='{0}/{1}/{2}/{3}'.format('/opt',teamhost.groupname,request.user,datetime)
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
                u=update(host.hostip,host.port,host.user,'','','','')
                p.apply_async(u.update(pathname,file.name))
            p.close()
            p.join()
        status=Status.objects.get(status='等待更新')
        Code.objects.get_or_create(team=teamhost,path=list,status=status,user=userid,date=datetime,dir=path)
        code=Code.objects.get(team=teamhost,path=list,status=status,user=userid,date=datetime)
        for host in teamhost.host.all():
            Relat.objects.create(code=code,host=host,status=status)
        return redirect(reverse('updateall'))
    return render(request,'upload.html',{"teamall":teamall})


@login_required(login_url=reverse_lazy('login'))
def status(request):
    return render(request, 'status.html')

@login_required(login_url=reverse_lazy('login'))
def updateall(request):
    user=User.objects.get(username=request.user)
    if user.is_superuser:
        updateall=Code.objects.all()
    else:
        updateall=Code.objects.filter(user=user)
    return render(request,'updateall.html',{'updateall':updateall})


@login_required(login_url=reverse_lazy('login'))
def backall(request):
    status=Status.objects.get(status="回退")
    backall=Code.objects.filter(status=status)
    return render(request,'backall.html',{"backall":backall})

@login_required(login_url=reverse_lazy('login'))
def tree(request,id):
    team=Team.objects.get(id=id)
    hostid=team.host.all()[0]
    u=update(hostid.hostip,hostid.port,hostid.user,'',team.path,'','')
    u.tree()
    return render(request,'tree.html')

@login_required(login_url=reverse_lazy('login'))
def release(request):
    if request.method=="POST":
        userid=User.objects.get(username=request.user)
        id=request.POST.get("id")
        code=Code.objects.get(id=id)
        status=Status.objects.get(status="正在发布")
        code.status=status
        code.save()
        hoststatus=HostStatus.objects.get(status="准生产")
        status=Status.objects.get(status='等待更新')
        host=code.team.host.get(status=hoststatus)
        test=Relat.objects.filter(code=code,host=host,status=status)
        if test.count() != 0:
            w=Relat.objects.get(code=code,host=host,status=status)
            print(w.host)
        else:
            #涉及灰度发布
            #摘nginx
            nginxhosts=code.team.nginxhost.all()#所有nginx
            nginxconf=code.team.nginxconf #nginx的配置文件
            status=Status.objects.get(status='等待更新')
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
        up=update(w.host.hostip,w.host.port,w.host.user,code.team.datapath,code.team.path,code,w)
        data=xlrd.open_workbook("{0}/{1}".format(code.dir,"readme.xls"))
        table=data.sheets()[0]
        nrows=table.nrows
        for r in range(nrows):
            p.apply_async(up.backup(table.cell(r,0).value,table.cell(r,1).value))
        p.close()
        p.join()
        urls=data.sheets()[1]
        urows=urls.nrows
        content=[]
        for url in range(urows):
            if curl(code,w.host.hostip,code.team.teamport,urls.cell(url,0).value):
                content.append("您发布的{0}项目的一台主机{1}的url为{2}，已经测试通过，在等待您的确认，请通过绑定host的方式去测试您的发布正确与否，测试通过，请前往发布系统确认，以便可以发布后续机器，谢谢！\n".format(code.team.groupname,w.host.hostip,urls.cell(url,0).value))
            else:
                content.append("您发布的{0}项目的一台主机{1}的url为{2}，发布失败,请重新发布！".format(code.team.groupname,w.host.hostip,url.cell(url,0).value))
        send_mail(userid.email,"发布平台通知",content)
            #发送邮件
        return HttpResponse('OK')


@login_required(login_url=reverse_lazy('login'))
def retype(request):
    if request.method=="POST":
        id=request.POST.get("id")
        code=Code.objects.get(id=id)
        status=Status.objects.get(status="测试通过")
        nginxhosts=code.team.nginxhost.all()#所有nginx
        nginxconf=code.team.nginxconf #nginx的配置文件
        testok=Relat.objects.filter(code=code,status=status) #项目所有测试通过的主机
        for t in testok:
            upstream='{0}:{1}'.format(t.host.hostip,code.team.teamport)
            p=Pool(5)
            for nginxhost in nginxhosts:
                ng=nginx(nginxhost,upstream,nginxconf,code)
                p.apply_async(ng.upteam())
            p.close()
            p.join()
        status=Status.objects.get(status='等待更新')
        waitupdate=Relat.objects.filter(code=code,status=status)
        if waitupdate.count()==0:
            status=Status.objects.get(status="发布成功")
        else:
            status=Status.objects.get(status="测试通过")
        code.status=status
        code.save()
        waitstatus=Status.objects.get(status='等待测试')
        status=Status.objects.get(status="测试通过")
        update=Relat.objects.get(code=code,status=waitstatus)
        update.status=status
        update.save()
        return HttpResponse("ok")

@login_required(login_url=reverse_lazy('login'))
def detail(request,id):
    code=Code.objects.get(id=id)
    retail=Relat.objects.filter(code=code)
    return render(request,'codedetail.html',{"code":code,"retail":retail})

@login_required(login_url=reverse_lazy('login'))
def log(request,id,hostid):
    host=Host.objects.get(id=hostid)
    u=update(host.hostip,host.port,host.user,'','','','')
    u.log(id)
    with open("/usr/local/task/logs/{0}.log".format(id),'r+') as f:
        data=f.read()
    #return render(request,'log.html',{'data':data})
    return HttpResponse(data)

@login_required(login_url=reverse_lazy('login'))
def goback(request,id):
    code=Code.objects.get(id=id)
    status=Status.objects.get(status='等待测试')
    task=Relat.objects.get(code=code,status=status)
    p=Pool(5)
    back=update(task.host.hostip,task.host.port,task.host.user,code.team.datapath,'','','')
    path='{0}/{1}/{2}/{3}'.format('/opt',code.team.groupname,request.user,code.date)
    xls=xlrd.open_workbook("{0}/{1}".format(path,"readme.xls"))
    table=xls.sheets()[0]
    nrows=table.nrows
    for r in range(nrows):
        p.apply_async(back.goback(table.cell(r,0).value,table.cell(r,1).value))
    p.close()
    p.join()
    backstatus=Status.objects.get(status='回退')
    code.status=backstatus
    code.save()
    task.status=backstatus
    task.save()
    return redirect('updateall')


@login_required(login_url=reverse_lazy('login'))
def delfile(request,id):
    code=Code.objects.get(id=id)
    p=Pool(5)
    path='{0}/{1}/{2}/{3}'.format('/opt',code.team.groupname,request.user,code.date)
    xls=xlrd.open_workbook("{0}/{1}".format(path,"readme.xls"))
    table=xls.sheets()[0]
    nrows=table.nrows
    rmstatus=Status.objects.get(status='已删除')
    for host in code.team.host.all():
        delssh=update(host.hostip,host.port,host.user,'','','','')
        for r in range(nrows):
            p.apply_async(delssh.delfile(table.cell(r,0).value,))
        p.close()
        p.join()
        relat=Relat.objects.get(code=code,host=host)
        relat.status=rmstatus
        relat.save()
    code.status=rmstatus
    code.save()
    shutil.rmtree(path)
    return redirect('updateall')

@login_required(login_url=reverse_lazy('login'))
def svncode(request):
    userid=User.objects.get(username=request.user)
    teamall=Team.objects.filter(userid=userid).all()
    if request.method=="POST":
        teamname=request.POST.get('teanname')
        version=request.POST.get('version')

    return render(request,'svn.html',{"teamall":teamall})


@login_required(login_url=reverse_lazy('login'))
def upyun(request):
    userid=User.objects.get(username=request.user)
    teamall=Team.objects.filter(userid=userid).all()
    if request.method =="POST":
        list=[]
        filename=request.FILES.getlist('files[]')
        teamname=request.POST.get('teamname')
        url=request.POST.get('url')
        teamhost=Team.objects.get(id=teamname)
        datetime=time.strftime("%Y-%m-%d-%H-%M",time.localtime())
        path='{0}/{1}/{2}/{3}'.format('/opt',teamhost.groupname,request.user,datetime)
        if not os.path.exists(path):
            os.makedirs(path)
        for file in filename:
            pathname='{0}/{1}'.format(path,file.name)
            with open(pathname,'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            if file.name != "readme.xls":
                list.append(file.name)
        #上传到upyun
        #TODO

    return render(request,'upyunupload.html',{"teamall":teamall})

def downloadxls(request):
    with open('/data/pycharm/django/task/templates/readme.xls') as f:
        c=f.read()
    return HttpResponse(c)