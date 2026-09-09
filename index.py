# Entidades del sistema de cafeteria
# En este caso cada producto es un diccionario que contiene información sobre el producto, como su id, nombre, precio, stock y stock mínimo. Esto permite almacenar y acceder a los datos de cada producto de manera estructurada.


#============================================================================================================
#================ ENTIDADES DEL SISTEMA DE CAFETERIA ========================================================
#============================================================================================================


# Productos disponibles en la cafeteria
producto = {
    "id": 1,
    "nombre": "Café Americano",
    "precio": 2500,
    "stock": 20,
    "stock_minimo": 5
}

# Usuario del sistema de cafeteria
usuario = {
    "id": 1,
    "nombre_usuario": "cajero1",
    "contrasena": "1234",
    "rol": "Cajero"   # o "Administrador"
}

# Venta realizada en la cafeteria
venta = {
    "id": 1,
    "cajero": "cajero1",
    "productos": [
        {"id_producto": 1, "cantidad": 2}
    ],
    "total": 5000,
    "recibido": 10000,
    "cambio": 5000,
    "fecha": "2026-09-09"
}

# Compra realizada a un proveedor para reabastecer productos en la cafeteria
compra = {
    "id": 1,
    "proveedor": "Distribuidora XYZ",
    "id_producto": 1,
    "cantidad": 10,
    "fecha": "2026-09-09"
}


# Listas para almacenar los datos de productos, usuarios, ventas y compras
productos = []   
usuarios = []    
ventas = []     
compras = []     


# Datos para la prueba del sistema de cafeteria
productos = [
    {"id": 1, "nombre": "Café Americano", "precio": 2500, "stock": 20, "stock_minimo": 5},
    {"id": 2, "nombre": "Café con Leche", "precio": 3000, "stock": 15, "stock_minimo": 5},
    {"id": 3, "nombre": "Empanada", "precio": 2000, "stock": 10, "stock_minimo": 5},
    {"id": 4, "nombre": "Jugo Natural", "precio": 3500, "stock": 4, "stock_minimo": 5},  # ya en alerta de stock bajo
    {"id": 5, "nombre": "Sándwich", "precio": 4500, "stock": 8, "stock_minimo": 5},
]

usuarios = [
    {"id": 1, "nombre_usuario": "admin", "contrasena": "admin123", "rol": "Administrador"},
    {"id": 2, "nombre_usuario": "cajero1", "contrasena": "caja123", "rol": "Cajero"},
]

ventas = []   # inicia vacía, se llena cuando el sistema esté en uso
compras = []  # inicia vacía, se llena cuando el sistema esté en uso


#============================================================================================================
#================ MODULO DE AUTENTICACION DE USUARIOS =======================================================
#============================================================================================================

def iniciar_sesion(usuarios):
    intentos = 3
    while intentos > 0:
        nombre_usuario = input("Ingrese su nombre de usuario: ")
        contrasena = input("Ingrese su contraseña: ")

        for usuario in usuarios:
            if usuario["nombre_usuario"] == nombre_usuario and usuario["contrasena"] == contrasena:
                print(f"Bienvenido {usuario['nombre_usuario']}! Rol: {usuario['rol']}")
                return usuario  # Retorna el diccionario del usuario autenticado

        intentos -= 1
        print(f"Credenciales incorrectas. Intentos restantes: {intentos}")

    print("Ha excedido el número de intentos. Acceso denegado.")
    return None  # Retorna None si no se pudo autenticar al usuario

usuario_actual = iniciar_sesion(usuarios)

if usuario_actual:
    print("Acceso concedido, rol:", usuario_actual["rol"])





#============================================================================================================
#================ MODULO DE GESTION DE PEDIDOS ==============================================================
#============================================================================================================

def mostrar_inventario(productos):
    print("\n--- INVENTARIO ---")
    for producto in productos:
        alerta = " STOCK BAJO" if producto["stock"] <= producto["stock_minimo"] else ""
        print(f"{producto['id']} - {producto['nombre']} | Stock: {producto['stock']}{alerta}")


def buscar_producto(productos, id_producto):
    for producto in productos:
        if producto["id"] == id_producto:
            return producto
    return None


def actualizar_stock(productos, id_producto, cantidad):
    # cantidad positiva = entra mercancía (compra)
    # cantidad negativa = sale mercancía (venta)
    producto = buscar_producto(productos, id_producto)

    if producto is None:
        print("Producto no encontrado.")
        return False

    if producto["stock"] + cantidad < 0:
        print("Stock insuficiente para esta operación.")
        return False

    producto["stock"] += cantidad

    if producto["stock"] <= producto["stock_minimo"]:
        print(f" Alerta: '{producto['nombre']}' llegó a stock mínimo ({producto['stock']} unidades)")

    return True