from wgpt_cd import app, db
from wgpt_cd.models import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

