def seleccion_opcion():
    opcion = 0
    while opcion < 1 or opcion > 3:
        opcion = int(input("Elige la opción que desees realizar:\n1. Cifrar\n2. Descifrar\n3. Salir\n"))
    return opcion

def validacion_mensaje():
    while True:
        mensaje = input("Coloque el mensaje, por favor: ")
        if mensaje.strip() == "":
            print("El mensaje no puede estar vacío. Por favor, inténtelo de nuevo.")
        else:
            return mensaje

def calcular_mcd(x, y):
    while y != 0:
        temp = y
        y = x % y
        x = temp
    return x

def hallar_d(functEuler):
    valores_d = []
    d = 2
    while d < functEuler:
        if calcular_mcd(d, functEuler) == 1:
            valores_d.append(d)
        d += 1

    print("Valores de d disponibles:", valores_d)
    valor_d_elegido = 0
    while valor_d_elegido not in valores_d:
        valor_d_elegido = int(input(f"Ingrese un valor de d de la siguiente lista: {', '.join(map(str, valores_d))}\n"))
    return valor_d_elegido

def congruencia_lineal(a, b, n):
    def euclides_extendido(x, y):
        old_r, r = x, y
        old_s, s = 1, 0
        old_t, t = 0, 1
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
        return old_r, old_s, old_t

    def inverso_multiplicativo(x, z):
        mcd, s, _ = euclides_extendido(x, z)
        if mcd != 1:
            raise ValueError(f"{x} no tiene inverso multiplicativo módulo {z}")
        return (s % z + z) % z

    inverso = inverso_multiplicativo(a, n)
    solucion = (b * inverso) % n
    return solucion

def tabla_equivalencia(letra):
    letra = letra.upper()
    if letra < "A" or letra > "Z":
        return "Fuera de rango"
    return ord(letra) - ord("A")

def tabla_inversa(numero):
    numero = numero % 26
    if numero < 0 or numero > 25:
        return "Fuera de rango"
    letra = chr(numero + ord("A"))
    return letra

def es_primo(numero):
    if numero <= 1:
        return False
    if numero <= 3:
        return True
    if numero % 2 == 0 or numero % 3 == 0:
        return False
    i = 5
    while i * i <= numero:
        if numero % i == 0 or numero % (i + 2) == 0:
            return False
        i += 6
    return True

def cifrar():
    mensaje = validacion_mensaje()
    p, q = 0, 0
    while not all(map(es_primo, [p, q])) or p == q:
        p = int(input("Elige un número primo: "))
        q = int(input("Elige otro número primo diferente al anterior: "))
    n = p * q
    euler = (p - 1) * (q - 1)
    d = hallar_d(euler)
    e = congruencia_lineal(d, 1, euler)
    C = []
    for caracter in mensaje:
        elemento_push = congruencia_lineal(1, tabla_equivalencia(caracter) ** e, n)
        C.append(tabla_inversa(elemento_push))
    return ''.join(C)

def descifrar():
    mensaje = validacion_mensaje()
    p, q = 0, 0
    while not all(map(es_primo, [p, q])) or p == q:
        p = int(input("Elige un número primo: "))
        q = int(input("Elige otro número primo diferente al anterior: "))
    n = p * q
    euler = (p - 1) * (q - 1)
    d = hallar_d(euler)
    M = []
    for caracter in mensaje:
        elemento_push = congruencia_lineal(1, tabla_equivalencia(caracter) ** d, n)
        M.append(tabla_inversa(elemento_push))
    return ''.join(M)

opcion = seleccion_opcion()
if opcion == 1:
    print('El mensaje cifrado es:', cifrar())
elif opcion == 2:
    print('El mensaje descifrado es:', descifrar())
else:
    print('Salida Exitosa')
