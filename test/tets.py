import  re,time
up=re.compile(r'upstream\s*new\{\n.*\}\n',re.S)
a=up.match("""upstream new{
    adsh
    jas
    dasdsa
    asd
    asd
    asdas
    dahjasd backup;
    }
dasjhjsad""")
print(a.group())

time.sleep(2)
b=re.compile(r'.*backup;',re.S)
c=b.match(r'.*backup;\n',str(a.group()))
print(c)