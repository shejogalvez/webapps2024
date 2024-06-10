import re
import filetype
from database import db 

def validate_username(value):
    return value and len(value) > 4


def validate_password(value):
    malas = ["1234", "admin1", "odio a mis Aux >:(2"]
    return bool(re.search(r"\d", value)) and not value in malas


def validate_email(value):
    return "@" in value


def validate_phone_number(value):
    return bool(re.search("^\\+?[1-9][0-9]{7,14}$", value)) or not value


def validate_min_max_length(value, min, max):
    return len(value) <= max and len(value) >= min


def validate_nonNull_value(value):
    return bool(value)


def validate_img(files):
    for conf_img in files:
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
        ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

        # check if a file was submitted
        if conf_img is None:
            return False

        # check if the browser submitted an empty file
        if conf_img.filename == "":
            return False
        
        # check file extension
        ftype_guess = filetype.guess(conf_img)
        if ftype_guess.extension not in ALLOWED_EXTENSIONS:
            return False
        # check mimetype
        if ftype_guess.mime not in ALLOWED_MIMETYPES:
            return False
    return True

def not_exist_in_db(array: list, query):
    return any([not query(x) for x in array])

def validate_prod_form(request):
    tipo_producto = request.form.get("tipo_producto")
    fruta_verduras = request.form.getlist("fruta_verdura_checkbox")
    region_id = request.form.get("region")
    comuna_id = request.form.get("comuna")
    nombre_productor = request.form.get("nombre_productor")
    email_productor = request.form.get("email_productor")
    celular_productor = request.form.get("celular_productor")

    print(tipo_producto,
fruta_verduras,
region_id,
comuna_id,
nombre_productor,
email_productor ,
celular_productor)

    errors = []
    if (tipo_producto not in ["fruta", "verdura"]): 
        errors.append("tipo producto es requerido")
    if (not validate_min_max_length(fruta_verduras, 1, 5) or not_exist_in_db(fruta_verduras, db.get_fruta_verduras_by_name)): 
        errors.append("debe seleccionar entre 1 y 5 frutas/verduras")
    if (not validate_nonNull_value(region_id)): 
        errors.append("tipo producto es requerido")
    if (not validate_nonNull_value(comuna_id) or not_exist_in_db([comuna_id], db.get_comuna_by_id)): 
        errors.append("tipo producto es requerido")
    if (not validate_min_max_length(nombre_productor, 3, 80)): 
        errors.append("nombre productor debe tener entre 3 y 80 caracteres")
    if (not validate_email(email_productor)): 
        errors.append("email inválido o nulo")
    if (not validate_phone_number(celular_productor)): 
        errors.append("número de teléfono inválido")
    return errors

def validate_photos(request):
    fotos_producto = request.files.getlist("foto_producto")
    errors = []
    if (not validate_img(fotos_producto)): 
        errors.append("imagen con formato inválido")
    if (not validate_min_max_length(fotos_producto, 1, 3)): 
        errors.append("debe seleccionar entre 1 y 3 imágenes")
    return errors