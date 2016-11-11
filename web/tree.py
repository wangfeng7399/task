#!/usr/bin/env python3
#coding:utf-8
import  os,json,sys
def tree(path):
    treelist=[]
    for item in os.listdir(path):
        temp=os.path.join(path,item)
        if not os.path.isdir(temp):
            treelist.append({"text":item,"icon":"glyphicon glyphicon-leaf"})
        else:
            treelist.append({"text":item,"children":tree(temp)})
    return treelist
if __name__ == '__main__':
    treejson=json.dumps(tree(sys.argv[1]),ensure_ascii=False)
    with open('/opt/json.json','wb+') as f:
        f.write(treejson)