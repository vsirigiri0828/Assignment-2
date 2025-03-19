import json
from flask import Flask, request, jsonify, render_template
from analyze import get_sentiment, compute_embeddings, classify_email

# Function to load classes from the classes.json file
def load_classes():
    with open("classes.json", "r") as file:
        data = json.load(file)
    return data["classes"]

# Function to save updated classes back to the classes.json file
def save_classes(classes):
    with open("classes.json", "w") as file:
        json.dump({"classes": classes}, file)

app = Flask(__name__, template_folder='templates')

@app.route("/api/v1/add-class/", methods=['POST'])
def add_class():
    if request.is_json:
        data = request.get_json()
        new_class = data.get("class")
        if new_class:
            classes = load_classes()
            classes.append(new_class)
            save_classes(classes)
            return jsonify({"message": f"Class '{new_class}' added successfully."}), 200
        return jsonify({"error": "No 'class' field provided."}), 400
    return jsonify({"error": "Invalid Content-Type"}), 400


@app.route("/")
def home():
    print("Home page")
    return render_template('index.html')


@app.route("/api/v1/sentiment-analysis/", methods=['POST'])
def analysis():
    if request.is_json:
        data = request.get_json()
        sentiment = get_sentiment(data['text'])
        return jsonify({"message": "Data received", "data": data, "sentiment": sentiment}), 200
    else:
        return jsonify({"error": "Invalid Content-Type"}), 400


@app.route("/api/v1/valid-embeddings/", methods=['GET'])
def valid_embeddings():
    embeddings = compute_embeddings()
    formatted_embeddings = []
    for text, vector in embeddings:
        formatted_embeddings.append({
            "text": text,
            "vector": vector.tolist() if hasattr(vector, 'tolist') else vector
        })
    embeddings = formatted_embeddings
    return jsonify({"message": "Valid embeddings fetched", "embeddings": embeddings}), 200


@app.route("/api/v1/classify/", methods=['POST'])
def classify():
    if request.is_json:
        data = request.get_json()
        text = data['text']
        classifications = classify_email(text)
        return jsonify({"message": "Email classified", "classifications": classifications}), 200
    else:
        return jsonify({"error": "Invalid Content-Type"}), 400


@app.route("/api/v1/classify-email/", methods=['GET'])
def classify_with_get():
    text = request.args.get('text')
    classifications = classify_email(text)
    return jsonify({"message": "Email classified", "classifications": classifications}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)