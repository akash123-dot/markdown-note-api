from flask import Flask,request, jsonify
import os
import language_tool_python
import markdown



folder_path = "notes"
os.makedirs(folder_path, exist_ok=True)

tool = language_tool_python.LanguageTool('en-US')


app = Flask(__name__)


@app.route("/check_grammar", methods=["POST"])
def check_grammar():
    text = request.json.get("note")
    filename = request.json.get("name")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    matches = tool.check(text)
    if matches:
        issues = []
        
        for match in matches:
            issues.append({
                "message" : match.message,
                "suggested_correction": match.replacements
            })

        corrected_text = tool.correct(text)

        return jsonify({
            "Total Error": len(matches),
            "issues" : issues,
            "corrected_text": corrected_text

        })

        
                           
    else:
        with open(os.path.join(folder_path, filename), "w") as f:
            f.write(text)

        return {"message": "Note saved."}
    

@app.route("/list_note", methods = ["GET"])
def list_note():
    listNote = os.listdir("notes")
    note_dict = {index + 1: note for index, note in enumerate(listNote)}
    
    return jsonify(note_dict)




@app.route("/render_note/<filename>", methods=["GET"])
def render_route(filename):
    if filename not in os.listdir(folder_path):
        return jsonify({"error": "Note not found"}), 404
    with open(os.path.join(folder_path, filename), "r") as f:
        note = f.read()
    html = markdown.markdown(note)
                             
    return html


if __name__ == "__main__":
    app.run(debug=True)


