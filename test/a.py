'''
import  os
def createdict(path):
    list=[]
    for p,item in enumerate(os.listdir(path)):
        children={}
        children["text"]=item
        if os.path.join(path,item):
            if len(os.listdir(os.path.join(path,item))) !=0:
                children["children"]=createdict(path)
            list.append(children)
        else:
            list.append(children)
    return list


c=createdict("/root")
print(c)
'''
'''
import  os,json,sys
def tree(path):
    list=[]
    for item in os.listdir(path):
        temp=os.path.join(path,item)
        if not os.path.isdir(temp):
            list.append({"text":item})
        else:
            list.append({"text":item,"children":tree(temp)})
    return list
print(json.dumps(tree(sys.argv[1]),ensure_ascii=False))
print()
'''
'''
with open("/root/install.log",'r+') as f:
    print(f.read())
'''
'''
import urllib.request,urllib.parse
url='http://10.10.0.50/zabbix/api_jsonrpc.php'
header={"Content-Type":"application/json-rpc"}
data={
    "jsonrpc":"2.0",
    "method":"user.login",
    "params":{
        "user":"wangsh",
        "password":"wodehao123",
    },
    "id":1,
}
try:
    values=urllib.parse.urlencode(data)
    print(values)
    values=values.encode("utf-8")
    req=urllib.request.Request(url,values,header)
    with urllib.request.urlopen(req) as response:
        print(response.read())
except urllib.error.URLError as e:
    print(e.reason)
'''

# from pyzabbix import ZabbixAPI
# z=ZabbixAPI("http://10.10.0.50/zabbix")
# z.login('wangsh','wodehao123')
# print(z.api_version())
import time
# 获取主机组
# for hg in z.hostgroup.get(output="extend"):
#     print(hg)
# 获取主机
# sum=0
# for h in z.host.get(output="extend"):
#     if h["hostid"] != "10084" and h["hostid"]!="10217" and h["hostid"]!="10214" and h["hostid"]!="10206":
#         for it in z.item.get(output="extend",hostids=h):
#             print('id为{0}的{1}的监控项有{2},id为{3}'.format(h["hostid"],h["name"],it["name"],it["itemid"]))
#             sum+=1
# print(sum)
#     print(h['hostid'],h['name'])
#     if '10.10.1.9' in h["name"]:
#         print(h["hostid"])
#
# 获取item
# for it in z.item.get(output="extend",hostids="10110"):
#     print(it["itemid"],it["name"])
# # 获取前15次数值
# for a in z.history.get(output="extend",history=0,itemids="23944",sortfield="clock",sortorder="DESC",limit=10):
#     print(a)
#     print(time.strftime("%m-%d %H:%M",time.localtime(int(a["clock"]))))
# import paramiko
# key_file='/root/.ssh/id_rsa'
# key=paramiko.RSAKey.from_private_key_file(key_file)
# ssh=paramiko.SSHClient()
# ssh.load_system_host_keys()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect("10.10.3.56",22,'root',pkey=key)
# stdit,stdou,_=ssh.exec_command("df")
# print(stdou.read())