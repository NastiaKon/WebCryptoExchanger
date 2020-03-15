from app import app, db
from app.models import User, Roles, Kind_operations, Transactions, Kind_currency
from config import Config
from flask_moment import Moment


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Roles': Roles, 'Kind_operations': Kind_operations, \
'Transactions': Transactions, 'Kind_currency': Kind_currency, 'Config':Config, 'Moment':Moment}
#    return {'db': db, 'User': User}f