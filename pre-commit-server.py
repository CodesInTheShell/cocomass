from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pymongo import DESCENDING

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client["cocomass"]
assessments_collection = db["assessments"]

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({'status': 'pong'}), 200

@app.route("/assessments", methods=["POST"])
def create_assessment():
    data = request.json
    if "filename" not in data or "comment" not in data or "author_name" not in data or "author_email" not in data:
        return jsonify({"error": "Fields 'filename', 'comment', 'author_name', and 'author_email' are required"}), 400

    assessment = {
        "filename": data["filename"],
        "comment": data["comment"],
        "author_name": data["author_name"],
        "author_email": data["author_email"],
        "criticality": data.get("criticality", "minor"),
        "created_at": datetime.utcnow()
    }
    result = assessments_collection.insert_one(assessment)
    assessment["_id"] = str(result.inserted_id)
    return jsonify(assessment), 201

@app.route("/assessments", methods=["GET"])
def get_assessments():

    query = {}

    queryValue = request.args.get('query', None)
    queryLimit = int(request.args.get('limit', 100))

    if queryValue:
        query['author_email'] = queryValue

    assessments = list(assessments_collection.find(query).sort("created_at", DESCENDING).limit(queryLimit))
    assessments = [serialize_doc(a) for a in assessments]

    return jsonify(assessments), 200

@app.route("/assessments/<string:assessment_id>", methods=["GET"])
def get_assessment(assessment_id):
    assessment = assessments_collection.find_one({"_id": ObjectId(assessment_id)})
    if not assessment:
        return jsonify({"error": "Assessment not found"}), 404
    return jsonify(serialize_doc(assessment)), 200

@app.route("/assessments/<string:assessment_id>", methods=["PUT"])
def update_assessment(assessment_id):
    data = request.json
    update_fields = {}
    if "filename" in data:
        update_fields["filename"] = data["filename"]
    if "comment" in data:
        update_fields["comment"] = data["comment"]
    if "author_name" in data:
        update_fields["author_name"] = data["author_name"]
    if "author_email" in data:
        update_fields["author_email"] = data["author_email"]
    if "criticality" in data:
        update_fields["criticality"] = data["criticality"]

    if not update_fields:
        return jsonify({"error": "No fields to update provided"}), 400

    result = assessments_collection.update_one(
        {"_id": ObjectId(assessment_id)},
        {"$set": update_fields}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Assessment not found"}), 404

    updated_assessment = assessments_collection.find_one({"_id": ObjectId(assessment_id)})
    return jsonify(serialize_doc(updated_assessment)), 200

@app.route("/assessments/<string:assessment_id>", methods=["DELETE"])
def delete_assessment(assessment_id):
    result = assessments_collection.delete_one({"_id": ObjectId(assessment_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Assessment not found"}), 404
    return jsonify({"message": "Assessment deleted"}), 200

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)

## Create
# curl -X POST -H "Content-Type: application/json" -d '{"filename": "example.txt", "comment": "This is a test comment", "author_name": "Initial commit", "criticality": "minor","author_email": "abc123"}' http://127.0.0.1:5000/assessments

## List all
# curl http://127.0.0.1:5000/assessments

## Get one
# curl http://127.0.0.1:5000/assessments/<assessment_id>

## Update
# curl -X PUT -H "Content-Type: application/json" -d '{"comment": "Updated comment", "author_name": "Updated commit", "author_email": "def456"}' http://127.0.0.1:5000/assessments/<assessment_id>

## Delete
# curl -X DELETE http://127.0.0.1:5000/assessments/<assessment_id>
