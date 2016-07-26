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

from pyzabbix import ZabbixAPI
z=ZabbixAPI("http://10.10.0.50/zabbix")
z.login('wangsh','wodehao123')
# print(z.api_version())

#获取主机组
# for hg in z.hostgroup.get(output="extend"):
#     print(hg)
#获取主机
for h in z.host.get(output="extend"):
    #print(h["hostid"],h["name"])
    if '10.10.1.9' in h["name"]:
        print(h["hostid"])

#获取item
# for it in z.item.get(output="extend",hostids="10110"):
#     print(it["itemid"],it["name"])
#获取前15次数值
# for a in z.history.get(output="extend",history=0,itemids="23944",limit=15):
#     print(a)
