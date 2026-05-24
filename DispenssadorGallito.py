import tkinter as tk

# =========================================
# VENTANA PRINCIPAL
# =========================================

ventana = tk.Tk()

ventana.title("Dispensador Gallito")

# tamaño pantalla completa
ancho = ventana.winfo_screenwidth()
alto = ventana.winfo_screenheight()

ventana.geometry(f"{ancho}x{alto}")

# color fondo
ventana.configure(bg="white")

# =========================================
# TITULO
# =========================================

titulo = tk.Label(
    ventana,
    text="Dispensador Gallito",
    font=("Arial", 30, "bold"),
    bg="white"
)

titulo.pack(pady=50)

# =========================================
# BOTON STOCK
# =========================================

boton_stock = tk.Button(
    ventana,
    text="Stock",
    font=("Arial", 20),
    width=20,
    height=2
)

boton_stock.pack(pady=20)

# =========================================
# BOTON VENTAS
# =========================================

boton_ventas = tk.Button(
    ventana,
    text="Ventas",
    font=("Arial", 20),
    width=20,
    height=2
)

boton_ventas.pack(pady=20)

# =========================================
# BOTON MANTENIMIENTO
# =========================================

boton_mantenimiento = tk.Button(
    ventana,
    text="Modo Mantenimiento",
    font=("Arial", 20),
    width=20,
    height=2
)

boton_mantenimiento.pack(pady=20)

# =========================================
# LOOP PRINCIPAL
# =========================================

ventana.mainloop()
