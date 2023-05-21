from flask import *
from models import *
from settings import Settings
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# import views.admin_overwrite as admin_overwrite

app = Flask(__name__)
app.config.from_object(Settings)
admin = Admin(app, name='Database')
db.init_app(app)
admin._menu = admin._menu[1:]

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Chair, db.session))

from views.api_views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
