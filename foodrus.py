from app import app, db
from app.models import User, Box, Indication, Device


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Box':Box, 'Indication':Indication, 'Device':Device}
