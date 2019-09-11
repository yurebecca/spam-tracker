import os
import sys
from api import app

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'api')
    )

context = app.app_context()
context.push()