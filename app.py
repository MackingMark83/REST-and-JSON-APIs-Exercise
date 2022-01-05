"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "nsajksnnsak"

connect_db(app)


@app.route("/")
def homepage():
    """Render homepage."""

    return render_template("homepage.html")


@app.route("/api/cupcakes")
def list_cupcakes():
    """Get data about all cupcakes..

    Respond with JSON like:
        {cupcakes: [{id, flavor, rating, size, image}, ...]}
    """

    cupcakes = [cupcake.to_serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Get data about a single cupcake.

    Respond with JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_serialize())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and 
    image data from the body of the request.

    Respond with JSON like::
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    
    return (jsonify(cupcake=cupcake.to_serialize()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the URL and flavor, size, 
    rating and image data from the body of the request.

    Respond with JSON of the newly-updated cupcake, like this:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_serialize())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake and returns message.

    Delete cupcake with the id passed in the URL. 
    Respond with JSON like {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

