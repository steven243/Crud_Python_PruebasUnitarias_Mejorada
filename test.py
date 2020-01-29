import unittest
import render
from render import app
from pymongo import MongoClient


class Testing(unittest.TestCase):
    
    
#---------------------------Conexion base de datos-------------------------------------------
    
    def conexion():
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Crud"]
        mycol = mydb["Formulario"]
        return mycol

    def leer():
        data = conexion()
        read = data.find()
        return read

#---------------------------Pruebas de conexion de base de datos---------------------------------
    
    def test_conection(self):
        con = conexion()
        self.assertEqual(render.conexion(), con)
        
    #def test_read(self):
     #   data = []
      #  lec = leer()
       # for datos in lec:
        #    data.append(datos)
            
        #self.assertEqual(render.leer(), data)


#----------------------Prueba de Carga de datos html-----------------------------------------------
    

    def test_load_index(self):
        test = app.test_client(self)
        response = test.get("/", content_type= 'html/text')
        self.assertEqual(response.status_code, 200)

    def test_load_list(self):
        test = app.test_client(self)
        response = test.get("/list", content_type='html/text')
        self.assertEqual(response.status_code,200)
        
    def test_load_operations(self):
        test = app.test_client(self)
        response = test.get("/login", content_type='html/text')
        self.assertEqual(response.status_code,200)
        
    def test_load_get(self):
        test = app.test_client(self)
        response = test.get("/edit/<string:usuario>", content_type='html/text')
        self.assertEqual(response.status_code,200)
        
    def test_load_update(self):
        test = app.test_client(self)
        response = test.get("/edit/<string:usuario>/edt", content_type='html/text')
        self.assertEqual(response.status_code,405)
        
        
    def test_load_delete(self):
        test = app.test_client(self)
        response = test.get("/delete/<string:usuario>", content_type='html/text')
        self.assertEqual(response.status_code,302)
        
    

#----------------------Prueba de datos de entrada------------------------------
    
    def test_all_data(self):
        
        usuario = 'StevenRojas'
        contra = 'stevenR'
 
        test = app.test_client(self)

        response = test.post('/login', data=dict(usuario=usuario,contra=contra),follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        

    def test_fist_input_empty(self):
            
            usuario = ''
            contra = 'stevenR'

            test = app.test_client(self)

            response = test.post('/login', data=dict(usuario=usuario,contra=contra),follow_redirects=False)
            self.assertIn(b"Ingrese todos los datos", response.data)

    def test_second_input_empty(self):
            
            usuario = 'StevenRojas'
            contra = ''

            test = app.test_client(self)

            response = test.post('/login', data=dict(usuario=usuario,contra=contra),follow_redirects=False)
            self.assertIn(b"Ingrese todos los datos", response.data)

    
    def test_all_data_empty(self):
            
            usuario = ''
            contra = ''

            test = app.test_client(self)

            response = test.post('/login', data=dict(usuario=usuario,contra=contra),follow_redirects=False)
            self.assertIn(b"Ingrese todos los datos", response.data)
            

#------------------------Pruebas de Edicion de datos--------------------------
            
            
    def test_pass_data_empty(self):
        
        contra = ''
        
        test = app.test_client(self)
        
        response = test.post('/edit/<string:usuario>/edt', data=dict(contra=contra),follow_redirects=False)
        self.assertIn(b"Ingrese todos los datos", response.data)
        
    
    def test_pass_data(self):
        
        contra = 'StevenRR'
        
        test = app.test_client(self)
        
        response = test.post('/edit/<string:usuario>/edt', data=dict(contra=contra),follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        
#---------------------Pruebas de eliminacion de datos-------------------------------
        
        
    def test_delete(self):
        
        usuario = 'StevenRojas'
        contra = 'stevenR'
        
        test = app.test_client(self)
        
        response = test.post('/delete/<string:usuario>', data=dict(usuario=usuario,contra=contra),follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        
    
            


if __name__ == '__main__':
    unittest.main()