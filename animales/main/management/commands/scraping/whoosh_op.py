import os
import shutil
import ssl
from tkinter import *
from tkinter import messagebox
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import query
from scraping.scraping import extraer_datos_principal
from whoosh import qparser, index, query
from whoosh.query import Every, And, Term, NumericRange

# Asegurando que SSL funcione correctamente
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def cargar():
    if index.exists_in("Index"):
        respuesta = messagebox.askyesno(title="Confirmar", message="El índice ya existe. \n¿Está seguro que quiere recargar los datos?. \nEsta operación puede ser lenta")
        if respuesta:
            almacenar_datos()
    else:
        almacenar_datos()

def almacenar_datos():
    schema = Schema(
        nombre=TEXT(stored=True),
        tipo=TEXT(stored=True),
        genero=TEXT(stored=True),
        raza=TEXT(stored=True),
        edad=NUMERIC(stored=True),
        tamano=TEXT(stored=True),
        url_foto=ID(stored=True),
        url_detalle=ID(stored=True)
    )

    # Eliminamos el directorio del índice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    
    os.mkdir("Index")
    ix = create_in("Index", schema=schema)
    writer = ix.writer()
    lista = extraer_datos_principal()
    for animal in lista:
        writer.add_document(
            nombre=animal[0],
            tipo=animal[1],
            genero=animal[2],
            raza=animal[3],
            edad=animal[4],
            tamano=animal[5],
            url_foto=animal[6],
            url_detalle=animal[7]
        )
    writer.commit()
    messagebox.showinfo("Fin de indexado", f"Se han indexado {len(lista)} animales")

def imprimir_lista(results):
    v = Toplevel()
    v.title("Lista de Animales")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    displayed_results = set()
    for row in results:
        unique_id = row['url_detalle']  # Evitar duplicados
        if unique_id not in displayed_results:
            displayed_results.add(unique_id)
            lb.insert(END, f"Nombre: {row['nombre']}")
            lb.insert(END, f"    Tipo: {row['tipo']}")
            lb.insert(END, f"    Género: {row['genero']}")
            lb.insert(END, f"    Raza: {row['raza']}")
            lb.insert(END, f"    Edad: {row.get('edad', 'Desconocido')}")
            lb.insert(END, f"    Tamaño: {row['tamano']}")
            lb.insert(END, f"    URL Foto: {row['url_foto']}")
            lb.insert(END, f"    URL Detalle: {row['url_detalle']}")
            lb.insert(END, "\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)

def imprimir_lista_1(results):
    v = Toplevel()
    v.title("Lista de Animales")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    displayed_results = set()
    for row in results:
        unique_id = row['url_detalle']  # Evitar duplicados
        if unique_id not in displayed_results:
            displayed_results.add(unique_id)
            lb.insert(END, row['nombre'])
            lb.insert(END, f"    Raza: {row['raza']}")
            lb.insert(END, "\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)

def buscar_nombre_o_raza():
    def mostrar_lista(event):
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            query = MultifieldParser(["nombre", "raza"], ix.schema).parse('"' + str(en.get()) + '"')
            results = searcher.search(query, limit=None)
            imprimir_lista_1(results)
    
    v = Toplevel()
    v.title("Búsqueda por Nombre o Raza")
        
    l1 = Label(v, text="Escriba el nombre o raza de algún animal:")
    l1.pack(side=LEFT)
    en = Entry(v, width=75)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)

def buscar_por_genero():
    def mostrar_lista():
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            selected_gender = gender_var.get()
            query = QueryParser("genero", ix.schema).parse(selected_gender)
            results = searcher.search(query, limit=None)
            imprimir_lista(results)
    
    v = Toplevel()
    v.title("Búsqueda por Género")
    
    l = Label(v, text="Seleccione el género:")
    l.pack(side=LEFT)
    
    gender_var = StringVar()
    gender_var.set("Macho")  # Valor predeterminado
    
    gender_spinbox = Spinbox(v, values=["Macho", "Hembra"], textvariable=gender_var, state="readonly")
    gender_spinbox.pack(side=LEFT)
    
    search_button = Button(v, text="Buscar", command=mostrar_lista)
    search_button.pack(side=LEFT)

def buscar_por_tipo():
    def mostrar_lista():
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            selected_type = type_var.get()
            query = QueryParser("tipo", ix.schema).parse(selected_type)
            results = searcher.search(query, limit=None)
            imprimir_lista(results)
    
    v = Toplevel()
    v.title("Búsqueda por Tipo")
    
    l = Label(v, text="Seleccione el tipo:")
    l.pack(side=LEFT)
    
    type_var = StringVar()
    type_var.set("Perro")  # Valor predeterminado
    
    type_spinbox = Spinbox(v, values=["Perro", "Gato"], textvariable=type_var, state="readonly")
    type_spinbox.pack(side=LEFT)
    
    search_button = Button(v, text="Buscar", command=mostrar_lista)
    search_button.pack(side=LEFT)


def buscar_por_tamano():
    def mostrar_lista(event=None):
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            lista_tamanos = [size.decode('utf-8') for size in searcher.lexicon('tamano')]
            selected_size = size_var.get()
            query = QueryParser("tamano", ix.schema).parse(selected_size)
            results = searcher.search(query, limit=None)
            imprimir_lista(results)

    v = Toplevel()
    v.title("Búsqueda por Tamaño")

    l = Label(v, text="Seleccione el tamaño:")
    l.pack(side=LEFT)

    size_var = StringVar()
    size_var.set("Pequeño")  # Valor predeterminado

    ix = open_dir("Index")
    with ix.searcher() as searcher:
        lista_tamanos = [size.decode('utf-8') for size in searcher.lexicon('tamano')]

    size_spinbox = Spinbox(v, values=lista_tamanos, textvariable=size_var, state="readonly")
    size_spinbox.pack(side=LEFT)

    search_button = Button(v, text="Buscar", command=mostrar_lista)
    search_button.pack(side=LEFT)






def buscar_por_tipo_y_tamano():
    def mostrar_lista():
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            tipo_seleccionado = type_var.get()
            tamano_seleccionado = size_var.get()
            # Construir la consulta correctamente
            query_tipo = QueryParser("tipo", ix.schema).parse(f'"{tipo_seleccionado}"')
            query_tamano = QueryParser("tamano", ix.schema).parse(f'"{tamano_seleccionado}"')
            query = query_tipo & query_tamano
            results = searcher.search(query, limit=None)
            imprimir_lista(results)
    
    v = Toplevel()
    v.title("Búsqueda por Tipo y Tamaño")
    
    l = Label(v, text="Seleccione el tipo:")
    l.pack(side=LEFT)
    
    # Spinbox para seleccionar el tipo
    type_var = StringVar()
    type_var.set("Perro")  # Valor predeterminado
    type_spinbox = Spinbox(v, values=["Perro", "Gato"], textvariable=type_var, state="readonly")
    type_spinbox.pack(side=LEFT)
    
    l1 = Label(v, text="Seleccione el tamaño:")
    l1.pack(side=LEFT)
    
    # Spinbox para seleccionar el tamaño
    size_var = StringVar()
    size_var.set("Pequeño")  # Valor predeterminado

    ix = open_dir("Index")
    with ix.searcher() as searcher:
        lista_tamanos = [size.decode('utf-8') for size in searcher.lexicon('tamano')]

    size_spinbox = Spinbox(v, values=lista_tamanos, textvariable=size_var, state="readonly")
    size_spinbox.pack(side=LEFT)

    # Botón de búsqueda
    b = Button(v, text="Buscar", command=mostrar_lista)
    b.pack(side=LEFT)


def buscar_por_rango_edades():
    def mostrar_lista():
        ix = open_dir("Index")
        with ix.searcher() as searcher:

            # Obtenemos los valores mínimo y máximo de edad insertados por el usuario
            start_age = int(start_var.get())
            end_age = int(end_var.get())
            # Creamos la consulta con el rango de edades
            query_range = NumericRange("edad", start_age, end_age)
            results = searcher.search(query_range, limit=None)
            imprimir_lista(results)

    v = Toplevel()
    v.title("Búsqueda por rango de edades")
    
    l1 = Label(v, text="Edad mínima:")
    l1.pack(side=LEFT)
    
    # Campo para insertar la edad mínima
    start_var = IntVar()
    en_start = Entry(v, textvariable=start_var)
    en_start.pack(side=LEFT)

    l2 = Label(v, text="Edad máxima:")
    l2.pack(side=LEFT)

    # Campo para insertar la edad mínima
    end_var = IntVar()
    en_end = Entry(v, textvariable=end_var)
    en_end.pack(side=LEFT)

    # Botón de búsqueda
    b = Button(v, text="Buscar", command=mostrar_lista)
    b.pack(side=LEFT)

def buscar_avanzado():
    def mostrar_lista():
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            conditions = []

            # Construye la consulta, ahora con todo en minúsculas
            if tipo_var.get():
                conditions.append(Term("tipo", tipo_var.get().lower()))

            if genero_var.get():
                conditions.append(Term("genero", genero_var.get().lower()))

            if raza_var.get():
                conditions.append(Term("raza", raza_var.get().lower()))

            if edad_min_var.get() and edad_max_var.get():
                conditions.append(NumericRange("edad", int(edad_min_var.get()), int(edad_max_var.get())))

            if tamano_var.get():
                conditions.append(Term("tamano", tamano_var.get().lower()))

            # Crear la consulta combinada
            if conditions:
                query = And(conditions)
            else:
                query = Every()

            results = searcher.search(query, limit=None)
            imprimir_lista(results)

    v = Toplevel()
    v.title("Búsqueda personalizada: No tienes que rellenar todos los campos")

    Label(v, text="Tipo:").pack(side=LEFT)
    tipo_var = StringVar()
    tipo_spinbox = Spinbox(v, values=["", "Perro", "Gato"], textvariable=tipo_var, state="readonly")
    tipo_spinbox.pack(side=LEFT)

    Label(v, text="Género:").pack(side=LEFT)
    genero_var = StringVar()
    genero_spinbox = Spinbox(v, values=["", "Macho", "Hembra"], textvariable=genero_var, state="readonly")
    genero_spinbox.pack(side=LEFT)

    Label(v, text="Raza:").pack(side=LEFT)
    raza_var = StringVar()
    Entry(v, textvariable=raza_var).pack(side=LEFT)

    Label(v, text="Edad mínima:").pack(side=LEFT)
    edad_min_var = StringVar()
    Entry(v, textvariable=edad_min_var).pack(side=LEFT)

    Label(v, text="Edad máxima:").pack(side=LEFT)
    edad_max_var = StringVar()
    Entry(v, textvariable=edad_max_var).pack(side=LEFT)

    Label(v, text="Tamaño:").pack(side=LEFT)
    tamano_var = StringVar()
    ix = open_dir("Index")
    with ix.searcher() as searcher:
        lista_tamanos = [""]
        lista_tamanos.extend([size.decode('utf-8') for size in searcher.lexicon('tamano')])




    tamano_spinbox = Spinbox(v, values=lista_tamanos, textvariable=tamano_var, state="readonly")
    tamano_spinbox.pack(side=LEFT)

    Button(v, text="Buscar", command=mostrar_lista).pack(side=LEFT)





def ventana_principal():
    def listar_todo():
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            results = searcher.search(query.Every(), limit=None)
            imprimir_lista(results)
          
    root = Tk()
    root.geometry("150x100")

    menubar = Menu(root)
    
    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=cargar)
    datosmenu.add_command(label="Listar", command=listar_todo)
    datosmenu.add_separator()   
    datosmenu.add_command(label="Salir", command=root.quit)
    
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Nombre o Raza", command=buscar_nombre_o_raza)
    
    buscarmenu.add_command(label="Género", command=buscar_por_genero)
    
    buscarmenu.add_command(label="Tipo", command=buscar_por_tipo)
    
    buscarmenu.add_command(label="Tamaño", command=buscar_por_tamano)
    
    buscarmenu.add_command(label="Tipo y Tamaño", command=buscar_por_tipo_y_tamano)

    buscarmenu.add_command(label="Rango Edades", command=buscar_por_rango_edades)



    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)

    menubar.add_command(label="Búsqueda Personalizada", command=buscar_avanzado)



        
    root.config(menu=menubar)
    root.mainloop()







if __name__ == "__main__":
    ventana_principal()


