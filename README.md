# Api de Doação de Livros

Essa é um API simples feita com Flask e SQLite3 para fins da escola Vai Na Web, ela permite cadastrar e listar dados.

# Como rodar o projeto

1. Faça o clone do repositório : 
'''bash
git clone <URL_DO_REPOSITORIO>
cd nome-do-projeto
'''

2. Crie um ambiente virtual (obrigatório):
'''bash
python -m venv venv
venv/Scripts/activate
'''

3. Instale as dependências
'''bash
pip install -r requirements.txt
'''
4. Inicie o servidor:
'''bash
python api.py

A api está disponível em http://127.0.0.1:5000

## Endpoints

### POST/doar

Endpoint para cadastrar um novo livro

**Formato de envio dos dados**
'''json 

**Resposta 201 (Created)**:
'''json
{
    "mensagem: "Livro cadastrado com sucesso"
}
'''


![Imaegm da página de doação de livros]
(image.png)

### GET/livros

Retorna toos os livros cadastrados em nossa API.

**Resposta (200)**:
'''json

{
    "id": 1,
    "titulo": "Nome do Livro,
    "categoria": "Ficção",
    "autor": "Autor do Livro",
    "imagem_url":
}
---