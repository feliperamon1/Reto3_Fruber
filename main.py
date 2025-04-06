import tkinter as tk
from tkinter import ttk, messagebox
from productos import productos
from operaciones import agregar_al_carrito, calcular_total, registrar_venta, historial_ventas, venta_por_producto, venta_por_cliente
from excepciones import *
import matplotlib.pyplot as plt

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
    total = calcular_total(carrito)
    total_label.config(text=f"Total: ${total:.0f}")

def actualizar_carrito():
    carrito_listbox.delete(0, tk.END)
    for item in carrito:
        carrito_listbox.insert(tk.END, f"{item['nombre']} x{item['cantidad']} = ${item['cantidad'] * item['precio']:.0f}")

def agregar_producto():
    seleccion = lista_productos.curselection()
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar un producto")
        return
    nombre = list(productos.keys())[seleccion[0]]
    cantidad = cantidad_entry.get()
    try:
        agregar_al_carrito(nombre, cantidad, carrito)
        actualizar_total()
        actualizar_lista_productos()
        actualizar_carrito()
        cantidad_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def actualizar_lista_productos():
    lista_productos.delete(0, tk.END)
    for prod in productos:
        lista_productos.insert(tk.END, f"{prod} - ${productos[prod]['precio']} - Stock: {productos[prod]['stock']}")

def finalizar_compra():
    if not carrito:
        messagebox.showinfo("Información", "El carrito está vacío")
        return
    nombre = nombre_entry.get().strip()
    cedula = cedula_entry.get().strip()
    if not nombre or not cedula:
        messagebox.showerror("Error", "Debe ingresar los datos del cliente")
        return
    cliente = {"nombre": nombre, "cedula": cedula}
    factura_id, venta, subtotal, iva, total, fecha, resumen = registrar_venta(carrito, cliente)
    messagebox.showinfo("Compra finalizada", resumen)
    carrito.clear()
    actualizar_total()
    actualizar_lista_productos()
    actualizar_carrito()
    nombre_entry.delete(0, tk.END)
    cedula_entry.delete(0, tk.END)
    cantidad_entry.delete(0, tk.END)

def mostrar_historial():
    hist_win = tk.Toplevel(root)
    hist_win.title("Historial de Ventas")
    hist_win.geometry("800x400")
    tree = ttk.Treeview(hist_win, columns=("Factura", "Cliente", "Total", "Fecha", "Detalle"), show='headings')
    tree.heading("Factura", text="Factura ID")
    tree.heading("Cliente", text="Cliente")
    tree.heading("Total", text="Total")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Detalle", text="Detalle")
    tree.pack(fill="both", expand=True)
    for venta in historial_ventas:
        cliente = f"{venta['cliente']['nombre']} ({venta['cliente']['cedula']})"
        detalle = ", ".join([f"{x['nombre']} x{x['cantidad']}" for x in venta["venta"]])
        tree.insert('', tk.END, values=(venta["id"], cliente, f"${venta['total']:.0f}", venta['fecha'], detalle))

def mostrar_estadisticas():
    if not venta_por_producto:
        messagebox.showinfo("Sin datos", "Aún no hay ventas registradas")
        return
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.bar(venta_por_producto.keys(), venta_por_producto.values())
    ax1.set_title("Productos más vendidos")
    ax1.set_ylabel("Cantidad")
    clientes = list(venta_por_cliente.keys())
    cantidades = [venta_por_cliente[c]["cantidad"] for c in clientes]
    valores = [venta_por_cliente[c]["valor"] for c in clientes]
    ax2.bar(clientes, valores)
    ax2.set_title("Ventas por cliente ($COP)")
    ax2.set_ylabel("Valor")
    plt.tight_layout()
    plt.show()
    
btn_agregar = ttk.Button(frame, text="Agregar al carrito", command=agregar_producto)
btn_agregar.grid(row=5, column=0, pady=5)
btn_finalizar = ttk.Button(frame, text="Finalizar Compra", command=finalizar_compra)
btn_finalizar.grid(row=5, column=1, pady=5)
btn_historial = ttk.Button(frame, text="Ver Historial de Ventas", command=mostrar_historial)
btn_historial.grid(row=6, column=0, columnspan=2)
btn_estadisticas = ttk.Button(frame, text="Estadísticas", command=mostrar_estadisticas)
btn_estadisticas.grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()