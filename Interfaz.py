import tkinter as tk
from PIL import Image, ImageTk
import socket
import threading
import os

# =========================================
# CONEXION TCP
# =========================================

PICO_IP   = "10.128.241.34"
PICO_PORT = 1717

tcp_socket = None
tcp_lock   = threading.Lock()

# =========================================
# PRECIOS
# =========================================

PRECIO_COLONES = 250
TIPO_CAMBIO    = 450

# =========================================
# STOCK ANTERIOR
# =========================================

stock_anterior = [9, 9, 9]

# =========================================
# ARCHIVO DE VENTAS
# =========================================

ARCHIVO_VENTAS = "ventas.txt"

def iniciar_archivo():
    if not os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, "w") as f:
            pass

def registrar_venta(producto):
    with open(ARCHIVO_VENTAS, "a") as f:
        f.write(str(producto) + "\n")

def leer_ventas():
    ventas = []
    if not os.path.exists(ARCHIVO_VENTAS):
        return ventas
    with open(ARCHIVO_VENTAS, "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea in ["1", "2", "3"]:
                ventas.append(linea)
    return ventas

def detectar_ventas(stock_nuevo):
    global stock_anterior
    for i in range(3):
        if stock_nuevo[i] < stock_anterior[i]:
            veces = stock_anterior[i] - stock_nuevo[i]
            for _ in range(veces):
                registrar_venta(i + 1)
    stock_anterior = stock_nuevo[:]

# =========================================
# CONEXION
# =========================================

def conectar():
    global tcp_socket
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.settimeout(3)
        tcp_socket.connect((PICO_IP, PICO_PORT))
        print("Conectado al Pico")
    except Exception as e:
        print("Error conexion:", e)
        tcp_socket = None

def obtener_stock():
    global tcp_socket
    with tcp_lock:
        try:
            if tcp_socket is None:
                conectar()
            tcp_socket.send("STOCK\n".encode())
            respuesta = tcp_socket.recv(1024).decode().strip()
            partes = respuesta.split(",")
            return [int(partes[0]), int(partes[1]), int(partes[2])]
        except:
            tcp_socket = None
            return [9, 9, 9]

def enviar_comando(comando):
    global tcp_socket
    with tcp_lock:
        try:
            if tcp_socket is None:
                conectar()
            tcp_socket.send((comando + "\n").encode())
        except:
            tcp_socket = None

# =========================================
# FUNCION LIMPIAR
# =========================================

def limpiar():

    for widget in ventana.winfo_children():
        widget.destroy()

# =========================================
# VOLVER MENU
# =========================================

def volver_menu():

    limpiar()
    menu_principal()

# =========================================
# VENTANA STOCK
# =========================================

def ventana_stock():

    limpiar()

    activo = [True]

    # =========================================
    # FONDO
    # =========================================

    fondo_label = tk.Label(ventana,image=fondo)

    fondo_label.place(x=0, y=0, relwidth=1,relheight=1)

    # =========================================
    # TITULO STOCK
    # =========================================

    titulo_stock = tk.Label(ventana, image=stock_titulo_img, bd=0, bg="#ea7fb3"
    )

    titulo_stock.pack(pady=(20, 40))

    # =========================================
    # FRAME PRODUCTOS
    # =========================================

    frame_productos = tk.Frame(ventana,bg="#ea7fb3")

    frame_productos.pack(pady=20 )

    # =========================================
    # CHICLES
    # =========================================

    label_chicles = tk.Label(frame_productos,image=chicles_img,bd=0,bg="#ea7fb3")

    label_chicles.grid(row=0,column=0,padx=38)

    # =========================================
    # CHOCOLATES
    # =========================================

    label_chocolates = tk.Label( frame_productos, image=chocolates_img, bd=0, bg="#ea7fb3" )

    label_chocolates.grid(row=0, column=1,padx=38  )

    # =========================================
    # CARAMELOS
    # =========================================

    label_caramelos = tk.Label(frame_productos,image=caramelos_img,bd=0,bg="#ea7fb3" )

    label_caramelos.grid( row=0, column=2, padx=38 )

    # =========================================
    # LABELS STOCK
    # =========================================

    label_stock_chicles = tk.Label( frame_productos, text="Stock: ...", bg="#ea7fb3", font=("Arial", 14, "bold") )

    label_stock_chicles.grid(   row=1,   column=0)

    label_stock_chocolates = tk.Label(frame_productos, text="Stock: ...",bg="#ea7fb3",font=("Arial", 14, "bold"))

    label_stock_chocolates.grid(row=1,column=1)

    label_stock_caramelos = tk.Label(frame_productos,text="Stock: ...",bg="#ea7fb3",font=("Arial", 14, "bold"))

    label_stock_caramelos.grid(row=1,column=2)

    # =========================================
    # ACTUALIZACION STOCK
    # =========================================

    def actualizar_stock():

        if not activo[0]:
            return

        def pedir():
            s = obtener_stock()
            detectar_ventas(s)
            if activo[0]:
                label_stock_chicles.config(text="Stock: " + str(s[0]))
                label_stock_chocolates.config(text="Stock: " + str(s[1]))
                label_stock_caramelos.config(text="Stock: " + str(s[2]))
            if activo[0]:
                ventana.after(2000, actualizar_stock)

        threading.Thread(target=pedir, daemon=True).start()

    def detener():
        activo[0] = False
        volver_menu()

    actualizar_stock()

    # =========================================
    # BOTON MENU
    # =========================================

    boton_menu = tk.Button(ventana,image=boton_menu_img,bd=0,highlightthickness=0,bg="#ea7fb3",activebackground="#ea7fb3",command=detener)

    boton_menu.pack(side="bottom", pady=95)

# =========================================
# VENTANA VENTAS
# =========================================

def ventana_ventas():

    limpiar()

    # =========================================
    # FONDO
    # =========================================

    fondo_label = tk.Label(ventana,image=fondo)

    fondo_label.place( x=0, y=0, relwidth=1, relheight=1)

    # =========================================
    # TITULO VENTAS
    # =========================================

    titulo_ventas = tk.Label(ventana,image=ventas_titulo_img,bd=0,bg="#ea7fb3")

    titulo_ventas.pack(pady=(25, 30))

    # =========================================
    # CALCULAR DATOS
    # =========================================

    ventas = leer_ventas()

    chicles    = 0
    chocolates = 0
    caramelos  = 0

    for v in ventas:
        if v == "1":
            chicles += 1
        elif v == "2":
            chocolates += 1
        elif v == "3":
            caramelos += 1

    total       = chicles + chocolates + caramelos
    ganancias_c = total * PRECIO_COLONES
    ganancias_d = round(ganancias_c / TIPO_CAMBIO, 2)

    # =========================================
    # FRAME DATOS
    # =========================================

    frame_datos = tk.Frame(ventana,bg="#ea7fb3")

    frame_datos.pack(pady=10)

    # =========================================
    # VENTAS POR PRODUCTO
    # =========================================

    tk.Label(frame_datos,text="Ventas por producto",bg="#ea7fb3",font=("Arial", 15, "bold") ).grid(row=0, column=0,columnspan=2, pady=(0, 10))

    tk.Label(frame_datos,text="Chicles:",bg="#ea7fb3",font=("Arial", 13)).grid(row=1,column=0, sticky="w", padx=20)

    tk.Label(frame_datos,text=str(chicles),bg="#ea7fb3",font=("Arial", 13, "bold")).grid(row=1,column=1,sticky="w")

    tk.Label(frame_datos,text="Chocolates:",bg="#ea7fb3",font=("Arial", 13)).grid(row=2,column=0,sticky="w",padx=20)

    tk.Label(frame_datos,text=str(chocolates),bg="#ea7fb3",font=("Arial", 13, "bold")).grid(row=2,column=1,sticky="w")

    tk.Label(frame_datos,text="Caramelos:",bg="#ea7fb3",font=("Arial", 13)).grid(row=3,column=0,sticky="w",padx=20)

    tk.Label(frame_datos,text=str(caramelos),bg="#ea7fb3",font=("Arial", 13, "bold")).grid(row=3,column=1,sticky="w" )

    tk.Label(frame_datos,text="Total ventas:",bg="#ea7fb3",font=("Arial", 13)).grid(row=4, column=0, sticky="w", padx=20,pady=(10, 0))

    tk.Label(frame_datos,text=str(total),bg="#ea7fb3",font=("Arial", 13, "bold")).grid(row=4,column=1,sticky="w",pady=(10, 0))

    # =========================================
    # GANANCIAS
    # =========================================

    tk.Label(frame_datos,text="Ganancias",bg="#ea7fb3",font=("Arial", 15, "bold")).grid( row=5, column=0, columnspan=2, pady=(20, 10))

    tk.Label( frame_datos, text="En colones:", bg="#ea7fb3", font=("Arial", 13)).grid(row=6,column=0,sticky="w",padx=20)

    tk.Label(frame_datos, text="₡" + str(ganancias_c), bg="#ea7fb3",font=("Arial", 13, "bold") ).grid(row=6,column=1,sticky="w")

    tk.Label(frame_datos,text="En dolares:",bg="#ea7fb3",font=("Arial", 13)).grid( row=7, column=0, sticky="w", padx=20)

    tk.Label(frame_datos,text="$" + str(ganancias_d),bg="#ea7fb3",font=("Arial", 13, "bold")).grid(row=7,column=1,sticky="w" )

    # =========================================
    # BOTON MENU
    # =========================================

    boton_menu = tk.Button(ventana,image=boton_menu_img,bd=0,highlightthickness=0,bg="#ea7fb3",activebackground="#ea7fb3",command=volver_menu)

    boton_menu.pack(side="bottom",pady=95)

# =========================================
# VENTANA MANTENIMIENTO
# =========================================

def ventana_mantenimiento():

    limpiar()

    mantenimiento_activo = [False]

    # =========================================
    # FONDO
    # =========================================

    fondo_label = tk.Label(ventana,image=fondo)

    fondo_label.place(x=0,y=0,relwidth=1,relheight=1 )

    # =========================================
    # TITULO MANTENIMIENTO
    # =========================================

    titulo_mantenimiento = tk.Label(ventana,image=mantenimiento_titulo_img,bd=0,bg="#ea7fb3" )

    titulo_mantenimiento.pack(pady=(25, 30))

    # =========================================
    # BOTON MANTENIMIENTO
    # =========================================

    label_estado = tk.Label(ventana,text="Modo mantenimiento: INACTIVO",bg="#ea7fb3",font=("Arial", 13) )

    label_estado.pack( pady=20 )

    def toggle_mantenimiento():

        if not mantenimiento_activo[0]:

            enviar_comando("MANTENIMIENTO_ON")
            mantenimiento_activo[0] = True
            label_estado.config(text="Modo mantenimiento: ACTIVO")
            boton_toggle.config(text="Desactivar mantenimiento",bg="#888888" )

        else:

            enviar_comando("MANTENIMIENTO_OFF")
            mantenimiento_activo[0] = False
            label_estado.config(text="Modo mantenimiento: INACTIVO")
            boton_toggle.config(text="Activar mantenimiento",bg="#d4599a")

    boton_toggle = tk.Button(ventana,text="Activar mantenimiento",font=("Arial", 13),bg="#d4599a",fg="white",bd=0,padx=20,pady=10,command=toggle_mantenimiento)

    boton_toggle.pack(pady=10)

    # =========================================
    # BOTON MENU
    # =========================================

    boton_menu = tk.Button(ventana,image=boton_menu_img,bd=0,highlightthickness=0,bg="#ea7fb3",activebackground="#ea7fb3",command=volver_menu)

    boton_menu.pack(side="bottom",pady=95)

# =========================================
# MENU PRINCIPAL
# =========================================

def menu_principal():

    fondo_label = tk.Label(ventana,image=fondo)

    fondo_label.place(x=0,y=0,relwidth=1,relheight=1)

    label_titulo = tk.Label(ventana,image=titulo,bd=0,bg="#ea7fb3")

    label_titulo.pack(
        pady=(30, 30))

    boton_stock = tk.Button( ventana, image=boton_stock_img, bd=0, highlightthickness=0, bg="#ea7fb3", activebackground="#ea7fb3", command=ventana_stock )

    boton_stock.pack(pady=15)

    boton_ventas = tk.Button(ventana,image=boton_ventas_img,bd=0,highlightthickness=0,bg="#ea7fb3",activebackground="#ea7fb3",command=ventana_ventas)

    boton_ventas.pack(pady=15)

    boton_mantenimiento = tk.Button(ventana,image=boton_mantenimiento_img,bd=0,highlightthickness=0,bg="#ea7fb3",activebackground="#ea7fb3",command=ventana_mantenimiento)

    boton_mantenimiento.pack(  pady=15)

# =========================================
# VENTANA PRINCIPAL
# =========================================

ventana = tk.Tk()

ventana.title("Dispensador Gallito")

ancho = ventana.winfo_screenwidth()
alto  = ventana.winfo_screenheight()

ventana.geometry(f"{ancho}x{alto}")

# =========================================
# CARGAR IMAGENES
# =========================================

imagen_fondo = Image.open("fondo1.png")
imagen_fondo = imagen_fondo.resize((ancho, alto))

fondo = ImageTk.PhotoImage(imagen_fondo)

imagen_titulo = Image.open("titulo.png")
imagen_titulo = imagen_titulo.resize((700, 180))

titulo = ImageTk.PhotoImage(imagen_titulo)

imagen_stock = Image.open("boton_stock.png")
imagen_stock = imagen_stock.resize((350, 100))

boton_stock_img = ImageTk.PhotoImage(imagen_stock)

imagen_ventas = Image.open("boton_ventas.png")
imagen_ventas = imagen_ventas.resize((350, 100))

boton_ventas_img = ImageTk.PhotoImage(imagen_ventas)

imagen_mantenimiento = Image.open("boton_mantenimiento.png")
imagen_mantenimiento = imagen_mantenimiento.resize((350, 100))

boton_mantenimiento_img = ImageTk.PhotoImage(imagen_mantenimiento)

imagen_menu = Image.open("boton_menu.png")
imagen_menu = imagen_menu.resize((210, 75))

boton_menu_img = ImageTk.PhotoImage(imagen_menu)

imagen_stock_titulo = Image.open("stock.png")
imagen_stock_titulo = imagen_stock_titulo.resize((520, 190))

stock_titulo_img = ImageTk.PhotoImage(imagen_stock_titulo)

imagen_ventas_titulo = Image.open("ventas.png")
imagen_ventas_titulo = imagen_ventas_titulo.resize((520, 150))

ventas_titulo_img = ImageTk.PhotoImage(imagen_ventas_titulo)

imagen_mantenimiento_titulo = Image.open("mantenimiento.png")
imagen_mantenimiento_titulo = imagen_mantenimiento_titulo.resize((620, 150))

mantenimiento_titulo_img = ImageTk.PhotoImage(imagen_mantenimiento_titulo)

imagen_chicles = Image.open("chicles.png")
imagen_chicles = imagen_chicles.resize((260, 220))

chicles_img = ImageTk.PhotoImage(imagen_chicles)

imagen_chocolates = Image.open("chocolates.png")
imagen_chocolates = imagen_chocolates.resize((260, 220))

chocolates_img = ImageTk.PhotoImage(imagen_chocolates)

imagen_caramelos = Image.open("caramelos.png")
imagen_caramelos = imagen_caramelos.resize((260, 220))

caramelos_img = ImageTk.PhotoImage(imagen_caramelos)

# =========================================
# INICIAR
# =========================================

iniciar_archivo()
conectar()
menu_principal()

# =========================================
# LOOP PRINCIPAL
# =========================================

ventana.mainloop()

