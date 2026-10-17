#--
import calendar  
import json      


ANIO = 2026                     
MES = 12                         
NOMBRE_ARCHIVO = "reservas.json"  

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}


TURNOS = {
    1: "09:00",
    2: "09:30",
    3: "10:00",
    4: "10:30",
    5: "11:00",
    6: "11:30",
    7: "16:00",
    8: "16:30",
    9: "17:00",
    10: "17:30",
    11: "18:00",
    12: "18:30",
    13: "19:00",
    14: "19:30"
}



# ==============================================================
# FUNCIONES PARA GUARDAR Y CARGAR EL ARCHIVO JSON
# ==============================================================
def validar_texto(mensaje):
    while True:
        texto = input(mensaje)
        valido = True
        if texto == "":
            valido = False
        else:
            i = 0
            while i < len(texto):
                c = texto[i]
                if not ((c >= "A" and c <= "Z") or (c >= "a" and c <= "z") or c == " "):
                    valido = False
                    break
                i += 1
        if valido:
            return texto
        else:
            print("Dato inválido. Solo letras y espacios. Intente otra vez.")


def cargar_reservas():
    
    try:
        
        with open(NOMBRE_ARCHIVO, "r") as archivo:
            reservas = json.load(archivo)
        return reservas
    except FileNotFoundError:
        
        return {}
    except json.JSONDecodeError:
       
        print("Aviso: el archivo de reservas está dañado. Se empieza sin reservas.")
        return {}


def guardar_reservas(reservas):
    
    try:
        
        with open(NOMBRE_ARCHIVO, "w") as archivo:
            # indent=4 deja el archivo ordenado y fácil de leer.
            # ensure_ascii=False permite guardar tildes y la letra ñ sin cambiarlas.
            json.dump(reservas, archivo, indent=4, ensure_ascii=False)
    except OSError:
       
        print("Error: no se pudo guardar el archivo de reservas.")


# ==============================================================
# FUNCIONES AUXILIARES  PARA TRABAJAR CON FECHAS
# ==============================================================

def crear_clave_fecha(dia):
   
    if dia < 10:
        texto_dia = "0" + str(dia)
    else:
        texto_dia = str(dia)
    return str(ANIO) + "-" + str(MES) + "-" + texto_dia


def es_dia_habil(dia):
    
    numero_dia_semana = calendar.weekday(ANIO, MES, dia)
    if numero_dia_semana < 5:
        return True
    else:
        return False


def describir_dia(dia):
    
    numero_dia_semana = calendar.weekday(ANIO, MES, dia)
    nombre_dia = DIAS_SEMANA[numero_dia_semana]
    return nombre_dia + " " + str(dia) + " de diciembre de " + str(ANIO)


def obtener_reservas_del_dia(reservas, dia):
    # Devuelve el diccionario con las reservas de un día.
    # Si ese día no tiene ninguna reserva, devuelve un diccionario vacío.
    clave = crear_clave_fecha(dia)
    if clave in reservas:
        return reservas[clave]
    else:
        return {}


# ==============================================================
# FUNCIONES PARA PEDIR DATOS AL USUARIO (con validación)
# ==============================================================

def pedir_dia():
    
    datos_mes = calendar.monthrange(ANIO, MES)
    cantidad_dias = datos_mes[1]  # Diciembre tiene 31

    while True:
        try:
            dia = int(input("Ingrese el día de diciembre (1-" + str(cantidad_dias) + ", 0 para volver al menú): "))

            if dia == 0:
                return 0
            elif dia < 1 or dia > cantidad_dias:
                print("Error: diciembre tiene días del 1 al " + str(cantidad_dias) + ".")
            elif es_dia_habil(dia) == False:
                nombre_dia = DIAS_SEMANA[calendar.weekday(ANIO, MES, dia)]
                print("Error: el " + str(dia) + " es " + nombre_dia + ". Solo se atiende de lunes a viernes.")
            else:
                
                return dia
        except ValueError:
            
            print("Error: debe ingresar un número entero.")


def pedir_numero_turno():
    
    while True:
        try:
            numero = int(input("Ingrese el número de turno (0 para volver al menú): "))

            if numero == 0:
                return 0
            elif numero in TURNOS:
                
                return numero
            else:
                print("Error: el número de turno debe estar entre 1 y " + str(len(TURNOS)) + ".")
        except ValueError:
            print("Error: debe ingresar un número entero.")


def pedir_texto(mensaje):
    
    while True:
        
        texto = validar_texto(mensaje)
        if texto == "":
            print("Error: este dato no puede quedar vacío.")
        else:
            return texto


def pedir_confirmacion(mensaje):
    
    while True:
        
        respuesta = input(mensaje).strip().lower()
        if respuesta == "si":
            return True
        elif respuesta == "no":
            return False
        else:
            print("Responda con 'si' o 'no'")


# ==============================================================
# FUNCIONES PARA MOSTRAR INFORMACIÓN
# ==============================================================

def mostrar_turnos_disponibles(reservas, dia):
    
    reservas_del_dia = obtener_reservas_del_dia(reservas, dia)

    print()
    print("TURNOS DISPONIBLES - " + describir_dia(dia))
    print("(cada turno dura 30 minutos)")

    cantidad_disponibles = 0

   
    for numero in TURNOS:
        hora = TURNOS[numero]
        
        if hora not in reservas_del_dia:
           
            print("  " + str(numero).rjust(2) + ") " + hora)
            cantidad_disponibles = cantidad_disponibles + 1

    if cantidad_disponibles == 0:
        print("  No quedan turnos disponibles para este día.")

    return cantidad_disponibles


def mostrar_turnos_reservados(reservas, dia):
    
    reservas_del_dia = obtener_reservas_del_dia(reservas, dia)

    print()
    print("TURNOS RESERVADOS - " + describir_dia(dia))

    cantidad_reservados = 0

    for numero in TURNOS:
        hora = TURNOS[numero]
        # Si la hora SÍ está entre las reservas del día, el turno está ocupado.
        if hora in reservas_del_dia:
            datos = reservas_del_dia[hora]
            print("  " + str(numero).rjust(2) + ") " + hora +
                  " - Mascota: " + datos["mascota"] +
                  " | Dueño: " + datos["dueno"])
            cantidad_reservados = cantidad_reservados + 1

    if cantidad_reservados == 0:
        print("  No hay reservas para este día.")

    return cantidad_reservados


def mostrar_calendario():

    semanas = calendar.monthcalendar(ANIO, MES)

    print()
    print("      DICIEMBRE " + str(ANIO))
    print("Lu  Ma  Mi  Ju  Vi  Sá  Do")

    for semana in semanas:
        linea = ""
        
        for posicion in range(7):
            dia = semana[posicion]
            if dia == 0:
                texto = "  "                  # Espacio vacío: el día es de otro mes
            elif posicion >= 5:
                texto = "--"                  # Sábado o domingo: no se atiende
            else:
                texto = str(dia).rjust(2)     # Día de atención
            linea = linea + texto + "  "
        print(linea)

    print()
    print("-- = no se atiende (fin de semana)")


# ==============================================================
# FUNCIONES PRINCIPALES DEL PROGRAMA (las opciones del menú)
# ==============================================================

def reservar_turno(reservas):
    
    print()
    print("--- RESERVAR UN TURNO ---")

    # Paso 1: elegir el día
    dia = pedir_dia()
    if dia == 0:
        return  # "return" sin valor termina la función: volvemos al menú

    # Paso 2: mostrar los turnos libres de ese día
    cantidad_disponibles = mostrar_turnos_disponibles(reservas, dia)
    if cantidad_disponibles == 0:
        return

    # Paso 3: elegir el turno
    numero_turno = pedir_numero_turno()
    if numero_turno == 0:
        return

    hora = TURNOS[numero_turno]

    # Paso 4: verificar que el turno elegido no esté ocupado
    reservas_del_dia = obtener_reservas_del_dia(reservas, dia)
    if hora in reservas_del_dia:
        print("Error: el turno de las " + hora + " ya está reservado.")
        return

    # Paso 5: pedir los datos del cliente
    nombre_dueno = pedir_texto("Nombre del dueño: ")
    nombre_mascota = pedir_texto("Nombre de la mascota: ")

    # Paso 6: guardar la reserva en el diccionario
    clave = crear_clave_fecha(dia)
    if clave not in reservas:
        # Si es la primera reserva de ese día, creamos su diccionario vacío.
        reservas[clave] = {}
    reservas[clave][hora] = {
        "dueno": nombre_dueno,
        "mascota": nombre_mascota
    }

    # Paso 7: guardar el diccionario completo en el archivo JSON
    guardar_reservas(reservas)

    print()
    print("¡Reserva confirmada! " + describir_dia(dia) + " a las " + hora +
          " - Mascota: " + nombre_mascota + " (Dueño: " + nombre_dueno + ")")


def cancelar_reserva(reservas):
    
    print()
    print("--- CANCELAR UNA RESERVA ---")

    # Paso 1: elegir el día
    dia = pedir_dia()
    if dia == 0:
        return

    
    cantidad_reservados = mostrar_turnos_reservados(reservas, dia)
    if cantidad_reservados == 0:
        return

    
    numero_turno = pedir_numero_turno()
    if numero_turno == 0:
        return

    hora = TURNOS[numero_turno]

    
    reservas_del_dia = obtener_reservas_del_dia(reservas, dia)
    if hora not in reservas_del_dia:
        print("Error: el turno de las " + hora + " no tiene ninguna reserva.")
        return

    
    datos = reservas_del_dia[hora]
    print()
    print("Reserva seleccionada: " + hora + " - Mascota: " + datos["mascota"] +
          " | Dueño: " + datos["dueno"])
    confirmado = pedir_confirmacion("¿Está seguro de que desea cancelarla? (si/no): ")

    if confirmado == True:
        clave = crear_clave_fecha(dia)
        # "del" elimina una clave (y su valor) de un diccionario.
        del reservas[clave][hora]

       
        if len(reservas[clave]) == 0:
            del reservas[clave]

        # Guardamos el cambio en el archivo JSON
        guardar_reservas(reservas)
        print("La reserva fue cancelada correctamente.")
    else:
        print("No se canceló ninguna reserva.")


def mostrar_menu():
    # Muestra las opciones del menú principal.
    print()
    print("=" * 40)  # "=" * 40 repite el signo "=" 40 veces
    print("  VETERINARIA - RESERVAS DE DICIEMBRE")
    print("=" * 40)
    print("1. Ver turnos disponibles")
    print("2. Ver turnos reservados")
    print("3. Reservar un turno")
    print("4. Cancelar una reserva")
    print("5. Ver calendario de diciembre")
    print("6. Salir")


def programa_principal():
    
    reservas = cargar_reservas()

    continuar = True

    while continuar == True:
        mostrar_menu()
        opcion = input("Elija una opción (1-6): ").strip()

        if opcion == "1":
            print()
            print("--- VER TURNOS DISPONIBLES ---")
            dia = pedir_dia()
            if dia != 0:
                mostrar_turnos_disponibles(reservas, dia)
        elif opcion == "2":
            print()
            print("--- VER TURNOS RESERVADOS ---")
            dia = pedir_dia()
            if dia != 0:
                mostrar_turnos_reservados(reservas, dia)
        elif opcion == "3":
            reservar_turno(reservas)
        elif opcion == "4":
            cancelar_reserva(reservas)
        elif opcion == "5":
            mostrar_calendario()
        elif opcion == "6":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            continuar = False  # Esto termina el while
        else:
            print("Opción no válida. Elija un número del 1 al 6.")


# --------------------------------------------------------------
# INICIO DEL PROGRAMA
# --------------------------------------------------------------
programa_principal()
