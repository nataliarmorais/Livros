from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
        """)
init_db()

# Rota para doar um livro
@app.route("/doar", methods=["POST"])
def doar():
    dados = request.get_json()
    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO LIVROS (titulo, categoria, autor, image_url)
            VALUES (?, ?, ?, ?)
        """, (titulo, categoria, autor, image_url))
        conn.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

# Rota para listar todos os livros
@app.route("/livros", methods=["GET"])
def listar_livros():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LIVROS")
        livros = cursor.fetchall()

    livros_formatados = [
        {"id": item[0], "titulo": item[1], "categoria": item[2], "autor": item[3], "image_url": item[4]}
        for item in livros
    ]

    return jsonify(livros_formatados), 200

# Rota para deletar um livro pelo ID
@app.route("/livros/<int:id>", methods=["DELETE"])
def deletar_livro(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LIVROS WHERE id = ?", (id,))
        livro = cursor.fetchone()

        if not livro:
            return jsonify({"erro": "Livro não encontrado"}), 404

        cursor.execute("DELETE FROM LIVROS WHERE id = ?", (id,))
        conn.commit()

    return jsonify({"mensagem": "Livro excluído com sucesso"}), 200

# Rota para atualizar a imagem de um livro pelo ID
@app.route("/livros/<int:id>", methods=["PATCH"])
def atualizar_livro(id):
    dados = request.get_json()
    nova_image_url = dados.get("image_url")

    if not nova_image_url:
        return jsonify({"erro": "O campo image_url é obrigatório"}), 400

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LIVROS WHERE id = ?", (id,))
        livro = cursor.fetchone()

        if not livro:
            return jsonify({"erro": "Livro não encontrado"}), 404

        cursor.execute("UPDATE LIVROS SET image_url = ? WHERE id = ?", (nova_image_url, id))
        conn.commit()

    return jsonify({"mensagem": "Imagem do livro atualizada com sucesso"}), 200

# Página inicial da API
@app.route("/")
def pagina_inicial():
    return "Bem-vindo à Biblioteca Online!"

if __name__ == "__main__":
    print("Servidor rodando em http://127.0.0.1:5000")
    app.run(debug=True)
