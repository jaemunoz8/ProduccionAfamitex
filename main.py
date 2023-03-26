from ast import For, Global, Try
from glob import glob
from operator import concat, truediv
from sqlite3 import Row
import string
from typing import Concatenate
from bson import ObjectId
from flask import Flask, render_template, redirect, request
import requests
from jmespath import search
import requests
import pymongo
from pymongo import MongoClient
from pymongo import MongoClient
from pymongo import ReturnDocument
from tomlkit import document, table
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import json
import os
from datetime import datetime
from pprint import pprint
import pyodbc
from getpass4 import getpass

server = 'JETT\SQLEXPRESS'
bd = 'produccion'
usuario = 'sa'
contrasena = 'produccion'

try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server};SERVER='+server+';DATABASE='+bd+';UID='+usuario+';PWD='+contrasena)
    print('CONEXIÓN EXITOSA')
except: print('ERROR DE CONEXIÓN')

datosJSON = []
def mostrarDatos():
    datosJSON.clear()
    cursor = conexion.cursor()
    print(cursor.execute("select * from octable"))
    #print(cursor)
    #oc = cursor.fetchone()
    oc = cursor.fetchall()
    # print(oc)
    for documento in oc:
        datosJSON.append({
        "_id":documento[0],"oc":documento[0],"cliente":documento[5] ,"referencia":documento[6] ,"fecha_solicitud":documento[1],
        "fecha_ingresado":documento[2], "ans":documento[4],"fecha_programada_entrega":documento[3],"total_despachado":documento[7],"estadooc":documento[8],"observaciones":documento[9]})
        oc = cursor.fetchone()
    #print(datosJSON[1]["oc"])
    cursor.close()
    conexion.commit()

datosJSONop = []
def mostrarDatosOp():
    datosJSONop.clear()
    cursor = conexion.cursor()
    print(cursor.execute("select * from optable"))
    print(cursor)
    #op = cursor.fetchone()
    op = cursor.fetchall()
    for documento in op:
        datosJSONop.append({
        "op":documento[1],"oc":documento[0],"color":documento[2] ,"color1":documento[3] ,"color2":documento[4],
        "espuma":documento[5], "cod_tela":documento[6],"talla":documento[7],"cantidad_solicitada":documento[8],"largo":documento[9]
        ,"ancho":documento[10],"tira":documento[11],"metros_espuma":documento[12],"metros_tela":documento[13],"metros_tela1":documento[14],"metros_tela2":documento[15]
        ,"verific_existencia_espuma":documento[16],"verific_existencia_tela":documento[17],"observaciones":documento[18],"cantidad_despachada":documento[19],"estadoop":documento[20]
        ,"asignado":documento[21],"inicio_real":documento[22],"usuario_inicio":documento[23],"final_real":documento[24],"usuario_final":documento[25],"pestana":documento[26]
        ,"referencia":documento[27],"cant_corte1":documento[28],"cant_corte2":documento[29],"cant_canastas_x_talla":documento[30],"cant_imperfectos":documento[31]
        ,"cant_prehor":documento[32],"cant_cp":documento[33],"cant_bond":documento[34],"fecha_facturacion":documento[35],"cant_emp":documento[36],"area":documento[37]})
        oc = cursor.fetchone()
    cursor.close()

datosOPporArea=[]
def OPporArea(arealog):
    datosOPporArea.clear()
    cursor = conexion.cursor()
    print(cursor.execute("select * from optable"))
    print(cursor)
    op = cursor.fetchall()
    i=0
    for documento in op: 
        if arealog==datosJSONop[i]["asignado"]:
            datosOPporArea.append({
        "op":documento[1],"oc":documento[0],"color":documento[2] ,"color1":documento[3] ,"color2":documento[4],
        "espuma":documento[5], "cod_tela":documento[6],"talla":documento[7],"cantidad_solicitada":documento[8],"largo":documento[9]
        ,"ancho":documento[10],"tira":documento[11],"metros_espuma":documento[12],"metros_tela":documento[13],"metros_tela1":documento[14],"metros_tela2":documento[15]
        ,"verific_existencia_espuma":documento[16],"verific_existencia_tela":documento[17],"observaciones":documento[18],"cantidad_despachada":documento[19],"estadoop":documento[20]
        ,"asignado":documento[21],"inicio_real":documento[22],"usuario_inicio":documento[23],"final_real":documento[24],"usuario_final":documento[25],"pestana":documento[26]
        ,"referencia":documento[27],"cant_corte1":documento[28],"cant_corte2":documento[29],"cant_canastas_x_talla":documento[30],"cant_imperfectos":documento[31]
        ,"cant_prehor":documento[32],"cant_cp":documento[33],"cant_bond":documento[34],"fecha_facturacion":documento[35],"cant_emp":documento[36],"area":documento[37]})
        # "op":documento[1],"oc":documento[0],"color":documento[2] ,"color1":documento[3] ,"color2":documento[4],
        # "espuma":documento[5], "cod_tela":documento[6],"talla":documento[7],"cantidad_solicitada":documento[8],"largo":documento[9]
        # ,"ancho":documento[10],"tira":documento[11],"metros_espuma":documento[12],"metros_tela":documento[13],"metros_tela1":documento[14],"metros_tela2":documento[15]
        # ,"verific_existencia_espuma":documento[16],"verific_existencia_tela":documento[17],"observaciones":documento[18],"cantidad_despachada":documento[19],"estadoop":documento[20]
        # ,"asignado":documento[21]})
        print(i)
        i=i+1
    cursor.close()
    return datosOPporArea

datosOPhistorial=[]
def OPhistorial(_oc):
    datosOPhistorial.clear()
    cursor = conexion.cursor()
    print(cursor.execute("select * from opLog where oc= '"+_oc+"' order by fecha_cambio desc"))
    print(cursor)
    opLog = cursor.fetchall()
    i=0
    for documento in opLog: 
        #if _oc==datosOPhistorial[i]["oc"]:
        datosOPhistorial.append({"op":documento[1],"oc":documento[0],"color":documento[2] ,"color1":documento[3] ,"color2":documento[4],
        "espuma":documento[5], "cod_tela":documento[6],"talla":documento[7],"cantidad_solicitada":documento[8],"largo":documento[9]
        ,"ancho":documento[10],"tira":documento[11],"metros_espuma":documento[12],"metros_tela":documento[13],"metros_tela1":documento[14],"metros_tela2":documento[15]
        ,"verific_existencia_espuma":documento[16],"verific_existencia_tela":documento[17],"observaciones":documento[18],"cantidad_despachada":documento[19],"estadoop":documento[20]
        ,"asignado":documento[21],"inicio_real":documento[22],"usuario_inicio":documento[23],"final_real":documento[24],"usuario_final":documento[25],"pestana":documento[26]
        ,"referencia":documento[27],"cant_corte1":documento[28],"cant_corte2":documento[29],"cant_canastas_x_talla":documento[30],"cant_imperfectos":documento[31]
        ,"cant_prehor":documento[32],"cant_cp":documento[33],"cant_bond":documento[34],"fecha_facturacion":documento[35],"cant_emp":documento[36],"area":documento[37]
        ,"fecha_cambio":documento[38],"usuario_cambio":documento[39]})
        print(i)
        i=i+1
    cursor.close()
    #return datosOPhistorial


datosJSONusuarios = []
def usuarios():
    datosJSONusuarios.clear()
    cursor = conexion.cursor()
    print(cursor.execute("select * from usuarios order by activo desc"))
    print(cursor)
    #op = cursor.fetchone()
    usuario = cursor.fetchall()
    for documento in usuario:
        datosJSONusuarios.append({
        "id":documento[0],"nombre":documento[1],"email":documento[2] ,"pass":documento[3] ,"area":documento[4],"rol":documento[5],"activo":documento[6]})
    cursor.close()

usuarios()
mostrarDatos()
mostrarDatosOp()

##################### INICIA LA COMPOSICIÓN CON FLASK ##################################################################
app = Flask(__name__)

@app.route('/')
def login():
    usuarios()
    return render_template('login.html',datos=datosJSONusuarios)

#usuarioLogueado = ""
@app.route('/validacion', methods=['POST'])
def validacion():
    _usuario = request.form['loginName']
    global arealog
    global rollog
    global usuarioLogueado
    global nombrelog
    usuarioLogueado=request.form['loginName']
    _contraseña = request.form['loginPassword'] 
    j=int(0)
    for j in range(0,len(datosJSONusuarios),1):
        if datosJSONusuarios[j]["id"] == _usuario:
            print("ingresó al if1")
            if _contraseña == datosJSONusuarios[j]["pass"]:
                nombrelog = datosJSONusuarios[j]["nombre"]
                arealog = datosJSONusuarios[j]["area"]
                rollog = datosJSONusuarios[j]["rol"]
                _id=datosJSONusuarios[j]["id"]
                if rollog=="Administrador":
                    print("ingresó administrador")
                    cursorInsertUser = conexion.cursor()
                    consultaLogin="insert into LogLogin(id, nombre, area, rol, fecha_login) values ('"+_id+"','"+nombrelog+"','"+arealog+"','"+rollog+"','"+str(datetime.now())+"')"
                    cursorInsertUser.execute(consultaLogin)
                    cursorInsertUser.close()
                    conexion.commit()
                    return redirect('/index')
                elif rollog=="Operario":
                    print("ingresó operario")
                    cursorInsertUser = conexion.cursor()
                    consultaLogin="insert into LogLogin(id, nombre, area, rol, fecha_login) values ('"+_id+"','"+nombrelog+"','"+arealog+"','"+rollog+"','"+str(datetime.now())+"')"
                    cursorInsertUser.execute(consultaLogin)
                    cursorInsertUser.close()
                    conexion.commit()
                    return redirect('/verOPoperario/'+arealog+'/'+nombrelog+'/'+_usuario+'')
                elif rollog=="Producción":
                    print("Ingresó producción")
                    return redirect('/index')
            else:
                print("Usuario correcto, falló contraseña")
                return redirect('/')
    return redirect('/')

@app.route('/registro')

@app.route('/index')
def index():
    mostrarDatos()
    return render_template('index.html',datos=datosJSON)

@app.route('/verUsers')
def verUsers():
    usuarios()
    return render_template('verUsers.html',datos=datosJSONusuarios)

@app.route('/createUser')
def createUser():
    fecha_actual=datetime.date(datetime.now())
    return render_template('createUser.html')

@app.route('/storeUser', methods=['POST'])
def storageUser():
    _txtid = request.form['txtid']
    _txtnombre = request.form['txtnombre']
    _txtemail = request.form['txtemail']
    _txtpass = request.form['txtpass']
    _txtarea = request.form['txtarea']
    _txtrol = request.form['txtrol']
    _txtactivo = request.form['txtactivo']
    cursorInsertUser = conexion.cursor()
    consulta="insert into usuarios(id, nombre, email, pass, area, rol, activo) values ('"+_txtid+"','"+_txtnombre+"','"+_txtemail+"','"+_txtpass+"','"+_txtarea+"','"+_txtrol+"','"+_txtactivo+"')"
    consultaLog="insert into usuariosLog(id, nombre, email, pass, area, rol, activo, fecha_cambio, usuario_cambio) values ('"+_txtid+"','"+_txtnombre+"','"+_txtemail+"','"+_txtpass+"','"+_txtarea+"','"+_txtrol+"','"+_txtactivo+"','"+str(datetime.now())+"','"+usuarioLogueado+"')"
    #consulta="insert into octable(oc) values ('SF50');"
    cursorInsertUser.execute(consulta)
    cursorInsertUser.execute(consultaLog)
    cursorInsertUser.close()
    conexion.commit()
    return redirect('/verUsers')

@app.route('/editUsers/<id>')
def editUsers(id):
    usuarios()
    i=0
    indic=0
    for i in range(0,len(datosJSONusuarios),1):
        n=str(datosJSONusuarios[i]["id"].strip())
        m=str(id)
        if n == m:
            indic = i
            break
    return render_template('editUsers.html',dato=datosJSONusuarios[indic])

@app.route('/updateUser', methods=['POST'])
def updateUser():
    _txtid = request.form['txtid']
    _txtnombre = request.form['txtnombre']
    _txtemail = request.form['txtemail']
    _txtpass = request.form['txtpass']
    _txtarea = request.form['txtarea']
    _txtrol = request.form['txtrol']
    _txtactivo = request.form['txtactivo']
    #id11 = request.form['txtID']
    #coleccion.update_many({'_id':ObjectId(id11)},{"$set":{"oc":_oc,"cliente":_cliente,"referencia":_referencia,"fecha_solicitud":_fecha_solicitud,"fecha_ingresado":_fecha_ingreso,"ans":_ans,"fecha_programada_entrega":_fecha_programada_entrega}},upsert=False)
    cursorUpdateUser = conexion.cursor()
    consulta="update usuarios set id='"+_txtid+"',nombre='"+_txtnombre+"',email='"+_txtemail+"',pass='"+_txtpass+"',area='"+_txtarea+"',rol='"+_txtrol+"',activo='"+_txtactivo+"' where id='"+_txtid+"'"
    consultaLog="insert into usuariosLog(id, nombre, email, pass, area, rol, activo, fecha_cambio, usuario_cambio) values ('"+_txtid+"','"+_txtnombre+"','"+_txtemail+"','"+_txtpass+"','"+_txtarea+"','"+_txtrol+"','"+_txtactivo+"','"+str(datetime.now())+"','"+usuarioLogueado+"')"    
    cursorUpdateUser.execute(consulta)
    cursorUpdateUser.execute(consultaLog)
    cursorUpdateUser.close()
    conexion.commit()
    return redirect('/verUsers')

@app.route('/destroy/<oc>')
def destroy(oc):
    print("Esta es la oc a borrar ",oc)
    cursorBorrar = conexion.cursor()
    consulta="delete from octable where oc='"+oc+"'"
    cursorBorrar.execute(consulta)
    cursorBorrar.close()
    conexion.commit()
    return redirect('/index')

@app.route('/destroyOP/<op>')
def destroyOP(op):
    print("Esta es la op a borrar ",op)
    cursorBorrar = conexion.cursor()
    consulta="delete from optable where op='"+op+"'"
    cursorBorrar.execute(consulta)
    cursorBorrar.close()
    conexion.commit()
    guion=op.find("-")
    _oc=op[0:guion]
    return redirect('/verOP/'+_oc+'')

@app.route('/verOP/<id>')
def verOP(id):
    mostrarDatosOp()
    i=0
    indice=0
    datosJsonEnviarOp = []
    datosJsonEnviarOp.clear()
    for i in range(0,len(datosJSONop),1):
        if str(datosJSONop[i]["oc"]) ==id:
            datosJsonEnviarOp.append(datosJSONop[i])
    i=0
    indic=0
    for i in range(0,len(datosJSON),1):
        n=str(datosJSON[i]["oc"].strip())
        m=str(id)
        if n == m:
            indic = i
            break
    return render_template('verOP.html',datos=datosJsonEnviarOp,datos1=datosJSON[indic],occonsulta=id)

@app.route('/verOPhistorial/<_op>/<_oc>')
def verOPhistorial(_op,_oc):
    OPhistorial(_oc)
    i=0
    indice=0
    datosJsonEnviarOphistorial = []
    datosJsonEnviarOphistorial.clear()
    for i in range(0,len(datosOPhistorial),1):
        if str(datosOPhistorial[i]["op"]) == _op:
            datosJsonEnviarOphistorial.append(datosOPhistorial[i])
    i=0
    indic=0
    for i in range(0,len(datosJSON),1):
        n=str(datosJSON[i]["oc"].strip())
        m=str(_oc)
        if n == m:
            indic = i
            break
    return render_template('verOPhistorial.html',datos=datosJsonEnviarOphistorial,datos1=datosJSON[indic],occonsulta=_oc)

@app.route('/verOPoperario/<arealog>/<nombrelog>/<usuario>')
def verOPoperario(arealog,nombrelog,usuario):
    mostrarDatosOp()
    i=0
    print(usuario)
    datosJSONoperario = []
    datosJSONoperario.clear()
    if arealog=="Corte_vertical" or arealog=="Bondeo":      #Caso que ingresa por área
        for i in range(0,len(datosJSONop),1):
            if str(datosJSONop[i]["area"]) == arealog:
                datosJSONoperario.append(datosJSONop[i])
                print("entró área")
                #Código para validar qué campos son editables y cuáles son readonly
    elif arealog=="Prehormado" or arealog=="Corte_plano" or arealog=="Empaque":   #Caso que ingresa por persona
        for i in range(0,len(datosJSONop),1):
            if str(datosJSONop[i]["asignado"]) == usuario:
                datosJSONoperario.append(datosJSONop[i])
                print("entró persona")
    return render_template('verOPoperario.html',datos=datosJSONoperario,area=arealog,nombre=nombrelog)


@app.route('/createOP/<oc>')
def createOP(oc):
    mostrarDatosOp()
    i=0
    cantidadops=0
    for i in range(0,len(datosJSONop),1):
        if datosJSONop[i]["oc"]==oc:
            cantidadops+=1
    opEnviar=oc+"-"+str(cantidadops+1)
    return render_template('createOP.html',_oc=oc,_op=opEnviar)

@app.route('/create')
def create():
    fecha_actual=datetime.date(datetime.now())
    return render_template('create.html', dato=fecha_actual)

@app.route('/store', methods=['POST'])
def storage():
    _oc = request.form['oc']
    _cliente = request.form['cliente'] 
    _referencia = request.form['referencia']
    _fecha_ingreso = request.form['fecha_ingreso']
    _fecha_solicitud = request.form['fecha_solicitud']
    _ans = request.form['ans']
    _fecha_programada_entrega = request.form['fecha_programada_entrega']
    _total_despachado = request.form['total_despachado']
    _estadooc = request.form['estadooc']
    _observaciones = request.form['observaciones']
    cursorInsert = conexion.cursor()
    consulta="insert into octable(oc,fecha_solicitud,fecha_ingreso,fecha_programada_entrega,ans,cliente,referencia,total_despachado,estadooc,observaciones) values ('"+_oc+"','"+_fecha_solicitud+"','"+str(datetime.now())+"','"+_fecha_programada_entrega+"','"+_ans+"','"+_cliente+"','"+_referencia+"','"+_total_despachado+"','"+_estadooc+"','"+_observaciones+"')"
    consultaLog="insert into ocLog(oc,fecha_solicitud,fecha_ingreso,fecha_programada_entrega,ans,cliente,referencia,total_despachado,estadooc,observaciones,fecha_cambio,usuario_cambio) values ('"+_oc+"','"+_fecha_solicitud+"','"+str(datetime.now())+"','"+_fecha_programada_entrega+"','"+_ans+"','"+_cliente+"','"+_referencia+"','"+_total_despachado+"','"+_estadooc+"','"+_observaciones+"','"+str(datetime.now())+"','"+usuarioLogueado+"')"
    cursorInsert.execute(consulta)
    cursorInsert.execute(consultaLog)
    cursorInsert.close()
    conexion.commit()
    return redirect('/index')

@app.route('/edit/<oc>')
def edit(oc):
    mostrarDatos()
    i=0
    indic=0
    for i in range(0,len(datosJSON),1):
        n=str(datosJSON[i]["oc"].strip())
        m=str(oc)
        if n == m:
            indic = i
            break
    return render_template('edit.html',dato=datosJSON[indic])

@app.route('/update', methods=['POST'])
def update():
    _oc = request.form['txtoc']
    _cliente = request.form['txtcliente']
    _referencia = request.form['txtreferencia']
    _fecha_solicitud = request.form['txtfecha_solicitud']
    _fecha_ingreso = request.form['txtfecha_ingreso']
    _ans = request.form['txtans']
    _fecha_programada_entrega = request.form['txtfecha_programada_entrega']
    _total_despachado= request.form['txttotal_despachado']
    _estadooc= request.form['txtestadooc']
    _observaciones= request.form['txtobservaciones']
    #id11 = request.form['txtID']
    #coleccion.update_many({'_id':ObjectId(id11)},{"$set":{"oc":_oc,"cliente":_cliente,"referencia":_referencia,"fecha_solicitud":_fecha_solicitud,"fecha_ingresado":_fecha_ingreso,"ans":_ans,"fecha_programada_entrega":_fecha_programada_entrega}},upsert=False)
    cursorUpdate = conexion.cursor()
    consulta="update octable set fecha_solicitud='"+_fecha_solicitud+"',fecha_programada_entrega='"+_fecha_programada_entrega+"',ans='"+_ans+"',cliente='"+_cliente+"',referencia='"+_referencia+"',total_despachado='"+_total_despachado+"',estadooc='"+_estadooc+"',observaciones='"+_observaciones+"' where oc='"+_oc+"'"
    consultaLog="insert into ocLog(oc,fecha_solicitud,fecha_ingreso,fecha_programada_entrega,ans,cliente,referencia,total_despachado,estadooc,observaciones,fecha_cambio,usuario_cambio) values ('"+_oc+"','"+_fecha_solicitud+"','"+str(datetime.now())+"','"+_fecha_programada_entrega+"','"+_ans+"','"+_cliente+"','"+_referencia+"','"+_total_despachado+"','"+_estadooc+"','"+_observaciones+"','"+str(datetime.now())+"','"+usuarioLogueado+"')"
    cursorUpdate.execute(consulta)
    cursorUpdate.execute(consultaLog)
    cursorUpdate.close()
    conexion.commit()
    return redirect('/index')

@app.route('/storeOP', methods=['POST'])
def storageOP():
    _oc = request.form['txtoc']
    op = request.form['txtop']
    _color = request.form['txtcolor']
    _color1 = request.form['txtcolor1']
    _color2 = request.form['txtcolor2']
    _espuma = request.form['txtespuma']
    _cod_tela = request.form['txtcod_tela']
    _talla= request.form['txttalla']
    _cantidad_solicitada= request.form['txtcantidad_solicitada']
    _largo= request.form['txtlargo']
    _ancho= request.form['txtancho']
    _tira= request.form['txttira']
    _metros_espuma= request.form['txtmetros_espuma']
    _metros_tela= request.form['txtmetros_tela']
    _metros_tela1= request.form['txtmetros_tela1']
    _metros_tela2= request.form['txtmetros_tela2']
    _verific_existencia_espuma= request.form['txtverific_existencia_espuma']
    _verific_existencia_tela= request.form['txtverific_existencia_tela']
    _observaciones= request.form['txtobservaciones']
    _cantidad_despachada= request.form['txtcantidad_despachada']
    _estadoop= request.form['txtestadoop']
    _asignado= request.form['txtasignado']
    _area= request.form['txtarea']
    _pestana= request.form['txtpestana']
    cursorInsertOP = conexion.cursor()
    consulta="insert into optable(oc,op,color,color1,color2,ref_espuma_color,cod_tela,talla,cantidad_solicitada,largo,ancho,tira,metros_espuma,metros_tela,metros_tela1,metros_tela2,verific_existencia_espuma,verific_existencia_tela,observaciones,cantidad_despachada,estadoop,asignado,area,pestana) values ('"+_oc+"','"+op+"','"+_color+"','"+_color1+"','"+_color2+"','"+_espuma+"','"+_cod_tela+"','"+_talla+"','"+_cantidad_solicitada+"','"+_largo+"','"+_ancho+"','"+_tira+"','"+_metros_espuma+"','"+_metros_tela+"','"+_metros_tela1+"','"+_metros_tela2+"','"+_verific_existencia_espuma+"','"+_verific_existencia_tela+"','"+_observaciones+"','"+_cantidad_despachada+"','"+_estadoop+"','"+_asignado+"','"+_area+"','"+_pestana+"')"
    consultaLog="insert into opLog(oc,op,color,color1,color2,ref_espuma_color,cod_tela,talla,cantidad_solicitada,largo,ancho,tira,metros_espuma,metros_tela,metros_tela1,metros_tela2,verific_existencia_espuma,verific_existencia_tela,observaciones,cantidad_despachada,estadoop,asignado,area,pestana,fecha_cambio,usuario_cambio) values ('"+_oc+"','"+op+"','"+_color+"','"+_color1+"','"+_color2+"','"+_espuma+"','"+_cod_tela+"','"+_talla+"','"+_cantidad_solicitada+"','"+_largo+"','"+_ancho+"','"+_tira+"','"+_metros_espuma+"','"+_metros_tela+"','"+_metros_tela1+"','"+_metros_tela2+"','"+_verific_existencia_espuma+"','"+_verific_existencia_tela+"','"+_observaciones+"','"+_cantidad_despachada+"','"+_estadoop+"','"+_asignado+"','"+_area+"','"+_pestana+"','"+str(datetime.now())+"','"+usuarioLogueado+"')"
    cursorInsertOP.execute(consulta)
    cursorInsertOP.execute(consultaLog)
    cursorInsertOP.close()
    conexion.commit()
    return redirect('/verOP/'+_oc+'')

@app.route('/editOP/<op>')
def editOP(op):
    mostrarDatosOp()
    i=0
    indice=0
    for i in range(0,len(datosJSONop),1):
        if str(datosJSONop[i]["op"]) == op:
            indice = i 
            break 
    showfield=[]
    if arealog=="Bondeo":
        showfield = {"op":"","oc":"","color":"readonly" ,"color1":"readonly" ,"color2":"readonly","espuma":"readonly", "cod_tela":"readonly","talla":"readonly","cantidad_solicitada":"readonly","largo":"readonly"
        ,"ancho":"readonly","tira":"readonly","metros_espuma":"readonly","metros_tela":"readonly","metros_tela1":"readonly","metros_tela2":"readonly","verific_existencia_espuma":""
        ,"verific_existencia_tela":"","observaciones":"","cantidad_despachada":"","estadoop":"readonly","asignado":"","inicio_real":"","usuario_inicio":"","final_real":""
        ,"usuario_final":"","pestana":"hidden","referencia":"readonly","cant_corte1":"hidden","cant_corte2":"hidden","cant_canastas_x_talla":"hidden","cant_imperfectos":"","cant_prehor":"hidden"
        ,"cant_cp":"hidden","cant_bond":"","fecha_facturacion":"hidden","cant_emp":"hidden","area":"","option":"disabled"}
    elif arealog=="Corte_vertical":
        showfield = {"op":"","oc":"","color":"readonly" ,"color1":"readonly" ,"color2":"readonly","espuma":"readonly", "cod_tela":"readonly","talla":"readonly","cantidad_solicitada":"readonly","largo":"readonly"
        ,"ancho":"readonly","tira":"readonly","metros_espuma":"readonly","metros_tela":"hidden","metros_tela1":"hidden","metros_tela2":"hidden","verific_existencia_espuma":"hidden"
        ,"verific_existencia_tela":"hidden","observaciones":"","cantidad_despachada":"","estadoop":"readonly","asignado":"","inicio_real":"","usuario_inicio":"","final_real":""
        ,"usuario_final":"","pestana":"hidden","referencia":"readonly","cant_corte1":"","cant_corte2":"","cant_canastas_x_talla":"","cant_imperfectos":"","cant_prehor":"hidden"
        ,"cant_cp":"hidden","cant_bond":"hidden","fecha_facturacion":"hidden","cant_emp":"hidden","area":"","option":"disabled"}
    elif arealog=="Prehormado":
        showfield = {"op":"","oc":"","color":"readonly" ,"color1":"readonly" ,"color2":"readonly","espuma":"readonly", "cod_tela":"hidden","talla":"readonly","cantidad_solicitada":"readonly","largo":"readonly"
        ,"ancho":"readonly","tira":"hidden","metros_espuma":"hidden","metros_tela":"hidden","metros_tela1":"hidden","metros_tela2":"hidden","verific_existencia_espuma":"hidden"
        ,"verific_existencia_tela":"hidden","observaciones":"","cantidad_despachada":"","estadoop":"readonly","asignado":"","inicio_real":"","usuario_inicio":"","final_real":""
        ,"usuario_final":"","pestana":"readonly","referencia":"readonly","cant_corte1":"hidden","cant_corte2":"hidden","cant_canastas_x_talla":"hidden","cant_imperfectos":"","cant_prehor":""
        ,"cant_cp":"hidden","cant_bond":"hidden","fecha_facturacion":"hidden","cant_emp":"hidden","area":"","option":"disabled"}
    elif arealog=="Corte_plano":
        showfield = {"op":"","oc":"","color":"readonly" ,"color1":"readonly" ,"color2":"readonly","espuma":"readonly", "cod_tela":"hidden","talla":"readonly","cantidad_solicitada":"readonly","largo":"hidden"
        ,"ancho":"hidden","tira":"hidden","metros_espuma":"hidden","metros_tela":"hidden","metros_tela1":"hidden","metros_tela2":"hidden","verific_existencia_espuma":"hidden"
        ,"verific_existencia_tela":"hidden","observaciones":"","cantidad_despachada":"","estadoop":"readonly","asignado":"","inicio_real":"","usuario_inicio":"","final_real":""
        ,"usuario_final":"","pestana":"hidden","referencia":"readonly","cant_corte1":"hidden","cant_corte2":"hidden","cant_canastas_x_talla":"hidden","cant_imperfectos":"hidden","cant_prehor":"hidden"
        ,"cant_cp":"","cant_bond":"hidden","fecha_facturacion":"hidden","cant_emp":"hidden","area":"","option":"disabled"}
    elif arealog=="Empaque":
        showfield = {"op":"","oc":"","color":"readonly" ,"color1":"readonly" ,"color2":"readonly","espuma":"readonly", "cod_tela":"hidden","talla":"readonly","cantidad_solicitada":"readonly","largo":"hidden"
        ,"ancho":"hidden","tira":"hidden","metros_espuma":"hidden","metros_tela":"hidden","metros_tela1":"hidden","metros_tela2":"hidden","verific_existencia_espuma":"hidden"
        ,"verific_existencia_tela":"hidden","observaciones":"","cantidad_despachada":"","estadoop":"readonly","":"readonly","inicio_real":"","usuario_inicio":"","final_real":""
        ,"usuario_final":"","pestana":"","referencia":"readonly","cant_corte1":"hidden","cant_corte2":"hidden","cant_canastas_x_talla":"hidden","cant_imperfectos":"","cant_prehor":"hidden"
        ,"cant_cp":"hidden","cant_bond":"hidden","fecha_facturacion":"","cant_emp":"","area":"","option":"disabled"}
    else :showfield = {"op":"","oc":"","color":"" ,"color1":"" ,"color2":"","espuma":"", "cod_tela":"","talla":"","cantidad_solicitada":"","largo":""
        ,"ancho":"","tira":"","metros_espuma":"","metros_tela":"","metros_tela1":"","metros_tela2":"","verific_existencia_espuma":"","verific_existencia_tela":"","observaciones":"","cantidad_despachada":"","estadoop":""
        ,"asignado":"","inicio_real":"","usuario_inicio":"","final_real":"","usuario_final":"","pestana":"","referencia":"","cant_corte1":"","cant_corte2":"","cant_canastas_x_talla":"","cant_imperfectos":""
        ,"cant_prehor":"","cant_cp":"","cant_bond":"","fecha_facturacion":"","cant_emp":"","area":""}
    
    return render_template('editOP.html',dato=datosJSONop[indice],show=showfield,user=usuarioLogueado,area=arealog,nombre=nombrelog)

@app.route('/updateOP', methods=['POST'])
def updateOP():
    _oc = request.form['txtoc']
    op = request.form['txtop']
    _color = request.form['txtcolor']
    _color1 = request.form['txtcolor1']
    _color2 = request.form['txtcolor2']
    _espuma = request.form['txtespuma']
    _cod_tela = request.form['txtcod_tela']
    _talla= request.form['txttalla']
    _cantidad_solicitada= request.form['txtcantidad_solicitada']
    _largo= request.form['txtlargo']
    _ancho= request.form['txtancho']
    _tira= request.form['txttira']
    _metros_espuma= request.form['txtmetros_espuma']
    _metros_tela= request.form['txtmetros_tela']
    _metros_tela1= request.form['txtmetros_tela1']
    _metros_tela2= request.form['txtmetros_tela2']
    _verific_existencia_espuma= request.form['txtverific_existencia_espuma']
    _verific_existencia_tela= request.form['txtverific_existencia_tela']
    _observaciones= request.form['txtobservaciones']
    #_cantidad_despachada= request.form['txtcantidad_despachada']
    _estadoop= request.form['txtestadoop']
    _asignado= request.form['txtasignado']
    _area= request.form['txtarea']
    _pestana= request.form['txtpestana']
    _canastas_x_talla= request.form['txtcanastas_x_talla']
    _cant_imperfectos= request.form['txtimperfectos']
    _referencia= request.form['txtreferencia']
    _cant_corte1= request.form['txtcant_corte1']
    _cant_corte2= request.form['txtcant_corte2']
    _cant_prehor= request.form['txtcant_prehor']
    _cant_cp= request.form['txtcant_cp']
    _cant_bond= request.form['txtcant_bond']
    _cant_emp= request.form['txtcant_emp']
    _fecha_facturacion= request.form['txtfecha_fact']

    # if _estadoop=="En proceso" and request.form['txtinicio']=="": ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++AQUI VOY
    #     _inicio=
    cursorUpdateOP = conexion.cursor()
    consulta="update optable set color='"+_color+"',color1='"+_color1+"',color2='"+_color2+"',ref_espuma_color='"+_espuma+"',cod_tela='"+_cod_tela+"',talla='"+_talla+"',cantidad_solicitada='"+_cantidad_solicitada+"',largo='"+_largo+"',ancho='"+_ancho+"',tira='"+_tira+"',metros_espuma='"+_metros_espuma+"',metros_tela='"+_metros_tela+"',metros_tela1='"+_metros_tela1+"',metros_tela2='"+_metros_tela2+"',verific_existencia_espuma='"+_verific_existencia_espuma+"',verific_existencia_tela='"+_verific_existencia_tela+"',observaciones='"+_observaciones+"',estadoop='"+_estadoop+"',asignado='"+_asignado+"',area='"+_area+"',pestana='"+_pestana+"',referencia='"+_referencia+"',cant_corte1='"+_cant_corte1+"',cant_corte2='"+_cant_corte2+"',cant_canastas_x_talla='"+_canastas_x_talla+"',cant_imperfectos='"+_cant_imperfectos+"',cant_prehor='"+_cant_prehor+"',cant_cp='"+_cant_cp+"',cant_bond='"+_cant_bond+"',cant_emp='"+_cant_emp+"',fecha_facturacion='"+_fecha_facturacion+"' where op='"+op+"'"
    consultaLog="insert into opLog(oc,op,color,color1,color2,ref_espuma_color,cod_tela,talla,cantidad_solicitada,largo,ancho,tira,metros_espuma,metros_tela,metros_tela1,metros_tela2,verific_existencia_espuma,verific_existencia_tela,observaciones,estadoop,asignado,area,pestana,referencia,cant_corte1,cant_corte2,cant_canastas_x_talla,cant_imperfectos,cant_prehor,cant_cp,cant_bond,cant_emp,fecha_facturacion,fecha_cambio,usuario_cambio) values ('"+_oc+"','"+op+"','"+_color+"','"+_color1+"','"+_color2+"','"+_espuma+"','"+_cod_tela+"','"+_talla+"','"+_cantidad_solicitada+"','"+_largo+"','"+_ancho+"','"+_tira+"','"+_metros_espuma+"','"+_metros_tela+"','"+_metros_tela1+"','"+_metros_tela2+"','"+_verific_existencia_espuma+"','"+_verific_existencia_tela+"','"+_observaciones+"','"+_estadoop+"','"+_asignado+"','"+_area+"','"+_pestana+"','"+_referencia+"','"+_cant_corte1+"','"+_cant_corte2+"','"+_canastas_x_talla+"','"+_cant_imperfectos+"','"+_cant_prehor+"','"+_cant_cp+"','"+_cant_bond+"','"+_cant_emp+"','"+_fecha_facturacion+"','"+str(datetime.now())+"','"+usuarioLogueado+"')"
    cursorUpdateOP.execute(consulta)
    cursorUpdateOP.execute(consultaLog)
    cursorUpdateOP.close()
    conexion.commit()
    if arealog=="Administrativa":
        return redirect('/verOP/'+_oc+'')
    else: return redirect('/verOPoperario/'+arealog+'/'+nombrelog+'/'+usuarioLogueado)
if __name__ == '__main__':
    app.run(host='192.168.1.47', port=27017, debug=True)