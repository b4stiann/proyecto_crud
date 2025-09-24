import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from flask import flash
from base.config.mysqlconnection import connectToMySQL


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


@dataclass
class Usuario:
    id: int
    nombre: str
    apellido: str
    email: str
    password: str
    created_at: Any
    updated_at: Any

    db: str = 'citas_db'

    @classmethod
    def crear(cls, data: Dict[str, Any]) -> int:
        query = (
            "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) "
            "VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());"
        )
        res = connectToMySQL(cls.db).query_db(query, data)
        return int(res[0]['lastrowid'])

    @classmethod
    def obtener_por_email(cls, email: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM usuarios WHERE email=%(email)s LIMIT 1;"
        rows = connectToMySQL(cls.db).query_db(query, {"email": email})
        return rows[0] if rows else None

    @classmethod
    def obtener_por_id(cls, usuario_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM usuarios WHERE id=%(id)s;"
        rows = connectToMySQL(cls.db).query_db(query, {"id": usuario_id})
        return rows[0] if rows else None

    @staticmethod
    def validar_registro(form: Dict[str, str]) -> bool:
        is_valid = True
        nombre = (form.get('nombre') or '').strip()
        apellido = (form.get('apellido') or '').strip()
        email = (form.get('email') or '').strip().lower()
        password = form.get('password') or ''
        confirm_password = form.get('confirm_password') or ''

        if len(nombre) < 2:
            flash('El nombre debe tener al menos 2 caracteres.', 'registro')
            is_valid = False
        if len(apellido) < 2:
            flash('El apellido debe tener al menos 2 caracteres.', 'registro')
            is_valid = False
        if not EMAIL_REGEX.match(email):
            flash('Email inválido.', 'registro')
            is_valid = False
        else:
            if Usuario.obtener_por_email(email):
                flash('El email ya está registrado.', 'registro')
                is_valid = False
        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'registro')
            is_valid = False
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'registro')
            is_valid = False
        return is_valid

