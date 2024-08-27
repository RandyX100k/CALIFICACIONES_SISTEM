#conexion
class DB():
    def __init__(self,host,user,clave,db):
        self.host = host
        self.user = user
        self.clave = clave
        self.db = db