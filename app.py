"""
Flask Web App with Add, Delete, and Edit Features
"""

from flask import Flask, render_template_string, request, redirect
import csv
import os

app = Flask(__name__)
CSV_FILE = "data.csv"

# Ensure CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "value"])

# Load CSV data
def load_data():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        return sorted(reader, key=lambda x: x["name"].lower())

# Save all data back to CSV
def save_all(data):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "value"])
        for row in data:
            writer.writerow([row["name"], row["value"]])

# Add new row
def save_data(name, value):
    all_data = load_data()
    all_data.append({"name": name, "value": value})
    save_all(all_data)

# HTML Template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Flask CRUD App</title>
<style>
body { font-family: Arial; background:#f2f2f2; padding:20px; }
.card { background:white; padding:20px; border-radius:8px; width:500px; margin:auto; }
input { width:100%; padding:10px; margin:5px 0; }
button { padding:10px; margin:5px 0; width:100%; background:blue; color:white; border:none; }
table { width:100%; margin-top:20px; border-collapse:collapse; }
td, th { border:1px solid #ccc; padding:8px; text-align:center; }
a { text-decoration:none; padding:5px 10px; border-radius:4px; }
.delete { background:red; color:white; }
.edit { background:green; color:white; }
</style>
</head>
<body>
<div class="card">
<h2>Add Data</h2>
<form method="POST" action="/add">
    <input name="name" placeholder="Enter name" required>
    <input name="value" placeholder="Enter value" required>
    <button type="submit">Add</button>
</form>

<h3>Stored Data</h3>
<table>
<tr><th>Name</th><th>Value</th><th>Actions</th></tr>
{% for row in data %}
<tr>
    <td>{{row.name}}</td>
    <td>{{row.value}}</td>
    <td>
        <a class="edit" href="/edit/{{row.name}}">Edit</a>
        <a class="delete" href="/delete/{{row.name}}">Delete</a>
    </td>
</tr>
{% endfor %}
</table>
</div>
</body>
</html>
"""

# Edit Template
EDIT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Edit</title>
<style>
body { font-family: Arial; background:#f2f2f2; padding:20px; }
.card { background:white; padding:20px; border-radius:8px; width:400px; margin:auto; }
input { width:100%; padding:10px; margin:5px 0; }
button { padding:10px; width:100%; background:green; color:white; border:none; }
</style>
</head>
<body>
<div class="card">
<h2>Edit Entry</h2>
<form method="POST">
    <input name="value" value="{{value}}" required>
    <button type="submit">Update</button>
</form>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    data = load_data()
    return render_template_string(TEMPLATE, data=data)

@app.route("/add", methods=["POST"])
def add():
    save_data(request.form["name"], request.form["value"])
    return redirect("/")

@app.route("/delete/<name>")
def delete(name):
    data = load_data()
    new_data = [row for row in data if row["name"].lower() != name.lower()]
    save_all(new_data)
    return redirect("/")

@app.route("/edit/<name>", methods=["GET", "POST"])
def edit(name):
    data = load_data()
    for row in data:
        if row["name"].lower() == name.lower():
            if request.method == "POST":
                row["value"] = request.form["value"]
                save_all(data)
                return redirect("/")
            return render_template_string(EDIT_TEMPLATE, value=row["value"])
    return "Not Found", 404

if __name__ == "__main__":
    app.run(debug=True)