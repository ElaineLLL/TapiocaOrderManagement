from typing import *

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float


items = {}

@app.get("/items", response_model=List[Item])
async def read_items():
    return list(items.values())

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    items[item.id] = item
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    items[item_id] = item
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    del items[item_id]
    return {"message": "Item deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011, reload = True)
    