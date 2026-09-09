administradores = []
cajeros = []

def registrar_usuario(rol_deseado, lista):
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
            contraseña = input("Ingresa la contraseña: ")
            confirmar_contraseña = input("Ingresa nuevamente la contraseña: ")
            
            try:
                clave_usuario = int(input("Ingresa la clave de administrador: "))
            except ValueError:
                print("Error: La clave debe ser numérica.")
                return

            if clave_usuario == clave_administrador and contraseña == confirmar_contraseña:
                lista.append({"cedula": cedula, "usuario": usuario, "contraseña": contraseña})
                print("Ha sido registrado correctamente como Administrador.")
            else:
                print("Información incorrecta: revise la clave de administrador o la coincidencia de contraseñas.")

        case "Cajero":
            print("\n--- Bienvenido Cajero ---")
            usuario = input("Ingresa tu nuevo usuario: ")
            contraseña = input("Ingresa la contraseña: ")
            confirmar_contraseña = input("Ingresa nuevamente la contraseña: ")

            if contraseña == confirmar_contraseña:
                lista.append({"usuario": usuario, "contraseña": contraseña})
                print("Ha sido registrado correctamente como Cajero.")
            else:
                print("Las contraseñas no coinciden.")
                
        case _:
            print("Rol no reconocido. Seleccione 'Administrador' o 'Cajero'.")

def main():
    rol_usuario = input("Ingresa tu rol (Administrador / Cajero): ").strip().capitalize()
    
    if rol_usuario == "Administrador":
        registrar_usuario(rol_usuario, administradores)
    elif rol_usuario == "Cajero":
        registrar_usuario(rol_usuario, cajeros)
    else:
        print("Opción inválida.")

main()
