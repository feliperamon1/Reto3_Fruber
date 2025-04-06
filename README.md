# Sistema de Facturación FRUBER 🍎🍌

Este es un sistema de facturación interactivo para una tienda tipo frutería, desarrollado en Python usando `Tkinter`. El sistema simula el flujo completo de ventas, generación de facturas y análisis estadístico.

---

## 🧰 Características Principales

- Interfaz gráfica amigable con **Tkinter**
- Selección de productos, cantidades y control de **stock**
- Registro de clientes con nombre y cédula/NIT
- Generación de **factura en PDF** con desglose de Subtotal, IVA (19%) y Total
- Visualización del **carrito de compras en tiempo real**
- Historial de ventas con detalle de productos vendidos
- Panel de **estadísticas**:
  - Productos más vendidos
  - Clientes con mayor volumen y valor de compra
- Valores en **pesos colombianos (COP)** 💵
- Interfaz personalizada con colores y branding de **TIENDA FRUBER**

---

## 📦 Estructura del Proyecto

```bash
Reto3_Fruber/
├── main.py               # Interfaz gráfica y lógica de interacción
├── productos.py          # Catálogo de productos y precios
├── excepciones.py        # Manejo de errores personalizados
├── operaciones.py        # Lógica de facturación, generación de PDF y estadísticas
├── facturas/             # Carpeta generada automáticamente con los PDFs
```

---

## 🚀 Requisitos

Asegúrate de tener Python 3 instalado.

Instala las dependencias necesarias:

```bash
pip install fpdf matplotlib
```

---

## ▶️ Ejecutar el programa

```bash
python main.py
```

---

## 📄 Licencia

Este proyecto se desarrolló con fines académicos. ¡Puedes usarlo, modificarlo y mejorarlo!

---

**Desarrollado con ❤️ para Fruber por Felipe Parada y Edinson Hernandez.**