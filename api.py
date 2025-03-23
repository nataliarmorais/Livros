from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/pagar")
def exibir_mensagem():
    return "Pagamento realizado com sucesso!"

def init_db():
    with sqlite3.connect("database.db") as conn:
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

@app.route("/doar", methods=["POST"])
def doar():
    dados = request.get_json()
    
    print("JSON recebido:", dados)

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

@app.route("/")
def pagina_inicial():
    return "Bem-vindo à Biblioteca Online!"

@app.route("/livros/<int:id>", methods=["DELETE"])
def deletar_livro(id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LIVROS WHERE id = ?", (id,))  # Passando o 'id' corretamente
        conn.commit()
    
    return jsonify({"mensagem": "Livro excluído com sucesso"}), 200


if __name__ == "__main__":
    print("Servidor rodando em http://127.0.0.1:5000")
    app.run(debug=True)
