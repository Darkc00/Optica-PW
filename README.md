# Requerimientos
Python3
Mysql o mariadb


# Backend REST Instalación
Ejecutar el SQL que está en el archivo OpticaDatabase.sql (en phpmyadmin, o mysqlworkbench)
Cree el entorno virtual, en el terminal:
### `py -m venv env`
Active el entorno:
### `env\Scripts\activate`
Para instalar los paquetes necesarios:
### `pip install -r requirements.txt`

Para ejecutar el proyecto proyecto:
### `cd src`
### `py app.py`

## Database

Asegúrese de haber creado y configurado la información de la BD en el archivo config.py. 

Recuerde activar el entorno cada vez que se vaya a ejecutar el proyecto
### abrir el cmd: env\Scripts\activate
## EndPoints

## Cliente

### CREATE (Method : POST)

http://127.0.0.1:5000/clientes

{
    "nombre": "Juan",
    "cedula": 1010,
    "celular": 322,
    "password": "1234",
    "fechaNacimiento": "1998-05-28",
    "genero": "M"
}
### GET ALL (Method : GET)
http://127.0.0.1:5000/clientes

### GET BY ID (Method : GET)

http://127.0.0.1:5000/clientes/<ID>

### UPDATE (Method : PUT)

http://127.0.0.1:5000/clientes/<ID>



## Pedidos

### CREATE (Method : POST)

http://127.0.0.1:5000/pedidos

{
    "idPedido": 1,
    "idCliente": 1,
    "cantidad": 15,
    "total": 15000,
    "estado": "PENDIENTE"
}

### GET ALL (Method : GET)
http://127.0.0.1:5000/pedidos

### GET BY ID (Method : GET)

http://127.0.0.1:5000/pedidos/<ID>

### UPDATE (Method : PUT)

http://127.0.0.1:5000/pedidos/<ID>

{
    "idCliente": 1,
    "cantidad": 15,
    "total": 15000,
    "estado": "PENDIENTE"
}

### DELETE (Method : DELETE)

http://127.0.0.1:5000/pedidos/<ID>


## Productos

### CREATE (Method : POST)

http://127.0.0.1:5000/productos

{
    "nombre": "Lentes",
    "descripcion": "Lentes Transition",
    "precioVenta": 15000,
    "precioCompra": 10000,
    "existencias": 15
}

### GET ALL (Method : GET)
http://127.0.0.1:5000/productos

### GET BY ID (Method : GET)

http://127.0.0.1:5000/productos/<ID>

### UPDATE (Method : PUT)

http://127.0.0.1:5000/productos/<ID>

{
    "nombre": "Lentes",
    "descripcion": "Lentes Transition",
    "precioVenta": 15000,
    "precioCompra": 10000,
    "existencias": 15
}

### DELETE (Method : DELETE)

http://127.0.0.1:5000/productos/<ID>


## Ventas

### CREATE (Method : POST)

http://127.0.0.1:5000/ventas

{
    "idVenta": 1,
    "idCliente": 1,
    "descuento": 15000,
    "total": 10000
}

### GET ALL (Method : GET)
http://127.0.0.1:5000/ventas

### GET BY ID (Method : GET)

http://127.0.0.1:5000/ventas/<ID>

### UPDATE (Method : PUT)

http://127.0.0.1:5000/ventas/<ID>

{
    "idCliente": 1,
    "descuento": 15000,
    "total": 10000
}

### DELETE (Method : DELETE)

http://127.0.0.1:5000/ventas/<ID>



## Ventas Pedidos

### CREATE (Method : POST)

http://127.0.0.1:5000/ventas-pedidos

{
    "idVenta": 1,
    "idPedido": 1
}

### GET ALL (Method : GET)
http://127.0.0.1:5000/ventas-pedidos

### GET BY ID (Method : GET)

http://127.0.0.1:5000/ventas-pedidos/<IDVENTA>/<IDPEDIDO>

#### Response 
{
    "VentaPedido": {
        "fecha": "Tue, 18 Oct 2022 00:00:00 GMT",
        "idPedido": 1,
        "idVenta": 1
    },
    "exito": true,
    "mensaje": "Venta y pedido encontrado."
}





