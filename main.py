
# lo primero que debo hacer es abrir el archivo txt y guardar los datos
#en listas que pueda utilizar

from flask import Flask, request, g, redirect, url_for, render_template, flash, session
import flask
import sys
from flask import json
import math
import ast



# Inicializacion de variables
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.secret_key = 'random string'

apInformation=[] # informacion de aereopuertos
afInformation=[] # informacion de vuelos
cuentas={"usuarios":[],"contraseñas":[]}

def abrirArchivo():
    """
    entra: archivo txt
    hace: transforma la informacion del txt a listas para su futuro uso
    sale: listas con datos de los vuelos
    """
    global apInformation, afInformation
    archivo= open(r"C:\Users\usuario\Desktop\Proyecto Programación\datos/datosVuelo.txt",mode="r+")
    apInformation = archivo.readlines() #lista
    afInformation = apInformation #lista
    apInformation=apInformation[13:36]
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


@app.route('/login',methods=['GET','POST'])
def login():
    """
    entran: usuario y contraseña
    hace: comprueba si el usuario se encuentra registrado
    sale: direcciona al usuario al menu en caso de estar registrado
          de lo contrario puede conectar con registro
    """
    global cuentas
    us=[] #usuarios
    cn=[] #contraseñas
    lista=  open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='r')
    
    for elem in lista:
        elem=ast.literal_eval(elem)
        print(elem)
        print(type(elem))
        elem=elem["login"]
        us.append(elem)
    lista.close()
    lista=  open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='r')
    for eleme in lista:
        eleme=ast.literal_eval(eleme)
        eleme=eleme["password"]
        cn.append(eleme)
    cuentas["usuarios"]=us
    cuentas["contraseñas"]=cn
    estado1=False
    estado2=False
    aux={"usuario":"","contraseña":""}
    lista.close()
    if(request.method == 'POST'):
        if(request.form['boton'] == 'Ingresar'):
            i=0
            for elem in cuentas["usuarios"]:
                if elem == request.form['usuario']:

                    estado1=True
                    j=0
                    for elemento in cuentas["contraseñas"]:
                        if elemento == request.form['password']:
                            estado2=True
                            break
                        else:
                            estado2=False
                            j+=1
                elif estado1== True:
                    break  

                else:
                    estado1=False
                    i+=1
                
            if estado2==True and estado1==True and i==j: 
                aux["usuario"]= request.form['usuario']
                aux["contraseña"]=request.form['password']
                lista=  open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='r')
                for elem in lista:
                    elem=ast.literal_eval(elem)
                    if elem["login"]==request.form['usuario']:
                        aux=elem
                return render_template('menu.html',usuario=aux)
            if estado1==True and (estado2==False or i!=j) :
                flash("la contraseña para el usuario "+request.form['usuario']+'\n'
                    +"esta errada")
                return redirect(url_for('main'))
            if estado1==False and estado2==True:
                flash(" el usuario "+request.form['usuario']+'\n'
                    +"esta errado")
                return redirect(url_for('main'))
            if estado1==False and estado2==False:
                flash("el usuario "+request.form['usuario']+'\n'
                    +"no se encuentra registrado")

                return redirect(url_for('main'))

@app.route('/registro',methods=['GET','POST'])
def registro():
    """
    funcion que enlaza el main con la pagina de registro
    """
    return render_template('registro.html')

@app.route('/registrar',methods=['GET','POST'])
def registrar():
    """
    entra: un diccionario de cuentas y datos ingresados por el usuario mediante el html
    hace: verific que un usuario no esta registrado, posteriormente procede con la primer parte del registro
    sale: un diccionario que contiene la informacion del usuario sin sus preferencias
    """
    global cuentas
    auxD={"nombre":"","apellido":"","email":"","login":"","password":"",
    "preferencias":{"aerolinea":"","escalas":"","horaSalida":"","horaLlegada":""
    ,"comida":[],"clase":""}}

    if(request.method == 'POST'):
        if(request.form['boton'] == 'siguiente'):
            if  request.form['loginR']==""or request.form["nombreR"]=="" or request.form["apellidoR"]=="" or request.form["passwordR"]=="" :
                flash("llene todos los campos")
                return redirect(url_for('registro'))
            elif request.form['loginR'] in cuentas["usuarios"]:
                flash("el usuario "+request.form['loginR']+'\n'
                    +"se encuentra registrado")
                return redirect(url_for('registro'))
            else:
                
                
                auxD["nombre"]=request.form["nombreR"]
                auxD["apellido"]=request.form["apellidoR"]
                auxD["email"]=request.form["correoR"]
                auxD["login"]=request.form["loginR"]
                auxD["password"]=request.form["passwordR"]
                
                return render_template('preferencias.html',datos=auxD)
@app.route('/preferencias/<datos>',methods=['GET','POST'])
def preferencias(datos):
    """
    entra: un diccionario con los datos del usuario sin sus preferencias
            ingresan las preferencias del usuario mediante html
    hace: guarda la preferencias el diccionario de datos del usuario y posteriormente
            lo guarda en un archivo de texto
    sale: un archivo de texto con el perfil del usuario
          se direcciona con la pagina de login
    """
    datos= ast.literal_eval(datos)
    if(request.method == 'POST'):
        if(request.form['boton'] == 'terminar'):
            datos["preferencias"]["aerolinea"]=request.form["aerolineaP"]
            datos["preferencias"]["escalas"]=request.form["escalasP"]
            datos["preferencias"]["horaSalida"]=request.form["horaSalidaP"]
            datos["preferencias"]["horaLlegada"]=request.form["horaLlegadaP"]
            datos["preferencias"]["comida"]=request.form.getlist('comida')
            datos["preferencias"]["clase"]=request.form.getlist('classe')
            archivo= open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='r+')
            if archivo.readlines()==[]:
                archivo.write(str(datos))
                archivo.close()
                flash("registrado exitosamente")
                return redirect(url_for('main'))
            else:
                archivo.write('\n'+str(datos))
                archivo.close()
                flash("registrado exitosamente")
                return redirect(url_for('main'))
        if (request.form['boton'] == 'editar'):
            datos["preferencias"]["aerolinea"]=request.form["aerolineaP"]
            datos["preferencias"]["escalas"]=request.form["escalasP"]
            datos["preferencias"]["horaSalida"]=request.form["horaSalidaP"]
            datos["preferencias"]["horaLlegada"]=request.form["horaLlegadaP"]
            datos["preferencias"]["comida"]=request.form.getlist('comida')
            datos["preferencias"]["clase"]=request.form.getlist('classe')
            archivo= open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='r+')
            lista=archivo.readlines()
            i=0
            for elem in lista:
                elem=str(elem).strip('\n')
                lista[i]=elem
                i+=1
            print(lista)
            i=0
            for elem in lista:
                elem= ast.literal_eval(elem)
                if elem["login"] == datos["login"]:
                    lista[i]=datos
                    break
                else:
                    i+=1
            archivo.close()
            #ingresar cada elemento de lista como una nueva linea excepto, primera que se agrega
            archivo= open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='w')
            i=0
            for dic in lista:
                if i == len(lista)-1:
                    archivo.write('\n'+str(dic))
                    break
                if i!= 0 and i!= len(lista):
                    archivo.write('\n'+str(dic))
                    i+=1
                elif i==0:
                    archivo.write(str(dic))
                    i+=1
                
               
                
            archivo.close()
            flash("ha realizado los cambios de manera satisfactoria")
            return render_template('menu.html',usuario=datos)



@app.route('/editarP/<datos>', methods=['GET','POST'])
def editarP(datos):
    """
    esta funcion sirve de puente entre menu y prefenrencias
    entra: un diccionario con los datos de un usuario
    hace: convierte el string en dict
    sale: redirecciona a preferencias y le envia un diccionario con informacion del usuario
    """
    datos= ast.literal_eval(datos)
    return render_template('preferencias.html',datos=datos)

@app.route('/sugerencias/<datos>', methods=['GET','POST'])
def sugerencia(datos):
    global apInformation, afInformation
    datos= ast.literal_eval(datos)
    preferencia= datos["preferencias"] ## este es el motor de busqueda
    
    iPuerto=apInformation
    iVuelos= afInformation
    mejor=[]
    regular=[]
    poco=[]
   
    for vuelos in iVuelos:
    
        estado1=False    #aerolinea
        estado2=False    #escalas
        estado3=False    #hora de salida
        estado4=False    #hora de llegada
        estado5=False    #comidas
        estado6=False    #clases
        if vuelos[0]== preferencia["aerolinea"]:
            estado1=True
        if  vuelos[6]== preferencia["escalas"] or vuelos[7]== preferencia["escalas"]:
            estado2=True
        if vuelos[3]==preferencia["horaSalida"]:
            estado3=True
        if vuelos[5]==preferencia["horaLlegada"]  :
            estado4=True
        if vuelos[6][0] in preferencia["comida"] or vuelos[6][-1] in preferencia["comida"]:
            estado5=True
        if vuelos[-1][0] in preferencia["clase"] or vuelos[-2][0] in preferencia["clase"] or vuelos[-3][0] in preferencia["clase"] or  vuelos[-4][0] in preferencia["clase"]or vuelos[-5][0] in preferencia["clase"]:
            estado6=True
        if estado1==True and estado2==True and estado3==True and estado4==True and estado5==True and estado6==True:
            mejor.append(vuelos)
    if mejor==[]:    
        for vuelos in iVuelos:
            estado1=False    #aerolinea
            estado2=False    #escalas
            estado3=False    #hora de salida
            estado4=False    #hora de llegada
            estado5=False    #comidas
            estado6=False    #clases
            if vuelos[0]== preferencia["aerolinea"]:
                estado1=True
            if  vuelos[6]== preferencia["escalas"] or vuelos[7]== preferencia["escalas"]:
                estado2=True
            if vuelos[3]==preferencia["horaSalida"]:
                estado3=True
            if vuelos[5]==preferencia["horaLlegada"]  :
                estado4=True
            if vuelos[6][0] in preferencia["comida"] or vuelos[6][-1] in preferencia["comida"]:
                estado5= True
            if vuelos[-1][0] in preferencia["clase"] or vuelos[-2][0] in preferencia["clase"] or vuelos[-3][0] in preferencia["clase"] or  vuelos[-4][0] in preferencia["clase"]or vuelos[-5][0] in preferencia["clase"]:
                estado6=True
            if (estado1==True and estado2==True and estado3==True and estado4==True) and (not vuelos in mejor):
                regular.append(vuelos)
    if mejor==[] and regular==[]:    
        for  vuelos in iVuelos:
            estado1=False    #aerolinea
            estado2=False    #escalas
            estado3=False    #hora de salida
            estado4=False    #hora de llegada
            estado5=False    #comidas
            estado6=False    #clases
            
            if vuelos[0]== preferencia["aerolinea"]:
                estado1=True
            if  vuelos[6]== preferencia["escalas"] or vuelos[7]== preferencia["escalas"]:
                estado2=True
            if vuelos[3]==preferencia["horaSalida"]:
                estado3=True
            if vuelos[5]==preferencia["horaLlegada"]  :
                estado4=True
            if vuelos[6][0] in preferencia["comida"] or vuelos[6][-1] in preferencia["comida"]:
                estado5=True
            if vuelos[-1][0] in preferencia["clase"] or vuelos[-2][0] in preferencia["clase"] or vuelos[-3][0] in preferencia["clase"] or  vuelos[-4][0] in preferencia["clase"]or vuelos[-5][0] in preferencia["clase"]:
                estado6=True
            if (estado1==True or estado2==True or estado3==True or estado4==True or estado5==True or estado6==True) and (not vuelos in mejor) and (not vuelos in regular):
                poco.append(vuelos)
            if  preferencia["aerolinea"]=="" and preferencia["escalas"]=="" and  preferencia["horaSalida"]=="" and  preferencia["horaLlegada"]=="" and  preferencia["comida"]==[] and preferencia["clase"]==[]:
                flash("no hay ningun sugerido con base a su preferencia")
                return render_template('menu.html',usuario=datos)
    print("mejorI",mejor)
    print("regular",regular)
    print("poco",poco)

        
    
    sugeridos={"mejor":mejor,"regular":regular,"poco":poco}
    return render_template('vuelo.html',usuario=datos,vuelos=sugeridos)

    
@app.route('/busqueda/<datos>',methods=['GET','POST'])
def busqueda(datos):
    datos=ast.literal_eval(datos)
    return render_template('BusquedaVuelos.html',datos=datos,vuelos="")

@app.route('/motor/<datos>', methods=['GET','POST'])
def motor(datos):
    global apInformation, afInformation
    datos= ast.literal_eval(datos)
    abrirArchivo() #lo quita
    preferencia= datos["preferencias"] ## este es el motor de busqueda
    iPuerto=apInformation
    iVuelos= afInformation
    mejor=[]
    aeroSalida=""
    aeroLlegada=""
    if(request.method == 'POST'):
        if(request.form['boton'] == 'Buscar'):
            if request.form["ciudadS"] != request.form["ciudadD"]:
                for port in iPuerto:
                    
                    if request.form["ciudadS"]==port[4]:
                       
                        aeroSalida=port[0]
                    
               
                for port in iPuerto:
                  
                    if request.form["ciudadD"]==port[4]:
                        aeroLlegada=port[0]
                        
              
                if request.form["preferencias"] == "no":
                    for vuelos in iVuelos:
                        if vuelos[2]==aeroSalida and vuelos[4]==aeroLlegada:
                            
                            mejor.append(vuelos)
                            
                    
                    if mejor==[]:
                        flash("no hay vuelos disponibles")
                        return render_template('BusquedaVuelos.html',datos=datos,vuelos="")
                    else:
                        sugerido={"mejor":mejor}
                        return render_template('BusquedaVuelos.html',datos=datos,vuelos=sugerido)
                if request.form["preferencias"]=="si":
                    for vuelos in iVuelos:
                        if vuelos[2]==aeroSalida and vuelos[4]==aeroLlegada and vuelos[0]== preferencia["aerolinea"] and (vuelos[6]== preferencia["escalas"] or vuelos[7]== preferencia["escalas"]) and vuelos[3]==preferencia["horaSalida"] and vuelos[5]==preferencia["horaLlegada"] and (vuelos[6][0] in preferencia["comida"] or vuelos[6][-1] in preferencia["comida"]) and (vuelos[-1][0] in preferencia["clase"] or vuelos[-2][0] in preferencia["clase"] or vuelos[-3][0] in preferencia["clase"] or  vuelos[-4][0] in preferencia["clase"]or vuelos[-5][0] in preferencia["clase"]):
                            mejor.append(vuelos)
                            sugerido={"mejor":mejor}
                            return render_template('BusquedaVuelos.html',datos=datos,vuelos=sugerido)
                    if mejor==[]:
                        flash("no hay vuelos, considere las preferencias")
                        return render_template('BusquedaVuelos.html',datos=datos,vuelos="")
            else:
                flash("no hay vuelos de una ciudad a ella misma")
                return render_template('BusquedaVuelos.html',datos=datos,vuelos="")
@app.route('/preReserva/<datos>/<vuelos>',methods=['GET','POST'])
def preReserva(datos,vuelos):
    if(request.method == 'POST'):
        if(request.form['boton'] == 'reservar'):
            return redirect(url_for('mapa',datos=datos,vuelos=vuelos))
        if(request.form['boton'] == 'hacer reserva'):
            datos=ast.literal_eval(datos)
            vuelos=ast.literal_eval(vuelos)
            print(vuelos)
            mejor=[]
            for vuelo in vuelos["mejor"]:
                if request.form["vuelo"]==vuelo[1]:
                    mejor.append(vuelo)
                    sugerencia={"mejor":mejor}
                    return render_template('hacerReserva.html',datos=datos,vuelos=sugerencia)
@app.route('/reservando/<datos>/<vuelos>',methods=['GET','POST'])   
def reservar(datos,vuelos):
    global afInformation
    datos=ast.literal_eval(datos)
    vuelos=ast.literal_eval(vuelos)
    #print(vuelos)
    #print(datos)
    mejor=[]
    if ("reservas" in datos):
        datos["reservas"]["aero"].append(vuelos["mejor"][0][0])
        datos["reservas"]["codigo"].append(vuelos["mejor"][0][1])
        datos["reservas"]["cSalida"].append(vuelos["mejor"][0][2])
        datos["reservas"]["cLlegada"].append(vuelos["mejor"][0][4])
        print("final",datos)
        archivo= open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='r+')
        lista=archivo.readlines()
        i=0
        for elem in lista:
            elem=str(elem).strip('\n')
            lista[i]=elem
            i+=1
        i=0
        for elem in lista:
            elem= ast.literal_eval(elem)
            if elem["login"] == datos["login"]:
                lista[i]=datos
                break
            else:
                i+=1
        archivo.close()
        #ingresar cada elemento de lista como una nueva linea excepto, primera que se agrega
        archivo= open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='w')
        i=0
        for dic in lista:
            if i==0:
                archivo.write(str(dic))
                i+=1
            else:
                archivo.write('\n'+str(dic))
                i+=1
            
        archivo.close()
        flash("ha realizado la reserva  de manera satisfactoria")
        i=0
        while i< len(datos["reservas"]["codigo"]):
            for vuelo in afInformation:
                if datos["reservas"]["codigo"][i] == vuelo[1] and datos["reservas"]["aero"][i]==vuelo[0] and datos["reservas"]["cSalida"][i]==vuelo[2] and datos["reservas"]["cLlegada"][i]==vuelo[4]:
                    
                    mejor.append(vuelo)
            i+=1
        vuelos["mejor"]=mejor
        
        return render_template('reservas.html',datos=datos,vuelos=vuelos)
    else:
        datos["reservas"]={"aero":[vuelos["mejor"][0][0]] ,"codigo":[vuelos["mejor"][0][1]],"cSalida":[vuelos["mejor"][0][2]] ,"cLlegada":[vuelos["mejor"][0][4]]} # en reservas solo se guarda el codigo del vuelo
        print("final",datos,datos["reservas"])
        archivo= open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='r+')
        lista=archivo.readlines()
        i=0
        for elem in lista:
            elem=str(elem).strip('\n')
            lista[i]=elem
            i+=1
        print(lista)
        i=0
        for elem in lista:
            elem= ast.literal_eval(elem)
            if elem["login"] == datos["login"]:
                lista[i]=datos
                break
            else:
                i+=1
        archivo.close()
        archivo= open(r'C:\Users\usuario\Desktop\Proyecto Programación\datos\datosUsuarios.txt', mode='w')
        i=0
        for dic in lista:
            if i==0:
                archivo.write(str(dic))
                i+=1
            else:
                archivo.write('\n'+str(dic))
                i+=1
            
        archivo.close()
        flash("ha realizado la reserva de manera satisfactoria")
        i=0
        while i< len(datos["reservas"]["codigo"]):
            for vuelo in afInformation:
                if datos["reservas"]["codigo"][i] == vuelo[1] and datos["reservas"]["aero"][i]==vuelo[0] and datos["reservas"]["cSalida"][i]==vuelo[2] and datos["reservas"]["cLlegada"][i]==vuelo[4]:
                    mejor.append(vuelo)
            i+=1
        vuelos["mejor"]=mejor
        print("vuelos fin ",vuelos)
        return render_template('reservas.html',datos=datos,vuelos=vuelos)

                        






@app.route('/historial/<datos>',methods=['GET','POST'])
def historial(datos):
    global afInformation
    datos=ast.literal_eval(datos)
    mejor=[]
    vuelos={}
    if ("reservas" in datos):
        i=0
        while i< len(datos["reservas"]["codigo"]):
            for vuelo in afInformation:
                if datos["reservas"]["codigo"][i] == vuelo[1] and datos["reservas"]["aero"][i]==vuelo[0] and datos["reservas"]["cSalida"][i]==vuelo[2] and datos["reservas"]["cLlegada"][i]==vuelo[4]:
                        
                    mejor.append(vuelo)
            i+=1
        vuelos["mejor"]=mejor
        return render_template('historial.html',datos=datos,vuelos=vuelos)
    else:
        flash("No tiene ninguna reserva")
        return render_template('menu.html',usuario=datos)
        
@app.route('/mapa/<datos>/<vuelos>',methods=['GET','POST'])
def mapa(datos,vuelos):
    global apInformation
    datos=ast.literal_eval(datos)
    vuelos=ast.literal_eval(vuelos)
    if len(vuelos)>1:
        mejor= vuelos["mejor"] #if != [] => es una lista de listas
        regular= vuelos["regular"]
        poco= vuelos["poco"]
     
      
        dibujoL=[]
        dibujoD={"cOrigen":"","xInicial":"","yInicial":"","cFinal":"","xFinal":"","yFinal":"","timeI":"","timeF":""}
        codigo=""
        if(request.method == 'POST'):
            if(request.form['boton'] == 'mas informacion'):
                codigo=request.form["vuelo"]
                
                if mejor!=[]:
                    i=0
                    for vuelo in mejor:
                      
                        if codigo== mejor[i][1]:
                            dibujoL=vuelo
                            break
                        i+=1
                if regular!=[]:     
                    i=0   
                    for vuelo in regular:
                       
                        if codigo== regular[i][1]:
                            dibujoL=vuelo
                            break
                        i+=1
                if poco!=[]:
                    i=0
                    for vuelo in poco:
                       
                        if codigo== poco[i][1]:
                            dibujoL=vuelo
                            break
                        i+=1
                
                for port in apInformation:
                    
                    if dibujoL[2]==port[0]:
                       
                        dibujoD["cOrigen"]=port[4]
                        dibujoD["xInicial"]=port[2]
                        dibujoD["yInicial"]=port[3]
                        dibujoD["timeI"]=port[1]
                        break
               
                for port in apInformation:
                    if dibujoL[4]==port[0]:
                        dibujoD["cFinal"]=port[4]
                        dibujoD["xFinal"]=port[2]
                        dibujoD["yFinal"]=port[3]
                        dibujoD["timeF"]=port[1]
                        break
              
                return render_template('mapa.html',datosDibujo=dibujoD,datos=datos)
    else:
        dibujoL=vuelos["mejor"][0]
        
        dibujoD={"cOrigen":"","xInicial":"","yInicial":"","cFinal":"","xFinal":"","yFinal":"","timeI":"","timeF":""}
        codigo=dibujoL[1]
        for port in apInformation:
                    
            if dibujoL[2]==port[0]:
                       
                dibujoD["cOrigen"]=port[4]
                dibujoD["xInicial"]=port[2]
                dibujoD["yInicial"]=port[3]
                dibujoD["timeI"]=port[1]
                break
               
        for port in apInformation:
            if dibujoL[4]==port[0]:
                dibujoD["cFinal"]=port[4]
                dibujoD["xFinal"]=port[2]
                dibujoD["yFinal"]=port[3]
                dibujoD["timeF"]=port[1]
                break
              
        return render_template('mapa.html',datosDibujo=dibujoD,datos=datos)








@app.route('/',methods=['GET','POST'])
def main():
    abrirArchivo()

    return render_template('main.html')
    



if __name__ == '__main__':
    app.run(debug=True,port=8000)
    # faltan mostrar las sugenrencias e iniciar con el algoritmo de reserva, segun caractersiticas.
    # ademas toca implementar el mapa y sale!


    
    
