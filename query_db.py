from app import app, db, Note
from sqlalchemy import text

def print_all_notes():
    with app.app_context():
        notes = Note.query.order_by(Note.timestamp.desc()).all()
        for note in notes:
            print(f"ID: {note.id}, Note: {note.note}, Timestamp: {note.timestamp}")

def run_custom_query(query):
    with app.app_context():
        result = db.session.execute(text(query))
        for row in result:
            print(row)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        print_all_notes()
    else:
        query = " ".join(sys.argv[1:])
        run_custom_query(query)