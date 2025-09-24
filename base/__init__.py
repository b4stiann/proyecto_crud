import os
from datetime import datetime
from flask import Flask, render_template, session, redirect


def _format_date(value, fmt='%d-%m-%Y %H:%M'):
    if value is None:
        return ''
    if isinstance(value, str):
        # Attempt common formats
        for pattern in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
            try:
                value = datetime.strptime(value, pattern)
                break
            except ValueError:
                continue
    return value.strftime(fmt)


def create_app() -> Flask:
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    # Blueprints
    from base.controllers.usuarios import bp as usuarios_bp
    from base.controllers.citas import bp as citas_bp
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(citas_bp, url_prefix='/citas')

    # Jinja filters
    app.add_template_filter(_format_date, name='format_date')

    @app.route('/')
    def index():
        if session.get('usuario_id'):
            return redirect('/citas')
        return render_template('auth.html')

    return app

