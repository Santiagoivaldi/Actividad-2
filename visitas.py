import sqlite3
import datetime

"""
datetime.datetime.now().replace(microsecond=0).isoformat()

devuelve fecha hora actual en formato ISO8601 simple

yyyymmddThh:mm:ss

"""

class Persona:
    def __init__(self, dni, apellido, nombre='', movil='', destino=''):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.movil= movil
        self.inside = 0
        self.outside = 0
        self.destino = destino


def ingresa_visita(persona):
    """Guarda los datos de una persona al ingresar"""
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT dni FROM personas WHERE dni = '{persona.dni}'"""

    resu = conn.execute(q)

    if resu.fetchone():
        print("ya existe")
    else:
        q = f"""INSERT INTO personas (dni, nombre, apellido, movil)
                VALUES ('{persona.dni}',
                        '{persona.nombre}',
                        '{persona.apellido}',
                        '{persona.movil}');"""
        print(q)
        conn.execute(q)
        conn.commit()
    
    persona.inside = datetime.datetime.now().replace(microsecond=0).isoformat()

    conn.close()
    

def egresa_visita (persona):
    """Coloca fecha y hora de egreso al visitante con dni dado"""
    persona.outside = datetime.datetime.now().replace(microsecond=0).isoformat()
    conn = sqlite3.connect('recepcion.db')

    r = f"""SELECT dni FROM personas WHERE dni = '{persona.dni}'"""
    x = conn.execute(r)
    if x.fetchone():
        r = f"""INSERT INTO ingresos_egresos (dni, fechahora_in, fechahora_out, destino)
            VALUES ('{persona.dni}',
                    '{persona.inside}',
                    '{persona.outside}',
                    '{persona.destino}');"""
        print(r)
        conn.execute(r)
        conn.commit()
    else:
        r = f"""INSERT INTO ingresos_egresos (dni, fechahora_in, fechahora_out, destino)
            VALUES ('{persona.dni}',
                    '{persona.inside}',
                    '{persona.outside}',
                    '{persona.destino}');"""
        print(r)
        conn.execute(r)
        conn.commit()
    
    persona.outside = datetime.datetime.now().replace(microsecond=0).isoformat()

    conn.close()
    


def lista_visitantes_en_institucion ():
    """Devuelve una lista de objetos Persona presentes en la institución"""
    
    conn = sqlite3.connect('recepcion.db')
    q = f"""SELECT * FROM personas;"""

    resu = conn.execute(q)
    
    for fila in resu:
        print(fila)
    conn.close()


def busca_visitantes(fecha_desde, fecha_hasta, destino, dni):
    """ busca visitantes segun criterios """
    conn = sqlite3.connect('recepcion.db')
    q = f"""SELECT * FROM ingresos_egresos WHERE fechahora_in = '{fecha_desde}' or fechahora_out = '{fecha_hasta}' or destino = '{destino}' and dni = '{dni}'"""
    
    x = conn.execute(q)

    for fila in x:
        print(fila)
    conn.close()




def iniciar():
    conn = sqlite3.connect('recepcion.db')

    qry = '''CREATE TABLE IF NOT EXISTS
                            personas
                    (dni TEXT NOT NULL PRIMARY KEY,
                     nombre   TEXT,
                     apellido TEXT  NOT NULL,
                     movil    TEXT  NOT NULL

           );'''

    conn.execute(qry)

    qry = '''CREATE TABLE IF NOT EXISTS
                            ingresos_egresos
                    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     dni TEXT NOT NULL,
                     fechahora_in TEXT  NOT NULL,
                     fechahora_out TEXT,
                     destino TEXT

           );'''

    conn.execute(qry)


if __name__ == '__main__':
    iniciar()

    """
    p = Persona('28123456', 'Álavarez', 'Ana', '02352-456789')

    ingresa_visita(p)
    """
    
    """
    doc = input("Igrese dni> ")
    apellido = input("Igrese apellido> ")
    nombre = input("nombre> ")
    movil = input("móvil > ")

    p = Persona(doc, apellido, nombre, movil)
    
    ingresa_visita(p)
    """
    
    # lista_visitantes_en_institucion()
    
