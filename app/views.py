# Vistas de Flask para manejar las rutas
from app import app
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from .forms import RegistrationForm
from .models import UserModel
from flask_mysqldb import MySQL
import cv2
import numpy as np
import json

@app.route('/')
def index():
    return "Hola, mundo!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file part")
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return 'No selected file'
        if file:
            print("File received:", file.filename)
            # Procesamiento adicional aquí
            return 'File uploaded successfully'
    return render_template('upload.html')

@app.route('/usuarios')
def listar_usuarios():
    users = UserModel.load_users()
    return jsonify({'users': users, 'mensaje': "Usuarios Listados"})
    
@app.route('/usuarios/<usuario>', methods = ['GET'])
def mostrar_usuario(usuario):
    user = UserModel.get(usuario)
    if(user != None):
        return jsonify({'user': user, 'mensaje': "Usuario Mostrado"})
    else:
        return jsonify({'mensaje' : "Usuario no encontrado"})
@app.route('/sign', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if True:#form.validate_on_submit():

        user = UserModel(
            username=form.username.data,
            name=form.name.data,
            surname=form.surname.data,
            password=form.password.data
        )
        cursor = conexion.connection.cursor()
        sql = "SELECT username FROM usuarios"
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos == None:
            print('Username already exists!')
            return render_template('register.html', form=form)
        existing_users = UserModel.load_users()
        if form.username.data in existing_users:
            print('Username already exists!')
            return render_template('register.html', form=form)
        
        user.save_to_file()
        
         # Leer el archivo JSON para mostrar el usuario registrado
        with open('users.json', 'r') as file:
            registered_users = json.load(file)
        
        print('Registration successful!')
        # Pasar el contenido JSON a la plantilla para mostrarlo
        return render_template('register_success.html', users=registered_users)
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    return UserModel.get('carlos')