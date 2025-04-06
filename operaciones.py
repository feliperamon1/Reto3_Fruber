from productos import productos
from excepciones import ProductoNoDisponibleError, CantidadInvalidaError, SinCantidadError
import uuid
from datetime import datetime
import os
import webbrowser
from fpdf import FPDF

# Variables globales visibles para main.py
historial_ventas = []
venta_por_producto = {}
venta_por_cliente = {}

CLIENTES = []  # Lista temporal de clientes

FACTURAS_DIR = "facturas"
os.makedirs(FACTURAS_DIR, exist_ok=True)

IVA_TASA = 0.19

def agregar_al_carrito(nombre, cantidad, carrito):
    if not cantidad:
        raise SinCantidadError("Debe ingresar una cantidad")
    try:
        cantidad = int(cantidad)
    except ValueError:
        raise CantidadInvalidaError("La cantidad debe ser un número entero")
    if cantidad <= 0:
        raise CantidadInvalidaError("La cantidad debe ser mayor que cero")
    if productos[nombre]["stock"] < cantidad:
        raise ProductoNoDisponibleError("Stock insuficiente")

    carrito.append({"nombre": nombre, "cantidad": cantidad, "precio": productos[nombre]["precio"]})
    productos[nombre]["stock"] -= cantidad

def calcular_total(carrito):
    return sum(item["cantidad"] * item["precio"] for item in carrito)

def registrar_venta(carrito, cliente):
    venta = []
    subtotal = 0
    for item in carrito:
        total_item = item["cantidad"] * item["precio"]
        venta.append({"nombre": item["nombre"], "cantidad": item["cantidad"], "total": total_item})
        subtotal += total_item
        venta_por_producto[item["nombre"]] = venta_por_producto.get(item["nombre"], 0) + item["cantidad"]

    iva = subtotal * IVA_TASA
    total = subtotal + iva
    factura_id = str(uuid.uuid4())[:8]
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    historial_ventas.append({
        "venta": venta,
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "cliente": cliente,
        "id": factura_id,
        "fecha": fecha
    })

    if cliente["nombre"] not in venta_por_cliente:
        venta_por_cliente[cliente["nombre"]] = {"cantidad": 0, "valor": 0}
    venta_por_cliente[cliente["nombre"]]["cantidad"] += sum(i["cantidad"] for i in venta)
    venta_por_cliente[cliente["nombre"]]["valor"] += total

    pdf_path = generar_pdf_factura(factura_id, cliente, venta, subtotal, iva, total, fecha)
    webbrowser.open_new(pdf_path)

    resumen = f"Factura ID: {factura_id}\nCliente: {cliente['nombre']} - {cliente['cedula']}\nFecha: {fecha}\n\n"
    for item in venta:
        resumen += f"{item['nombre']} x{item['cantidad']} = ${item['total']:.0f}\n"
    resumen += (
        f"\nSubtotal: ${subtotal:.0f}\n"
        f"IVA (19%): ${iva:.0f}\n"
        f"Total: ${total:.0f}\n\n"
        "Factura guardada como PDF."
    )

    return factura_id, venta, subtotal, iva, total, fecha, resumen

def generar_pdf_factura(factura_id, cliente, venta, subtotal, iva, total, fecha):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_fill_color(230, 230, 250)
    pdf.cell(200, 10, txt="Fruber - Factura de Venta", ln=1, align="C", fill=True)
    pdf.cell(200, 10, txt=f"Factura ID: {factura_id}", ln=2)
    pdf.cell(200, 10, txt=f"Cliente: {cliente['nombre']} - {cliente['cedula']}", ln=3)
    pdf.cell(200, 10, txt=f"Fecha: {fecha}", ln=4)
    pdf.ln(10)

    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, txt="Producto", border=1, fill=True)
    pdf.cell(40, 10, txt="Cantidad", border=1, fill=True)
    pdf.cell(40, 10, txt="Total", border=1, fill=True)
    pdf.ln()
    for item in venta:
        pdf.cell(60, 10, txt=item['nombre'], border=1)
        pdf.cell(40, 10, txt=str(item['cantidad']), border=1)
        pdf.cell(40, 10, txt=f"${item['total']:.0f}", border=1)
        pdf.ln()
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Subtotal: ${subtotal:.0f}", ln=1)
    pdf.cell(200, 10, txt=f"IVA (19%): ${iva:.0f}", ln=1)
    pdf.cell(200, 10, txt=f"Total a pagar: ${total:.0f}", ln=1)
    pdf_path = os.path.abspath(f"{FACTURAS_DIR}/Factura_{factura_id}.pdf")
    pdf.output(pdf_path)
    return pdf_path
