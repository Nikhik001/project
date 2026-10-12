SCHOOL BOARD RESULT ANALYSIS WEBSITE

Files:
- index.html: website interface
- app.py: small Flask server that receives pasted text and runs ss.py unchanged
- ss.py: exact copy of the original script you provided
- requirements.txt: Flask dependency

Run:
1. Install Python.
2. Open a terminal in this folder.
3. Run: pip install -r requirements.txt
4. Run: python app.py
5. Open http://127.0.0.1:5000 in your browser.

The app writes the pasted text to a temporary file named kk.py because the
original ss.py expects that filename. It then executes the original ss.py
without modifying its code. The original sorting remains d.sort(reverse=True)
(descending). The text must match the format expected by your original code.
