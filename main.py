from flask import Flask, render_template, request, redirect, url_for
import os
from pallete_giver import PalleteGiver

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():
    filename = request.args.get("filename")
    palletes = []
    if filename:
        file = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        pg = PalleteGiver(file)
        palletes = pg.get_pallete()
    return render_template("index.html", filename=filename, palletes=palletes)

@app.route("/upload_file", methods=["POST", "GET"])
def upload():
    if "image" not in request.files:
        return "No File Part"

    file = request.files["image"]

    if file.filename == "":
        return "No File Selected"

    if file and file.filename.lower().endswith(("png", "jpg", "jpeg", "gif")):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        ext = file_path.split(".")[1]
        new_name = "image." + ext
        new_path = os.path.join(app.config["UPLOAD_FOLDER"], new_name)
        files = os.listdir(app.config["UPLOAD_FOLDER"])
        for file in files:
            if file.startswith("image"):
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], file))
        os.rename(file_path, new_path)

        return redirect(url_for("index", filename=new_name))
    return "Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed."

if __name__ == "__main__":
    app.run(debug=True)