from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import mapping_config
from app import createApp
from app import db


app = createApp(mapping_config['dev'])
# 扩展
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

import www
if __name__ == '__main__':
    # app.run()
    manager.run()