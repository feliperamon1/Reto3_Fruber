import tkinter as tk
from tkinter import ttk, messagebox
from productos import productos

carrito = []

root = tk.Tk()
root.title("FRUBER - Caja Registradora")
root.geometry("600x500")
root.configure(bg="#eafaf1")

# Título
titulo = ttk.Label(root, text="TIENDA FRUBER", font=("Helvetica", 20, "bold"), background="#eafaf1", foreground="#2d6a4f")
titulo.pack(pady=10)

frame = ttk.Frame(root, padding=10)
frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Datos del cliente
ttk.Label(frame, text="Nombre Cliente:").grid(row=0, column=0)
nombre_entry = ttk.Entry(frame)
nombre_entry.grid(row=0, column=1)

ttk.Label(frame, text="Cédula / NIT:").grid(row=1, column=0)
cedula_entry = ttk.Entry(frame)
cedula_entry.grid(row=1, column=1)

lista_productos = tk.Listbox(frame, height=10, width=50)
for prod in productos:
    lista_productos.insert(tk.END, f"{prod} - ${productos[prod]['precio']} - Stock: {productos[prod]['stock']}")
lista_productos.grid(row=2, column=0, columnspan=2, pady=5)

cantidad_label = ttk.Label(frame, text="Cantidad:")
cantidad_label.grid(row=3, column=0)
cantidad_entry = ttk.Entry(frame)
cantidad_entry.grid(row=3, column=1)

total_label = ttk.Label(frame, text="Total: $0")
total_label.grid(row=4, column=0, columnspan=2)

# Carrito a la derecha
carrito_frame = ttk.Frame(root, padding=10)
carrito_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

ttk.Label(carrito_frame, text="Carrito de Compras:", font=("Helvetica", 12, "bold")).pack()
carrito_listbox = tk.Listbox(carrito_frame, height=20, width=40)
carrito_listbox.pack(pady=5)

def actualizar_total():
    pass

def actualizar_carrito():
    pass

def agregar_producto():
    pass

def actualizar_lista_productos():
    pass

def finalizar_compra():
    pass

def mostrar_historial():
    pass

def mostrar_estadisticas():
    pass

btn_agregar = ttk.Button(frame, text="Agregar al carrito", command=agregar_producto)
btn_agregar.grid(row=5, column=0, pady=5)
btn_finalizar = ttk.Button(frame, text="Finalizar Compra", command=finalizar_compra)
btn_finalizar.grid(row=5, column=1, pady=5)
btn_historial = ttk.Button(frame, text="Ver Historial de Ventas", command=mostrar_historial)
btn_historial.grid(row=6, column=0, columnspan=2)
btn_estadisticas = ttk.Button(frame, text="Estadísticas", command=mostrar_estadisticas)
btn_estadisticas.grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()