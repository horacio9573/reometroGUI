import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import os
import sys
import csv
import shutil
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from tkinter import filedialog
#_*_ coding: utf-8 _*_

# defino tokens como un diccionario Clave:Valor y otras yerbas
Token={"Car70":"EC7000","Des70":"ED7000","Din7005":"EO7005","Din7010":"EO7010","Din7015":"EO7015",
       "Car35":"EC3500","Des35":"ED3500","Din3505":"EO3505","Din3510":"EO3510","Din3515":"EO3515",
       "Car17":"EC1700","Des17":"ED1700","Din1705":"EO1705","Din1710":"EO1710","Din1715":"EO1715",
       "Parar":"M00000","Hom70":"M07000","Hom35":"M03500","Hom17":"M01700"
}

#metodos globales
# defino vectores de almacenamiento
X=[]
Y=[]
T=[]

def Tomar_datos():
   """
   Carga los datos de tiempo (T), Eje R (Y) y Eje T (X) desde el archivo
   'input.csv'.

   El archivo CSV debe tener un delimitador ';'. Los datos se filtran para
   considerar solo registros donde el valor de A_1 (registro[2]) sea mayor a 1,
   y los valores numéricos se convierten, reemplazando la coma por un punto.

   Returns:
       int: 0 si la lectura fue exitosa, 1 si hubo un error al abrir el archivo.
   """
   # si las listas no están vacias las limpia
   if len(T)!=0:
       X.clear()
       Y.clear()
       T.clear()
   try:
       archivo=open("input.csv","r")
   except:
       print("Error al abrir  temporario")
       return 1
   try:
       i=0
       lector=csv.reader(archivo,delimiter=';')
       for registro in lector:
           if i>3:
               aux=float(registro[0].replace(",", "."))
               A_1=float(registro[2].replace(",", "."))
               A_3=float(registro[3].replace(",", "."))
               if A_1 >1:
                   Y.append(A_1)
                   X.append(A_3)
                   T.append(aux)
           i+=1
   finally:
       archivo.close()
   return 0
#
# método para graficar datos sin plotear los guarda en "input.png"
def Dibujar():
   """
   Genera y guarda un gráfico de dos subplots a partir de los datos almacenados
   en las listas T (Tiempo), Y (Eje R) y X (Eje T).

   El gráfico se guarda como "input.png". Utiliza matplotlib para crear
   dos gráficos de línea: Eje R vs. Tiempo y Eje T vs. Tiempo.

   Returns:
       int: 0 (siempre retorna 0, indicando que la operación terminó).
   """
   fig, axes = plt.subplots(nrows=2, ncols=1)
   ax0, ax1 = axes.flat
   plt.ion()
   #
   ax0.plot(T, Y)
   ax0.set_title('Eje R ')
   ax0.spines['right'].set_visible(False)
   ax0.spines['top'].set_visible(False)
   #
   ax1.plot(T, X)
   ax1.set_title('Eje T ')
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   # Evita el solapamiento
   plt.subplots_adjust(hspace=0.5)
   plt.ioff()
   plt.savefig("input.png")
   plt.close()
   return 0

#defino la clase interface
class GUI:
   """
   Clase principal para la Interfaz Gráfica de Usuario (GUI) del Reómetro Eritrocitário.

   Gestiona la configuración de la ventana principal, los widgets (botones,
   radiobuttons, pantalla de estado) y la lógica de control para los ensayos
   del reómetro (Carga, Descarga, Dinámico, Homogeneizar).
   """
   def __init__(self, raiz):
       """
       Inicializa la GUI y configura la ventana principal.

       Args:
           raiz (tk.Tk): La instancia raíz de Tkinter.
       """
       #variables de la clase
       self.master=raiz
       self.mensajePantalla=tk.StringVar()
       self.mensajePantalla.set("Estado por defecto desconectado, Fr=0,5 Hz, RPM=70")
       self.puerto=tk.IntVar()
       self.puerto.set(0)
       self.Fr=tk.StringVar()
       self.Fr.set("05")
       self.Rpm_v=tk.StringVar()
       self.Rpm_v.set("70")
       self.Motor=tk.IntVar()
       self.Motor.set(0)
       # Se define el título y la geometría de la ventana...
       raiz.title("Reómetro Eritrocitário GUI")
       # ... [código de configuración de geometría, color y estilo] ...
       width=800
       height=600
       screenwidth = raiz.winfo_screenwidth()
       screenheight = raiz.winfo_screenheight()
       alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
       raiz.geometry(alignstr)
       raiz.resizable(width=False, height=False)
       raiz.config(bg="spring green")
       raiz.config(relief="sunken") 
       raiz.config(bd=10)
       #ícono
       icono = tk.PhotoImage(file="rojo.png")
       raiz.iconphoto(True, icono)
       
       # ... [código de creación y colocación de widgets (pantalla, etiquetas, frames, botones)] ...
       pantalla=tk.Entry(raiz,textvariable=self.mensajePantalla)
       pantalla.config(bg="black",fg="#03f943",justify="center",width=50)
       pantalla.place(x=300, y=50)
       
       ft=tkFont.Font(family="Timnes", size=14)
       
       etiqueta_titulo=tk.Label(raiz)
       etiqueta_titulo["anchor"] = "nw"
       etiqueta_titulo["bg"]="spring green"
       etiqueta_titulo["font"] = tkFont.Font(family="Timnes", size=18)
       etiqueta_titulo["justify"] = "center"
       etiqueta_titulo["text"] = "Interfaz Gráfica de Usuario"
       etiqueta_titulo.place(x=210,y=10)
       
       Frame_1=tk.Frame(raiz)
       Frame_1.place(x=30,y=40)
       
       boton_carga=tk.Button(Frame_1, text="Carga", command=self.carga,width=14)
       boton_carga["font"]=ft
       boton_carga.grid(row=1,column=1)
       
       boton_descarga=tk.Button(Frame_1, text="Descarga", command=self.descarga,width=14)
       boton_descarga["font"]=ft
       boton_descarga.grid(row=2,column=1)
       
       boton_dinamico=tk.Button(Frame_1, text="Dinámico", command=self.dinamico,width=14)
       boton_dinamico["font"]=ft
       boton_dinamico.grid(row=3,column=1)
       
       boton_homogeneo=tk.Button(Frame_1, text="Homogeneizar", command=self.homogeneo, width=14 )
       boton_homogeneo["font"]=ft
       boton_homogeneo.grid(row=4,column=1)
       
       boton_parar=tk.Button(Frame_1, text="Parar Motor", command=self.parar, width=14)
       boton_parar["font"]=ft
       boton_parar["bg"]="red"
       boton_parar.grid(row=5,column=1)
       
       #radio button de conexión
       Frame_2=tk.Frame(raiz)
       Frame_2.place(x=30,y=240)
       etiqueta_puerto=tk.Label(Frame_2)
       etiqueta_puerto["text"]="Conectar con el controlador:"
       etiqueta_puerto.grid(row=1,column=1)
       rb_21=tk.Radiobutton(Frame_2, text="conectar    .", variable=self.puerto, value=1,command=self.enchufar)
       rb_21.grid(row=2,column=1)
       rb_22=tk.Radiobutton(Frame_2, text="desconectar", variable=self.puerto, value=0,command=self.enchufar)
       rb_22.grid(row=3,column=1)
       
       #radio button de self.Frecuencia 
       Frame_3=tk.Frame(raiz)
       Frame_3.place(x=30, y=320)
       etiqueta_Frecuencia=tk.Label(Frame_3)
       etiqueta_Frecuencia["text"]="self.Frecuencia de ensayo dinámico:"
       etiqueta_Frecuencia.grid(row=1,column=1)
       rb_31=tk.Radiobutton(Frame_3, text="0,5 Hz", variable=self.Fr, value="05",command=self.Frecuencia)
       rb_31.grid(row=2,column=1)
       rb_32=tk.Radiobutton(Frame_3, text="1,0 Hz", variable=self.Fr, value="10",command=self.Frecuencia)
       rb_32.grid(row=3,column=1)
       rb_33=tk.Radiobutton(Frame_3, text="1,5 Hz", variable=self.Fr, value="15",command=self.Frecuencia)
       rb_33.grid(row=4,column=1)
       
       #radio button Rpm
       Frame_4=tk.Frame(raiz)
       Frame_4.place(x=30, y=420)
       etiqueta_motor=tk.Label(Frame_4)
       etiqueta_motor["text"]="Revoluciones del motor:"
       etiqueta_motor.grid(row=1,column=1)
       rb_41=tk.Radiobutton(Frame_4, text="17 Rpm", variable=self.Rpm_v, value="17",command=self.Rpm)
       rb_41.grid(row=2,column=1)
       rb_42=tk.Radiobutton(Frame_4, text="35 Rpm", variable=self.Rpm_v, value="35",command=self.Rpm)
       rb_42.grid(row=3,column=1)
       rb_43=tk.Radiobutton(Frame_4, text="70 Rpm", variable=self.Rpm_v, value="70",command=self.Rpm)
       rb_43.grid(row=4,column=1)
       
       #salir
       boton_salir=tk.Button(raiz, text="Salir", command=self.salir)
       boton_salir["font"]=ft
       boton_salir["bg"]="red2"
       boton_salir["fg"]="yellow"
       boton_salir.pack(side="bottom", anchor="se")
       #Exportar datos
       boton_exportar = tk.Button(self.master, text="Exportar", command=self.exportar, bg="red2", fg="yellow")
       boton_exportar.pack(side="bottom", anchor="se")

       # Frame imagen inicial
       cosa = Image.open("rojo_inicio.png")
       img=cosa.resize((450, 350))
       self.my_img=ImageTk.PhotoImage(img)
       self.label= tk.Label(self.master,image=self.my_img)
       self.label.place(x=300, y=100)
       
       pass
      
   def carga(self):
       """
       Ejecuta el ensayo de Carga.

       Verifica la conexión con el controlador. Si está conectado, copia
       'carga.csv' a 'input.csv', toma los datos, los grafica y actualiza la
       imagen en la GUI. Establece el estado del motor a encendido (1).

       Returns:
           int: 0 si fue exitoso, 1 si no está conectado.
       """
       if self.puerto.get()==0:
           messagebox.showwarning("Advertencia!!", "No está conectado al controlador!!")
           return 1
       self.mensajePantalla.set("Se activó ensayo carga")
       shutil.copy("carga.csv","input.csv")
       Tomar_datos()
       Dibujar()
       imagen = Image.open("input.png")
       imagen = imagen.resize((450, 350))
       self.my_img = ImageTk.PhotoImage(imagen)
       self.label = tk.Label(self.master, image=self.my_img)
       self.label.place(x=300, y=100)
       self.Motor.set(1)
       return 0       

   def descarga(self):
       """
       Ejecuta el ensayo de Descarga.

       Verifica la conexión. Si está conectado, copia 'descarga.csv' a
       'input.csv', toma los datos, los grafica y actualiza la imagen.
       Establece el estado del motor a encendido (1).

       Returns:
           int: 0 si fue exitoso, 1 si no está conectado.
       """
       if self.puerto.get()==0:
           messagebox.showwarning("Advertencia!!", "No está conectado al controlador!!")
           return 1
       self.mensajePantalla.set("Se activo ensayo descarga wee")
       shutil.copy("descarga.csv","input.csv")
       Tomar_datos()
       Dibujar()
       imagen = Image.open("input.png")
       imagen = imagen.resize((450, 350))
       self.my_img = ImageTk.PhotoImage(imagen)
       self.label = tk.Label(self.master, image=self.my_img)
       self.label.place(x=300, y=100)
       self.Motor.set(1)
       return 0

   def dinamico(self):
       """
       Ejecuta el ensayo Dinámico.

       Verifica la conexión. Si está conectado, selecciona el archivo CSV
       ('05.csv', '10.csv', o '15.csv') basándose en la frecuencia (self.Fr),
       lo copia a 'input.csv', toma los datos, los grafica y actualiza la
       imagen. Establece el estado del motor a encendido (1).

       Returns:
           int: 0 si fue exitoso, 1 si no está conectado.
       """
       if self.puerto.get()==0:
           messagebox.showwarning("Advertencia!!", "No está conectado al controlador!!")
           return 1
       if self.Fr.get()=="05":
           self.mensajePantalla.set("Dinámico Fr=0,5 Hz a "+self.Rpm_v.get()+" RPM")
           shutil.copy("05.csv","input.csv")
       if self.Fr.get()=="10":
           self.mensajePantalla.set("Dinámico Fr=1,0 Hz a "+self.Rpm_v.get()+" RPM")
           shutil.copy("10.csv","input.csv")
       if self.Fr.get()=="15":
           self.mensajePantalla.set("Dinámico Fr=1,5 Hz a "+self.Rpm_v.get()+" RPM")
           shutil.copy("15.csv","input.csv")
       Tomar_datos()
       Dibujar()
       imagen= Image.open("input.png")
       imagen = imagen.resize((450, 350))
       self.my_img = ImageTk.PhotoImage(imagen)
       self.label = tk.Label(self.master, image=self.my_img)
       self.label.place(x=300, y=100)
       self.Motor.set(1)
       return 0

   def homogeneo(self):
       """
       Activa el modo de Homogeneización.

       Verifica la conexión. Si está conectado, actualiza el mensaje de estado
       e indica que el motor está en marcha (1).

       Returns:
           int: 0 si fue exitoso, 1 si no está conectado.
       """
       if self.puerto.get()==0:
           messagebox.showwarning("Advertencia!!", "No está conectado al controlador!!")
           return 1
       self.mensajePantalla.set("Homogeneizando")
       self.Motor.set(1)
       return 0

   def parar(self):
       """
       Detiene el motor.

       Verifica la conexión y el estado actual del motor. Si está conectado y
       el motor está encendido, lo detiene (Motor.set(0)) y actualiza el mensaje.

       Returns:
           int: 0 si el motor fue detenido o ya estaba parado, 1 si no está conectado.
       """
       if self.puerto.get()==0:
           messagebox.showwarning("Advertencia!!", "No está conectado al controlador!!")
           return 1
       if self.Motor.get()==0:
           messagebox.showwarning("Advertencia!!", "El motor está parado!!")
           return 0
       self.mensajePantalla.set("Se detuvo motor")
       self.Motor.set(0)
       return 0
       
   def enchufar(self):
       """
       Cambia y actualiza el estado de conexión al controlador.

       El valor de self.puerto (1: conectado, 0: desconectado) se refleja
       en el mensaje de la pantalla de estado.

       Returns:
           int: 0 (siempre retorna 0).
       """
       # print(self.puerto.get())
       if self.puerto.get()==1:
           self.mensajePantalla.set("Enchufado")
       else:
           self.mensajePantalla.set("No enchufado")
       return 0
    
   def Frecuencia(self):
       """
       Actualiza el mensaje de la pantalla según la frecuencia dinámica (self.Fr)
       seleccionada (0,5 Hz, 1,0 Hz o 1,5 Hz).

       Returns:
           int: 0 (siempre retorna 0).
       """
       if self.Fr.get()=="05":
           self.mensajePantalla.set("Se eligió 0,5 Hz")
       if self.Fr.get()=="10":
           self.mensajePantalla.set("Se eligió 1,0 Hz")
       if self.Fr.get()=="15":
           self.mensajePantalla.set("Se eligió 1,5 Hz")
       return 0
   
   def Rpm(self):
       """
       Actualiza el mensaje de la pantalla según las RPM (self.Rpm_v)
       seleccionadas (70 Rpm, 35 Rpm o 17 Rpm).

       Returns:
           int: 0 (siempre retorna 0).
       """
       if self.Rpm_v.get()=="70":
           self.mensajePantalla.set("Se eligió 70 Rpm")
       if self.Rpm_v.get()=="35":
           self.mensajePantalla.set("Se eligió 35 Rpm")
       if self.Rpm_v.get()=="17":
           self.mensajePantalla.set("Se eligió 17 Rpm")
       return 0

   def salir(self):
       """
       Muestra un cuadro de diálogo de confirmación para salir de la aplicación.

       Si el usuario confirma, destruye la ventana principal.

       Returns:
           int: 0 (siempre retorna 0).
       """
       respuesta=messagebox.askquestion("Ventana de pregunta","Desea salir realmente?")
       if respuesta=="yes":
           self.master.destroy()
       return 0
   
   def exportar(self):
       """
       Permite al usuario guardar los datos actuales (T, X, Y) en un archivo CSV.

       Verifica la conexión y la existencia de datos en memoria. Si las
       condiciones son válidas, abre un cuadro de diálogo para seleccionar la
       ubicación y el nombre del archivo.

       Returns:
           int: 0 si fue exitoso, 1 si no está conectado, 2 si no hay datos.
       """
       if self.puerto.get()==0:
           messagebox.showwarning("Advertencia!!", "No está conectado al controlador!!")
           return 1
       if len(T)==0:
           messagebox.showwarning("Advertencia!!", "No hay datos en la memoria!!")
           return 2
       archivo=filedialog.asksaveasfilename(filetypes=[("cvs file",".csv")],defaultextension=".csv")
       # NOTA: En una versión completa, aquí iría el código para escribir T, X, Y al archivo 'archivo'.
       print("Lo guardo en: "+archivo)
       return 0

   pass

if __name__ == "__main__":
   raiz = tk.Tk()
   app = GUI(raiz)
   #for i in Token.keys():
   #    print(Token[i])
   
   raiz.mainloop()
