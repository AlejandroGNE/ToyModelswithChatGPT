from flask import Flask, jsonify, request
from views import views
from RAG import load_index, construct_index


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")

index = None


@app.route('/callLoad')
def callLoadIndex():
    global index
    index = load_index()
    return jsonify({"message": "Index loaded successfully"}), 200


@app.route('/callGenerate')
def callGenerateIndex():
    global index
    index = construct_index(directory_path="Extracted_Data")
    return jsonify({"message": "Index constructed successfully"}), 200


@app.route('/query', methods=['POST'])
def queryIndex():
    global index
    if index is None:
        return jsonify({"error": "Index not loaded or constructed"}), 400

    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt not provided"}), 400

    try:
        query_engine = index.as_query_engine()
        response = query_engine.query(prompt)
        print(response)
        # Assuming response has a method to get a JSON serializable representation
        response_data = convert_response_to_serializable(response)

        return jsonify({"response": response_data}), 200

    except Exception as e:
        app.logger.error(f"Error querying index: {e}")
        return jsonify({"error": "Failed to process query"}), 500


def convert_response_to_serializable(response):
    # Implement this function based on how NodeWithScore and query response look
    # Example placeholder implementation:
    if hasattr(response, 'to_dict'):
        return response.to_dict()  # or whatever method you use
    return str(response)  # Fallback to string conversion

if __name__ == '__main__':
    app.run(debug=False, port=3000)
