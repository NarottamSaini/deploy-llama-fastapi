from fastapi import FastAPI

# Link: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # uses current directory visibility
    import schemas
    import models
    from database import engine, SessionLocal, get_db
    from routers import product, seller, login
else:
    # uses current package visibility
    from . import schemas
    from . import models
    from . database import engine, SessionLocal, get_db
    from .routers import product, seller, login

app = FastAPI()

@app.post('/product_temp')
def product_temp(request: schemas.Product):
    return request
