'''
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



Libros:

Dar de alta un libro.
Modificar los datos de un libro. Eso incluye la condición.
Dar de baja un libro.
Consultar un libro en particular por su nombre.
Mostrar todos los libros cargados.


Préstamos:

Registrar un préstamo.
Dar por terminado un préstamo.
Reclamar un préstamo: esta situación se plantea cuando el usuario controla 
los préstamos vigentes y el programa detecta que hay préstamos que no se 
devolvieron, inmediatamente el programa muestra los datos de la persona a la
que se le prestó el libro para que el usuario pueda comunicarse con él/ella 
y así poder acordar la devolución.

'''

# <> \n \n\

import datetime as dt
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import sqlite3

# Clases.
class Libro:
    def __init__(self):
        self.título = ''
        self.autor = ''
        self.edición = ''
        self.lugar_de_impresión = ''
        self.editorial = ''
        self.es_traducción = False # ¿El libro es una traducción?
        self.páginas = 0
        self.condición = 0

    # Retornar si es una traducción.
    def getEs_traducción(self):
        trad_str = ''
        if self.es_traducción:
            trad_str = 'Es una traducción.'
        else:
            trad_str = 'No es una traducción.'
        return trad_str

    # Retornar si es una traducción pero devolviendo enteros.
    def getIntEs_traducción(self):
        trad_int = ''
        if self.es_traducción:
            trad_int = 1
        else:
            trad_int = 0
        return trad_int

    # Retornar condición.
    def getCondición(self):
        cond_str = ''
        if self.condición == 0:
            cond_str = 'Préstamo en proceso.'
        elif self.condición == 1:
            cond_str = 'Disponible.'
        elif self.condición == 2:
            cond_str = 'Retraso.'
        elif self.condición == 3:
            cond_str = 'En restauración.'
        else:
            error(AttributeError, f"Este libro tiene cargado como condición '{self.condición}', lo cual no es válido.")
        return cond_str

    # toString de Libro.
    def __str__(self):
        toString = 'Título: ' + self.título + '\n'
        toString += 'Autor: ' + self.autor + '\n'
        toString += 'Edición: ' + self.edición + '\n'
        toString += 'Lugar de impresión: ' + self.lugar_de_impresión + '\n'
        toString += 'Editorial: ' + self.editorial + '\n'
        toString += '¿Es una traducción?: ' + self.getEs_traducción() + '\n'
        toString += 'Páginas: ' + str(self.páginas) + '\n'
        toString += 'Condición: ' + self.getCondición() + '\n'
        return toString

class Persona:
    def __init__(self):
        self.nombre = ''
        self.teléfono = 0
        self.mail = ''

    # toString de Persona.
    def __str__(self):
        toString = 'Nombre: ' + str(self.nombre) + '\n'
        toString += 'Teléfono: ' + str(self.teléfono) + '\n'
        toString += 'Mail: ' + self.mail + '\n'
        return toString

class Prestamo:
    def __init__(self):
        self.persona = Persona()
        self.fecha_de_inicio = ''
        self.fecha_de_devolución = ''
        self.libro = Libro() # Libro a prestar.

    # toString de Prestamo.
    def __str__(self):
        toString = 'Persona: ' + self.persona.nombre + '\n'
        toString += 'Fecha de inicio: ' + self.fecha_de_inicio + '\n'
        toString += 'Fecha de devolución: ' + self.fecha_de_devolución + '\n'
        toString += 'Libro: ' + self.libro.título + '\n'
        return toString

# Funciones de GUI.
# -----------------

# Ventana de presentación y créditos.
def presentar():
    ventana = tk.Tk()
    ventana.title('¡Bienvenido!')
    ventana.geometry('250x100')

    label = tk.Label(ventana, text = 'Programa Gestionador de Biblioteca.\n\nPor Matías Bonino.\n\nVersión 0.1, lanzada en 2/5/2021.')
    label.grid(column=0, row=0)
    label.configure(foreground = 'black')

    ventana.mainloop()

# Ventana de error en caso de que ocurra una excepción. Para el texto de la descripción y solución se coloca '\n' cada 57 caracteres o menos.
def error(excepción, descripción_y_solución):
    ventana = tk.Tk()
    ventana.title('Error')
    ventana.geometry('300x150')

    label = tk.Label(ventana, text = f'{excepción}:\n\n{descripción_y_solución}')
    label.grid(column=0, row=0)
    label.configure(foreground = 'black')

    #botonAceptar = tk.Button(ventana, text = 'Aceptar', command = ventana.quit)
    '''if salir:
        botonAceptar.configure(command = sys.exit) # Hace falta un 'import sys'.'''
    #botonAceptar.grid(column=0, row=1)        

    ventana.mainloop()

# Ventana de operación exitosa. Para el texto de la descripción se coloca '\n' cada 57 caracteres o menos.
def exito(descripción):
    ventana = tk.Tk()
    ventana.title('Operación exitosa')
    ventana.geometry('300x100')

    label = tk.Label(ventana, text = f'Operación exitosa:\n\n{descripción}')
    label.grid(column=0, row=0)
    label.configure(foreground = 'black')

    ventana.mainloop()

# Revisar fechas de vencimientos.
def revisarVencimientos():
    # Por cada préstamo en la tabla préstamos de biblioteca.db, si el libro se venció, cambiar su condición a 'Retraso' y reclamar a la persona.
    pres_vencidos = []
    filas = []
    id = 0
    try:
        conexion = sqlite3.connect('biblioteca.db')
        cursor = conexion.execute('select * from prestamos')
        filas = cursor.fetchall()

        if filas != None:
            try:
                # Por cada préstamo, ...
                for i in range(len(filas)):
                    id = int(filas[i][0])

                    pres = Prestamo()
                    pres.persona.nombre = filas[i][1]
                    pres.persona.teléfono= int(filas[i][2])
                    pres.persona.mail = filas[i][3]
                    pres.fecha_de_inicio = filas[i][4]
                    pres.fecha_de_devolución = filas[i][5]
                    pres.libro.título = filas[i][6]

                    # si el libro se venció, ...
                    if (dt.datetime.strptime(pres.fecha_de_devolución, '%d-%m-%Y').date() < dt.datetime.now().date()):
                        # cambiar su condición a 'Retraso'...
                        pres.libro.condición = 2 # (Retraso).
                        cursor2 = conexion.execute('update libros set condición=? where título=?', (2, pres.libro.título))
                        conexion.commit()
                        #print(f'Debug: _ Libro vencido: {pres.libro.título}, ID = {id}, Nueva condición: {pres.libro.condición}')

                        # y reclamar a la persona.
                        VentanaRecl(pres)

                    pres_vencidos.append(pres)
            except IndexError as ier:
                error(ier, f"El índice de la lista de datos recolectados de la base de\ndatos está fuera de rango. Solución desconocida.")
            #except Exception as ex:
                #error(ex, 'Solución desconocida.')
        else:
            error(KeyError, f'No se encontró ningún préstamo.')

        conexion.commit()

    except sqlite3.OperationalError as oe:
        error(oe, "No se encontró la tabla 'prestamos' en la base de datos\n'biblioteca.db'. Puede crear una registrando préstamos.")
    except tk.TclError as tcler:
        error(tcler, f"Dato inválido. El texto '{id}' ingresado en el campo 'ID'\nno es numérico o estaba vacío. Debe ingresar un número\nentero positivo.")
    except Exception as ex:
        error(ex, 'Solución desconocida.')
    finally:
        conexion.close()

# Ventana para dar de alta un libro.
class VentanaDarDeAlta():
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title('Dar de alta un libro')
        self.ventana.geometry('300x310')

        labelTítulo = tk.Label(self.ventana, text = 'Título:')
        labelTítulo.grid(column=0, row=0)
        labelTítulo.configure(foreground = 'black')

        labelAutor = tk.Label(self.ventana, text = 'Autor:')
        labelAutor.grid(column=0, row=1)
        labelAutor.configure(foreground = 'black')

        labelEdición = tk.Label(self.ventana, text = 'Edición:')
        labelEdición.grid(column=0, row=2)
        labelEdición.configure(foreground = 'black')

        labelLugarDeImpresión = tk.Label(self.ventana, text = 'Lugar de impresión:')
        labelLugarDeImpresión.grid(column=0, row=3)
        labelLugarDeImpresión.configure(foreground = 'black')

        labelEditorial = tk.Label(self.ventana, text = 'Editorial:')
        labelEditorial.grid(column=0, row=4)
        labelEditorial.configure(foreground = 'black')

        labelEsTraducción = tk.Label(self.ventana, text = '¿Es una traducción?:')
        labelEsTraducción.grid(column=0, row=5)
        labelEsTraducción.configure(foreground = 'black')

        labelPáginas = tk.Label(self.ventana, text = 'Páginas:')
        labelPáginas.grid(column=0, row=7)
        labelPáginas.configure(foreground = 'black')

        labelCondición = tk.Label(self.ventana, text = 'Condición:')
        labelCondición.grid(column=0, row=8)
        labelCondición.configure(foreground = 'black')

        self.datoTítulo = tk.StringVar(self.ventana)
        self.entryTítulo = tk.Entry(self.ventana, width=10, textvariable = self.datoTítulo)
        self.entryTítulo.grid(column=1, row=0)

        self.datoAutor = tk.StringVar(self.ventana)
        self.entryAutor = tk.Entry(self.ventana, width=10, textvariable = self.datoAutor)
        self.entryAutor.grid(column=1, row=1)

        self.datoEdición = tk.StringVar(self.ventana)
        self.entryEdición = tk.Entry(self.ventana, width=10, textvariable = self.datoEdición)
        self.entryEdición.grid(column=1, row=2)

        self.datoLugarDeImpresión = tk.StringVar(self.ventana)
        self.entryLugarDeImpresión = tk.Entry(self.ventana, width=10, textvariable = self.datoLugarDeImpresión)
        self.entryLugarDeImpresión.grid(column=1, row=3)

        self.datoEditorial = tk.StringVar(self.ventana)
        self.entryEditorial = tk.Entry(self.ventana, width=10, textvariable = self.datoEditorial)
        self.entryEditorial.grid(column=1, row=4)

        self.datoEsTraducción = tk.IntVar(self.ventana)
        self.datoEsTraducción.set(0)

        self.es_tr_radio_1 = tk.Radiobutton(self.ventana, text = 'Si', variable = self.datoEsTraducción, value=0)
        self.es_tr_radio_1.grid(column=1, row=5)
        self.es_tr_radio_2 = tk.Radiobutton(self.ventana, text = 'No', variable = self.datoEsTraducción, value=1)
        self.es_tr_radio_2.grid(column=1, row=6)

        self.datoPáginas = tk.IntVar(self.ventana)
        self.entryPáginas = tk.Entry(self.ventana, width=10, textvariable = self.datoPáginas)
        self.entryPáginas.grid(column=1, row=7)

        self.datoCondición = tk.IntVar(self.ventana)
        self.datoCondición.set(1)

        self.es_cond_radio_1 = tk.Radiobutton(self.ventana, text = 'Préstamo en proceso.', variable = self.datoCondición, value=0)
        self.es_cond_radio_1.grid(column=1, row=8)
        self.es_cond_radio_2 = tk.Radiobutton(self.ventana, text = 'Disponible.', variable = self.datoCondición, value=1)
        self.es_cond_radio_2.grid(column=1, row=9)
        self.es_cond_radio_3 = tk.Radiobutton(self.ventana, text = 'Retraso.', variable = self.datoCondición, value=2)
        self.es_cond_radio_3.grid(column=1, row=10)
        self.es_cond_radio_4 = tk.Radiobutton(self.ventana, text = 'En restauración.', variable = self.datoCondición, value=3)
        self.es_cond_radio_4.grid(column=1, row=11)

        botonAceptar = tk.Button(self.ventana, text = 'Aceptar', command = self.darDeAlta)
        botonAceptar.grid(column=0, row=12)

        self.ventana.mainloop()

    # Dar de alta un libro.
    def darDeAlta(self):
        try:
            conexion = sqlite3.connect('biblioteca.db')
            datos = (self.datoTítulo.get(), self.datoAutor.get(), self.datoEdición.get(), self.datoLugarDeImpresión.get(), 
            self.datoEditorial.get(), self.datoEsTraducción.get(), self.datoPáginas.get(), self.datoCondición.get())
            try:
                conexion.execute('''create table libros (
                                id integer primary key AUTOINCREMENT,  
                                título text,
                                autor text,
                                edición text,
                                lugar_de_impresión text,
                                editorial text,
                                es_traducción integer,
                                páginas integer,
                                condición integer
                                )''')
                print("Se creó la tabla 'libros'.")
            except:
                print("La tabla 'libros' ya existe.")
            conexion.execute('insert into libros(título,autor,edición,lugar_de_impresión,editorial,es_traducción,páginas,condición) \
values(?,?,?,?,?,?,?,?)', datos)
            conexion.commit() # Confirmamos la actualización de los cambios de la tabla.
            exito(f"Libro '{self.datoTítulo.get()}' cargado con éxito.")
        except tk.TclError as tcler:
            error(tcler, "Dato inválido. Seguramente haya puesto un carácter\nno numérico en el campo 'Páginas'.")
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()

# Ventana para modificar los datos de un libro.
class VentanaMod:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title('Modificar un libro')
        self.ventana.geometry('350x340')

        labelBuscadorId = tk.Label(self.ventana, text = 'Buscar libro por su ID:')
        labelBuscadorId.grid(column=0, row=0)
        labelBuscadorId.configure(foreground = 'black')

        self.datoBuscadorId = tk.IntVar(self.ventana)
        self.entryBuscadorId = tk.Entry(self.ventana, width=10, textvariable = self.datoBuscadorId)
        self.entryBuscadorId.grid(column=1, row=0)
    
        botonBuscadorId = ttk.Button(self.ventana, text = 'Buscar', command = self.buscarPorId)
        botonBuscadorId.grid(column=2, row=0)

        # --------------------------------------------------

        labelTítulo = tk.Label(self.ventana, text = 'Título:')
        labelTítulo.grid(column=0, row=1)
        labelTítulo.configure(foreground = 'black')

        labelAutor = tk.Label(self.ventana, text = 'Autor:')
        labelAutor.grid(column=0, row=2)
        labelAutor.configure(foreground = 'black')

        labelEdición = tk.Label(self.ventana, text = 'Edición:')
        labelEdición.grid(column=0, row=3)
        labelEdición.configure(foreground = 'black')

        labelLugarDeImpresión = tk.Label(self.ventana, text = 'Lugar de impresión:')
        labelLugarDeImpresión.grid(column=0, row=4)
        labelLugarDeImpresión.configure(foreground = 'black')

        labelEditorial = tk.Label(self.ventana, text = 'Editorial:')
        labelEditorial.grid(column=0, row=5)
        labelEditorial.configure(foreground = 'black')

        labelEsTraducción = tk.Label(self.ventana, text = '¿Es una traducción?:')
        labelEsTraducción.grid(column=0, row=6)
        labelEsTraducción.configure(foreground = 'black')

        labelPáginas = tk.Label(self.ventana, text = 'Páginas:')
        labelPáginas.grid(column=0, row=8)
        labelPáginas.configure(foreground = 'black')

        labelCondición = tk.Label(self.ventana, text = 'Condición:')
        labelCondición.grid(column=0, row=9)
        labelCondición.configure(foreground = 'black')

        self.datoTítulo = tk.StringVar(self.ventana)
        self.entryTítulo = tk.Entry(self.ventana, width=10, textvariable = self.datoTítulo)
        self.entryTítulo.grid(column=1, row=1)

        self.datoAutor = tk.StringVar(self.ventana)
        self.entryAutor = tk.Entry(self.ventana, width=10, textvariable = self.datoAutor)
        self.entryAutor.grid(column=1, row=2)

        self.datoEdición = tk.StringVar(self.ventana)
        self.entryEdición = tk.Entry(self.ventana, width=10, textvariable = self.datoEdición)
        self.entryEdición.grid(column=1, row=3)

        self.datoLugarDeImpresión = tk.StringVar(self.ventana)
        self.entryLugarDeImpresión = tk.Entry(self.ventana, width=10, textvariable = self.datoLugarDeImpresión)
        self.entryLugarDeImpresión.grid(column=1, row=4)

        self.datoEditorial = tk.StringVar(self.ventana)
        self.entryEditorial = tk.Entry(self.ventana, width=10, textvariable = self.datoEditorial)
        self.entryEditorial.grid(column=1, row=5)

        self.datoEsTraducción = tk.IntVar(self.ventana)
        self.datoEsTraducción.set(0)

        self.es_tr_radio_1 = tk.Radiobutton(self.ventana, text = 'Si', variable = self.datoEsTraducción, value=0)
        self.es_tr_radio_1.grid(column=1, row=6)
        self.es_tr_radio_2 = tk.Radiobutton(self.ventana, text = 'No', variable = self.datoEsTraducción, value=1)
        self.es_tr_radio_2.grid(column=1, row=7)

        self.datoPáginas = tk.IntVar(self.ventana)
        self.entryPáginas = tk.Entry(self.ventana, width=10, textvariable = self.datoPáginas)
        self.entryPáginas.grid(column=1, row=8)

        self.datoCondición = tk.IntVar(self.ventana)
        self.datoCondición.set(1)

        self.es_cond_radio_1 = tk.Radiobutton(self.ventana, text = 'Préstamo en proceso.', variable = self.datoCondición, value=0)
        self.es_cond_radio_1.grid(column=1, row=9)
        self.es_cond_radio_2 = tk.Radiobutton(self.ventana, text = 'Disponible.', variable = self.datoCondición, value=1)
        self.es_cond_radio_2.grid(column=1, row=10)
        self.es_cond_radio_3 = tk.Radiobutton(self.ventana, text = 'Retraso.', variable = self.datoCondición, value=2)
        self.es_cond_radio_3.grid(column=1, row=11)
        self.es_cond_radio_4 = tk.Radiobutton(self.ventana, text = 'En restauración.', variable = self.datoCondición, value=3)
        self.es_cond_radio_4.grid(column=1, row=12)

        botonAceptar = tk.Button(self.ventana, text = 'Aceptar', command = self.mod)
        botonAceptar.grid(column=0, row=13)

        self.ventana.mainloop()

    # Buscar libro por su ID.
    def buscarPorId(self):
        fila = []
        id = 0
        try:
            conexion = sqlite3.connect('biblioteca.db')
            sql = 'select título,autor,edición,lugar_de_impresión,editorial,es_traducción,páginas,condición from libros where id=?'
            id = self.datoBuscadorId.get()
            #print(f'Debug: _ SQL: {sql}, ID: {id}')
            cursor = conexion.execute(sql, (id, ))
            fila = cursor.fetchone()
        except tk.TclError as tcler:
            error(tcler, "Dato inválido. Seguramente haya puesto un carácter\nno numérico en el campo 'Buscar libro por su ID'.")
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()
        
        if fila != None:
            try:
                self.entryTítulo.delete(0, tk.END)
                self.entryAutor.delete(0,  tk.END)
                self.entryEdición.delete(0,  tk.END)
                self.entryLugarDeImpresión.delete(0, tk.END)
                self.entryEditorial.delete(0, tk.END)
                self.entryPáginas.delete(0, tk.END)

                self.entryTítulo.insert(0, fila[0])
                self.entryAutor.insert(0, fila[1])
                self.entryEdición.insert(0, fila[2])
                self.entryLugarDeImpresión.insert(0, fila[3])
                self.entryEditorial.insert(0, fila[4])
                self.datoEsTraducción.set(fila[5])
                self.entryPáginas.insert(0, fila[6])
                self.datoCondición.set(fila[7])
            except tk.TclError as tcler:
                error(tcler, "El valor requerido para la búsqueda no existe. Se buscó\ncon el campo 'Buscar libro por su ID' vacío. Es un error\nleve que se soluciona al salir.")
        else:
            error(KeyError, f'No se encontró ningún libro con ID = {id}.\nPorfavor, intente de nuevo con otro número.')

    # Modificar los datos de un libro.
    def mod(self):
        try:
            conexion = sqlite3.connect('biblioteca.db')
            datos = (self.datoTítulo.get(), self.datoAutor.get(), self.datoEdición.get(), self.datoLugarDeImpresión.get(), 
            self.datoEditorial.get(), self.datoEsTraducción.get(), self.datoPáginas.get(), self.datoCondición.get(), self.datoBuscadorId.get())
            sql = 'update libros set título=?,autor=?,edición=?,lugar_de_impresión=?,editorial=?,es_traducción=?,páginas=?,condición=? where id=?'
            conexion.execute(sql, datos)
            conexion.commit() # Confirmamos la actualización de los cambios de la tabla.
            exito(f"Libro '{self.datoTítulo.get()}' modificado con éxito.")
        except tk.TclError as tcler:
            error(tcler, "Dato inválido. Seguramente haya puesto un carácter\nno numérico en el campo 'Páginas'.")
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()

# Ventana para dar de baja un libro.
class VentanaDarDeBaja:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title('Dar de baja un libro')
        self.ventana.geometry('450x200')

        labelBuscadorId = tk.Label(self.ventana, text = 'Buscar libro por su ID:')
        labelBuscadorId.grid(column=0, row=0)
        labelBuscadorId.configure(foreground = 'black')

        self.datoBuscadorId = tk.IntVar(self.ventana)
        self.entryBuscadorId = tk.Entry(self.ventana, width=10, textvariable = self.datoBuscadorId)
        self.entryBuscadorId.grid(column=1, row=0)
    
        botonBuscadorId = ttk.Button(self.ventana, text = 'Buscar', command = self.buscarPorId)
        botonBuscadorId.grid(column=2, row=0)

        botonDarDeBaja = ttk.Button(self.ventana, text = 'Dar de baja', command = self.darDeBaja)
        botonDarDeBaja.grid(column=3, row=0)

        self.labelDisplay = tk.Label(self.ventana, text = 'Libro:\n\n-')
        self.labelDisplay.grid(column=0, row=1)
        self.labelDisplay.configure(foreground = 'black')

        self.ventana.mainloop()

    # Buscar libro por su ID.
    def buscarPorId(self):
        fila = []
        id = 0
        try:
            conexion = sqlite3.connect('biblioteca.db')
            sql = 'select título,autor,edición,lugar_de_impresión,editorial,es_traducción,páginas,condición from libros where id=?'
            id = self.datoBuscadorId.get()
            #print(f'Debug: _ SQL: {sql}, ID: {id}')
            cursor = conexion.execute(sql, (id, ))
            fila = cursor.fetchone()
        except tk.TclError as tcler:
            error(tcler, f"Dato inválido. El texto '{id}' ingresado en el campo 'ID'\nno es numérico o estaba vacío. Debe ingresar un número\nentero positivo.")
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()

        if fila != None:
            try:
                libro = Libro()
                libro.título = fila[0]
                libro.autor = fila[1]
                libro.edición = fila[2]
                libro.lugar_de_impresión = fila[3]
                libro.editorial = fila[4]
                libro.es_traducción = bool(fila[5])
                libro.páginas = int(fila[6])
                libro.condición = int(fila[7])

                self.labelDisplay.configure(text = 'Libro:\n\n' + str(libro))
            except IndexError as ier:
                error(ier, f"El índice de la lista de datos recolectados de la base de\ndatos está fuera de rango. Debido a que se buscó con el\n\
campo 'Buscar libro por su ID' vacío. Es un error leve\nque se soluciona al salir.")
            except Exception as ex:
                error(ex, 'Solución desconocida.')
        else:
            error(KeyError, f'No se encontró ningún libro con ID = {id}.\nPorfavor, intente de nuevo con otro número.')

    # Dar de baja un libro.
    def darDeBaja(self):
        fila = []
        id = 0
        try:
            conexion = sqlite3.connect('biblioteca.db')
            sql_buscar = 'select título,autor,edición,lugar_de_impresión,editorial,es_traducción,páginas,condición from libros where id=?'
            id = self.datoBuscadorId.get()
            #print(f'Debug: _ ID: {id}')
            cursor = conexion.execute(sql_buscar, (id, ))
            fila = cursor.fetchone()

            if fila != None:
                    sql_eliminar = '''delete from libros where id = ?'''
                    cursor.execute(sql_eliminar, (id, ))
                    conexion.commit()
                    exito(f"Libro '{fila[0]}' dado de baja con éxito.")
            else:
                error(KeyError, f'No se encontró ningún libro con ID = {id}.\nPorfavor, intente de nuevo con otro número.')
            
        except IndexError as ier:
            error(ier, f"El índice de la lista de datos recolectados de la base de\ndatos está fuera de rango. Debido a que se buscó con el\n\
campo 'Buscar libro por su ID' vacío. Es un error leve\nque se soluciona al salir.")
        except tk.TclError as tcler:
            error(tcler, f"Dato inválido. El texto '{id}' ingresado en la entrada\nno es numérico o estaba vacío. Debe ingresar un número\nentero positivo.")
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()

# Ventana para consultar un libro en particular por su título.
class VentanaCons:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title('Consultar un libro por su título')
        self.ventana.geometry('450x200')

        labelBuscador = tk.Label(self.ventana, text = 'Consultar un libro por su título:')
        labelBuscador.grid(column=0, row=0)
        labelBuscador.configure(foreground = 'black')

        self.datoBuscador = tk.StringVar(self.ventana)
        self.entryBuscador = tk.Entry(self.ventana, width=10, textvariable = self.datoBuscador)
        self.entryBuscador.grid(column=1, row=0)
    
        botonBuscadorId = ttk.Button(self.ventana, text = 'Buscar', command = self.cons)
        botonBuscadorId.grid(column=2, row=0)

        self.labelDisplay = tk.Label(self.ventana, text = 'Libro:\n\n-')
        self.labelDisplay.grid(column=0, row=1)
        self.labelDisplay.configure(foreground = 'black')

        self.ventana.mainloop()

    # Consultar un libro en particular por su título.
    def cons(self):
        fila = []
        título = ''
        try:
            conexion = sqlite3.connect('biblioteca.db')
            sql = 'select título,autor,edición,lugar_de_impresión,editorial,es_traducción,páginas,condición from libros where título=?'
            título = self.datoBuscador.get()
            #print(f'Debug: _ SQL: {sql}, Título: {título}')
            cursor = conexion.execute(sql, (título, ))
            fila = cursor.fetchone()
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()

        if fila != None:
            try:
                libro = Libro()
                libro.título = fila[0]
                libro.autor = fila[1]
                libro.edición = fila[2]
                libro.lugar_de_impresión = fila[3]
                libro.editorial = fila[4]
                libro.es_traducción = bool(fila[5])
                libro.páginas = int(fila[6])
                libro.condición = int(fila[7])

                self.labelDisplay.configure(text = 'Libro:\n\n' + str(libro))
            except IndexError as ier:
                error(ier, f"El índice de la lista de datos recolectados de la base de\ndatos está fuera de rango. Debido a que se buscó con el\n\
campo 'Buscar libro por su título' vacío. Es un error\nleve que se soluciona al salir.")
            except Exception as ex:
                error(ex, 'Solución desconocida.')
        else:
            error(KeyError, f"No se encontró ningún libro con título '{título}'.\nPorfavor, intente de nuevo con otro título.")

# Ventana para mostrar todos los libros cargados.
class VentanaMos:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title('Mostrar todos los libros cargados')
        self.ventana.geometry('450x500')
        
        self.textarea = scrolledtext.ScrolledText(self.ventana, width=53, height=30)

        self.mos() # Mostrar todos los libros cargados.

        self.textarea.grid(column=0, row=0)

        self.ventana.mainloop()

    # Mostrar todos los libros cargados.
    def mos(self):
        filas = []
        texto = ''
        try:
            conexion = sqlite3.connect('biblioteca.db')
            sql = 'select * from libros'
            cursor = conexion.execute(sql)
            filas = cursor.fetchall()

            if filas == None:
                texto = "(No se detectó ningún libro en la base de datos. Si cree que esto es un error, cierre el programa,\n\
mueva la base de datos a otra ubicación y repárela manualmente con el software 'DB Browser (SQLite)'\n\
conseguido en 'https://sqlitebrowser.org/')."
            else:
                for i in range(len(filas)):
                    libro = Libro()
                    id = filas[i][0]
                    libro.título = filas[i][1]
                    libro.autor = filas[i][2]
                    libro.edición = filas[i][3]
                    libro.lugar_de_impresión = filas[i][4]
                    libro.editorial = filas[i][5]
                    libro.es_traducción = bool(filas[i][6])
                    libro.páginas = int(filas[i][7])
                    libro.condición = int(filas[i][8])

                    texto += 'ID: ' + str(id) + '\n' + str(libro) + '\n'
                
                self.textarea.insert(tk.INSERT, texto)
        
        except Exception as ex:
            error(ex, "Seguramente no se ha podido acceder a la base de datos\n'biblioteca.db' porque está corrupta. De ser el caso,\n\
cierre el programa, mueva la base de datos a otra\nubicación y repárela manualmente con el software\n'DB Browser (SQLite)' conseguido en\n\
'https://sqlitebrowser.org/'. De no ser el caso, la\nsolución es desconocida.")
        finally:
            conexion.close()

# Ventana para registrar un préstamo.
class VentanaReg:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title('Registrar un préstamo')
        self.ventana.geometry('300x160')

        labelNombre = tk.Label(self.ventana, text = 'Nombre de la persona:')
        labelNombre.grid(column=0, row=0)
        labelNombre.configure(foreground = 'black')

        labelTeléfono = tk.Label(self.ventana, text = 'Teléfono de la persona:')
        labelTeléfono.grid(column=0, row=1)
        labelTeléfono.configure(foreground = 'black')

        labelMail = tk.Label(self.ventana, text = 'Mail de la persona:')
        labelMail.grid(column=0, row=2)
        labelMail.configure(foreground = 'black')

        labelFechaDeInicio = tk.Label(self.ventana, text = 'Fecha de inicio:')
        labelFechaDeInicio.grid(column=0, row=3)
        labelFechaDeInicio.configure(foreground = 'black')

        labelFechaDeDevolución = tk.Label(self.ventana, text = 'Fecha de devolución:')
        labelFechaDeDevolución.grid(column=0, row=4)
        labelFechaDeDevolución.configure(foreground = 'black')

        labelLibro = tk.Label(self.ventana, text = 'Libro a prestar:')
        labelLibro.grid(column=0, row=5)
        labelLibro.configure(foreground = 'black')

        self.datoNombre = tk.StringVar(self.ventana)
        self.entryNombre = tk.Entry(self.ventana, width=10, textvariable = self.datoNombre)
        self.entryNombre.grid(column=1, row=0)

        self.datoTeléfono = tk.IntVar(self.ventana)
        self.entryTeléfono = tk.Entry(self.ventana, width=10, textvariable = self.datoTeléfono)
        self.entryTeléfono.grid(column=1, row=1)

        self.datoMail = tk.StringVar(self.ventana)
        self.entryMail = tk.Entry(self.ventana, width=10, textvariable = self.datoMail)
        self.entryMail.grid(column=1, row=2)

        self.datoFechaDeInicio = tk.StringVar(self.ventana)
        self.entryFechaDeInicio = tk.Entry(self.ventana, width=10, textvariable = self.datoFechaDeInicio)
        self.entryFechaDeInicio.grid(column=1, row=3)

        self.datoFechaDeDevolución = tk.StringVar(self.ventana)
        self.entryFechaDeDevolución = tk.Entry(self.ventana, width=10, textvariable = self.datoFechaDeDevolución)
        self.entryFechaDeDevolución.grid(column=1, row=4)

        self.datoLibro = tk.StringVar(self.ventana)
        self.entryLibro = tk.Entry(self.ventana, width=10, textvariable = self.datoLibro)
        self.entryLibro.grid(column=1, row=5)

        botonAceptar = tk.Button(self.ventana, text = 'Aceptar', command = self.reg)
        botonAceptar.grid(column=1, row=12)

        self.ventana.mainloop()

    # Registrar un préstamo.
    def reg(self):
        disponible = True
        try:
            conexion = sqlite3.connect('biblioteca.db')
            datos = (self.datoNombre.get(), self.datoTeléfono.get(), self.datoMail.get(), self.datoFechaDeInicio.get(), self.datoFechaDeDevolución.get(), self.datoLibro.get())
            
            # Confirmar que el libro existe y está disponible.
            sql = 'select condición from libros where título=?'
            título = self.datoLibro.get()
            #print(f'Debug: _ SQL: {sql}, Título: {título}')
            cursorLibroDisponible = conexion.execute(sql, (título, ))
            fila = cursorLibroDisponible.fetchone()

            if fila == None:
                error(KeyError, f"No se encontró ningún libro con título '{título}'.\nPorfavor, intente de nuevo con otro título.")
                disponible = False
            else:
                print(f"El libro '{título}' existe.")

            if fila[0] == 0 or fila[0] == 2 or fila[0] == 3:
                error(KeyError, f"La condición del libro no es 'Disponible'.")
                disponible = False
            else:
                print(f"El libro '{título}' existe.")

            if disponible:
                try:
                    conexion.execute('''create table prestamos (
                                    id integer primary key AUTOINCREMENT,  
                                    nombre text,
                                    telefono integer,
                                    mail text,
                                    fecha_de_inicio text,
                                    fecha_de_devolucion text,
                                    libro text
                                    )''')
                    print("Se creó la tabla 'prestamos'.")
                except:
                    print("La tabla 'prestamos' ya existe.")
                conexion.execute('insert into prestamos(nombre,telefono,mail,fecha_de_inicio,fecha_de_devolucion,libro) values(?,?,?,?,?,?)', datos)
                conexion.commit()
                conexion.execute('update libros set condición=? where título=?', (0, título)) # Cambiar la condición del libro a 'Préstamo en proceso'.
                conexion.commit()
                exito(f"Préstamo del libro '{self.datoLibro.get()}'\na {self.datoNombre.get()}\ncargado con éxito.")
        except tk.TclError as tcler:
            error(tcler, "Dato inválido. Seguramente haya puesto un carácter\nno numérico en el campo 'Teléfono'.")
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()

# Ventana para dar por terminado un préstamo.
class VentanaTermin:
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.title('Terminar un préstamo')
        self.ventana.geometry('450x150')

        labelBuscadorId = tk.Label(self.ventana, text = 'Buscar préstamo por su ID:')
        labelBuscadorId.grid(column=0, row=0)
        labelBuscadorId.configure(foreground = 'black')

        self.datoBuscadorId = tk.IntVar(self.ventana)
        self.entryBuscadorId = tk.Entry(self.ventana, width=10, textvariable = self.datoBuscadorId)
        self.entryBuscadorId.grid(column=1, row=0)
    
        botonBuscadorId = ttk.Button(self.ventana, text = 'Buscar', command = self.buscarPorId)
        botonBuscadorId.grid(column=2, row=0)

        botonDarDeBaja = ttk.Button(self.ventana, text = 'Terminar', command = self.termin)
        botonDarDeBaja.grid(column=3, row=0)

        self.labelDisplay = tk.Label(self.ventana, text = 'Préstamo:\n\n-')
        self.labelDisplay.grid(column=0, row=1)
        self.labelDisplay.configure(foreground = 'black')

        self.ventana.mainloop()

    # Buscar préstamo por su ID.
    def buscarPorId(self):
        fila = []
        id = 0
        try:
            conexion = sqlite3.connect('biblioteca.db')
            sql = 'select nombre,telefono,mail,fecha_de_inicio,fecha_de_devolucion,libro from prestamos where id=?'
            id = self.datoBuscadorId.get()
            #print(f'Debug: _ SQL: {sql}, ID: {id}')
            cursor = conexion.execute(sql, (id, ))
            fila = cursor.fetchone()
        except tk.TclError as tcler:
            error(tcler, f"Dato inválido. El texto '{id}' ingresado en el campo 'ID'\nno es numérico o estaba vacío. Debe ingresar un número\nentero positivo.")
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()

        if fila != None:
            try:
                pres = Prestamo()
                pres.persona.nombre = fila[0]
                pres.persona.teléfono= int(fila[1])
                pres.persona.mail = fila[2]
                pres.fecha_de_inicio = fila[3]
                pres.fecha_de_devolución = fila[4]
                pres.libro.título = fila[5]

                self.labelDisplay.configure(text = 'Préstamo:\n\n' + str(pres))
            except IndexError as ier:
                error(ier, f"El índice de la lista de datos recolectados de la base de\ndatos está fuera de rango. Debido a que se buscó con el\n\
campo 'Buscar préstamo por su ID' vacío. Es un error leve\nque se soluciona al salir.")
            except Exception as ex:
                error(ex, 'Solución desconocida.')
        else:
            error(KeyError, f'No se encontró ningún préstamo con ID = {id}.\nPorfavor, intente de nuevo con otro número.')

    # Dar por terminado un préstamo.
    def termin(self):
        fila = []
        id = 0
        try:
            conexion = sqlite3.connect('biblioteca.db')
            sql_buscar = 'select nombre,telefono,mail,fecha_de_inicio,fecha_de_devolucion,libro from prestamos where id=?'
            id = self.datoBuscadorId.get()
            #print(f'Debug: _ ID: {id}')
            cursor = conexion.execute(sql_buscar, (id, ))
            fila = cursor.fetchone()

            if fila != None:
                # Eliminar préstamo de la base de datos 'biblioteca.db'.
                sql_eliminar = '''delete from prestamos where id = ?'''
                cursor.execute(sql_eliminar, (id, ))
                conexion.commit()

                # Cambiar la condición del libro a 'Disponible'.
                cursor2 = conexion.execute('update libros set condición=? where título=?', (1, fila[5]))
                conexion.commit()

                exito(f"Préstamo del libro '{fila[5]}' a {fila[0]} terminado con éxito.")
            else:
                error(KeyError, f'No se encontró ningún préstamo con ID = {id}.\nPorfavor, intente de nuevo con otro número.')
            
        except IndexError as ier:
            error(ier, f"El índice de la lista de datos recolectados de la base de\ndatos está fuera de rango. Debido a que se buscó con el\n\
campo 'Buscar préstamo por su ID' vacío. Es un error leve\nque se soluciona al salir.")
        except tk.TclError as tcler:
            error(tcler, f"Dato inválido. El texto '{id}' ingresado en la entrada\nno es numérico o estaba vacío. Debe ingresar un número\nentero positivo.")
        except Exception as ex:
            error(ex, 'Solución desconocida.')
        finally:
            conexion.close()

# Ventana para reclamar un préstamo.
'''
Esta situación se plantea cuando el usuario controla 
los préstamos vigentes y el programa detecta que hay préstamos que no se 
devolvieron, inmediatamente el programa muestra los datos de la persona a la
que se le prestó el libro para que el usuario pueda comunicarse con él/ella 
y así poder acordar la devolución.
'''
class VentanaRecl:
    def __init__(self, pres):
        ventana = tk.Tk()
        ventana.title('Advertencia de retraso en la devolución de libro')
        ventana.geometry('400x180')

         # Advertencia de retraso en la devolución de libro.
        label = tk.Label(ventana, text = f"Retraso en la devolución de libro:\n\n{pres.persona.nombre} no ha devuelto el libro '{pres.libro.título}' a tiempo.\n\n\
Fecha de devolución: {pres.fecha_de_devolución}\nFecha actual: {dt.datetime.now().date()}\n\n\
Persona:\n\
_ Nombre: {pres.persona.nombre}\n\
_ Mail: {pres.persona.mail}\n\
_ Teléfono: {pres.persona.teléfono}\n\
")
        label.grid(column=0, row=0)
        label.configure(foreground = 'black')

        ventana.mainloop()

 