# server/app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db, Earthquake  # <-- use db from models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # <-- this is the critical link!
migrate = Migrate(app, db)

@app.route("/earthquakes/<int:id>")
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [{
            "id": q.id,
            "location": q.location,
            "magnitude": q.magnitude,
            "year": q.year
        } for q in quakes]
    }), 200

if __name__ == "__main__":
    app.run(port=5555, debug=True)
