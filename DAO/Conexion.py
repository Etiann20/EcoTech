import pymysql


def conectar():
    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="ecotech",
            port=3306
        )

        print("Conexión exitosa a la base de datos.")
        return conexion

    except pymysql.MySQLError as e:
        print("Error al conectar con la base de datos:", e)
        return None