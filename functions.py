import connection

# ----------------------------- ADDING REGISTERS TO DB -----------------------------
def addUser(nombre: str, password: str):
    result = connection.dbExecute(
        """
            SELECT *
            FROM usuarios
            WHERE nombre = %s
        """, (nombre,)
    ).fetchone()

    if(result):
        return None
    else:
        result = connection.dbExecute(
            """INSERT INTO usuarios (nombre, password)
            VALUES (%s, %s)""",
            (nombre, password), commit=True
        )
        return result.lastrowid

def addEvent(nombre: str, fecha: str, ubicacion: str, idUsuario: int):
    result = connection.dbExecute(
        """INSERT INTO eventos (nombre, fecha, ubicacion, idUsuario)
        VALUES (%s,%s,%s,%s)
        """,
        (nombre, fecha, ubicacion, idUsuario), commit=True
    )

    return result.lastrowid

def addImage(rutaImagen: str, descripcion: str, idEvento: int, idUsuario: int):
    imagen = open(rutaImagen, "rb").read()
    result = connection.dbExecute(
        """
            INSERT INTO fotos (imagen, descripcion, idEvento, idUsuario)
            VALUES (%s,%s,%s,%s)
        """,
        (imagen, descripcion, idEvento, idUsuario), commit=True
    )

    return result.lastrowid

def addPerson(nombre: str):
    result = connection.dbExecute(
        """
            INSERT INTO personas (nombre)
            VALUES (%s)
        """,
        (nombre,), commit=True
    )

    return result.lastrowid

def addAparition(nombrePersona: str, idEvento: int):
    result = connection.dbExecute(
        """
            INSERT INTO apariciones (idPersona, idEvento)
            VALUES ((select idPersona from personas where nombre = %s), %s)
        """,
        (nombrePersona, idEvento), commit=True
    )

    return result.lastrowid

# ----------------------------- APP FUNCTIONS -----------------------------
def validLogin(nombre: str, password: str) -> int:
    userId = -1
    result = connection.dbExecute("""
        Select idUsuario 
        FROM usuarios
        WHERE nombre = %s and password = %s
    """, (nombre, password))

    result = result.fetchone()

    if(result):
        userId = result[0]

    return userId

def getAllEvents() -> list:
    result = connection.dbExecute(
        """
            SELECT *
            FROM eventos
        """
    )
    return result.fetchall()

def getImages(idEvento: int) -> list:
    result = connection.dbExecute(
        """
            SELECT imagen, descripcion
            FROM fotos
            WHERE idEvento = %s
        """, (idEvento,)
    )
    return result.fetchall()

def getEvent(idEvento: int) -> tuple:
    result = connection.dbExecute(
        """
            SELECT *
            FROM eventos
            WHERE idEvento = %s
        """, (idEvento,)
    )
    return result.fetchone()

def editEvent(idEvento: int, nombre: str):
    result = connection.dbExecute(
        """
            UPDATE eventos
            SET nombre = %s
            WHERE idEvento = %s
        """, (nombre, idEvento), commit=True
    )

def filterEvents(createdBy, appear, startDate, endDate, location):
    query = """
        select idEvento, nombre
        from eventos
        where true
    """
    params = []

    if(createdBy != ""):
        query += """
            and idUsuario in (
                select idUsuario
                from usuarios
                where nombre = %s
            )
        """
        params.append(createdBy)

    if(appear != ""):
        query += """
            and idEvento in (
                select idEvento 
                from apariciones
                where idPersona in (
                    select idPersona
                    from personas
                    where nombre = %s
                )
            )
        """
        params.append(appear)

    if(startDate != ""):
        query += """
            and fecha >= %s and fecha <= %s
        """
        params.append(createdBy)

    if(location != ""):
        query += """
            and ubicacion = location
        """
        params.append(location)
    
    result = connection.dbExecute(query, tuple(params))

    return result.fetchall()

    """
        select idEvento, nombre
        from eventos
        where true
        and idUsuario in (
            select idUsuario
            from usuarios
            where nombre = %s
        )
        and idEvento in (
            select idEvento 
            from apariciones
            where idPersona in (
                select idPersona
                from personas
                where nombre = %s
            )
        )
        and fecha >= %s and fecha <= %s
        and ubicacion = %s
    """