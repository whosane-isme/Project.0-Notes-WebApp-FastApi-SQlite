from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import sqlite3
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Note(BaseModel):
    title: str
    context: str



def setup_db():
    try:
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        context TEXT 
        )
    ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"setup error: {e}")

setup_db()

@app.get("/notes/")
#async?
async def read_note():
    try:
        conn = sqlite3.connect("notes.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM notes''')
        rows = cursor.fetchall()
        notes = [dict(row) for row in rows]
        conn.close()
        return notes
    except sqlite3.Error as e:
        print(f"error read: {e}")

@app.post("/notes/")
async def create_note(note: Note):
    try:
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (title, context) VALUES (?, ?)', (note.title, note.context))
        conn.commit()
        conn.close()
        return {"message": "Note added successfully"}
    except sqlite3.Error as e:
        print(f"error create: {e}")
@app.put("/notes/{id}")
async def update_note(id: int, note: Note):
  try:
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = ?, context = ? WHERE id = ?",
                  (note.title, note.context, id))
    conn.commit()
    conn.close()
    return {"id": id, **note.dict()}
  except sqlite3.Error as e:
    print(e)
    return {"error": "Failed to update note"}


@app.delete("/notes/{id}")
async def delete_note(id: int):
  try:
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Note deleted"}
  except sqlite3.Error as e:
    print(e)
    return {"error": "Failed to delete note"}
