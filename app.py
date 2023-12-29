from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'admin'  # Clave de producción

# Configura la conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Herlindo58",
    database="sensores_data",
    use_pure=True
)

# Función para obtener datos de humedad del suelo
def get_humidity_soil_data(date_filter):
    cursor = None
    try:
        if mydb.is_connected():
            cursor = mydb.cursor()
            cursor.execute("SELECT id, humedad_suelo, hora FROM sensorsuelo WHERE fecha = %s", (date_filter,))
            data = cursor.fetchall()
            sorted_data = sorted(data, key=lambda x: x[2])  # Cambié a x[2] para ordenar por hora
            hours_soil = [row[2].total_seconds() / 3600 for row in sorted_data]
            humidity_soil = [row[1] for row in sorted_data]
            return humidity_soil, hours_soil

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()

    return None, None

# Función para obtener datos de la tabla de automatización
def get_data_from_table(date_filter):
    cursor = None
    try:
        if mydb.is_connected():
            cursor = mydb.cursor()
            cursor.execute("SELECT id, temperatura, humedad, fecha, hora FROM datos_automatizacion WHERE fecha = %s", (date_filter,))
            data = cursor.fetchall()
            sorted_data = sorted(data, key=lambda x: x[4])
            hours_amb = [row[4].total_seconds() / 3600 for row in sorted_data]
            temperatures_amb = [row[1] for row in sorted_data]
            humidity_amb = [row[2] for row in sorted_data]
            return temperatures_amb, humidity_amb, hours_amb
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()

    return None, None, None

# Ruta de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar las credenciales (reemplazar con lógica real de autenticación)
        if username == 'ProAdm' and password == 'admin':
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Credenciales incorrectas'

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session or not session['loggedin']:
        return redirect(url_for('index'))

    # Obtener la fecha proporcionada por la página HTML, si no se proporciona, usar la fecha actual
    date_filter = request.args.get('date_filter', default=datetime.now().strftime('%Y-%m-%d'), type=str)

    # Obtener datos de humedad y temperatura ambiente
    temperatures_amb, humidity_amb, hours_amb = get_data_from_table(date_filter)
    # Obtener datos de humedad del suelo
    humidity_soil, hours_soil = get_humidity_soil_data(date_filter)

    # Renderizar la plantilla con los datos obtenidos
    return render_template('dashboard.html',
                           temperatures_amb=temperatures_amb, humidity_amb=humidity_amb, hours_amb=hours_amb,
                           humidity_soil=humidity_soil, hours_soil=hours_soil, username=session['username'])

@app.route('/activar_riego')
def activar_riego():
    # Lógica para activar el riego (puedes llamar a una función específica aquí)
    # ...

    return 'Riego 10 minutos'

@app.route('/activar_ventilacion')
def activar_ventilacion():
    # Lógica para activar la ventilación (puedes llamar a una función específica aquí)
    # ...

    return 'Ventilación 10 minutos'

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Iniciar la aplicación Flask
    app.run(debug=True, host='0.0.0.0')


# Ruta de inicio de sesión con mysql
# Función para verificar las credenciales en la base de datos
"""
def verificar_credenciales(username, password):
    cursor = None
    try:
        if mydb.is_connected():
            cursor = mydb.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (username,))
            user = cursor.fetchone()

            if user and user['contrasena'] == password:
                return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar las credenciales contra la base de datos
        if verificar_credenciales(username, password):
            session['loggedin'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Credenciales incorrectas'

    return render_template('index.html')
"""