from app import app, db
from app.models import User, Movie, Genres

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Movie': Movie, "Genres": Genres}

# if __name__ == '__main__':
#     app.run(debug=True)
