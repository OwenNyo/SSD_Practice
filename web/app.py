from flask import Flask, render_template, request, redirect, url_for
import re
import html

app = Flask(__name__)

# Basic regex patterns for detecting XSS or SQLi (not comprehensive but good for demonstration)
def is_xss_attack(input_str):
    xss_pattern = re.compile(r"<script.*?>.*?</script.*?>", re.IGNORECASE)
    return bool(xss_pattern.search(input_str))

def is_sql_injection(input_str):
    sql_keywords = ['SELECT', 'INSERT', 'DELETE', 'UPDATE', 'DROP', '--', ';', "' OR '1'='1"]
    for keyword in sql_keywords:
        if keyword.lower() in input_str.lower():
            return True
    return False

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        term = request.form.get("search_term", "")
        if is_xss_attack(term):
            return render_template("index.html", error="XSS attack detected! Input cleared.")
        if is_sql_injection(term):
            return render_template("index.html", error="SQL Injection detected! Input cleared.")
        return redirect(url_for("result", term=term))
    return render_template("index.html")

@app.route("/result")
def result():
    term = request.args.get("term", "")
    # Sanitize to prevent reflected XSS
    safe_term = html.escape(term)
    return render_template("result.html", term=safe_term)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)