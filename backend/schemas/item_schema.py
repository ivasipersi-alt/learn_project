from apiflask import Schema
from apiflask.fields import String, Integer, List, Nested

class ItemSchema(Schema):
    id = Integer()
    name = String()
    description = String()
    price = Integer()

class ItemOutSchema(Schema):
    items = List(Nested(ItemSchema))