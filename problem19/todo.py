import csv
import os
from contextlib import asynccontextmanager
from typing import Dict, List
from fastapi import FastAPI, APIRouter, HTTPException

CSV_FILENAME = 'todo_list.csv'
todo_list: List[Dict[str, str]] = []


def load_data_from_csv():
    if not os.path.exists(CSV_FILENAME):
        return

    with open(CSV_FILENAME, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        todo_list.clear()
        for row in reader:
            todo_list.append(row)


def save_data_to_csv():
    with open(CSV_FILENAME, mode='w', encoding='utf-8', newline='') as f:
        fieldnames = ['id', 'content']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in todo_list:
            writer.writerow(item)


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    load_data_from_csv()
    yield


app = FastAPI(lifespan=lifespan_handler)
router = APIRouter()


@router.post('/add_todo')
async def add_todo(item: Dict) -> Dict:
    content = item.get('content')
    if not content:
        raise HTTPException(status_code=400, detail='내용(content)이 없습니다.')

    if todo_list:
        last_id = int(todo_list[-1]['id'])
        new_id = str(last_id + 1)
    else:
        new_id = '1'

    new_todo = {'id': new_id, 'content': content}
    
    todo_list.append(new_todo)
    save_data_to_csv()

    return {'msg': '등록 성공', 'data': new_todo}


@router.get('/retrieve_todo')
async def retrieve_todo() -> Dict:
    load_data_from_csv()
    return {'total_count': len(todo_list), 'data': todo_list}


app.include_router(router)