from flask import Flask, request, render_template, redirect, url_for, session
from utils.validations import validate_prod_form, validate_photos
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import uuid
import json

UPLOAD_FOLDER = 'static/uploads'
ITEMS_IN_PAGE = 5

app = Flask(__name__, static_url_path="/static")
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/agregar-producto", methods=["GET"])
def agregar_producto():
    data = {
        "regiones" : [{"id": tup[0], "nombre": tup[1]} for tup in db.get_regiones()]
    }
    return render_template("form/agregar_producto.html", data=data)

@app.route("/agregar-pedido", methods=["GET"])
def agregar_pedido():
    data = {
        "regiones" : [{"id": tup[0], "nombre": tup[1]} for tup in db.get_regiones()]
    }
    return render_template("form/agregar_pedido.html", data=data)

@app.route("/api/get_comunas", methods=["GET"])
def get_comunas():
    region_id = int(request.args.get("region_id"))
    
    return {"data": [{"id": tup[0], "nombre": tup[1]} for tup in db.get_comunas_by_regionID(region_id)]}

@app.route("/detalles-pedido", methods=["GET"])
def detalles_pedido():
    # id, tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor
    producto_id = request.args.get("id")
    producto = db.get_producto_by_id(producto_id)
    fv = db.get_fruta_verdura_by_productoID(producto_id)
    region = db.get_region_by_comunaID(producto[3])[0]
    comuna = db.get_comuna_by_id(producto[3])[1]
    return render_template("detalles/detalles_pedido.html", producto=producto, region=region, comuna=comuna, fv=fv)

@app.route("/detalles-producto", methods=["GET"])
def detalles_producto():
    # id, tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor
    producto_id = request.args.get("id")
    producto = db.get_producto_by_id(producto_id)
    fv = db.get_fruta_verdura_by_productoID(producto_id)
    region = db.get_region_by_comunaID(producto[3])[0]
    comuna = db.get_comuna_by_id(producto[3])[1]
    photos = db.get_photos_by_productoID(producto_id)
    return render_template("detalles/detalles_producto.html", producto=producto, region=region, comuna=comuna, photos=photos, fv=fv)

def get_list_data(page, get_items_query, count_query) -> list:
    start = page * ITEMS_IN_PAGE
    # print(db.get_sorted_productos_range(start, ITEMS_IN_PAGE))
    print(db.get_single_photo_by_productoID(db.get_sorted_productos_range(start, ITEMS_IN_PAGE)[0][0])  )
    data = [
        {
            "id": tup[0],
            "tipo": tup[1],
            # nombre,
            "fruta_verdura": db.get_fruta_verdura_by_productoID(tup[0]),
            # nombre,
            "region": db.get_region_by_comunaID(tup[3])[0],
            # region_id, nombre
            "comuna": db.get_comuna_by_id(tup[3])[1],
            # ruta_archivo, nombre_archivo
            "fotosrc": db.get_single_photo_by_productoID(tup[0])[1] if db.get_single_photo_by_productoID(tup[0]) else "",

            "nombre_comprador": tup[4],
        }
        # id, tipo, descripcion, comuna_id, nombre_productor, email_productor, celular_productor
        for tup in get_items_query(start, ITEMS_IN_PAGE)
    ]
    args = {
        "data" : data,
        "detallesURL" : '',
        "page": page+1,
        "template": '',
        "total_pages" : (count_query()[0]-1)//ITEMS_IN_PAGE + 1
    }
    return args

@app.route("/display/<filename>", methods=["GET"])
def display_image(filename):
    return redirect(url_for('static', filename='uploads/'+filename))

@app.route("/ver-pedidos/<int:page>", methods=["GET"])
def ver_pedidos(page=1):
    args = get_list_data(page-1, db.get_sorted_pedidos_range, db.count_pedidos)
    args["detallesURL"] = url_for("detalles_pedido")
    args["template"] = 'ver_pedidos'
    return render_template("list/ver_pedidos.html", args=args)

@app.route("/ver-productos/<int:page>", methods=["GET"])
def ver_productos(page=1):
    args = get_list_data(page-1, db.get_sorted_productos_range, db.count_productos)
    args["detallesURL"] = url_for("detalles_producto")
    args["template"] = 'ver_productos'
    
    return render_template("list/ver_productos.html", args=args)

def upload_images(fotos_producto, producto_id):
    # 1. generate random name for img
    for foto_producto in fotos_producto:
        _filename = hashlib.sha256(
            secure_filename(foto_producto.filename).encode("utf-8")
            ).hexdigest()
        _extension = filetype.guess(foto_producto).extension
        img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"

        # 2. save img as a file
        ruta_foto = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
        foto_producto.save(ruta_foto)

        db.insert_photo_to_producto(ruta_foto, img_filename, producto_id)


def save_producto_frutas(request, insert_query, FV_query):
    tipo_producto = request.form.get("tipo_producto")
    fruta_verduras = request.form.getlist("fruta_verdura_checkbox")
    descripcion = request.form.get("descripcion")
    comuna_id = request.form.get("comuna")
    nombre_productor = request.form.get("nombre_productor")
    email_productor = request.form.get("email_productor")
    celular_productor = request.form.get("celular_productor")
    # save producto in db
    id = insert_query(tipo_producto, descripcion, comuna_id, nombre_productor, email_productor, celular_productor)
    #print(producto_id)

    # add relations to created producto
    for item in fruta_verduras:
        fruta_verdura_id = db.get_fruta_verduras_by_name(item)
        #print("fruta name, id= ", item, fruta_verdura_id)
        FV_query(id, fruta_verdura_id)

    return id

@app.route("/post-prod", methods=["POST"])
def post_prod():
    fotos_producto = request.files.getlist("foto_producto")
    #print(tipo_producto, fruta_verduras, fotos_producto, region_id, comuna_id, nombre_productor, email_productor, celular_productor , sep= "\n")
    errors = validate_prod_form(request) + validate_photos(request)
    if len(errors) == 0:
        producto_id = save_producto_frutas(request, db.create_producto, db.insert_fruta_verdura_to_producto)
            
        upload_images(fotos_producto, producto_id)
        return redirect(url_for("success", msg = "de producto" ))
    else:
        return errors, 400

@app.route("/post-pedido", methods=["POST"])
def post_pedido():
    #print(tipo_producto, fruta_verduras, fotos_producto, region_id, comuna_id, nombre_productor, email_productor, celular_productor , sep= "\n")
    errors = validate_prod_form(request)
    if len(errors) == 0:
        save_producto_frutas(request, db.create_pedido, db.insert_fruta_verdura_to_pedido)
        return redirect(url_for("success", msg = "de pedido" ))
    else:
        return errors, 400

@app.route("/success", methods=["GET"])
def success():
    msg = request.args.get("msg")
    return render_template("form/form_success.html", successMsg=f"Hemos recibido el registro {msg}. Muchas gracias")

if __name__ == "__main__":
    app.run(debug=True)
