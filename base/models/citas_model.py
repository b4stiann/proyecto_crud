from base.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Cita:
    @classmethod
    def obtener_citas_usuarios(cls, usuario_id):
        query = "SELECT * FROM citas WHERE autor_id =%(usuario_id)s;"
        data = {'usuario_id': usuario_id}
        resultado = connectToMySQL(cls.db).query_db(query, data)

        