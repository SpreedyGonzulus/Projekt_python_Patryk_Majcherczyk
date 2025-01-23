from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Ścieżka do pliku z danymi
DATA_FILE = "hasla.txt"

def load_data():
    """Wczytuje dane z pliku."""
    with open(DATA_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

def save_data(data):
    """Zapisuje dane do pliku."""
    with open(DATA_FILE, "w") as file:
        file.writelines(line + "\n" for line in data)

@app.route("/", methods=["GET", "POST"])
def search():
    query = ""
    results = []
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        data = load_data()
        # Filtrujemy dane zawierające frazę
        results = [line for line in data if query.lower() in line.lower()]
    
    return render_template("index.html", query=query, results=results)

@app.route("/delete_record", methods=["POST"])
def delete_record():
    """Usuwa konkretny rekord z pliku i zachowuje wyniki."""
    record_to_delete = request.form.get("record")
    query = request.form.get("query", "").strip()
    if record_to_delete:
        data = load_data()
        # Usuwamy dokładnie ten rekord, jeśli istnieje
        new_data = [line for line in data if line.strip() != record_to_delete.strip()]
        save_data(new_data)
        # Odtwarzamy wyniki po usunięciu rekordu
        results = [line for line in new_data if query.lower() in line.lower()]
        # Jeśli brak wyników, przekieruj na stronę główną
        if not results:
            return redirect(url_for('search'))
        # W przeciwnym razie wyświetl wyniki
        return render_template("index.html", query=query, results=results)
    # Jeśli nic nie zostało usunięte, wróć na stronę główną
    return redirect(url_for('search'))

if __name__ == "__main__":
    app.run(debug=True)
