import re
import filetype

def validate_username(value):
    return value and len(value) > 4


def validate_password(value):
    malas = ["1234", "admin1", "odio a mis Aux >:(2"]
    return bool(re.search(r"\d", value)) and not value in malas


def validate_email(value):
    return "@" in value


def validate_phone_number(value):
    return bool(re.search("^\\+?[1-9][0-9]{7,14}$", value))


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


def validate_prod_form(tipo_producto, fruta_verduras, fotos_producto, region, comuna, nombre_productor, email_productor, celular_productor):
    errors = []
    if (not validate_nonNull_value(tipo_producto)): 
        errors.append("tipo producto es requerido")
    if (not validate_min_max_length(fruta_verduras, 1, 5)): 
        errors.append("debe seleccionar entre 1 y 5 frutas/verduras")
    if (not validate_img(fotos_producto)): 
        errors.append("imagen con formato inválido")
    if (not validate_min_max_length(fotos_producto, 1, 3)): 
        errors.append("debe seleccionar entre 1 y 3 imágenes")
    if (not validate_nonNull_value(region)): 
        errors.append("tipo producto es requerido")
    if (not validate_nonNull_value(comuna)): 
        errors.append("tipo producto es requerido")
    if (not validate_min_max_length(nombre_productor, 3, 80)): 
        errors.append("nombre productor debe tener entre 3 y 80 caracteres")
    if (not validate_email(email_productor)): 
        errors.append("email inválido o nulo")
    if (not validate_phone_number(celular_productor)): 
        errors.append("número de teléfono inválido")
    return errors
