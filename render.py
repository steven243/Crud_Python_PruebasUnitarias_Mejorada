from flask import Flask, render_template, request, redirect
from pymongo import MongoClient


def conexion():
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Crud"]
    mycol = mydb["Formulario"]
    return mycol

def leer():
    data = conexion()
    read = data.find()
    return read

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def logeo():
    data = []
    if request.method == 'POST':
        request2 = conexion()
        usuario = request.form["usuario"]
        contra = request.form["contra"]
        
        if usuario =="" or contra =="":
            msg = "Ingrese todos los datos"
            return render_template("index.html", msg=msg)
        else:
            data = {"usuario": usuario, "contra":contra}
            request2.insert_one(data)

    return render_template('operations.html')


@app.route('/list', methods=['POST','GET'])
def lista():
    
    data=[]
    
    cur = leer()
    for result in cur :
        data.append(result) 
        
    return render_template('list.html', usuarios = data)



@app.route('/edit/<string:usuario>', methods=['GET'])
def editar(usuario):
    return render_template('update.html', usuario = usuario)



@app.route('/edit/<string:usuario>/edt', methods=['POST'])
def actualizar(usuario): 

    data = conexion()
    contra = request.form["contra"]
    
    if contra == "":
        msg = "Ingrese todos los datos"
        return render_template("update.html",usuario=usuario, msg=msg)
    else:
        data.update_one({"usuario":usuario},{'$set':{"contra": contra}})


    return redirect('/list') 



@app.route('/delete/<string:usuario>',methods=['GET','POST'])
def eliminar(usuario):

    data = conexion()
    data.delete_one({'usuario':usuario})
    return redirect('/list')



if __name__ == '__main__':
    app.run(debug=True)