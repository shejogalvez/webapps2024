import pymysql
import json

DB_NAME = "tarea2"
DB_USERNAME = "root"
DB_PASSWORD = "0123456789"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

with open('database/querys.json', 'r') as querys:
	QUERY_DICT = json.load(querys)

# -- conn ---

def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn

# -- querys --
	# -- productos --
def get_producto_by_id(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_producto_by_id"], (id,))
	producto = cursor.fetchone()
	return producto

def create_producto(tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["create_producto"], (tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor))
	conn.commit()
	return cursor.lastrowid

def get_sorted_productos_range(start, size):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_sorted_productos_range"], (start, size))
	productos = cursor.fetchall()
	return productos

def get_productos_comuna_range(start, size):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_productos_comuna_range"], (start, size))
	productos = cursor.fetchall()
	return productos

	# -- fruta-verdura --
	
def insert_fruta_verdura_to_producto(producto_id, tipo_verdura_fruta_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insert_fruta_verdura_to_producto"], (producto_id, tipo_verdura_fruta_id))
	conn.commit()

def get_fruta_verdura_by_productoID(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_fruta_verdura_by_productoID"], (id,))
	fruta_verduras = cursor.fetchall()
	return fruta_verduras

	# -- fotos --

def insert_photo_to_producto(ruta_archivo, nombre_archivo, producto_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["insert_photo_to_producto"], (ruta_archivo, nombre_archivo, producto_id))
	conn.commit()


def get_photos_by_productoID(id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_photos_by_productoID"], (id,))
	photos = cursor.fetchall()
	return photos

	# -- extra --
def get_lastID():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_lastID"])
	id = cursor.fetchone()
	return id

def get_fruta_verduras_by_name(nombre):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_fruta_verduras_by_name"], (nombre,))
	user = cursor.fetchone()
	return user

# returns: id, nombre
def get_regiones():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_regiones"])
	user = cursor.fetchall()
	return user

# returns: id, nombre
def get_comunas():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_comunas"])
	user = cursor.fetchall()
	return user

# returns: id, nombre
def get_comunas_by_regionID(id):
	conn = get_conn()
	cursor = conn.cursor()
	print(QUERY_DICT["get_comunas_by_regionID"])
	cursor.execute(QUERY_DICT["get_comunas_by_regionID"], (id,))
	user = cursor.fetchall()
	return user
# -- db-related functions --


