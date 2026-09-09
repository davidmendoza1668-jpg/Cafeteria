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

            if contrasena == confirmar_contrasena:  # Corregido: sin eñes
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


def main():
    rol_usuario = input("Ingresa tu rol (Administrador / Cajero): ").strip().capitalize()
    
    # Pasamos la lista 'usuarios' para que los nuevos registros se puedan usar en el Login
    if rol_usuario in ["Administrador", "Cajero"]:
        registrar_usuario(rol_usuario, usuarios)
    else:
        print("Opción inválida.")

if __name__ == "__main__":
    main()

