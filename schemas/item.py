from ma import ma
from models.item import ItemModel
from models.store import StoreModel
# importing it, because there is a relationship between StoreModel and ItemModel
# so we can load all dependencies



class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ('store',)  # store property defined in ItemModel
        dump_only = ('id', )
        include_fk = True  # include store_id defined in ItemModel


