from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from domain.question import question_router

app = FastAPI(title='Mars Bulletin Board')

app.include_router(question_router.router)

app.mount('/static', StaticFiles(directory='frontend'), name='static')


@app.get('/')
def root():
    return {'message': 'Mars Bulletin Board API. Visit /docs for API documentation.'}