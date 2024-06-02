import uuid

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

