from flask import Flask, jsonify, request, render_template, redirect, session
from flask import  make_response
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from config import config
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config.from_object(config['development'])
# Enable CORS
CORS(app, resources={r"/ventas/*": {"origins": "http://localhost"}})
CORS(app, resources={r"/clientes/*": {"origins": "http://localhost"}})
CORS(app, resources={r"/productos/*": {"origins": "http://localhost"}})
CORS(app, resources={r"/ventas-pedidos/*": {"origins": "http://localhost"}})
conexion = MySQL(app)
 
app.secret_key = 'super secret key'

#Vistas del HTML
@app.route('/', methods=['GET'])
def vista_inicio():
    return render_template('inicio.html')

@app.route('/inicio', methods=['GET'])
def redirect_inicio():
    return redirect("/")

@app.route('/lentes', methods=['GET'])
def vista_lentes():
    return render_template('lentes.html')
 
@app.route('/monturas', methods=['GET'])
def vista_monturas():
    return render_template('monturas.html')
 
@app.route('/reseña', methods=['GET'])
def vista_reseña():
    return render_template('reseña.html')
 
@app.route('/gafas-sol', methods=['GET'])
def vista_gafas_sol():
    return render_template('gafas-sol.html')
 
@app.route('/contacto', methods=['GET'])
def vista_contacto():
    return render_template('contacto.html')
   
@app.route('/login', methods=['GET'])
def vista_login():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def vista_register(): 
    return render_template('register.html')

@app.route('/createProducts', methods=['GET'])
def vista_createProducts():
    return render_template('createProducts.html')
 
@app.route('/editar/<prod_id>', methods=['GET'])
def vista_editProduct(prod_id): 
    return render_template('createProducts.html',id_prod = prod_id)

@app.route('/getProducts', methods=['GET'])
def vista_getProducts():
    return render_template('getProducts.html')

@app.route('/getPedidos', methods=['GET'])
def vista_getPedidos():
    return render_template('getPedidos.html')
 
   
# APIS
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    print(session)
    return redirect('/')


# VALIDACION TOKEN  
# JWT Configuration
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing! '}), 401

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid! '}), 401
        return f(current_user, *args, **kwargs)
    return decorated


# Clientes Controller
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT nombre, cedula, genero, celular, fechaNacimiento FROM cliente ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        clientes = []
        for fila in datos:
            cliente = {'nombre': fila[0], 'cedula': fila[1], 'genero': fila[2],
                       'celular': fila[3], 'fechaNacimiento': fila[4]}
            clientes.append(cliente)
        return jsonify({'clientes': clientes, 'mensaje': "Clientes listados.", 'exito': True})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error", 'exito': False})


def leer_cliente_bd(cedula):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT nombre, cedula, genero, celular, fechaNacimiento, id FROM cliente WHERE cedula = '{0}'".format(
            cedula)
        cursor.execute(sql)
        datos = cursor.fetchone()

        if datos != None:

            cliente = {'nombre': datos[0], 'cedula': datos[1], 'genero': datos[2],
                       'celular': datos[3], 'fechaNacimiento': datos[4],'id':datos[5]}
            return cliente
        else:
            return None
    except Exception as ex:
        print(ex)
        return None

#Login Controller
@app.route('/login', methods=['POST'])
def login():
    try:
        # check if password is correct
        cliente = leer_cliente_bd(request.json['cedula'])
        if cliente != None:
            cursor = conexion.connection.cursor()
            sql = "SELECT password FROM login WHERE cedula = '{0}'".format(
                cliente['cedula'])
            cursor.execute(sql)
            datos = cursor.fetchone()
            if check_password_hash(datos[0], request.json['password']):
                session["username"] = cliente['cedula']
                session["user_id"] = cliente['id']
                return jsonify({'mensaje': 'exito','exito':True})
            return jsonify({'cliente': cliente, 'mensaje': "Contraseña inválida.", 'exito': True})
        else:
            return jsonify({'mensaje': "Cliente no encontrado.", 'exito': False})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/clientes/<cedula>', methods=['GET'])
def leer_cliente(cedula):
    try:
        cliente = leer_cliente_bd(cedula)
        if cliente != None:
            return jsonify({'cliente': cliente, 'mensaje': "Cliente encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Cliente no encontrado.", 'exito': False})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error", 'exito': False})

 
@app.route('/clientes', methods=['POST'])
def registrar_cliente():
    try:
        cliente = leer_cliente_bd(request.json['cedula'])
        if cliente != None:
            return jsonify({'mensaje': "Cédula ya existe, no se puede duplicar.", 'exito': False})
        else:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO cliente (nombre, cedula, genero, celular, fechaNacimiento) 
            VALUES ('{0}', {1}, '{2}', {3},'{4}')""".format(request.json['nombre'],
                                                            request.json['cedula'], request.json['genero'], request.json['celular'], request.json['fechaNacimiento'])
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de inserción.
            #Llenar el Login 
            hash_password = generate_password_hash(request.json['password'], method='sha256')
            sql = """INSERT INTO login (cedula, password) 
            VALUES ({0}, '{1}')""".format(request.json['cedula'], hash_password)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Cliente registrado.", 'exito': True})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "No ha llenado todos los campos", 'exito': False})
 

@app.route('/clientes/<cedula>', methods=['PUT'])
def actualizar_cliente(cedula):
    try:
        cliente = leer_cliente_bd(cedula)
        if cliente != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE cliente SET nombre = '{0}', genero = '{1}', celular = {2}, fechaNacimiento = '{3}' 
            WHERE cedula = {4}""".format(request.json['nombre'], request.json['genero'], request.json['celular'], request.json['fechaNacimiento'], cedula)
            cursor.execute(sql)
            # Confirma la acción de actualización.
            conexion.connection.commit()
            return jsonify({'mensaje': "Cliente actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Cliente no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/clientes/<cedula>', methods=['DELETE'])
def eliminar_cliente(cedula):
    try:
        cliente = leer_cliente_bd(cedula)
        if cliente != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM cliente WHERE cedula = '{0}'".format(cedula)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Cliente eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Cliente no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


# Pedidos Controller
 
@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idPedido, idCliente, cantidad, total, estado FROM pedido ORDER BY idPedido ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        pedidos = []
        for fila in datos:
            pedido = {'idPedido': fila[0], 'idCliente': fila[1],
                      'cantidad': fila[2], 'total': fila[3], 'estado': fila[4]}
            pedidos.append(pedido)
        return jsonify({'pedidos': pedidos, 'mensaje': "pedidos listados.", 'exito': True})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error", 'exito': False})


def leer_pedido_bd(idPedido):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idPedido, idCliente, cantidad, total, estado  FROM pedido WHERE idPedido = {0}".format(
            idPedido)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            pedido = {'idPedido': datos[0], 'idCliente': datos[1],
                      'cantidad': datos[2], 'total': datos[3], 'estado': datos[4]}
            return pedido
        else:
            return None
    except Exception as ex:
        return None


@app.route('/pedidos/<idPedido>', methods=['GET'])
def leer_pedido(idPedido):
    try:
        pedido = leer_pedido_bd(idPedido)
        if pedido != None:
            return jsonify({'pedido': pedido, 'mensaje': "Pedido encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Pedido no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/pedidos', methods=['POST'])
def registrar_pedido():
    try:
        try:
            pedido = leer_pedido_bd(request.json['idPedido'])
        except Exception as ex:
            pedido = None
        if pedido != None:
            return jsonify({'mensaje': "Pedido ya existe, no se puede duplicar.", 'exito': False})
        else:

            cursor = conexion.connection.cursor()
            sql = """INSERT INTO pedido ( idCliente, cantidad, total, estado) 
                VALUES ({0}, {1}, {2}, '{3}')""".format(
                                                    session["user_id"],
                                                    request.json['cantidad'], 
                                                    request.json['total'], 
                                                    'pedido'
                                                    )

            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de inserción.
            return jsonify({'mensaje': "pedido registrado.", 'exito': True})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/pedidos/<idPedido>', methods=['PUT'])
def actualizar_pedido(idPedido):
    try:
        pedido = leer_pedido_bd(idPedido)
        if pedido != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE pedido SET idCliente = '{0}', cantidad = '{1}', total = {2}, estado = '{3}' 
            WHERE idPedido = {4}""".format(request.json['idCliente'], request.json['cantidad'], request.json['total'], request.json['estado'], idPedido)
            cursor.execute(sql)
            # Confirma la acción de actualización.
            conexion.connection.commit()
            return jsonify({'mensaje': "pedido actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "pedido no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/pedidos/del/<idPedido>', methods=['GET'])
def eliminar_pedido(idPedido):
    try:
        pedido = leer_pedido_bd(idPedido)
        if pedido != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM pedido WHERE idPedido = '{0}'".format(idPedido)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "pedido eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "pedido no encontrado.", 'exito': False})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error", 'exito': False})

# Productos Controller


@app.route('/productos', methods=['GET'])
def listar_productos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idProducto , nombre, descripcion, precioVenta, precioCompra, existencias, image, categoria  FROM producto ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        productos = []
        for fila in datos:
            producto = {'idProducto': fila[0], 'nombre': fila[1], 'descripcion': fila[2],
                        'precioVenta': fila[3], 'precioCompra': fila[4], 'existencias': fila[5],
                        'image':fila[6],'categoria':fila[7]
                        }
            productos.append(producto)
        return jsonify({'productos': productos, 'mensaje': "productos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

 
def leer_producto_bd(idProducto):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idProducto , nombre, descripcion, precioVenta, precioCompra, existencias, categoria, image  FROM producto WHERE idProducto = '{0}'".format(
            idProducto)
        cursor.execute(sql)
        datos = cursor.fetchone()

        if datos != None:
            producto = {'idProducto': datos[0], 'nombre': datos[1], 'descripcion': datos[2],
                        'precioVenta': datos[3], 'precioCompra': datos[4], 'existencias': datos[5],
                        'categoria': datos[6], 'image': datos[7],
                        }
            return producto
        else:
            return None
    except Exception as ex:
        return None


def leer_producto_by_name_bd(nombre):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idProducto , nombre, descripcion, precioVenta, precioCompra, existencias  FROM producto WHERE nombre = '{0}'".format(
            nombre)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            producto = {'idProducto': datos[0], 'nombre': datos[1], 'descripcion': datos[2],
                        'precioVenta': datos[3], 'precioCompra': datos[4], 'existencias': datos[5]}
            return producto
        else:
            return None
    except Exception as ex:
        return None

def leer_producto_by_cat_bd(categoria):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idProducto , nombre, descripcion, precioVenta, precioCompra, existencias, image   FROM producto WHERE categoria = '{0}'".format(
            categoria)
        cursor.execute(sql)
        datos = cursor.fetchall()
        productos = []
        if datos != None:
            for fila in datos:
                producto = {'idProducto': fila[0], 'nombre': fila[1], 'descripcion': fila[2],
                            'precioVenta': fila[3], 'precioCompra': fila[4], 'existencias': fila[5],
                            'image': fila[6],
                            }
                productos.append(producto)
            return productos
        else:
            return None
    except Exception as ex:
        return None


@app.route('/productos/<idProducto>', methods=['GET'])
def leer_producto(idProducto):
    try:
        producto = leer_producto_bd(idProducto)
        if producto != None:
            return jsonify({'producto': producto, 'mensaje': "producto encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "producto no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/productos/cat/<categoria>', methods=['GET'])
def getProdByCategory(categoria):
    try:
        producto = leer_producto_by_cat_bd(categoria)
        print(producto)
        if producto != None:
            return jsonify({'producto': producto, 'mensaje': "producto encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "producto no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})



@app.route('/productos', methods=['POST'])
def registrar_producto():

    try:
        producto = leer_producto_by_name_bd(request.json['nombre'])
        if producto != None:
            return jsonify({'mensaje': "Producto ya existe, no se puede duplicar.", 'exito': False})
        else: 
            cursor = conexion.connection.cursor()
  
            sql = """INSERT INTO producto (nombre, descripcion, precioVenta, precioCompra, existencias, image,categoria) 
            VALUES ('{0}', '{1}', {2}, {3},{4},'{5}','{6}')""".format(request.json['nombre'],
                                                          request.json['descripcion'], 
                                                          request.json['precioVenta'], 
                                                          request.json['precioCompra'], 
                                                          request.json['existencias'],
                                                          request.json['image'],
                                                           request.json['categoria']
                                                          )

            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de inserción.
            return jsonify({'mensaje': "producto registrado.", 'exito': True})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error", 'exito': False})
 

@app.route('/productos/update/<idProducto>', methods=['POST'])
def actualizar_producto(idProducto):
    try: 
        producto = leer_producto_bd(idProducto)
        if producto != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE producto SET 
            nombre = '{0}', descripcion = '{1}', precioVenta = {2}, precioCompra = {3}, existencias = {4}, image = '{6}', categoria = '{7}' 
            WHERE idProducto = {5}""".format(
                request.json['nombre'], request.json['descripcion'], request.json['precioVenta'], 
                request.json['precioCompra'], request.json['existencias'], idProducto,
                request.json['image'], request.json['categoria']
                )
            cursor.execute(sql)
            # Confirma la acción de actualización.
            conexion.connection.commit()
            return jsonify({'mensaje': "producto actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "producto no encontrado.", 'exito': False})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/productos/del/<idProducto>', methods=['GET'])
def eliminar_producto(idProducto):
    try:
        producto = leer_producto_bd(idProducto)
        if producto != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM producto WHERE idProducto = '{0}'".format(
                idProducto)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "producto eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "producto no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

# Controller Ventas


@app.route('/ventas', methods=['GET'])
def listar_ventas():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idVenta , idCliente, descuento, total FROM venta ORDER BY idVenta ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        ventas = []
        for fila in datos:
            venta = {'idVenta': fila[0], 'idCliente': fila[1],
                     'descuento': fila[2], 'total': fila[3]}
            ventas.append(venta)
        return jsonify({'ventas': ventas, 'mensaje': "ventas listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def leer_venta_bd(idVenta):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idVenta , idCliente, descuento, total FROM venta WHERE idVenta = '{0}'".format(
            idVenta)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            venta = {'idVenta': datos[0], 'idCliente': datos[1],
                     'descuento': datos[2], 'total': datos[3]}
            return venta
        else:
            return None
    except Exception as ex:
        return None


@app.route('/ventas/<idVenta>', methods=['GET'])
def leer_venta(idVenta):
    try:
        venta = leer_venta_bd(idVenta)
        if venta != None:
            return jsonify({'venta': venta, 'mensaje': "venta encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "venta no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/ventas', methods=['POST'])
def registrar_venta():
    try:
        venta = leer_venta_bd(request.json['idVenta'])
        if venta != None:
            return jsonify({'mensaje': "venta ya existe, no se puede duplicar.", 'exito': False})
        else:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO venta (idVenta, idCliente, descuento, total) 
            VALUES ({0}, {1}, {2}, {3})""".format(request.json['idVenta'],
                                                  request.json['idCliente'], request.json['descuento'], request.json['total'])
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de inserción.
            return jsonify({'mensaje': "Venta registrada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/ventas/<idVenta>', methods=['PUT'])
def actualizar_venta(idVenta):
    try:
        venta = leer_venta_bd(idVenta)
        if venta != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE venta SET idCliente = {0}, descuento = {1}, total = {2}
            WHERE idVenta = {3}""".format(request.json['idCliente'], request.json['descuento'], request.json['total'], idVenta)
            cursor.execute(sql)
            # Confirma la acción de actualización.
            conexion.connection.commit()
            return jsonify({'mensaje': "venta actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "venta no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/ventas/<idVenta>', methods=['DELETE'])
def eliminar_venta(idVenta):
    try:
        venta = leer_venta_bd(idVenta)
        if venta != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM venta WHERE idVenta = '{0}'".format(idVenta)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "venta eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "venta no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

#Venta Pedidos Controller
def leer_venta_pedidos_bd(idVenta, idPedido):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idVenta , idPedido, fecha FROM venta_pedido WHERE idVenta = '{0}' and idPedido = '{1}'".format(
            idVenta, idPedido)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            venta_pedido = {'idVenta': datos[0], 'idPedido': datos[1],
                     'fecha': datos[2]}
            return venta_pedido
        else:
            return None
    except Exception as ex:
        return None
    
@app.route('/ventas-pedidos', methods=['POST'])
def registrar_venta_pedido():
    try:
        venta = leer_venta_pedidos_bd(request.json['idVenta'], request.json['idPedido'])
        if venta != None:
            return jsonify({'mensaje': "Ya existe una venta con ese, no se puede duplicar.", 'exito': False})
        else:
            date = datetime.now()
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO venta_pedido (idVenta, idPedido, fecha) 
            VALUES ({0}, {1}, '{2}')""".format(request.json['idVenta'],
                                                  request.json['idPedido'], date)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de inserción.
            return jsonify({'mensaje': "Venta registrada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/ventas-pedidos/<idVenta>/<idPedido>', methods=['GET'])
def leer_venta_pedidos(idVenta, idPedido):
    try:
        
        venta = leer_venta_pedidos_bd(idVenta, idPedido)
        
        if venta != None:
            return jsonify({'VentaPedido': venta, 'mensaje': "Venta y pedido encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "venta y pedido no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})

@app.route('/ventas-pedidos', methods=['GET'])
def listar_ventas_pedidos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idVenta , idPedido, fecha  FROM venta_pedido ORDER BY idVenta ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        ventas = []
        for fila in datos:
            venta_pedido = {'idVenta': fila[0], 'idPedido': fila[1],
                     'fecha': fila[2]}
            ventas.append(venta_pedido)
        return jsonify({'ventas_pedidos': ventas, 'mensaje': "ventas y pedidos listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
