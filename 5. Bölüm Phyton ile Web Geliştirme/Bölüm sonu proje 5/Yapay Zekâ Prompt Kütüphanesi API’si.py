from flask import Flask, jsonify, request

app = Flask(__name__)

prompts = []
next_prompt_id = 1


def find_prompt(prompt_id):
    return next((prompt for prompt in prompts if prompt["id"] == prompt_id), None)


@app.post("/api/prompts")
def create_prompt():
    global next_prompt_id

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON veri gonderilmelidir"}), 400

    for field in ("title", "prompt_text", "category"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({"error": "title, prompt_text ve category zorunludur"}), 400

    prompt = {
        "id": next_prompt_id,
        "title": data["title"].strip(),
        "description": str(data.get("description", "")).strip(),
        "prompt_text": data["prompt_text"].strip(),
        "category": data["category"].strip(),
        "usage_count": 0,
    }
    prompts.append(prompt)
    next_prompt_id += 1
    return jsonify(prompt), 201


@app.get("/api/prompts")
def list_prompts():
    category = request.args.get("category")
    sort = request.args.get("sort")
    result = prompts

    if category:
        result = [prompt for prompt in result if prompt["category"] == category]
    if sort == "popular":
        result = sorted(result, key=lambda prompt: prompt["usage_count"], reverse=True)

    return jsonify(result)


@app.get("/api/prompts/<int:prompt_id>")
def get_prompt(prompt_id):
    prompt = find_prompt(prompt_id)
    if prompt is None:
        return jsonify({"error": "Prompt bulunamadi"}), 404
    return jsonify(prompt)


@app.get("/api/prompts/<int:prompt_id>/use")
def use_prompt(prompt_id):
    prompt = find_prompt(prompt_id)
    if prompt is None:
        return jsonify({"error": "Prompt bulunamadi"}), 404

    prompt["usage_count"] += 1
    return jsonify(prompt)


if __name__ == "__main__":
    app.run(debug=True)
