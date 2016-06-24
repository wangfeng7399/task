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
list=[]
import  os,json
def tree(path):
    for item in os.listdir(path):
        temp=os.path.join(path,item)
        print(temp)
        if not os.path.isdir(temp):
            list.append({"text":item})
        else:
            list.append({"text":item,"children":tree(temp)})
    return list
#print(tree('/data/pycharm/django/tasknew'))
#print(json.dumps(tree('/data/pycharm/django/tasknew')))
tup=(1,2,3,4,5,6,7,1,2)
print(set(tup))