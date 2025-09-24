from flask import Flask, render_template
from datetime import datetime

#importar controllers

#definir un filtro de jinja2 para formatear fechas
def format_datetime(value, format='%d-%m-%Y %H:%M'):
    """Format a date time to (Default): d-m-Y H:M"""
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return value.strftime(format)

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='sqlite:///db.sqlite'
    )

    # Registrar los blueprints de los controllers
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(citas_bp)

    app.add_template_filter(format_data)

    @app.route('/')
    def index():
        return render_template('auth.html')