from ..loader import collection
async def create_order(_id, **kwargs):
    user =  collection.insert_one({'_id': _id, **kwargs})
    return user