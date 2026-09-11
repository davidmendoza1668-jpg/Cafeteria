# ============================================================================================================
# ================= ENTIDADES DEL SISTEMA DE CAFETERIA ========================================================
# ============================================================================================================

# Datos iniciales para la prueba del sistema de cafeteria
productos = [
    {"id": 1, "nombre": "Café Americano", "precio": 2500, "stock": 20, "stock_minimo": 5},
    {"id": 2, "nombre": "Café con Leche", "precio": 3000, "stock": 15, "stock_minimo": 5},
    {"id": 3, "nombre": "Empanada", "precio": 2000, "stock": 10, "stock_minimo": 5},
    {"id": 4, "nombre": "Jugo Natural", "precio": 3500, "stock": 4, "stock_minimo": 5},  # Alerta stock bajo
    {"id": 5, "nombre": "Sándwich", "precio": 4500, "stock": 8, "stock_minimo": 5},
]

usuarios = [
    {"id": 1, "nombre_usuario": "admin", "contrasena": "admin123", "rol": "Administrador"},
    {"id": 2, "nombre_usuario": "cajero1", "contrasena": "caja123", "rol": "Cajero"},
]

ventas = []   # inicia vacía, se llena cuando el sistema esté en uso
compras = []  # inicia vacía, se llena cuando el sistema esté en uso


# ============================================================================================================
# ================= MODULO DE AUTENTICACION Y REGISTRO DE USUARIOS ===========================================
# ============================================================================================================

def registrar_usuario(rol_deseado, lista_usuarios):
    nuevo_id = len(lista_usuarios) + 1

    match rol_deseado:
        case "Administrador":
            clave_administrador = 113344
            print("\n--- Bienvenido Administrador ---")
            print("Ingresa los siguientes datos para crear tu usuario:")
            
            try:
                cedula = int(input("Ingresa el número de tu cédula: "))
            except ValueError:
                print("Error: La cédula debe ser numérica.")
                return

            usuario = input("Ingresa tu nuevo usuario: ")
            contrasena = input("Ingresa la contraseña: ")
            confirmar_contrasena = input("Ingresa nuevamente la contraseña: ")
            
            try:
                clave_usuario = int(input("Ingresa la clave de administrador: "))
            except ValueError:
                print("Error: La clave debe ser numérica.")
                return

            if clave_usuario == clave_administrador and contrasena == confirmar_contrasena:
                lista_usuarios.append({
                    "id": nuevo_id,
                    "cedula": cedula,
                    "nombre_usuario": usuario, 
                    "contrasena": contrasena,
                    "rol": "Administrador"
                })
                print("Ha sido registrado correctamente como Administrador.")
            else:
                print("Información incorrecta: revise la clave de administrador o la coincidencia de contraseñas.")

        case "Cajero":
            print("\n--- Bienvenido Cajero ---")
            usuario = input("Ingresa tu nuevo usuario: ")
            contrasena = input("Ingresa la contraseña: ")
            confirmar_contrasena = input("Ingresa nuevamente la contraseña: ")

            if contrasena == confirmar_contrasena:  
                lista_usuarios.append({
                    "id": nuevo_id,
                    "nombre_usuario": usuario, 
                    "contrasena": contrasena,
                    "rol": "Cajero"
                })
                print("Ha sido registrado correctamente como Cajero.")
            else:
                print("Las contraseñas no coinciden.")
                
        case _:
            print("Rol no reconocido. Seleccione 'Administrador' o 'Cajero'.")


def iniciar_sesion(usuarios):
    intentos = 3
    while intentos > 0:
        nombre_usuario = input("\nIngrese su nombre de usuario: ")
        contrasena = input("Ingrese su contraseña: ")

        for usuario in usuarios:
            if usuario["nombre_usuario"] == nombre_usuario and usuario["contrasena"] == contrasena:
                print(f"Bienvenido {usuario['nombre_usuario']}! Rol: {usuario['rol']}")
                return usuario  # Retorna el diccionario del usuario autenticado

        intentos -= 1
        print(f"Credenciales incorrectas. Intentos restantes: {intentos}")

    print("Ha excedido el número de intentos. Acceso denegado.")
    return None


# ============================================================================================================
# ================= MODULO DE GESTION DE PEDIDOS ==============================================================
# ============================================================================================================

def mostrar_inventario(productos):
    print("\n--- INVENTARIO ---")
    for producto in productos:
        alerta = " [STOCK BAJO]" if producto["stock"] <= producto["stock_minimo"] else ""
        print(f"{producto['id']} - {producto['nombre']} | Stock: {producto['stock']}{alerta}")


def buscar_producto(productos, id_producto):
    for producto in productos:
        if producto["id"] == id_producto:
            return producto
    return None


def actualizar_stock(productos, id_producto, cantidad):
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


def imprimir_factura(productos_vendidos, total, recibido, cambio):
    print("\n----- FACTURA -----")
    for item in productos_vendidos:
        subtotal = item["cantidad"] * item["precio_unitario"]
        print(f"{item['nombre']}  x{item['cantidad']}  Unidad {item['precio_unitario']}  = {subtotal}")
    print("--------------------")
    print(f"TOTAL:     {total}")
    print(f"Recibido:  {recibido}")
    print(f"Cambio:    {cambio}")


def registrar_venta(productos, ventas, usuario):
    productos_vendidos = []
    total_venta = 0

    while True:
        mostrar_inventario(productos)
        id_producto = int(input("Ingresa el ID del producto a vender (o '0' para finalizar): "))

        if id_producto == 0:
            break

        producto = buscar_producto(productos, id_producto)

        if producto is None:
            print("Producto no encontrado.")
            continue

        cantidad = int(input(f"Ingresa la cantidad de '{producto['nombre']}' a vender: "))
        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            continue

        if cantidad > producto["stock"]:
            print("Stock insuficiente.")
            continue

        actualizar_stock(productos, id_producto, -cantidad)
        total_venta += cantidad * producto["precio"]
        
        productos_vendidos.append({
            "id_ventas": len(ventas) + 1,
            "id_producto": producto["id"],
            "nombre": producto["nombre"],
            "cantidad": cantidad,
            "precio_unitario": producto["precio"],
            "anulada": False,
        })

    if productos_vendidos:
        print(f"Total de la venta: {total_venta}")
        monto_recibido = float(input("Ingresa el monto recibido del cliente: "))
        while monto_recibido < total_venta: 
            print("Monto insuficiente. Intenta nuevamente.")
            monto_recibido = float(input("Ingresa el monto recibido del cliente: "))

        cambio = monto_recibido - total_venta
        print(f"Cambio a entregar: {cambio}")
        
        imprimir_factura(productos_vendidos, total_venta, monto_recibido, cambio)

        ventas.append({
            "id": len(ventas) + 1,
            "productos": productos_vendidos,
            "total": total_venta,
            "recibido": monto_recibido,
            "cambio": cambio,
            "anulada": False,
            "usuario": usuario["nombre_usuario"]
        })
    else:
        print("No se registró ninguna venta.")

    
def listar_ventas(ventas):
    print("\n--- LISTA DE VENTAS ---")
    for venta in ventas:
        estado = "Anulada" if venta["anulada"] else "Activa"
        print(f"\nID Venta: {venta['id']} | Total: {venta['total']} | Estado: {estado}")
        for item in venta["productos"]:
            print(f"   - {item['nombre']} x{item['cantidad']} @ {item['precio_unitario']}")

def anular_venta(ventas , productos, id_venta):
        for venta in ventas:
            if venta["id"] == id_venta:
                if venta["anulada"]:
                    print("La venta ya ha sido anulada previamente.")
                    return
                venta["anulada"] = True
                # Revertir el stock
                for item in venta["productos"]:
                    actualizar_stock(productos, item["id_producto"], item["cantidad"])
                print(f"Venta ID {id_venta} ha sido anulada y el stock revertido.")
                return
        print("Venta no encontrada.")

def menu_administrador(usuario):
    while True:
        print(f"\n--- Menú Administrador ({usuario['nombre_usuario']}) ---")
        print("1. Ver inventario")
        print("2. Registrar venta")
        print("3. Ver ventas")
        print("4. Anular venta")
        print("5. Volver")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrar_inventario(productos)
        elif opcion == "2":
            registrar_venta(productos, ventas, usuario)
        elif opcion == "3":
            listar_ventas(ventas)
        elif opcion == "4":
            id_venta = int(input("Ingresa el ID de la venta a anular: "))
            anular_venta(ventas, productos, id_venta)
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")


def menu_cajero(usuario):
    while True:
        print(f"\n--- Menú Cajero ({usuario['nombre_usuario']}) ---")
        print("1. Ver inventario")
        print("2. Registrar venta")
        print("3. Ver ventas")
        print("4. Volver")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrar_inventario(productos)
        elif opcion == "2":
            registrar_venta(productos, ventas, usuario)
        elif opcion == "3":
            listar_ventas(ventas)
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")

def main():
    while True:
        print("\n=== RINCÓN CAFETERO ===")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            usuario_actual = iniciar_sesion(usuarios)
            if usuario_actual:
                if usuario_actual["rol"] == "Administrador":
                    menu_administrador(usuario_actual)
                else:
                    menu_cajero(usuario_actual)

        elif opcion == "2":
            rol_usuario = input("Ingresa tu rol (Administrador / Cajero): ").strip().capitalize()
            if rol_usuario in ["Administrador", "Cajero"]:
                registrar_usuario(rol_usuario, usuarios)
            else:
                print("Opción inválida.")

        elif opcion == "3":
            print("Hasta pronto.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()