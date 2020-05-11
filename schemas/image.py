from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage



class FileStorageField(fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid image.'
    }

    def _deserialize(self, value, attr, data) -> FileStorage:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail('invalid')  # raises ValidationError

        return value


# NOTE - Image has no db model, therefore, the use here with vanilla marshmallow
class ImageSchema(Schema):
    image = FileStorageField(required=True)
