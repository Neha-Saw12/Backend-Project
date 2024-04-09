
from fastapi import FastAPI, HTTPException, Response
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

app = FastAPI()

mongo_user_url = "mongodb+srv://sahuneha4954:RROyrp7q1Fi9XICf@cluster0.fpfa99v.mongodb.net/"

# MongoDB connection
client = MongoClient(mongo_user_url)
db = client["Books"]
collection = db["LibraryBooks"]

error_500msg = "Oops! Something went wrong"

class Book(BaseModel):
    title: str
    author: str
    isbn: str
    taken : bool = False

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    taken : Optional[bool] = None

@app.post("/books/", )
async def create_book(book: Book):
    try:
        # Create a new book in the database
        book_data = {"title": book.title, "author": book.author, "isbn": book.isbn, "taken": False}
        result = collection.insert_one(book_data)
        msg = {"id": str(result.inserted_id)}
        print(msg)
        return msg
        #return Response(content=msg, status_code=200)
    except:
        return Response(content = error_500msg ,status_code=500)


@app.get("/books/{book_id}")
async def read_book(book_id: str):
    try:
        # Read a book from the database
        book = collection.find_one({"_id": ObjectId(book_id)})
        if book:
            msg = {"id": str(book["_id"]), "title": book["title"], "author": book["author"], "isbn": book["isbn"], "taken":book["taken"]}
            return msg
            #return Response(content=msg, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except:
        return Response(content = error_500msg ,status_code=500)


@app.put("/books/{book_id}")
async def update_book(book_id: str, book_update: UpdateBook):
    try:
        # Update a book in the database
        book = {}

        my_book = collection.find_one({"_id":ObjectId(book_id)})
        if my_book:
            print(my_book)
            print(my_book["title"])
        else:
            msg = {"message": "Book not found!"}
            return msg

        book = {}

        if book_update.title is not None:
            book["title"] = book_update.title
        else:
            book["title"] = my_book["title"]
        if book_update.author is not None:
            book["author"] = book_update.author
        else:
            book["author"] = my_book["author"]
        if book_update.isbn is not None:
            book["isbn"] = book_update.isbn
        else:
            book['isbn'] = my_book["isbn"]
        
        if book_update.taken is not None:
            book["taken"] = book_update.taken
        else:
            book['taken'] = my_book["taken"]        

        result = collection.update_one({"_id": ObjectId(book_id)},
                                    {"$set": {"title": book["title"], "author": book["author"], "isbn": book["isbn"], "taken": book["taken"]}})
        
        if result.modified_count == 1:
            msg = {"id": book_id}
            return msg
            #return Response(content=msg, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except:
        return Response(content = error_500msg ,status_code=500)


@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    try:
        # Delete a book from the database
        result = collection.delete_one({"_id": ObjectId(book_id)})
        if result.deleted_count == 1:
            msg = {"message": "Book deleted successfully"}
            return msg
            
            #return Response(status_code=204)
            # return {"message": "Book deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except:
        return Response(content = error_500msg ,status_code=500)



