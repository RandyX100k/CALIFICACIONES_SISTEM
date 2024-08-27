from flask import Flask , render_template , redirect , url_for , flash , request , jsonify , session
from flask_mysqldb import MySQL
import bcrypt
import datetime
import random
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from conexion.conexion import DB
from plantillas.cursos import Cursos as cs
from functools import wraps
from datetime import timedelta
from io import BytesIO
import MySQLdb
from io import BytesIO
from flask import make_response
from io import BytesIO
from flask import make_response
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from flask import make_response
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph


bd = DB('localhost', 'root', '', 'dboperaciones')


#aplicacion
app = Flask(__name__)


#configuracion bases de datos
try:
    app.config['MYSQL_HOST'] = bd.host
    app.config['MYSQL_USER'] = bd.user
    app.config['MYSQL_PASSWORD'] = bd.clave
    app.config['MYSQL_DB'] = bd.db
except Exception as e:
    print(e)
myqsl = MySQL(app)

#llave secreta
app.secret_key = '123'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('Debe iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('Index'))
        return f(*args, **kwargs)
    return decorated_function
    
#ruta principal
@app.route('/')
def Index():                       
    return render_template('login.html')

#registro
@app.route('/Register')
def Register():
    return render_template('registrate.html')

#crub
@app.route('/Crub')
@login_required
def Admin():
   # usuarioL = request.args.get('usuarioL')
    cur = myqsl.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()
    return render_template('crub.html',users=data)

#editar usuario
@login_required
@app.route('/editarUser/<id>' , methods=['POST'])
def EditarUser(id):
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        cur = myqsl.connection.cursor()
        cur.execute('select * from usuarios where usuario = %s and pass = %s',(usuario,clave))
        Validar_User = cur.fetchall()
        if Validar_User:
            flash('Usuario existente ingresa otro usuario')
            return redirect(url_for('Admin'))
        else:
            cur.execute('UPDATE usuarios SET usuario = %s, pass = %s WHERE id = %s', (usuario, clave, id))
            myqsl.connection.commit()
            flash('Editado correctamente')
            return redirect(url_for('Admin'))
#eliminar usuarios
@app.route('/eliminarUser/<id>' ,methods=['POST'])
def DeleteUser(id):
    try:
        cur = myqsl.connection.cursor()
        cur.execute('delete from usuarios where id = %s',(id,))
        myqsl.connection.commit()
        flash('Eliminado Correctamente')
        return redirect(url_for('Admin'))
    except MySQLdb.IntegrityError:
        flash('No se puede eliminar ya que es un alumno')
        return redirect(url_for('Admin'))

#usuario
@app.route('/user')
@login_required
def User():
    usuarioL = request.args.get('email')
    cur = myqsl.connection.cursor()
    cur.execute('SELECT Nombre_Completo FROM alumnos WHERE Email = %s', (usuarioL,))

    data = cur.fetchall()
    if data:
        cur = myqsl.connection.cursor()
        cur.execute('select * from calificaciones where Nombre = %s', (data[0],))

        Alumno = cur.fetchall()
        return render_template('usuarios.html',user_ = usuarioL , user = Alumno)

# función para enviar correo electrónico

def send_email(to, subject, body):
    gmail_user = "ciprianrandy@gmail.com"
    gmail_password = "deqoejxpymfddcmu"

    # Crea el mensaje de correo electrónico
    message = MIMEMultipart()
    message["From"] = gmail_user
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(body, "html", "utf-8"))

    try:
        # Inicia sesión en el servidor SMTP de Gmail y envía el correo electrónico
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, message.as_string())
        server.quit()
        print("Correo electrónico enviado con éxito!")
    except Exception as e:
        print("Hubo un error al enviar el correo electrónico:", e)


#logica registro
@app.route('/registrate', methods=['POST'])
def Registrate():
    if request.method == 'POST':
        usuario = request.form['usuario']
        nombre = request.form['nombre']
        email = request.form['email']
        clave = request.form['clave']

        rol = request.form['rol']
        if rol != 'user':
            flash('Error el rol tiene un valor alterado')
            return redirect(url_for('Register'))
        else: 
            fecha = datetime.datetime.now()
            fecha_Actual = fecha.date()
            #verificar si el usuario ya existe en la bases de datos 
            cur = myqsl.connection.cursor()
            cur.execute('select * from usuarios where email = %s',(email,))
            data = cur.fetchone()

            if data:
                flash('Usuario ya existe')
                return redirect(url_for('Register'))
            else:
                codigo_enviado = str(random.randint(100000, 999999))
                subject = "Bienvenido a nuestra aplicación"
                body = f"""
    <html>
        <head>
            <style>
                /* Estilos generales */
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                }}

                /* Estilos para el contenedor principal */
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.1);
                }}

                /* Estilos para los encabezados */
                h1, h2 {{
                    color: #008080;
                }}

                /* Estilos para el código enviado */
                .code {{
                    font-size: 36px;
                    color: #666;
                    font-weight: bold;
                    margin-top: 20px;
                    margin-bottom: 20px;
                }}

                /* Estilos para el footer */
                .footer {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #999;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <center><h1>Bienvenido a nuestro sistema</h1></center>
                <h2>Verifica tu identidad ingresando el código:</h2>
                <p class="code">{codigo_enviado}</p>
                <div class="footer">
                    <p>Este correo electrónico fue enviado automáticamente. Por favor no responder a este correo electrónico.</p>
                </div>
            </div>
        </body>
    </html>
"""
                t = threading.Thread(target=send_email, args=(email, subject, body))
                t.start()
                t.join()
                return redirect(url_for('Verificar_Codigo', usuario=usuario, nombre=nombre, email=email, clave=clave, rol=rol, fecha_Actual=fecha_Actual, codigo_enviado=codigo_enviado))


#plantila para verificar el correo
@app.route('/Verificar')
def Verificar_Codigo():
    usuario = request.args.get('usuario')
    nombre = request.args.get('nombre')
    email = request.args.get('email')
    clave = request.args.get('clave')
    rol = request.args.get('rol')
    fecha_Actual = request.args.get('fecha_Actual')
    codigo = request.args.get('codigo_enviado')
    # Almacenar los valores en la sesión del usuario
    session['usuario'] = usuario
    session['nombre'] = nombre
    session['email'] = email
    session['clave'] = clave
    session['rol'] = rol
    session['fecha_Actual'] = fecha_Actual
    session['codigo'] = codigo
    return render_template('verificar.html',usuario=usuario,email=email,clave=clave,rol=rol,fecha=fecha_Actual,codigo=codigo)

#confirmar codigo
@app.route('/confirmar',methods=['POST'])
def confirmar_codigo():
    if request.method == 'POST':
        codigo = request.form['codigo']
        #datos
        usuario = session.get('usuario')
        nombre = session.get('nombre')
        email = session.get('email')
        clave = session.get('clave')
        rol = session.get('rol')
        fecha = session.get('fecha_Actual')
        codigo_Recibido = session.get('codigo')

        if codigo == codigo_Recibido:
            cur = myqsl.connection.cursor()
            cur.execute('Insert into usuarios (usuario,Nombre_Completo,email,pass,rol,Fecha_Reg) values(%s,%s,%s,%s,%s,%s)',
            (usuario,nombre,email,clave,rol,fecha))
            myqsl.connection.commit()
            flash('Almacenado correctamente espera a que el admin te agregue')
            return redirect(url_for('Index'))
        else:
            flash('Codigo Incorrecto')
            return redirect(url_for('Register'))
    flash('Ocurrio un error')
    return redirect(url_for('Index'))








#logica login
@app.route('/Login', methods=['POST'])
def Inicia_Session():
    if request.method == 'POST':
        email_or_usuario = request.form['email']
        clave = request.form['clave']
        try:
            if '@' in email_or_usuario:
                cur = myqsl.connection.cursor()
                cur.execute('SELECT * FROM usuarios WHERE email = %s  AND pass = %s', (email_or_usuario,clave))
                login = cur.fetchone()
                if login:
                    #enviar un email de inicio de session
                    user = login
                    #almacenar la session
                    rol = user[5]
                    session['rol'] = rol
                    fecha = datetime.datetime.now()
                    fecha_A = fecha.date()
                    #verificar la session
                    cur = myqsl.connection.cursor()
                    cur.execute('select * from session where Email = %s and Fecha = %s',(email_or_usuario,fecha_A))
                    verificar = cur.fetchone()
                    if verificar:
                        print('Session existe')
                    else:
                        ip = request.remote_addr
                        cur = myqsl.connection.cursor()
                        cur.execute('insert into session (Email,IP,rol,Fecha) values(%s,%s,%s,%s)',
                        (email_or_usuario,ip,rol,fecha_A))
                        myqsl.connection.commit()
                        print('datos almacenados')
                    #iniciar sessiom
                    if user[5] == 'user':
                        cur = myqsl.connection.cursor()
                        cur.execute('select * from alumnos where Email = %s',(email_or_usuario,))
                        userA = cur.fetchone()
                        if userA:
                            session['email'] = userA[3]                                                                    
                            flash('User')
                            return redirect(url_for('User',email = email_or_usuario))
                        else:
                            flash('Aun no eres alumno session almacenada')
                            return redirect(url_for('Index'))
                    elif user[4] == 'admin':
                        session['email'] = email_or_usuario
                        flash('Admin')
                        return redirect(url_for('Admin'))
                else:
                    print("Ha ocurrido un error")
            else:
                cur = myqsl.connection.cursor()
                cur.execute('SELECT * FROM usuarios WHERE usuario = %s  AND pass = %s', (email_or_usuario,clave))
                login = cur.fetchone()
                if login:
                    ip = request.remote_addr
                    user = login
                    #almacenar la session
                    rol = user[5]
                    session['rol'] = rol
                    fecha = datetime.datetime.now()
                    fecha_A = fecha.date()
                    #verificar la session
                    cur = myqsl.connection.cursor()
                    cur.execute('select * from session where Email = %s and Fecha = %s',(login[2],fecha_A))
                    verificar = cur.fetchone()
                    if verificar:
                        print('Session existe')
                    else:
                        cur = myqsl.connection.cursor()
                        cur.execute('insert into session (Email,IP,rol,Fecha) values(%s,%s,%s,%s)',
                        (user[3],ip,rol,fecha_A))
                        myqsl.connection.commit()
                        print('datos almacenados')
                    #iniciar session
                    if user[5] == 'user':
                        cur = myqsl.connection.cursor()
                        cur.execute('select email from usuarios where usuario = %s',(email_or_usuario,))
                        session_Alumno = cur.fetchone()
                        print(session_Alumno[0])
                        if session_Alumno:
                            cur = myqsl.connection.cursor()
                            cur.execute('select * from alumnos where Email = %s',(session_Alumno[0],))
                            sessionIniciada = cur.fetchone()
                            if sessionIniciada:
                                session['email'] = sessionIniciada[0]
                                flash('User')
                                return redirect(url_for('User',email = email_or_usuario))
                            else:
                                flash('No eres Alumnos')
                                return redirect(url_for('Index'))
                        else:
                            flash('No eres Alumno')
                            return redirect(url_for('Admin'))
                    elif user[5] == 'admin':
                        session['email'] = user[3]
                        flash('Admin')
                        return redirect(url_for('Admin'))
                else:
                    print("Ha ocurrido un error")
            flash('Usuario incorrecto')
            return redirect(url_for('Index'))
        except Exception as e:
            print(e)
                            
#sessiones
class Sessiones():
    def __init__(self,app):
        self.app = app
    def User_Sessiones(self,tabla):
        cur = myqsl.connection.cursor()
        cur.execute('select * from {}'.format(tabla))
        datos = cur.fetchall()
        return datos

sessions = Sessiones(app)
@app.route('/Sessiones')
@login_required
def Sessiones():
    datos = sessions.User_Sessiones('session')  
    if datos:
        return render_template('sessiones.html', s=datos) 
    else:
        return render_template('sessiones.html')

#imprimir reporte de sessiones

@app.route('/generar-informeSessiones')
def sessiones_generar_informe():

    informe = SimpleDocTemplate("informe.pdf", pagesize=letter)

    # Crear estilo para el título
    estilo_titulo = ParagraphStyle(name='Calificaciones', fontSize=18, leading=24)

    # Crear título
    titulo = Paragraph('Calificaciones', estilo_titulo)

    # Crear tabla para el contenido
    tabla_datos = []

    # Agregar filas de encabezado
    encabezado = ["Email","IP", "Rol", "Fecha"]
    tabla_datos.append(encabezado)
  

    # Agregar filas de datos
    cur = myqsl.connection.cursor()
    cur.execute('select * from session')
    datos = cur.fetchall()
    for fila in datos:
        fila_datos = [fila[1], fila[2] , fila[3]]
        fila_datos.extend(fila[4:])
        tabla_datos.append(fila_datos)

    # Crear tabla y establecer estilo
    tabla = Table(tabla_datos)
    tabla.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
        # Agregar tabla al contenido del informe
    contenido = []
    contenido.append(tabla)

# Generar el informe y cerrar objeto Canvas
    informe.build(contenido)

# Leer archivo PDF como bytes
    with open('informe.pdf', 'rb') as archivo:
        contenido = archivo.read()

# Crear respuesta de Flask y establecer contenido del PDF
    respuesta = make_response(contenido)
    respuesta.headers['Content-Type'] = 'application/pdf'
    respuesta.headers['Content-Disposition'] = 'attachment; filename=informe.pdf'

# Devolver respuesta
    return respuesta


#calificaciones
@app.route('/calificaciones')
@login_required
def calificaciones():
    cur = myqsl.connection.cursor()
    cur.execute("SELECT * FROM calificaciones WHERE Materia = 'administracion de bases de datos' and Curso = '5T0F-01'")
    notas_ra1 = cur.fetchall()


    cur = myqsl.connection.cursor()
    cur.execute('select M1,M2 from ra1')
    ra1 = cur.fetchall()
    
    cur = myqsl.connection.cursor()
    cur.execute('select M1,M2 from ra2')
    ra2 = cur.fetchall()

    cur = myqsl.connection.cursor()
    cur.execute('select M1,M2 from ra3')
    ra3 = cur.fetchall()

    cur = myqsl.connection.cursor()
    cur.execute('select M1,M2 from ra4')
    ra4 = cur.fetchall()

    cur = myqsl.connection.cursor()
    cur.execute('select M1,M2 from ra5')
    ra5 = cur.fetchall()
    return render_template('calificaciones.html', ra1=notas_ra1, recuperacion=ra1, ra2=ra2)



@app.route('/generar-informe')
def ruta_generar_informe():

    informe = SimpleDocTemplate("informe.pdf", pagesize=letter)

    # Crear estilo para el título
    estilo_titulo = ParagraphStyle(name='Calificaciones', fontSize=18, leading=24)

    # Crear título
    titulo = Paragraph('Calificaciones', estilo_titulo)

    # Crear tabla para el contenido
    tabla_datos = []

    # Agregar filas de encabezado
    encabezado = ["Nombre","Materia", "Curso", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]
    tabla_datos.append(encabezado)
  

    # Agregar filas de datos
    cur = myqsl.connection.cursor()
    cur.execute('select * from calificaciones')
    datos = cur.fetchall()
    for fila in datos:
        fila_datos = [fila[1], fila[2] , fila[3]]
        fila_datos.extend(fila[4:])
        tabla_datos.append(fila_datos)

    # Crear tabla y establecer estilo
    tabla = Table(tabla_datos)
    tabla.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
        # Agregar tabla al contenido del informe
    contenido = []
    contenido.append(tabla)

# Generar el informe y cerrar objeto Canvas
    informe.build(contenido)

# Leer archivo PDF como bytes
    with open('informe.pdf', 'rb') as archivo:
        contenido = archivo.read()

# Crear respuesta de Flask y establecer contenido del PDF
    respuesta = make_response(contenido)
    respuesta.headers['Content-Type'] = 'application/pdf'
    respuesta.headers['Content-Disposition'] = 'attachment; filename=informe.pdf'

# Devolver respuesta
    return respuesta



@app.route('/generar-informera1')
def ra1_generar_informe():

    informe = SimpleDocTemplate("informe.pdf", pagesize=letter)

    # Crear estilo para el título
    estilo_titulo = ParagraphStyle(name='Calificaciones', fontSize=18, leading=24)

    # Crear título
    titulo = Paragraph('Calificaciones', estilo_titulo)

    # Crear tabla para el contenido
    tabla_datos = []

    # Agregar filas de encabezado
    encabezado = ["Nombre","Materia", "Curso", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]
    tabla_datos.append(encabezado)
  

    # Agregar filas de datos
    cur = myqsl.connection.cursor()
    cur.execute('select * from ra1')
    datos = cur.fetchall()
    for fila in datos:
        fila_datos = [fila[1], fila[2] , fila[3]]
        fila_datos.extend(fila[4:])
        tabla_datos.append(fila_datos)

    # Crear tabla y establecer estilo
    tabla = Table(tabla_datos)
    tabla.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
        # Agregar tabla al contenido del informe
    contenido = []
    contenido.append(tabla)

# Generar el informe y cerrar objeto Canvas
    informe.build(contenido)

# Leer archivo PDF como bytes
    with open('informe.pdf', 'rb') as archivo:
        contenido = archivo.read()

# Crear respuesta de Flask y establecer contenido del PDF
    respuesta = make_response(contenido)
    respuesta.headers['Content-Type'] = 'application/pdf'
    respuesta.headers['Content-Disposition'] = 'attachment; filename=informe.pdf'

# Devolver respuesta
    return respuesta
    

    




@app.route('/generar-informera2')
def ra2_generar_informe():

    informe = SimpleDocTemplate("informe.pdf", pagesize=letter)

    # Crear estilo para el título
    estilo_titulo = ParagraphStyle(name='Calificaciones', fontSize=18, leading=24)

    # Crear título
    titulo = Paragraph('Calificaciones', estilo_titulo)

    # Crear tabla para el contenido
    tabla_datos = []

    # Agregar filas de encabezado
    encabezado = ["Nombre","Materia", "Curso", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]
    tabla_datos.append(encabezado)
  

    # Agregar filas de datos
    cur = myqsl.connection.cursor()
    cur.execute('select * from ra2')
    datos = cur.fetchall()
    for fila in datos:
        fila_datos = [fila[1], fila[2] , fila[3]]
        fila_datos.extend(fila[4:])
        tabla_datos.append(fila_datos)

    # Crear tabla y establecer estilo
    tabla = Table(tabla_datos)
    tabla.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
        # Agregar tabla al contenido del informe
    contenido = []
    contenido.append(tabla)

# Generar el informe y cerrar objeto Canvas
    informe.build(contenido)

# Leer archivo PDF como bytes
    with open('informe.pdf', 'rb') as archivo:
        contenido = archivo.read()

# Crear respuesta de Flask y establecer contenido del PDF
    respuesta = make_response(contenido)
    respuesta.headers['Content-Type'] = 'application/pdf'
    respuesta.headers['Content-Disposition'] = 'attachment; filename=informe.pdf'

# Devolver respuesta
    return respuesta
    

#materias
@app.route('/materias')
@login_required
def Materias():
    cur = myqsl.connection.cursor()
    cur.execute('select * from materias ')
    materias = cur.fetchall()
    return render_template('materias.html',materias=materias)

#alumnos
@app.route('/alumnos')
@login_required
def alumnos():
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    data = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('Select * from cursos')
    cursor = cur.fetchall()
    #email de los usuarios
    cur = myqsl.connection.cursor()
    cur.execute("SELECT * FROM usuarios where rol = 'user' ")
    e = cur.fetchall()
    return render_template('alumnos.html',alumnos=data,cursos=cursor,email=e)
#agregar alumnos
@app.route('/ADDALUMNOS' , methods=['POST'])
#nombre , curso , email
def ADDALUMNOS():
    if request.method == 'POST':
        nombre = request.form['nombre']
        curso = request.form['curso']
        email = request.form['email']

        #consulta verificar si el alumnos existe

        cur = myqsl.connection.cursor()
        cur.execute('select * from alumnos where Email = %s',(email,))
        existe = cur.fetchall()
        if existe:
            flash('El alumnos ya existe')
            return redirect(url_for('alumnos'))
        else:
            cur = myqsl.connection.cursor()
            cur.execute('select pass from usuarios where email = %s',(email,))
            clave = cur.fetchone()
            cur = myqsl.connection.cursor()
            cur.execute('insert into alumnos (Nombre_Completo,Curso,Email) values(%s,%s,%s)',
            (nombre,curso,email))
            myqsl.connection.commit()
            subject = "Bienvenido al sistema ipopsa"
            body = f"""
            <html>
                <head>
                <style>
                    /* Agrega estilos CSS aquí */
                    .footer {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #999;
                }}
                </style>
            </head>
            <body>
                <h1>Bienvenido al sistema ipopsa</h1>
                <p>Estimado/a {nombre},</p>
                <p>Gracias por unirte a nuestro sistema. Ya puedes iniciar sesión para ver tus calificaciones.</p>
                <p>Tus datos de inicio de sesión son:</p>
                <ul>
                    <li>Nombre: {nombre}</li>
                    <li>Curso: {curso}</li>
                    <li>Email: {email}</li>
                    <li>Clave: {clave[0]}</li>
                    
                </ul>
                <p>¡Esperamos que disfrutes de la experiencia!</p>
                 <div class="footer">
                    <p>Este correo electrónico fue enviado automáticamente. Por favor no responder a este correo electrónico.</p>
                </div>
            </div>
            </body>

        </html>
        """






            t = threading.Thread(target=send_email, args=(email, subject, body))
            t.start()
            t.join()
            flash('Agregago exitosamente')
            return redirect(url_for('alumnos'))
#RA1
@app.route('/RA1')
@login_required
def RA1():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute('select * from materias')
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("SELECT * FROM ra1 WHERE Materia = 'Administracion de bases de datos'")   
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA1.html',alumnos=datos,materias=materia,ra1=ra,cursos=cursos,totalM1 = m1)

@app.route('/RA1_')
@login_required
def RA1_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra1 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA1_.html',alumnos=datos,materias=materia,ra1=ra,cursos=cursos,totalM1 = m1)
@app.route('/RA1ADD' , methods=['POST'])
def RA1ADD():
    if request.method == 'POST':
        m1 = request.args.get('m1')
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA1'))
        cur = myqsl.connection.cursor() 
        cur.execute('select * from ra1 where Nombre = %s and materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA1'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Ingresa solo numeros')
                return redirect(url_for('RA1'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir + recuperacionM1 + recuperacionM2
            cur.execute("insert into calificaciones (Nombre, Curso, Materia, RA1) values (%s, %s, %s, %s)", (nombre,curso,materia,total))
            myqsl.connection.commit()
            #RA1
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra1 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total,M1,M2)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total,recuperacionM1,recuperacionM2))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA1',totalR=total))
#recuperacionRA1
@app.route('/M1ADD/<id>' , methods=['POST'])
def M1ADD(id):
    if request.method == 'POST':
        m1 = request.form.get('m1', 0)
        totalR = request.form.get('totalR', 0)
        nombre = request.form.get('nombre')
        m1_convertir = int(m1) if m1 is not None else 0
        totalR_convertir = int(totalR) if totalR is not None else 0
        cur = myqsl.connection.cursor()
        cur.execute('UPDATE ra1 SET M1 = %s WHERE ID = %s', (m1,id))
        myqsl.connection.commit()


        cur = myqsl.connection.cursor()
        cur.execute('select * from calificaciones')
        data = cur.fetchone()
        total = data[4]

        suma = int(total) + int(m1)

        cur = myqsl.connection.cursor()
        cur.execute("UPDATE calificaciones SET RA1 = %s WHERE Nombre = %s", (suma, nombre))
        myqsl.connection.commit()

        return redirect(url_for('RA1'))

@app.route('/M1ADDD/<id>' , methods=['POST'])
def M1ADDD(id):
    if request.method == 'POST':
        m1 = request.form.get('m1', 0)
        totalR = request.form.get('totalR', 0)
        print(totalR)
        m1_convertir = int(m1) if m1 is not None else 0
        totalR_convertir = int(totalR) if totalR is not None else 0
        cur = myqsl.connection.cursor()
        cur.execute("UPDATE ra1 SET M1 = %s WHERE ID = %s and Materia = 'Desarrollo de aplicaciones' ", (m1,id))
        myqsl.connection.commit()   
        return redirect(url_for('RA1_'))
@app.route('/M2ADD/<id>' ,methods=['POST'])
def M2ADD(id):
    if request.method =='POST':
        m2 = request.form.get('m2',0)
        totalR = request.form.get('totalR',0)
        m2_convertir = int(m2) if m2 is not None else 0
        total_Convertir = int(totalR) if totalR is not None else 0
        cur = myqsl.connection.cursor()
        cur.execute('update ra1 set M2 = %s where ID = %s' , (m2,id))
        myqsl.connection.commit()
        return redirect(url_for('RA1'))


    
#RA2
@app.route('/RA2')
@login_required
def RA2():
     #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #materias
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    dataC = cur.fetchall()
    cur = myqsl.connection.cursor()
    cur.execute('select * from materias')
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra2 where Materia = 'Administracion de bases de datos'")
    ra = cur.fetchall()
    return render_template('RA2.html',alumnos=datos,materias=materia,ra2=ra,cursos=dataC)

@app.route('/RA2_')
@login_required
def RA2_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1s
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra2 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA2_.html',alumnos=datos,materias=materia,ra1=ra,cursos=cursos,totalM1 = m1)
@app.route('/RA2ADD' , methods=['POST'])
def RA2ADD():
    if request.method == 'POST':
        m1 = request.args.get('m1')
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA2'))
        cur = myqsl.connection.cursor() 
        cur.execute('select * from ra2 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA2'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Debes ingresar solo numeros')
                return redirect(url_for('RA2'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir + recuperacionM1 + recuperacionM2
            cur.execute('UPDATE calificaciones set RA2 = %s where Nombre = %s',(total,nombre))
            myqsl.connection.commit()
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra2 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total,M1,M2)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total,recuperacionM1,recuperacionM2))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA2',totalR=total))

#MOMENTO1 RA2
@app.route('/M1ADDRA2/<id>' , methods=['POST'])
def M1ADDRA2(id):
    if request.method == 'POST':
        m1 = request.form.get('m1', 0)
        totalR = request.form.get('totalR', 0)
        m1_convertir = int(m1) if m1 is not None else 0
        totalR_convertir = int(totalR) if totalR is not None else 0
        cur = myqsl.connection.cursor()
        cur.execute('UPDATE ra2 SET M1 = %s WHERE ID = %s', (m1,id))
        myqsl.connection.commit()
        return redirect(url_for('RA2'))

#MOMENTO2 RA2
@app.route('/M2ADDRA2/<id>' ,methods=['POST'])
def M2ADDRA2(id):
    if request.method =='POST':
        m2 = request.form.get('m2',0)
        totalR = request.form.get('totalR',0)
        m2_convertir = int(m2) if m2 is not None else 0
        total_Convertir = int(totalR) if totalR is not None else 0
        cur = myqsl.connection.cursor()
        cur.execute('update ra2 set M2 = %s where ID = %s' , (m2,id))
        myqsl.connection.commit()
        return redirect(url_for('RA2'))

#RA3
@app.route('/RA3')
@login_required
def RA3():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute('select * from materias')
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra3 where Materia = 'Administracion de bases de datos' ")
    ra = cur.fetchall()
    return render_template('RA3.html',alumnos=datos,materias=materia,ra3=ra,cursos=cursos)
@app.route('/RA3_')
@login_required
def RA3_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra3 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA3_.html',alumnos=datos,materias=materia,ra1=ra,cursos=cursos,totalM1 = m1)
@app.route('/RA3ADD' , methods=['POST'])
def RA3ADD():
    if request.method == 'POST':
        m1 = request.args.get('m1')
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA1'))
        cur = myqsl.connection.cursor() 
        cur.execute('select * from ra3 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA3'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Solo debes ingresar numeros')
                return redirect(url_for('RA3'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir + recuperacionM1 + recuperacionM2
            cur.execute('UPDATE calificaciones set RA3 = %s where Nombre = %s and Materia = %s',(total,nombre,materia))
            myqsl.connection.commit()
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra3 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total,M1,M2)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total,recuperacionM1,recuperacionM2))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA3',totalR=total))

#MOMENTO1 RA3
@app.route('/M1ADDRA3/<id>' , methods=['POST'])
def M1ADDRA3(id):
    if request.method == 'POST':
        m1 = request.form.get('m1', 0)
        totalR = request.form.get('totalR', 0)
        m1_convertir = int(m1) if m1 is not None else 0
        totalR_convertir = int(totalR) if totalR is not None else 0
        cur = myqsl.connection.cursor()
        cur.execute('UPDATE ra3 SET M1 = %s WHERE ID = %s', (m1,id))
        myqsl.connection.commit()
        return redirect(url_for('RA3'))

#MOMENTO2 RA3
@app.route('/M2ADDRA3/<id>' ,methods=['POST'])
def M2ADDRA3(id):
    if request.method =='POST':
        m2 = request.form.get('m2',0)
        totalR = request.form.get('totalR',0)
        m2_convertir = int(m2) if m2 is not None else 0
        total_Convertir = int(totalR) if totalR is not None else 0
        cur = myqsl.connection.cursor()
        cur.execute('update ra3 set M2 = %s where ID = %s' , (m2,id))
        myqsl.connection.commit()
        return redirect(url_for('RA3'))
#RA4
@app.route('/RA4')
@login_required
def RA4():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute('select * from materias')
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra4 where Materia = 'Administracion de bases de datos' ")
    ra = cur.fetchall()
    return render_template('RA4.html',alumnos=datos,materias=materia,ra4=ra,cursos=cursos)

@app.route('/RA4_')
@login_required
def RA4_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra4 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA4_.html',alumnos=datos,materias=materia,ra1=ra,cursos=cursos,totalM1 = m1)
@app.route('/RA4ADD' , methods=['POST'])
def RA4ADD():
    if request.method == 'POST':
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA3'))
        cur = myqsl.connection.cursor()
        cur.execute('select * from ra4 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA4'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Solo debes ingresar numeros')
                return redirect(url_for('RA4'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir
            cur.execute("UPDATE calificaciones SET RA4 = %s WHERE Nombre = %s", (total,nombre))
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra4 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA4'))
#RA5
@app.route('/RA5')
@login_required
def RA5():
     #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute('select * from materias')
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra5 where Materia = 'Administracion de bases de datos' ")
    ra = cur.fetchall()
    return render_template('RA5.html',alumnos=datos,materias=materia,ra5=ra,cursos=cursos)

@app.route('/RA5_')
@login_required
def RA5_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra5 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA5_.html',alumnos=datos,materias=materia,ra1=ra,cursos=cursos,totalM1 = m1)
@app.route('/RA5ADD' , methods=['POST'])
def RA5ADD():
    if request.method == 'POST':
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA5'))
        cur = myqsl.connection.cursor()
        cur.execute('select * from ra5 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA5'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Solo debes ingresar numeros')
                return redirect(url_for('RA5'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir
            cur.execute("UPDATE calificaciones SET RA5 = %s WHERE Nombre = %s", (total,nombre))
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra5 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA5'))
#RA6
@app.route('/RA6')
@login_required
def RA6():
     #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute('select * from materias')
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra6 where Materia = 'Administracion de bases de datos'")
    ra = cur.fetchall()
    return render_template('RA6.html',alumnos=datos,materias=materia,ra6=ra,cursos=cursos)
@app.route('/RA6_')
@login_required
def RA6_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra6 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA6_.html',alumnos=datos,materias=materia,ra6=ra,cursos=cursos,totalM1 = m1)
@app.route('/RA6ADD' , methods=['POST'])
def RA6ADD():
    if request.method == 'POST':
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA6'))
        cur = myqsl.connection.cursor()
        cur.execute('select * from ra6 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA6'))
        else:
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Solo debes ingresar numeros')
                return redirect(url_for('RA6')) 
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir
            cur.execute("UPDATE calificaciones SET RA6 = %s WHERE Nombre = %s", (total,nombre))
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra6 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA6'))
#RA7
@app.route('/RA7')
@login_required
def RA7():
     #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute('select * from materias')
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra7 where Materia = 'Administracion de bases de datos' ")
    ra = cur.fetchall()
    return render_template('RA7.html',alumnos=datos,materias=materia,ra7=ra,cursos=cursos)

@app.route('/RA7_') 
@login_required
def RA7_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra7 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA7_.html',alumnos=datos,materias=materia,ra7=ra,cursos=cursos,totalM1 = m1)

@app.route('/RA7ADD' , methods=['POST'])
def RA7ADD():
    if request.method == 'POST':
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA7'))
        cur = myqsl.connection.cursor()
        cur.execute('select * from ra7 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA7'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Solo debes ingresar numeros')
                return redirect(url_for('RA7'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir
            cur.execute("UPDATE calificaciones SET RA7 = %s WHERE Nombre = %s", (total,nombre))
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra7 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA7'))
#RA8
@app.route('/RA8')
@login_required
def RA8():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Administracion de bases de datos'")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra8 where Materia = 'Administracion de bases de datos'")
    ra = cur.fetchall()
    return render_template('RA8.html',alumnos=datos,materias=materia,ra8=ra,cursos=cursos)

@app.route('/RA8_')
@login_required
def RA8_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra8 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA8_.html',alumnos=datos,materias=materia,ra8=ra,cursos=cursos,totalM1 = m1)

@app.route('/RA8ADD' , methods=['POST'])
def RA8ADD():
    if request.method == 'POST':
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA3'))
        cur = myqsl.connection.cursor()
        cur.execute('select * from ra8 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data: 
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA8'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Solo debes ingresar numeros')
                return redirect(url_for('RA8'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir
            cur.execute("UPDATE calificaciones SET RA8 = %s WHERE Nombre = %s", (total,nombre))
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra8 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA8'))
#RA9
@app.route('/RA9')
@login_required
def RA9():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Administracion de bases de datos'")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra9 where Materia = 'Administracion de bases de datos' ")
    ra = cur.fetchall()
    return render_template('RA9.html',alumnos=datos,materias=materia,ra9=ra,cursos=cursos)

@app.route('/RA9_')
@login_required
def RA9_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra9 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA9_.html',alumnos=datos,materias=materia,ra9=ra,cursos=cursos,totalM1 = m1)

@app.route('/RA9ADD' , methods=['POST'])
def RA9ADD():
    if request.method == 'POST':
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA9'))
        cur = myqsl.connection.cursor()
        cur.execute('select * from ra9 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA9'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Solo debes ingresar numeros')
                return redirect(url_for('RA9'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir
            cur.execute("UPDATE calificaciones SET RA9 = %s WHERE Nombre = %s", (total,nombre))
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra9 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA9'))
#RA10
@app.route('/RA10')
@login_required
def RA10():
     #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Administracion de bases de datos'")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra10 where Materia = 'Administracion de bases de datos' ")
    ra = cur.fetchall()
    return render_template('RA10.html',alumnos=datos,materias=materia,ra10=ra,cursos=cursos)

@app.route('/RA10_')
@login_required
def RA10_():
    #alumnos
    cur = myqsl.connection.cursor()
    cur.execute('select * from alumnos')
    datos = cur.fetchall()
    #cursos
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()
    #materias
    cur = myqsl.connection.cursor()
    cur.execute("select * from materias where Materia = 'Desarrollo de aplicaciones' ")
    materia = cur.fetchall()
    #ra1
    cur = myqsl.connection.cursor()
    cur.execute("select * from ra10 where Materia = 'Desarrollo de aplicaciones' ")
    ra = cur.fetchall()
    m1 = request.args.get('totalR')
    return render_template('RA10_.html',alumnos=datos,materias=materia,ra1=ra,cursos=cursos,totalM1 = m1)

@app.route('/RA10ADD' , methods=['POST'])
def RA10ADD():
    if request.method == 'POST':
        nombre = request.form['nombre']
        materia = request.form['materia']
        curso = request.form['curso']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        if len(p1) <1 or len(p2) < 1 or len(p3) <1 or len(p4) < 1 or len(p5) <1  or len(cuaderno) <1:
            flash('Rellena todos los campos')
            return redirect(url_for('RA10'))
        cur = myqsl.connection.cursor()
        cur.execute('select * from ra10 where Nombre = %s and Materia = %s',(nombre,materia))
        data = cur.fetchall()
        if data:
            flash('Ya hay una calificacion con esa materia')
            return redirect(url_for('RA10'))
        else:
            #convertir a numerico
            try:
                asistencia_convertir = float(asistencia)
                p1_convertir = float(p1)
                p2_convertir = float(p2)
                p3_convertir = float(p3)
                p4_convertir = float(p4)
                p5_convertir = float(p5)
                cuaderno_convertir = float(cuaderno)
                recuperacionM1 = 0
                recuperacionM2 = 0
            except ValueError:
                flash('Solo debes ingresar numeros')
                return redirect(url_for('RA10'))
            #calificaciones
            total = asistencia_convertir + p1_convertir + p2_convertir + p3_convertir + p4_convertir + p5_convertir + cuaderno_convertir
            cur.execute("UPDATE calificaciones SET RA10 = %s WHERE Nombre = %s", (total,nombre))
            #RA2
            cur = myqsl.connection.cursor()
            cur.execute('INSERT INTO ra10 (Nombre,Materia,Curso,Asistencia,P1,P2,P3,P4,P5,Cuaderno,Total)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (nombre,materia,curso,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,total))
            myqsl.connection.commit()
            flash('Calificacion agregada con exito')
            return redirect(url_for('RA10'))

       
CursosT = cs(app)
@app.route('/Curso5TF02')
@login_required
def Curso5F_02():
    cur = myqsl.connection.cursor()
    cur.execute("select * from calificaciones where Curso = '5TOF-02' ")
    data = cur.fetchall()           
    return CursosT.Curso_template('5TOF-02.html',curso=data)



@app.route('/6F')
@login_required
def Curso_6F():
    cur = myqsl.connection.cursor()
    cur.execute("select * from calificaciones where Curso = '1' ")
    data = cur.fetchall()
    return CursosT.Curso_template('6F.html',curso=data)

#obtener los cursos

@app.route('/cursos')
@login_required
def Cursos():
    cur = myqsl.connection.cursor()
    cur.execute('select * from cursos')
    cursos = cur.fetchall()

    return render_template('cursos.html',curso=cursos)

class Addcurso():
    def __init__(self,app):
        self.app = app
    def Insertar_Curso(self,nombre):
        cur = myqsl.connection.cursor()
        cur.execute('insert into cursos (Curso) values(%s)',(nombre,))
        myqsl.connection.commit()
@app.route('/ADDCURSO' , methods=['POST'])
def Inser_Curso():
    if request.method == 'POST':
        curso = request.form['curso']
        Curso = Addcurso(app)
        Curso.Insertar_Curso(curso)
        flash('Agregado exitosamente')
        return redirect(url_for('Cursos'))


@app.route('/desarrollo')
@login_required
def desarrollo():
    cur = myqsl.connection.cursor()
    cur.execute("SELECT * FROM calificaciones WHERE Materia = 'Desarrollo de aplicaciones'")
    notas_ra1 = cur.fetchall()
    return render_template('desarrollo.html',desarrollo=notas_ra1)



@app.route('/delete/<id>')
def Delete(id):
    cur = myqsl.connection.cursor()
    cur.execute('delete from calificaciones where Nombre = %s ',(id,))
    cur.execute('delete from ra1 where Nombre = %s' ,(id,))
    myqsl.connection.commit()
    myqsl.connection.commit()
    flash('Eliminado exitosamente')
    return redirect(url_for('RA1'))

#logout
@app.route('/cerrarSession')
def Logout():
    session.clear()
    return redirect(url_for('Index'))


#editar alumnos
@app.route('/editarAlumno/<id>' , methods=['POST'])
def EditarAlumno(id):
    if request.method == 'POST':
        curso = request.form['curso']
        cur = myqsl.connection.cursor()
        cur.execute('update alumnos set Curso = %s where id = %s',(curso,id))
        myqsl.connection.commit()
        flash('Actualizado correctamente')
        return redirect(url_for('alumnos'))

@app.route('/eliminar/<id>',methods=['POST'])
def ElminarAlumno(id):
    try:
        cur = myqsl.connection.cursor()
        cur.execute('delete from alumnos where id = %s',(id,))
        myqsl.connection.commit()
        flas('Eliminado exitosamente')
    except MySQLdb.IntegrityError:
        flash('Este alumno tiene calificaciones no se puede borrar')
        return(redirect(url_for('alumnos')))


class Update():
    def __init__(self, app):
        self.app = app
    
    def Actualizar(self, table, nombre,asistencia, p1, p2, p3, p4, p5,cuaderno,id):
        suma = asistencia + p1 + p2 + p3 + p4 + p5
        cur = myqsl.connection.cursor()
        cur.execute(f"""
            UPDATE {table} SET 
            Asistencia = {asistencia},
            P1 = {p1},
            P2 = {p2},
            P3 = {p3},
            P4 = {p4},
            P5 = {p5},
            Cuaderno = {cuaderno},
            Total = {suma}
            WHERE ID = '{id}'
        """)
        myqsl.connection.commit()
        cur = myqsl.connection.cursor()
        cur.execute(f"""
        update calificaciones set
        RA1 = {suma}
        where Nombre = '{nombre}'
        """)
        myqsl.connection.commit()
        flash('Actualizado correctamente')
Actualizado = Update(app)
@app.route('/update_califiacion/<id>',methods=['POST'])
def ActualizarCalificacion(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        asistencia = request.form['asistencia']
        p1 = request.form['p1']
        p2 = request.form['p2']
        p3 = request.form['p3']
        p4 = request.form['p4']
        p5 = request.form['p5']
        cuaderno = request.form['cuaderno']
        try:
            asistencia_convertir = int(asistencia)
            p1_convertir = int(p1)
            p2_convertir = int(p2)
            p3_convertir = int(p3)
            p4_convertir = int(p4)
            p5_convertir = int(p5)
            cuaderno_convertir = int(cuaderno)
        except Exception as e:
            print(e)
        
        Actualizado.Actualizar('RA1',nombre,asistencia_convertir,p1_convertir,p2_convertir,p3_convertir,p4_convertir,p5_convertir,cuaderno_convertir,id)
        return redirect(url_for('RA1'))

#inicio del programa entrypoint
if __name__ == '__main__':
    app.run(debug=True)
