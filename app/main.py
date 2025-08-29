from fastapi import FastAPI, BackgroundTasks
import uvicorn

app = FastAPI()


@app.post("/send")
async def email_worker():
    """Adds tasks in queue"""
    BackgroundTasks.add_task()
    pass


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000, reload=True)
