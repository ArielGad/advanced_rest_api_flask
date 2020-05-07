from ma import ma
from models.item import ItemModel
from models.store import StoreModel
from schemas.item import ItemSchema
# importing it, because there is a relationship between StoreModel and ItemModel
# so we can load all dependencies



class StoreSchema(ma.ModelSchema):
    # this declares that there are something nested inside a store that has many item schemas
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        dump_only = ('id', )
        include_fk = True  # include store_id defined in ItemModel


