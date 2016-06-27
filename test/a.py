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