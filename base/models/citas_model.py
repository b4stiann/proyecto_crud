from typing import Any, Dict, List, Optional
from base.config.mysqlconnection import connectToMySQL
from flask import flash


class Cita:
    db: str = 'citas_db'

    @staticmethod
    def validar_cita(form: Dict[str, str]) -> bool:
        is_valid = True
        texto = (form.get('cita') or '').strip()
        autor = (form.get('autor') or '').strip()
        if len(texto) < 5:
            flash('La cita debe tener al menos 5 caracteres.', 'cita')
            is_valid = False
        if len(autor) < 3:
            flash('El autor debe tener al menos 3 caracteres.', 'cita')
            is_valid = False
        return is_valid

    @classmethod
    def crear(cls, data: Dict[str, Any]) -> int:
        query = (
            "INSERT INTO citas (cita, autor, usuario_id, created_at, updated_at) "
            "VALUES (%(cita)s, %(autor)s, %(usuario_id)s, NOW(), NOW());"
        )
        res = connectToMySQL(cls.db).query_db(query, data)
        return int(res[0]['lastrowid'])

    @classmethod
    def obtener_todas(cls) -> List[Dict[str, Any]]:
        query = (
            "SELECT c.*, u.nombre, u.apellido FROM citas c "
            "JOIN usuarios u ON u.id = c.usuario_id "
            "ORDER BY c.created_at DESC;"
        )
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def obtener_por_id(cls, cita_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM citas WHERE id=%(id)s;"
        rows = connectToMySQL(cls.db).query_db(query, {"id": cita_id})
        return rows[0] if rows else None

    @classmethod
    def actualizar(cls, data: Dict[str, Any]) -> None:
        query = "UPDATE citas SET cita=%(cita)s, autor=%(autor)s, updated_at=NOW() WHERE id=%(id)s;"
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def borrar(cls, cita_id: int) -> None:
        connectToMySQL(cls.db).query_db("DELETE FROM favoritos WHERE cita_id=%(id)s;", {"id": cita_id})
        connectToMySQL(cls.db).query_db("DELETE FROM citas WHERE id=%(id)s;", {"id": cita_id})

    @classmethod
    def obtener_por_usuario(cls, usuario_id: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM citas WHERE usuario_id=%(uid)s ORDER BY created_at DESC;"
        return connectToMySQL(cls.db).query_db(query, {"uid": usuario_id})

    # Favoritos
    @classmethod
    def agregar_favorito(cls, usuario_id: int, cita_id: int) -> None:
        query = (
            "INSERT IGNORE INTO favoritos (usuario_id, cita_id, created_at) VALUES (%(uid)s, %(cid)s, NOW());"
        )
        connectToMySQL(cls.db).query_db(query, {"uid": usuario_id, "cid": cita_id})

    @classmethod
    def quitar_favorito(cls, usuario_id: int, cita_id: int) -> None:
        query = "DELETE FROM favoritos WHERE usuario_id=%(uid)s AND cita_id=%(cid)s;"
        connectToMySQL(cls.db).query_db(query, {"uid": usuario_id, "cid": cita_id})

    @classmethod
    def obtener_favoritos_de_usuario(cls, usuario_id: int) -> List[Dict[str, Any]]:
        query = (
            "SELECT c.* FROM favoritos f JOIN citas c ON c.id = f.cita_id "
            "WHERE f.usuario_id=%(uid)s ORDER BY f.created_at DESC;"
        )
        return connectToMySQL(cls.db).query_db(query, {"uid": usuario_id})

    @classmethod
    def es_favorito(cls, usuario_id: int, cita_id: int) -> bool:
        query = "SELECT 1 FROM favoritos WHERE usuario_id=%(uid)s AND cita_id=%(cid)s LIMIT 1;"
        rows = connectToMySQL(cls.db).query_db(query, {"uid": usuario_id, "cid": cita_id})
        return bool(rows)
