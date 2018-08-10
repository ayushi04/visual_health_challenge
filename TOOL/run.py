import os
import config
from app import app
from controllers import mod_controllers

app.register_blueprint(mod_controllers)
os.system('mkdir ' + config.STATIC_DIR)
os.system('mkdir ' + config.UPLOADS_DIR)
print('App ready to run')

app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
