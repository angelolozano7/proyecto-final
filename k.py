archivo= open(r"C:\Users\usuario\Desktop\Proyecto Programación\datos/datosVuelo.txt",mode="r+")
apInformation = archivo.readlines()
afInformation = apInformation
apInformation=apInformation[13:36] #listas de lineas
afInformation=afInformation[59:len(afInformation)-1]
i=0
for elem in apInformation:
    elem=str(elem).strip("\n")
    elem=str(elem).split(" ")
    apInformation[i]=elem
    i+=1
i=0
for elem in afInformation:
    elem=str(elem).strip("\n")
    elem=str(elem).split()
    if len(elem[0])>2:
        elem.insert(1,elem[0][2:6])
        elem[0]=elem[0][0:2]
    afInformation[i]=elem
    i+=1
    
i=0
while i< len(apInformation):
    apInformation[i][1]=str(apInformation[i][1]).strip("-")
    i+=1
    
i=0
while i< len(apInformation):
    j=0
    while j<len(apInformation[i]):
        if apInformation[i][j]=="":
            apInformation[i].pop(j)
        else:
            j+=1
    i+=1
    
i=0
while i< len(apInformation):
    if len(apInformation[i][4])==3 or len(apInformation[i][4])==2:
        apInformation[i][4]=apInformation[i][4]+" "+ apInformation[i][5]
        apInformation[i].pop(5)
        apInformation[i][4]=str(apInformation[i][4]).strip(",")
    else:
        apInformation[i][4]=str(apInformation[i][4]).strip(",")
    i+=1

    
archivo.close()
print(apInformation)

print("||||||||||||||||||||||!")
print("quinto caso")
print(afInformation[4])
print("sexto caso")
print(afInformation[33])
print("septimo caso")
print(afInformation[200])
print("octavo caso")
print(afInformation[134])
print("||||||||||||||||||||||!")
i=0
h1=[2,3,4,5,6,7,7,7,7,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,11,12,13]
h2=[2,4,5,6,7,7,7,7,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,11,12,13]
h3=[2,3,4,6,7,7,7,7,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,11,12,13]
h4=[2,4,6,7,7,7,7,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,11,12,13]
h5=[1,2,3,4,5,6,7,7,7,7,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,11,12,13]
h6=[1,2,4,5,6,7,7,7,7,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,11,12,13]
h7=[1,2,3,4,6,7,7,7,7,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,11,12,13]
h8=[1,2,4,6,7,7,7,7,8,8,8,9,9,9,9,9,9,9,9,9,9,9,10,11,12,13]
##for elem in afInformation:
##    
##    if elem[1]!="":
##        if (elem[4]=="") and (elem[8]==""):
##            print("c1")
##            for n in h1:
##                elem.pop(n)
##                print(elem)
##        elif elem[4]!="" and elem[7]=="":
##            print("c2")
##            
##            for n in h2:
##                elem.pop(n)
##        elif elem[4]=="" and elem[8]!="":
##            print("c3")
##            
##            for n in h3:
##                elem.pop(n)
##                
##        elif (elem[4]!="")and (elem[7]!=""):
##            print("c4")
##            
##            for n in h4:
##                elem.pop(n)
##                
##    else:
##         if (elem[5]=="") and (elem[9]==""):
##            print("c5")
##            
##            for n in h5:
##                
##                elem.pop(n)
##                
##         elif elem[5]!="" and elem[8]=="":
##            print("c6")
##            
##            for n in h6:
##                elem.pop(n)
##                
##         elif elem[5]=="" and elem[9]!="":
##            print("c7")
##            
##            for n in h7:
##                elem.pop(n)
##                
##         elif (elem[5]!="")and (elem[8]!=""):
##            print("c8") #correo  #jhonatan: plage174@gmail.com
##            
##            for n in h8:
##                elem.pop(n)
                
##    
##    #print(elem)
##    afInformation[i]=elem
##    i+=1
##mini=0
##i=0
##for number in lend:
##    if mini==0:
##        mini=number
##    elif mini==30:
##        break
##    else:
##        if number<mini:
##            mini=number
##    i+=1

##print(mini,"+",i)
##print(lend[2586])
##print(lend)
##print("1 ",afInformation[1])
##print("5 ",afInformation[4])
##print("7 ",afInformation[200])
#____________________________________________________________#
aero=[]

for aerolineas in afInformation:
    if aerolineas[0][2:5] in aero:
        pass
    else:
        aero.append(aerolineas[0][2:6]) # esta es la forma de hallar los codigos que estan pegados con la aerolinea

aero.pop(0)        
##print(aero)

estado1=True
estado2="Tru"

if (estado1 and estado2)==True:
    print("hola")
x="1 2,3,4"
x=x.split(" ")
y=str(x).strip("[")
y=y.strip("]")
y=y.split(",")
h=[]
for e in y:
    e=e.strip(" ")
    e=e.strip("''")
    
    h.append(e)
    
print("y",y,len(y))
print("h",h,len(h))

h=[2,4,6,8,10,12,13,14,15,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,34,36,38]
print(len(h))
print(":::::::::::::::::::::::::::::::::::::::::::::::::"+'\n')
def dic():
    dic={}
    dic["hola"]="chao"
    print(dic)
    dic["chao"]=5
    print(dic)
    if not("como" in dic):
        print("hola")
    else:
        print(13)
