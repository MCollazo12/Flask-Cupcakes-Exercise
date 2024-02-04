from flask import Flask, request, render_template, redirect, jsonify
from models import db, connect_db, Cupcake
from forms import CupcakeForm
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "kumasan"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)


@app.route("/", methods=["GET", "POST"])
def index():
    
    cupcakes = Cupcake.query.all()
    form = CupcakeForm()
    
    if form.validate_on_submit():
        flavor = form.flavor.data
        size = form.size.data
        rating = form.rating.data
        image = form.image.data

        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
        db.session.add(new_cupcake)
        db.session.commit()

        return redirect("/")

    return render_template("index.html", form=form, cupcakes=cupcakes)


@app.route("/api/cupcakes")
def list_cupcakes():
    """
    Get data about all cupcakes. 
    Respond with JSON.
    """

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """
    Get data about a single cupcake. 
    Responds with a JSON or a 404 error 
    if the cupcake cannot be found
    """

    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """
    Create a cupcake with flavor, size, rating 
    and image data from the body of the request. 
    Respond with JSON.
    """

    # Extract JSON data from the POST request
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]

    # If no image is provided in the request, use a default image
    if "image" in request.json:
        image = request.json["image"]
    else:
        image = "https://tinyurl.com/demo-cupcake"

    # Create a new Cupcake instance with the collected data and add to database
    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()

    # Return JSON dict along with a 201 status code
    return (jsonify(cupcake=cupcake.serialize()), 201)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """
    Update a cupcake with the id passed in the URL and 
    flavor, size, rating and image data from the body 
    of the request.
    """

    # Retrieve specific cupcake using its id
    cupcake = Cupcake.query.get_or_404(id)
    
    # Update the cupcake based off of the new data in the request
    updated_cupcake = request.json
    db.session.query(Cupcake).filter_by(id=id).update(updated_cupcake)

    # Update cupcake fields with the provided data
    for key, value in updated_cupcake.items():
        setattr(cupcake, key, value)

    # Commit changes to the database - Return an error if the update fails
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(error=str(Exception)), 500 

    # Return a success response with the updated cupcake data
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """
    Delete cupcake with the passed in id. Raises a 404 
    error if the cupcake cannot be found.
    """
    
    cupcake = Cupcake.query.get_or_404(id)
    
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(msg="Cupcake deleted")
