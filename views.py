from sqlite3 import IntegrityError

from starlette.responses import JSONResponse
from starlette.routing import Route

import contacts_repository as contacts

user_not_found = {'error': 'user not found'}
user_exists = {'error': "user with this 'number' already exists"}


def as_dict(data):
    return dict({k: data[k] for k in data.keys()})


async def get_all(request):
    result = await contacts.get()
    response = list((as_dict(res) for res in result))
    return JSONResponse(response)


async def get(request):
    _id = request.path_params['id']

    if not await contacts.exists(_id):
        return JSONResponse(user_not_found)
    else:
        result = await contacts.get(_id)
    return JSONResponse(as_dict(result.pop()))


async def post(request):
    body = await request.json()
    try:
        _id = await contacts.create(values=body)
        result = await contacts.get(_id)
        return JSONResponse(as_dict(result))
    except IntegrityError as e:
        return JSONResponse(user_exists)


async def delete(request):
    _id = request.path_params['id']

    if not await contacts.exists(_id):
        return JSONResponse(user_not_found)
    else:
        result = await contacts.get(_id)
        await contacts.delete(_id)
        return JSONResponse(as_dict(result.pop()))


async def patch(request):
    _id = request.path_params['id']
    body = await request.json()
    if not (await contacts.exists(_id)):
        return JSONResponse(user_not_found)

    await contacts.update(_id, values=body)
    result = await contacts.get(_id)

    return JSONResponse(as_dict(result.pop()))


routes = [
    Route('/contacts', get_all, methods=['GET']),
    Route('/contacts', post, methods=['POST']),
    Route('/contacts/{id}', get, methods=['GET']),
    Route('/contacts/{id}', delete, methods=['DELETE']),
    Route('/contacts/{id}', patch, methods=['PATCH']),
]
