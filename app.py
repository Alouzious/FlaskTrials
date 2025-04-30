from app import create_app  # Correct import
from app.models import db  # Make sure models.py is inside app/

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
