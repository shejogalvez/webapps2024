from flask import Flask, request, render_template, redirect, url_for, session
from utils.validations import validate_prod_form, validate_img
from database import db
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import uuid
import json

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/agregar-producto", methods=["GET"])
def agregar_producto():
    data = {
        "regiones" : [{"id": tup[0], "nombre": tup[1]} for tup in db.get_regiones()]
    }
    print(data)
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
    return render_template("detalles_pedido.html")

@app.route("/detalles-producto", methods=["GET"])
def detalles_producto():
    return render_template("detalles_producto.html")

@app.route("/ver-pedidos", methods=["GET"])
def ver_pedidos():
    return render_template("ver_pedidos.html")

@app.route("/ver-productos", methods=["GET"])
def ver_productos():
    return render_template("ver_productos.html")

@app.route("/post-prod", methods=["POST"])
def post_prod():

    tipo_producto = request.form.get("tipo_producto")
    fruta_verduras = request.form.getlist("fruta_verdura_checkbox")
    descripcion = request.form.get("descripcion")
    fotos_producto = request.files.getlist("foto_producto")
    region_id = request.form.get("region")
    comuna_id = request.form.get("comuna")
    nombre_productor = request.form.get("nombre_productor")
    email_productor = request.form.get("email_productor")
    celular_productor = request.form.get("celular_productor")

    print(tipo_producto, fruta_verduras, fotos_producto, region_id, comuna_id, nombre_productor, email_productor, celular_productor , sep= "\n")
    errors = validate_prod_form(tipo_producto, fruta_verduras, fotos_producto, region_id, comuna_id, nombre_productor, email_productor, celular_productor)
    if len(errors) == 0:
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

        # 3. save producto in db
        producto_id = db.create_producto(tipo_producto, descripcion, comuna_id, nombre_productor, email_productor, celular_productor)
        print(producto_id)

        # 4. add relations to created producto
        for item in fruta_verduras:
            fruta_verdura_id = db.get_fruta_verduras_by_name(item)
            print("fruta name, id= ", item, fruta_verdura_id)
            if not fruta_verdura_id:
                continue
            db.insert_fruta_verdura_to_producto(producto_id, fruta_verdura_id)
        
        db.insert_photo_to_producto(ruta_foto, img_filename, producto_id)

    return redirect(url_for("success", msg = "de producto" ))

@app.route("/success", methods=["GET"])
def success():
    msg = request.args.get("msg")
    return render_template("form_success.html", successMsg=f"Hemos recibido el registro {msg}. Muchas gracias")

if __name__ == "__main__":
    app.run(debug=True)
