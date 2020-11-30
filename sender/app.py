from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pika


class Task(BaseModel):
    taskid: str
    title: str
    params: Optional[dict] = None


app = FastAPI()

credentials = pika.PlainCredentials(username='user', password='password')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', virtual_host='/', credentials=credentials)
)

channel = connection.channel()
channel.queue_declare(queue='privat')


@app.post("/task")
async def add_task(task: Task):
    channel.basic_publish(exchange='', routing_key='privat', body=task.json())

    print("Published ...")


"""if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)"""
