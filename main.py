from starlette.applications import Starlette
from views import routes
from contacts_repository import database

app = Starlette(
    routes=routes,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect]
)
