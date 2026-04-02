from apiflask import Schema
from apiflask.fields import String, Integer

class StatusSchema(Schema):
    status = String()
    message = String()
    service = String()
    items_count = Integer()