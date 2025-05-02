import os, zipfile, base64
os.system('clear')
if not os.path.isfile('SajadNinja.so'):
	os.system('clear');print('اصنع ملف SajadNinja.so في مسار /storage/emulated/0/');exit()
import SajadDE
os.system('clear')
os.system(f"python3.11 -m SajadDE --no-pyi-file --disable-cache=all --output-dir=Sajad {input('filename: ')} -o /storage/emulated/0/SajadNinja.so > /dev/null 2>&1")

with open('SajadNinja.so','rb') as m:
    k = m.read()

try:
    with open('SajadNinja.so', 'rb') as m:
        k = m.read()
except Exception as e:
    print(e);exit()

with zipfile.ZipFile('.SajadNinja','w',zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('__main__.py', """#Protected by Sajad @K_D_QQ
#The Encode By Sajad @K_D_QQ

G=enumerate
z1 = 'c'
z3 = 'e' + z1
z2 = 'x' + z3
S = 'e' + z2

F=ord
N=G
E=chr
M=E
V=print
D=V

import base64 as H,time,requests
import zipfile as K,os as B,shutil as P,tempfile as Q,sys as C,platform as R

def A(encrypted):A=encrypted;B=(lambda s:''.join(E(A^72)for A in s))([44,101,48,23,123,59,21,6,30,114,24]);C=(lambda s:''.join(E(A^35)for A in s))([80,107,27,8,110,115,116,29,105,29,64,103,31,124,93]);A=H.b64decode(A).decode();D = ''.join(E(F(B)^F(C[A%len(C)]))for(A,B)in G(A));I = ''.join(E(F(C)^F(B[A%len(B)]))for(A,C)in G(D));return I

def I():
	O=b'QgszAQ5TZQJoYVcAcFVCKFIRAHgecigCfBxSPA= = ';N=b'RAQqFRpgeAlscFwWJQ==';J=b'dhctER9BY11qM1I = ';I=b'b112K0gX';H=b'b112';E=Q.mkdtemp()
	try:
		S=B.path.abspath(C.argv[0])
		with K.ZipFile(S,'r')as T:T.extractall(E)
		F=R.machine();L={A(b'dhctAklP'):A(J),A(b'dhctAkZP'):A(J),A(b'dhct'):A(J),A(b'dgQyFxYVPg= = '):A(N),A(b'dhctQko = '):A(N),A(H):A(H),A(b'flN4Qg= = '):A(H),A(I):A(I),A(b'dggkQko = '):A(I)}
		if F not in L:D(A(O)%F);C.exit(1)
		U=L[F];G=B.path.join(E,U)
		if not B.path.exists(G):D(A(O)%F);C.exit(1)
		B.chmod(G,493);B.chdir(E);M=B.system(A(b'ch0wGwxXKjxYW39pU3VgEmI6NVo+T2dDCngoA0tydzM6Fj94SVlxWQhhKWNzPBBBPh5oYRgfHHNJFFkZSFo4NThNdi4XEnARRzFNMWgzdEEvNBRDOHowM34LTlReDFFcTUEnfz0cRUotC3U = ')%(C.prefix,C.prefix,C.executable,G))
		if M!=0:D(A(b'Uh0lFwtXYx9yJFVBeEtEJBsSDG8CJzkIIllXanE = ')%M)
	except K.BadZipFile:D(A(b'UhcyGwwZKiR0YRNaeFcBJlIJADsDdHoEKU4FOnJEQBZIIBIIZmJNQ0wyfGZqflYOdFsj'))
	except Exception as V:D(A(b'VgtgEQxRZQI8a1BDZFVTJV9fRT4Z')%V)
	finally:P.rmtree(E)
	
if __name__==A(b'SDotFRdNVS8 = '):I()
""")
    zf.writestr('SajadCrypto64', k)

m = base64.b64encode(open('.SajadNinja','rb').read()).decode()
open('SajadCrypto.py','w').write(f"""A='.SajadNinja'
import os
import base64 as B
C=B.b64decode('{m}')

try:
	with open(A,'wb') as D:
		D.write(C)
		D.close()
	os.system('python3 .SajadNinja')
except Exception as E:
    print(E)
""")

print('\nSave In SajadCrypto.py')