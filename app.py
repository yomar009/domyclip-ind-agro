from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    # Configura la conexión a la base de datos
    conexion = mysql.connector.connect(
        host="localhost", # Nombre de usuario de la base de datos
        user="root", # Contraseña del usuario de la base de datos
        password="Herlindo58", # Puedes usar '127.0.0.1' o 'localhost' si es local
        database="sensores_data" # Nombre de la base de datos a la que deseas conectarte
    )

    # Crea un objeto cursor para interactuar con la base de datos
    cursor = conexion.cursor()

    try:
        # Ejemplo: ejecutar una consulta SELECT
        consulta = "SELECT * FROM datos_automatizacion"
        cursor.execute(consulta)

        # Recupera todos los resultados de la consulta
        resultados = cursor.fetchall()

        # Renderiza la plantilla HTML con los resultados
        return render_template('index.html', resultados=resultados)

    except mysql.connector.Error as error:
        return f"Error: {error}"

    finally:
        # Cierra el cursor y la conexión
        cursor.close()
        conexion.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
