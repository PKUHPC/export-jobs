import subprocess

def parse_tres(tres,gpu_id=1001):
    if tres is '':
        return 0,0,0,0
    a=0;b=0;c=0;d=0;
    
    for item in tres.split(","):
        ks = item.split("=")
        if ks[1].isdigit():
            if int(ks[0]) == 1:
                a=ks[1]
            elif int(ks[0]) == 2:
                b=ks[1]
            elif int(ks[0]) == 4:
                c=ks[1]
            elif int(ks[0]) == gpu_id:
                d=ks[1]
    return a,b,c,d


def parse_gres(gres):
    if gres is '' or ":" not in gres:
        return 0
    item = gres.split(":")
    return item[1] if item[1].isdigit() else 0

def execute_shell(command):
    try:
        ret = subprocess.check_output(command,shell=True).decode().strip()
        return True,ret
    except:
        return False,"ERROR! Execute command Failed"

