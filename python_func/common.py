import uuid
from flask import session
from python_func.sql_connector import SqliteConnector
import random

class CommonObjectProcessor():
    def __init__(self):
        self.generated_ids = []

    # Generate ID 
    def generate_uuid(self, namespace_identifier, name):
        # Create a UUID object using the specified namespace identifier and name
        uuid_obj = uuid.uuid5(namespace_identifier, name)

        # Convert the UUID object to a string representation
        uuid_string = str(uuid_obj)

        # Return the generated UUID string
        return uuid_string

    def get_user_id(self):
        user_id = session.get('user_id')
        # Use SqliteConnector for thread-safe connection
        with SqliteConnector('fes_app.db') as db:
            user = db.fetch_data('SELECT * FROM User WHERE user_id = ?', (user_id,))
        return user
    
#cop = CommonObjectProcessor()
#print(cop.generate_uuid(uuid.NAMESPACE_DNS, 'cipher_長さ'))
