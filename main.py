import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random

def validacion_mensaje():
    mensaje = mensaje_entry.get()
    if mensaje.strip() == "":
        messagebox.showwarning("Advertencia", "El mensaje no puede estar vacío. Por favor, inténtelo de nuevo.")
        return None
    elif any(char.isdigit() for char in mensaje):
        messagebox.showwarning("Advertencia", "El mensaje no puede contener números. Por favor, inténtelo de nuevo.")
        return None
    else:
        return mensaje

def calcular_mcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x

def hallar_d(functEuler):
    valores_d = []
    d = 2
    while d < functEuler:
        if calcular_mcd(d, functEuler) == 1:
            valores_d.append(d)
        d += 1
    return random.choice(valores_d)

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
        raise ValueError("Fuera de rango")
    return ord(letra) - ord("A")

def tabla_inversa(numero):
    numero = numero % 26
    if numero < 0 or numero > 25:
        raise ValueError("Fuera de rango")
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

def obtener_primos():
    while True:
        p = simpledialog.askinteger("Input", "Elige un número primo: ")
        q = simpledialog.askinteger("Input", "Elige otro número primo diferente al anterior: ")
        if es_primo(p) and es_primo(q) and p != q:
            return p, q
        else:
            messagebox.showwarning("Advertencia", "Ambos números deben ser primos y diferentes. Inténtelo de nuevo.")

def cifrar_mensaje(mensaje):
    p, q = obtener_primos()
    n = p * q
    euler = (p - 1) * (q - 1)
    d = hallar_d(euler)
    e = congruencia_lineal(d, 1, euler)
    
    # Filtrar caracteres inválidos
    mensaje = ''.join([caracter for caracter in mensaje if 'A' <= caracter.upper() <= 'Z'])
    
    C = [tabla_inversa(pow(tabla_equivalencia(caracter), e, n)) for caracter in mensaje]
    return ''.join(C), p, q, d

def descifrar_mensaje(mensaje, p, q, d):
    n = p * q
    
    # Filtrar caracteres inválidos
    mensaje = ''.join([caracter for caracter in mensaje if 'A' <= caracter.upper() <= 'Z'])
    
    M = [tabla_inversa(pow(tabla_equivalencia(caracter), d, n)) for caracter in mensaje]
    return ''.join(M)

def seleccionar_archivo():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        return filepath
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo")
        return None

def cifrar_archivo():
    filepath = seleccionar_archivo()
    if filepath:
        with open(filepath, 'r') as file:
            contenido = file.read()
        mensaje_cifrado, p, q, d = cifrar_mensaje(contenido)
        with open(filepath + '.enc', 'w') as file:
            file.write(mensaje_cifrado)
        messagebox.showinfo("Éxito", f"Archivo cifrado y guardado como {filepath}.enc\np={p}, q={q}, d={d}")

def descifrar_archivo():
    filepath = seleccionar_archivo()
    if filepath:
        with open(filepath, 'r') as file:
            contenido = file.read()
        p = simpledialog.askinteger("Input", "Ingrese el número primo p: ")
        q = simpledialog.askinteger("Input", "Ingrese el número primo q: ")
        d = simpledialog.askinteger("Input", "Ingrese el valor de d: ")
        mensaje_descifrado = descifrar_mensaje(contenido, p, q, d)
        with open(filepath.replace('.enc', '.dec'), 'w') as file:
            file.write(mensaje_descifrado)
        messagebox.showinfo("Éxito", f"Archivo descifrado y guardado como {filepath.replace('.enc', '.dec')}")

# Interfaz gráfica
root = tk.Tk()
root.title("Cifrado y Descifrado RSA")
root.geometry("500x300")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

mensaje_label = tk.Label(frame, text="Ingrese el mensaje:")
mensaje_label.pack(pady=5)
mensaje_entry = tk.Entry(frame)
mensaje_entry.pack(pady=5)

btn_cifrar_texto = tk.Button(frame, text="Cifrar Texto", command=lambda: cifrar_texto())
btn_cifrar_texto.pack(fill='x', pady=5)

btn_descifrar_texto = tk.Button(frame, text="Descifrar Texto", command=lambda: descifrar_texto())
btn_descifrar_texto.pack(fill='x', pady=5)

btn_cifrar_archivo = tk.Button(frame, text="Cifrar Archivo", command=cifrar_archivo)
btn_cifrar_archivo.pack(fill='x', pady=5)

btn_descifrar_archivo = tk.Button(frame, text="Descifrar Archivo", command=descifrar_archivo)
btn_descifrar_archivo.pack(fill='x', pady=5)

def cifrar_texto():
    mensaje = validacion_mensaje()
    if mensaje:
        resultado, p, q, d = cifrar_mensaje(mensaje)
        messagebox.showinfo("Resultado", f"Mensaje cifrado: {resultado}\np={p}, q={q}, d={d}")

def descifrar_texto():
    mensaje = validacion_mensaje()
    if mensaje:
        p = simpledialog.askinteger("Input", "Ingrese el número primo p: ")
        q = simpledialog.askinteger("Input", "Ingrese el número primo q: ")
        d = simpledialog.askinteger("Input", "Ingrese el valor de d: ")
        resultado = descifrar_mensaje(mensaje, p, q, d)
        messagebox.showinfo("Resultado", f"Mensaje descifrado: {resultado}")
root.mainloop()