from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cupcake(db.Model):
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(
        db.String, nullable=False, default="https://tinyurl.com/demo-cupcake"
    )
    
    def serialize(cupcake):
        """Serialize cupcake object into a dictionary"""
        return {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
        }


def connect_db(app):
    db.app = app
    db.init_app(app)
    
