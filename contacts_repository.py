from databases import Database
from sqlalchemy import Column, INTEGER, MetaData, String, Table

database = Database('sqlite:///contacts')

metadata = MetaData()

contacts = Table(
    'contacts',
    metadata,
    Column('id', INTEGER(), primary_key=True),
    Column('name', String()),
    Column('number', String(), unique=True)
)


async def get(_id=None):
    query = contacts.select()
    if _id:
        query = query.where(contacts.columns.id == _id)

    return await database.fetch_all(query)


async def create(values):
    query = contacts.insert(values)
    return await database.execute(query)


async def update(_id, values):
    query = contacts.update.where(contacts.columns.id == _id).values(values)
    return await database.execute(query)


async def delete(_id):
    query = contacts.delete().where(contacts.columns.id == _id)
    return await database.execute(query)


async def exists(_id):
    row = await get(_id)
    if len(row) == 0:
        return False
    return True
