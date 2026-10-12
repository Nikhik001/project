from flask import Flask, request, jsonify, send_file, send_from_directory
from pathlib import Path
import csv
import io
import subprocess
import sys
import tempfile
import shutil

BASE_DIR = Path(__file__).resolve().parent
ORIGINAL_SCRIPT = BASE_DIR / "ss.py"
app = Flask(__name__)

@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.get("/source")
def source():
    # Return the uploaded source exactly as stored; it is not rewritten.
    return ORIGINAL_SCRIPT.read_text(encoding="utf-8")

@app.post("/run")
def run_original():
    payload = request.get_json(silent=True) or {}
    pasted_text = payload.get("text", "")
    if not isinstance(pasted_text, str) or not pasted_text.strip():
        return jsonify(error="Paste the contents of the text file first."), 400

    # The original script expects a file named kk.py and writes students.csv.
    # Create those files in an isolated temporary folder, then execute ss.py unchanged.
    with tempfile.TemporaryDirectory(prefix="school_result_") as temp_name:
        workdir = Path(temp_name)
        (workdir / "kk.py").write_text(pasted_text, encoding="utf-8")
        shutil_script = workdir / "ss.py"
        shutil_script.write_bytes(ORIGINAL_SCRIPT.read_bytes())
        try:
            completed = subprocess.run(
                [sys.executable, str(shutil_script)],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=20,
            )
        except subprocess.TimeoutExpired:
            return jsonify(error="The program took too long to run."), 408

        if completed.returncode != 0:
            message = completed.stderr.strip() or "The original script stopped with an error."
            return jsonify(error=message), 400

        csv_path = workdir / "students.csv"
        if not csv_path.exists():
            return jsonify(error="The program finished but did not create students.csv."), 500
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        # Store the CSV in memory for the download endpoint. This app is intended
        # for a single-user local school-project demonstration.
        app.config["latest_csv"] = csv_path.read_bytes()
        return jsonify(
            rows=rows,
            message="The original code ran successfully. " + (completed.stdout.strip()[-500:] if completed.stdout.strip() else "CSV created.")
        )

@app.get("/download")
def download_csv():
    content = app.config.get("latest_csv")
    if not content:
        return jsonify(error="Run the program first."), 404
    return send_file(
        io.BytesIO(content),
        mimetype="text/csv",
        as_attachment=True,
        download_name="students.csv",
    )

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
