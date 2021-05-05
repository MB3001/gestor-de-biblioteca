'''
Trabajo Práctico Final: Programa gestionador de biblioteca.

Por Matías Bonino.


Aspecto visual:

Ventanilla de presentación y créditos.
Pestañas con botones: libros y préstamos.
Ventana de error.

Pseudocódigo:

Biblioteca [

class Libro
    Título, autor, edición, lugar de impresión, editorial, si es una traducción, cantidad de páginas, condición.

    Condición:
    _ Préstamo en proceso: cuando el libro está en medio de un préstamo a alguno de los afiliados a la biblioteca.
    _ Disponible: esta condición indica que el libro está disponible para ser prestado a algún afiliado.
    _ Retraso: cuando un libro no ha sido devuelto una vez llegada la fecha de devolución.
    _ En restauración: hay libros que, llegado cierto momento, pueden necesitar una restauración, durante las cuales no se puede prestar el libro.

    Únicamente se puede prestar un libro en condición de disponible, toda otra condición debe hacer que el programa impida registrar el préstamo.

class Préstamo
    Nombre completo de la persona a la que se va a prestar, Teléfono, Mail, Fecha de inicio de préstamo, Fecha de devolución, Libro a prestar.

Menú principal {

Libros {

Dar de alta un libro.
Modificar los datos de un libro. Eso incluye la condición.
Dar de baja un libro.
Consultar un libro en particular por su nombre.
Mostrar todos los libros cargados.
}
Préstamos {

Registrar un préstamo.
Dar por terminado un préstamo.
Reclamar un préstamo: esta situación se plantea cuando el usuario controla 
los préstamos vigentes y el programa detecta que hay préstamos que no se 
devolvieron, inmediatamente el programa muestra los datos de la persona a la
que se le prestó el libro para que el usuario pueda comunicarse con él/ella 
y así poder acordar la devolución.
}
}
]
'''

# <> \n \n\

import tkinter as tk
from tkinter import ttk
import functions as funct

class Aplicacion:
    def __init__(self):
        # Inicialización de la ventana.
        self.ventana = tk.Tk()
        self.ventana.title('Gestionador de Biblioteca')
        self.ventana.geometry('300x200')

        # Inicialización de las pestañas.
        self.cuaderno = ttk.Notebook(self.ventana)
        self.pagina_1 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina_1, text='Libros')
        self.pagina_2 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina_2, text='Préstamos')

        # Botones.
        self.botonAlta = tk.Button(self.pagina_1, text = 'Dar de alta un libro', command = funct.VentanaDarDeAlta)
        self.botonAlta.grid(column=0, row=0)
        self.botonMod = tk.Button(self.pagina_1, text = 'Modificar los datos de un libro', command = funct.VentanaMod)
        self.botonMod.grid(column=0, row=1)
        self.botonBaja = tk.Button(self.pagina_1, text = 'Dar de baja un libro', command = funct.VentanaDarDeBaja)
        self.botonBaja.grid(column=0, row=2)
        self.botonCons = tk.Button(self.pagina_1, text = 'Consultar un libro en particular por su nombre', command = funct.VentanaCons)
        self.botonCons.grid(column=0, row=3)
        self.botonMos = tk.Button(self.pagina_1, text = 'Mostrar todos los libros cargados', command = funct.VentanaMos)
        self.botonMos.grid(column=0, row=4)

        self.botonReg = tk.Button(self.pagina_2, text = 'Registrar un préstamo', command = funct.VentanaReg)
        self.botonReg.grid(column=0, row=0)
        self.botonTerm = tk.Button(self.pagina_2, text = 'Dar por terminado un préstamo', command = funct.VentanaTermin)
        self.botonTerm.grid(column=0, row=1)

        self.cuaderno.grid(column=0, row=0)

        self.ventana.mainloop()


funct.presentar()
funct.revisarVencimientos()
app = Aplicacion()
