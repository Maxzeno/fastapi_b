from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

# In-memory "database"
items = []

# class ErrorSchema(BaseModel):
#     message: str

class MessageSchema(BaseModel):
    detail: str


class ItemSchema(BaseModel):
    id: int
    name: str
    description: str | None = None

# CREATE
@app.post("/items", status_code=status.HTTP_201_CREATED,
          responses={
        201: {"description": "Item created successfully"},
        400: {"model": MessageSchema, "description": "Item already exists"},
    },)
def create_item(item: ItemSchema) -> ItemSchema:
    for i in items:
        if i["id"] == item.id:
            raise HTTPException(status_code=400, detail="Item already exists")
    items.append(item.dict())
    return item

# READ ALL
@app.get("/items")
def get_items(item_id_gt: Optional[int]=None, limit: int=2, offset: int=0) -> list[ItemSchema]:
    res = items
    if item_id_gt:
        res = []
        for i in items:
            if i['id'] > item_id_gt:
                res.append(i)
    res = res[offset: offset+limit]
    return res

# READ ONE
@app.get("/items/{item_id}",
    response_model=ItemSchema,
    responses={
        400: {"model": MessageSchema, "description": "Bad Request"},
        404: {"model": MessageSchema, "description": "Item not found"},
    }
)
def get_item(item_id: int) -> ItemSchema:
    if item_id > 10:
        return JSONResponse(
            status_code=400,
            content={"detail": "Item id greater than 10"}
        )

    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# # UPDATE with GET
# @app.get("/items/{item_id}")
# def update_item_with_get(item_id: int, id: int, name: str, description: str) -> ItemSchema:
#     updated_item = {
#         'id': id,
#         'name': name,
#         'description': description,
#     }
#     for index, item in enumerate(items):
#         if item["id"] == item_id:
#             items[index] = updated_item
#             return updated_item
#     raise HTTPException(status_code=404, detail="Item not found")


# UPDATE
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: ItemSchema) -> ItemSchema:
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items[index] = updated_item.dict()
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> MessageSchema:
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(index)
            return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
