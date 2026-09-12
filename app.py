from flask import Flask, request
from database import conectar_bd

app = Flask(__name__)


@app.route("/probar")
def probar_data():
    conec = conectar_bd()

    if conec.is_connected():
        conec.close()

    return {
        "mensaje": "conexion ok"
    }


# consultar hv por id
@app.route("/api/consultahv/<int:id>", methods=["GET"])
def obtener_hvida(id):

    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)
    sql = """SELECT * FROM hojas_vida WHERE id=%s"""
    cursor.execute(sql, (id,))

    datos = cursor.fetchone()

    cursor.close()
    conec.close()

    # que pasa cuando es nulo
    if datos is None:
        return {"no se encontro la hoja de vida"}

    return datos


# eliminar
@app.route("/api/eliminarhv/<int:id>", methods=["DELETE"])
def eliminar_hv(id):
    conec = conectar_bd()
    cursor = conec. cursor()

    cursor.execute("SELECT id FROM hojas_vida WHERE id=%s",(id,))
    existe = cursor.fetchone()

    if existe is None:
        cursor.close()
        conec.close()
        return ("no se encontro la hoja de vida")

    sql = "DELETE FROM hojas_vida WHERE id=%s"
    cursor.execute(sql, (id,))
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Hoja de vida eliminada correctamente"
    }


# actualizar
@app.route("/api/actualizarhv/<int:id>", methods=["PUT"])
def actualizarhojavida(id):
    datos = request.get_json()
    conexion = conectar_bd()
    cursor = conexion.cursor(buffered=True)

    #Verificar que la hoja exista
    buscar = "SELECT id FROM hojas_vida where id = %s"
    cursor.execute(buscar,(id,))
    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conexion.close()
        return{
            "Mensaje" : "No se encontro la hoja de vida"
        }
    sqlcorreo = "SELECT id FROM hojas_vida where Correo = %s and id != %s"
    cursor.execute(sqlcorreo,(datos["Correo"], id))
    resultado = cursor.fetchone()

    if resultado is not None:
            cursor.close()
            conexion.close()
            return{
                "Mensaje" : "correo electronico ya esta registrado en otra hoja de vida"
            }
    sqlactualizar = "UPDATE hojas_vida SET Nombre = %s, Ciudad = %s, Edad = %s, Correo = %s, Fotografia = %s, Programa = %s, Ficha = %s, Jornada = %s WHERE id = %s"
    valores = (datos["Nombre"],
                 datos["Ciudad"],
                 datos["Edad"],
                 datos["Correo"],
                 datos.get("Fotografia"),
                 datos["Programa"],
                 datos["Ficha"],
                 datos["Jornada"],
                 id)
    
    cursor.execute(sqlactualizar,valores)
    conexion.commit()
    cursor.close()
    
    return{
        "Mensaje" : "hoja de vida actualizada",
        "id":id
    }




# registrar hoja_vida
@app.route("/api/registrohv", methods=["POST"])
def registrohv():
    conec = conectar_bd()
    cursor = conec.cursor()
    datos = request.json

    # Consultar si el correo existe
    sql_consulta = "SELECT id FROM hojas_vida WHERE correo = %s"
    cursor.execute(sql_consulta, (datos["correo"],))

    resultado = cursor.fetchone()

    if resultado:
        cursor.close()
        conec.close()

        return {
            "mensaje": "El usuario ya existe"
        }

    # Registrar hoja de vida
    sql = """
        INSERT INTO hojas_vida
        (nombre, edad, ciudad, correo, fotografia, programa, ficha, jornada)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    valor = (
        datos["nombre"],
        datos["edad"],
        datos["ciudad"],
        datos["correo"],
        datos.get("fotografia"),
        datos["programa"],
        datos["ficha"],
        datos["jornada"]
    )

    cursor.execute(sql, valor)
    conec.commit()

    # Manejo del ID
    id_generado = cursor.lastrowid

    cursor.close()
    conec.close()

    return {
        "mensaje": "hoja de vida creada",
        "id": id_generado
    }


@app.route("/")
def inicio():
    return "conexion exitosa"


# Obtener una hoja de vida por ID
@app.route("/api/hojas_vida/<int:id>")
def obtener_hojas_vidaid(id):
    return {
        "mensaje": "Hoja de vida encontrada","id": id
    }


# Hacer un listado de hojas de vida
@app.route("/api/hojas_vida")
def obtener_hojas_vida():
    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hojas_vida")

    hojas_vida = cursor.fetchall()

    cursor.close()
    conec.close()

    return hojas_vida



#taller


# registrar un estudio
@app.route("/api/registrarestu/<int:id>", methods=["POST"])
def registrar_estudio(id):

    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()

    # Verificar que exista la hoja de vida
    sql = "SELECT id FROM hojas_vida WHERE id = %s"
    cursor.execute(sql, (id,))
    hoja = cursor.fetchone()

    if hoja is None:
        cursor.close()
        conec.close()

        return {
            "mensaje": "No se encontró la hoja de vida"
        }

    # Registrar estudio
    sql = """
        INSERT INTO estudios (hoja_vida_id, nivel, institucion, titulo, anio_graduacion) 
         """

    valor = (
        id,
        datos["nivel"],
        datos["institucion"],
        datos["titulo"],
        datos["anio_graduacion"]
    )

    cursor.execute(sql, valor)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Estudio registrado correctamente"
    }


#consultar estudio

@app.route("/api/consultarestu/<int:id>", methods=["GET"])
def consultar_estudios(id):

    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)

    sql = "SELECT * FROM estudios WHERE hoja_vida_id = %s"
    cursor.execute(sql, (id,))

    estudios = cursor.fetchall()

    cursor.close()
    conec.close()

    return estudios


#consultar estudio especifico
@app.route("/api/consultarestuespecifico/<int:id>", methods=["GET"])
def consultar_estudio_especifico(id):

    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)

    sql = "SELECT * FROM estudios WHERE id = %s"
    cursor.execute(sql, (id,))

    estudio = cursor.fetchone()

    cursor.close()
    conec.close()

    if estudio is None:
        return {
            "mensaje": "No se encontró el estudio"
        }

    return estudio

#actualizar

@app.route("/api/actualizarestu/<int:id>", methods=["PUT"])
def actualizar_estudio(id):

    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT id FROM estudios WHERE id = %s"
    cursor.execute(sql, (id,))
    estudio = cursor.fetchone()

    if estudio is None:
        cursor.close()
        conec.close()
        return {
            "mensaje": "No se encontró el estudio"
        }

    sql = """
        UPDATE estudios
        SET nivel=%s, institucion=%s, titulo=%s, anio_graduacion=%s WHERE id=%s """

    valor = (
        datos["nivel"],
        datos["institucion"],
        datos["titulo"],
        datos["anio_graduacion"],
        id
    )

    cursor.execute(sql, valor)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Estudio actualizado correctamente"
    }

#eliminar
@app.route("/api/eliminarestu/<int:id>", methods=["DELETE"])
def eliminar_estudio(id):

    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT id FROM estudios WHERE id = %s"
    cursor.execute(sql, (id,))
    estudio = cursor.fetchone()

    if estudio is None:
        cursor.close()
        conec.close()
        return {
            "mensaje": "No se encontró el estudio"
        }

    sql = "DELETE FROM estudios WHERE id = %s"
    cursor.execute(sql, (id,))

    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Estudio eliminado correctamente"
    }

#parte de experiencia

#consultar experiencia
@app.route("/api/consultarexpe/<int:id>", methods=["GET"])
def consultar_expe(id):

    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)
   
    sql = "SELECT * FROM experiencias WHERE hoja_vida_id = %s"
    cursor.execute(sql, (id,))
   
    experiencias = cursor.fetchall()
   
    cursor.close()
    conec.close()
   
    return experiencias



# registrar experiencia
@app.route("/api/registrarexpe/<int:id>", methods=["POST"])
def registrar_experiencia(id):

    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()

    # Verificar que exista la hoja de vida
    sql = "SELECT id FROM hojas_vida WHERE id = %s"
    cursor.execute(sql, (id,))
    hoja = cursor.fetchone()

    if hoja is None:
        cursor.close()
        conec.close()

        return {
            "mensaje": "No se encontró la hoja de vida"
        }

    # Registrar experiencia
    sql = """
        INSERT INTO experiencias (hoja_vida_id, empresa, cargo, tiempo, funciones) VALUES (%s, %s, %s, %s, %s) """

    valor = (
        id,
        datos["empresa"],
        datos["cargo"],
        datos["tiempo"],
        datos["funciones"]
    )

    cursor.execute(sql, valor)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "experiencia registrado correctamente"
    }
    

#consultar una experiencia especifica

@app.route("/api/consultarexpeespecifico/<int:id>", methods=["GET"])
def consultar_experiencia_especifico(id):

    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)

    sql = "SELECT * FROM experiencia WHERE id = %s"
    cursor.execute(sql, (id,))

    experiencia = cursor.fetchone()

    cursor.close()
    conec.close()

    if experiencia is None:
        return {
            "mensaje": "No se encontró la experiencia"
        }

    return experiencia

#actualizar una experiencia
@app.route("/api/actualizarexpe/<int:id>", methods=["PUT"])
def actualizar_experiencia(id):

    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT id FROM experiencias WHERE id = %s"
    cursor.execute(sql, (id,))
    estudio = cursor.fetchone()

    if estudio is None:
        cursor.close()
        conec.close()
        return {
            "mensaje": "No se encontró la experiencia"
        }

    sql = """
        UPDATE experiencias SET empresa=%s, cargo=%s, tiempo=%s, funciones=%s WHERE id=%s """

    valor = (
        datos["empresa"],
        datos["cargo"],
        datos["tiempo"],
        datos["funciones"],
        id
    )

    cursor.execute(sql, valor)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Experiencia actualizado correctamente"
    }
    

#eliminar experiencia
@app.route("/api/eliminarexpe/<int:id>", methods=["DELETE"])
def eliminar_experiencia(id):

    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT id FROM experiencias WHERE id = %s"
    cursor.execute(sql, (id,))
    experiencia = cursor.fetchone()

    if experiencia is None:
        cursor.close()
        conec.close()
        return {
            "mensaje": "No se encontró la experiencia"
        }

    sql = "DELETE FROM experiencias WHERE id = %s"
    cursor.execute(sql, (id,))

    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Experiencias eliminado correctamente"
    }


# registrar una habilidad
@app.route("/api/registrarhabilidad/<int:id>", methods=["POST"])
def registrar_habilidad(id):

    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()

    # Verificar que exista la experiencia
    sql = "SELECT id FROM experiencias WHERE id = %s"
    cursor.execute(sql, (id,))
    experiencias = cursor.fetchone()

    if experiencias is None:
        cursor.close()
        conec.close()

        return {
            "mensaje": "No se encontró la experiencia"
        }

    # Registrar habilidad
    sql = """INSERT INTO habilidades (experiencia_id, nombre)
             VALUES (%s, %s)"""

    valor = (
        id,
        datos["nombre"]
    )

    cursor.execute(sql, valor)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Habilidad registrada correctamente"
    }
    
    
#consultar habilidad

@app.route("/api/consultarhabilidad/<int:id>", methods=["GET"])
def consultar_habilidad(id):

    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)
   
    sql = "SELECT * FROM habilidades WHERE experiencia_id = %s"
    cursor.execute(sql, (id,))
   
    habilidades = cursor.fetchall()
   
    cursor.close()
    conec.close()
   
    return habilidades


#actualizar una habilidad
@app.route("/api/actualizarhabilidad/<int:id>", methods=["PUT"])
def actualizar_habilidad(id):

    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT id FROM habilidades WHERE id = %s"
    cursor.execute(sql, (id,))
    habilidad = cursor.fetchone()

    if habilidad is None:
        cursor.close()
        conec.close()
        return {
            "mensaje": "No se encontró la habilidad"
        }

    sql = """
        UPDATE habilidades SET nombre=%s  WHERE id=%s """

    valor = (
        datos["nombre"],
        id
    )

    cursor.execute(sql, valor)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "habilidad actualizado correctamente"
    }
    
#eliminar habilidad
@app.route("/api/eliminarhabilidad/<int:id>", methods=["DELETE"])
def eliminar_habilidad(id):

    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT id FROM habilidades WHERE id = %s"
    cursor.execute(sql, (id,))
    habilidad = cursor.fetchone()

    if habilidad is None:
        cursor.close()
        conec.close()
        return {
            "mensaje": "No se encontró la habilidad"
        }

    sql = "DELETE FROM habilidades WHERE id = %s"
    cursor.execute(sql, (id,))

    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "habilidad eliminado correctamente"
    }
    
    
# consultar cursos

@app.route("/api/consultarcurso/<int:id>", methods=["GET"])
def consultar_curso(id):

    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)

    sql = "SELECT * FROM cursos WHERE hoja_vida_id = %s"
    cursor.execute(sql, (id,))

    cursos = cursor.fetchall()

    cursor.close()
    conec.close()

    return cursos
    

# registrar curso
@app.route("/api/registrarcurso/<int:id>", methods=["POST"])
def registrar_curso(id):

    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()

    # Verificar que exista la hoja de vida
    sql = "SELECT id FROM hojas_vida WHERE id = %s"
    cursor.execute(sql, (id,))
    hoja = cursor.fetchone()

    if hoja is None:
        cursor.close()
        conec.close()

        return {
            "mensaje": "No se encontró la hoja de vida"
        }

    # Registrar curso
    sql = """ INSERT INTO cursos (hoja_vida_id, nombre)  VALUES (%s, %s)"""

    valor = (
        id,
        datos["nombre"]
    )

    cursor.execute(sql, valor)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Curso registrado correctamente"
    }
       
       
# consultar curso específico

@app.route("/api/consultarcursoespecifico/<int:id>", methods=["GET"])
def consultar_curso_especifico(id):

    conec = conectar_bd()
    cursor = conec.cursor(dictionary=True)

    sql = "SELECT * FROM cursos WHERE id = %s"
    cursor.execute(sql, (id,))

    curso = cursor.fetchone()

    cursor.close()
    conec.close()

    if curso is None:
        return {
            "mensaje": "No se encontró el curso"
        }

    return curso

# actualizar curso
@app.route("/api/actualizarcurso/<int:id>", methods=["PUT"])
def actualizar_curso(id):

    datos = request.json
    conec = conectar_bd()
    cursor = conec.cursor()

    # Verificar que exista el curso
    sql = "SELECT id FROM cursos WHERE id = %s"
    cursor.execute(sql, (id,))
    curso = cursor.fetchone()

    if curso is None:
        cursor.close()
        conec.close()

        return {
            "mensaje": "No se encontró el curso"
        }

    # Actualizar curso
    sql = """
        UPDATE cursos SET nombre=%s WHERE id=%s """

    valor = (
        datos["nombre"],
        id
    )

    cursor.execute(sql, valor)
    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Curso actualizado correctamente"
    }


# eliminar curso
@app.route("/api/eliminarcurso/<int:id>", methods=["DELETE"])
def eliminar_curso(id):

    conec = conectar_bd()
    cursor = conec.cursor()

    sql = "SELECT id FROM cursos WHERE id = %s"
    cursor.execute(sql, (id,))
    curso = cursor.fetchone()

    if curso is None:
        cursor.close()
        conec.close()

        return {
            "mensaje": "No se encontró el curso"
        }

    sql = "DELETE FROM cursos WHERE id = %s"
    cursor.execute(sql, (id,))

    conec.commit()

    cursor.close()
    conec.close()

    return {
        "mensaje": "Curso eliminado correctamente"
    }
    
    


if __name__ == "__main__":
  app.run(debug=True)