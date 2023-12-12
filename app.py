from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# Configura la conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost", # Puedes usar '127.0.0.1' o 'localhost' si es local
    user="root", # Nombre de usuario de la base de datos
    password="Herlindo58",  # Contraseña del usuario de la base de datos
    database="sensores_data", # Nombre de la base de datos a la que deseas conectarte
    use_pure=True
)

def get_humidity_soil_data(date_filter):
    try:
        if mydb.is_connected():
            # Crear un objeto cursor para ejecutar consultas
            cursor = mydb.cursor()
            # Consulta SQL para obtener los datos de humedad del suelo
            cursor.execute("SELECT id, humedad_suelo, hora FROM sensorsuelo WHERE fecha = %s", (date_filter,))
            data = cursor.fetchall()
            # Ordenar los datos por hora
            sorted_data = sorted(data, key=lambda x: x[1])
            # Convertir las horas a formato adecuado
            hours_soil = [row[1].total_seconds() / 3600 for row in sorted_data]
            # Datos de humedad del suelo
            humidity_soil = [row[0] for row in sorted_data]
            return humidity_soil, hours_soil

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        mydb.close()

    return None, None

def get_data_from_table( date_filter):
    try:
        if mydb.is_connected():
            # Crear un objeto cursor para ejecutar consultas
            cursor = mydb.cursor()
            # Consulta SQL para obtener los datos de la tabla
            cursor.execute(f"SELECT id, temperatura, humedad, fecha, hora FROM datos_automatizacion WHERE fecha = %s", (date_filter,))
            data = cursor.fetchall()
            # Ordenar los datos por hora
            sorted_data = sorted(data, key=lambda x: x[4])
            # Convertir las horas a formato adecuado
            hours_amb = [row[4].total_seconds() / 3600 for row in sorted_data]
            # Datos de temperatura
            temperatures_amb = [row[1] for row in sorted_data]
            # Datos de humedad
            humidity_amb = [row[2] for row in sorted_data]
            return temperatures_amb, humidity_amb, hours_amb
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        mydb.close()
    return None, None, None

@app.route('/')
def index():
    # Obtener la fecha proporcionada por la página HTML
    date_filter = request.args.get('date_filter', default=None, type=str)

    # Validar que se proporcionó una fecha
    if date_filter is None:
        return "Por favor, proporciona una fecha."

    # Obtener datos de humedad y temperatura ambiente
    temperatures_amb, humidity_amb, hours_amb = get_data_from_table(date_filter)
    # Obtener datos de humedad del suelo
    humidity_soil, hours_soil = get_humidity_soil_data(date_filter)

    # Renderizar la plantilla con los datos obtenidos
    return render_template('index.html',
                           temperatures_amb=temperatures_amb, humidity_amb=humidity_amb, hours_amb=hours_amb,
                           humidity_soil=humidity_soil, hours_soil=hours_soil)

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

if __name__ == '__main__':
    # Iniciar la aplicación Flask
    app.run(debug=True, host='0.0.0.0')

