import tkinter as tk
from tkinter import ttk
from pytube import YouTube
import os
import threading

# Función para limpiar el nombre del archivo
def limpiar_nombre(nombre):
    caracteres_invalidos = '\\/:*?"<>|'
    for caracter in caracteres_invalidos:
        nombre = nombre.replace(caracter, '_')
    return nombre

# Función para descargar el video o audio
def descargar():
    url = entrada.get()
    try:
        video = YouTube(url)
        
        if seleccion.get() == 1:  # Si la opción seleccionada es descargar video
            stream = video.streams.get_highest_resolution()  # Descargar video con la mejor calidad disponible en formato mp4
            extension = "mp4"
        else:  # Si la opción seleccionada es descargar audio
            stream = video.streams.filter(only_audio=True).first()  # Descargar audio con la mejor calidad disponible en formato mp3
            extension = "mp3"  # Cambiar a formato wav
        
        # Obtener la carpeta de descargas por defecto
        carpeta_descargas = os.path.expanduser('~\Downloads')
        
        # Limpiar el nombre del archivo
        nombre_archivo = limpiar_nombre(video.title)
        
        # Agregar la extensión correspondiente según la elección
        nombre_archivo += f".{extension}"
        
        # Función para descargar el video o audio en un hilo separado
        def descargar_video():
            stream.download(output_path=carpeta_descargas, filename=nombre_archivo)
            estado.config(text="Descarga completada en la carpeta de Descargas.")
            barra_progreso.stop()  # Detener la barra de progreso al finalizar la descarga
        
        # Iniciar la descarga en un hilo separado para no bloquear la interfaz
        descarga_thread = threading.Thread(target=descargar_video)
        descarga_thread.start()
        barra_progreso.start()  # Iniciar la barra de progreso al iniciar la descarga
        
    except Exception as e:
        estado.config(text="Ocurrió un error al descargar el archivo.")

# Función para abrir la carpeta de descargas
def abrir_descargas():
    carpeta_descargas = os.path.expanduser('~\Downloads')
    os.startfile(carpeta_descargas)

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("download music")
ventana.geometry("400x300")  # Tamaño de la ventana
ventana.configure(bg='#F0F0F0')  # Fondo de la ventana

# Etiqueta y entrada para la URL
etiqueta = ttk.Label(ventana, text="Ingresa la URL del video de YouTube:", background='#F0F0F0', font=('Arial', 12))
etiqueta.pack()

entrada = ttk.Entry(ventana, width=50, font=('Arial', 10))
entrada.pack()

# Funciones para habilitar copiar, cortar y pegar en la entrada de texto
def copiar():
    ventana.clipboard_clear()
    ventana.clipboard_append(entrada.get())

def cortar():
    copiar()
    entrada.delete("sel.first", "sel.last")

def pegar():
    entrada.insert(tk.INSERT, ventana.clipboard_get())

# Configuración del menú contextual para la entrada de texto
menu_contextual = tk.Menu(ventana, tearoff=0)
menu_contextual.add_command(label="Copiar", command=copiar)
menu_contextual.add_command(label="Cortar", command=cortar)
menu_contextual.add_command(label="Pegar", command=pegar)

def mostrar_menu(event):
    menu_contextual.post(event.x_root, event.y_root)

# Enlazar el menú contextual con el evento del botón derecho del mouse
entrada.bind("<Button-3>", mostrar_menu)

# Contenedor para organizar los botones en una fila
contenedor_botones = ttk.Frame(ventana)
contenedor_botones.pack()

# Botones de selección para elegir descargar video o audio - ahora alineados horizontalmente
seleccion = tk.IntVar()
seleccion.set(1)  # Establecer el valor predeterminado para descargar video

boton_video = ttk.Radiobutton(contenedor_botones, text="Video", variable=seleccion, value=1, style='TRadiobutton')
boton_video.pack(side='left', padx=5)  # Alineados a la izquierda con un pequeño espaciado

boton_audio = ttk.Radiobutton(contenedor_botones, text="Audio (mp3)", variable=seleccion, value=2, style='TRadiobutton')
boton_audio.pack(side='left', padx=5)  # Alineados a la izquierda con un pequeño espaciado

# Barra de progreso
style = ttk.Style()
style.configure('TProgressbar', thickness=5, borderwidth=5, relief='flat', troughcolor='#1f67db', background='##1f67db')
barra_progreso = ttk.Progressbar(ventana, mode='indeterminate', length=200, style='TProgressbar')
barra_progreso.pack()

# Botón de descarga
boton_descargar = ttk.Button(ventana, text="Descargar", command=descargar, style='TButton')
boton_descargar.pack(pady=10)

# Estado de la descarga
estado = ttk.Label(ventana, text="", background='#F0F0F0', font=('Arial', 10))
estado.pack()

# Botón para abrir carpeta de descargas
boton_ver_descargas = ttk.Button(ventana, text="Ver Descargas", command=abrir_descargas, style='TButton')
boton_ver_descargas.pack(pady=5)

# Ejecución de la interfaz gráfica
ventana.mainloop()
