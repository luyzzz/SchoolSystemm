from flask import Flask, jsonify, request

app = Flask(__name__)

professores = [
    {"id": 1, "nome": "João Silva", "disciplina": "Matemática"},
    {"id": 2, "nome": "Maria Souza", "disciplina": "Português"}
]

alunos = [
    {"id": 1, "nome": "Carlos Silva", "idade": 19},
    {"id": 2, "nome": "Ana Costa", "idade": 20}
]

turmas = [
    {"id": 1, "professor_id": 1, "alunos": [1, 2], "nome": "Turma A"},
    {"id": 2, "professor_id": 2, "alunos": [1], "nome": "Turma B"}
]

id_professor = len(professores) + 1
id_aluno = len(alunos) + 1
id_turma = len(turmas) + 1

def buscar_indice(lista, id):
    for index, item in enumerate(lista):
        if item['id'] == id:
            return index
    return None  # Retorna None se não encontrar o item


@app.route('/professores', methods=['GET'])
def listar_professores():
    return jsonify(professores)


@app.route('/professores/id/<int:id>', methods=['GET'])
def obter_professor_por_id(id):
    index = buscar_indice(professores, id)
    if index is not None:
        return jsonify(professores[index])
    return jsonify({"erro": "Professor não encontrado"}), 404

@app.route('/professores', methods=['POST'])
def cadastrar_professor():
    global id_professor
    dados = request.json
    novo_professor = {
        "id": id_professor,
        "nome": dados["nome"],
        "disciplina": dados["disciplina"]
    }
    professores.append(novo_professor)
    id_professor += 1
    return jsonify(novo_professor), 201

@app.route('/professores/id/<int:id>', methods=['PUT'])
def atualizar_professor_por_id(id):
    dados = request.json
    for professor in professores:
        if professor["id"] == id:
            professor.update(dados)
            return jsonify({"mensagem": "Professor atualizado com sucesso!", "professor": professor}), 200
    return jsonify({"erro": "ID não encontrado"}), 404



@app.route('/professores/id/<int:id>', methods=['DELETE'])
def deletar_professor_por_id(id):
    # Usando list comprehension para procurar o professor com o ID
    professor_a_deletar = next((prof for prof in professores if prof["id"] == id), None)

    if professor_a_deletar:
        professores.remove(professor_a_deletar)  # Remover o professor da lista
        return jsonify({"mensagem": "Professor deletado com sucesso!"}), 200
    else:
        return jsonify({"erro": "Professor não encontrado"}), 404



@app.route('/alunos', methods=['GET'])
def listar_alunos():
    return jsonify(alunos)


@app.route('/alunos/id/<int:id>', methods=['GET'])
def obter_aluno_por_id(id):
    index = buscar_indice(alunos, id)
    if index is not None:
        return jsonify(alunos[index])
    return jsonify({"erro": "Aluno não encontrado"}), 404

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    global id_aluno
    dados = request.json
    novo_aluno = {
        "id": id_aluno,
        "nome": dados["nome"],
        "idade": dados["idade"]
    }
    alunos.append(novo_aluno)
    id_aluno += 1
    return jsonify(novo_aluno), 201


@app.route('/alunos/id/<int:id>', methods=['PUT'])
def atualizar_aluno_por_id(id):
    index = buscar_indice(alunos, id)
    if index is not None:
        alunos[index].update(request.json)
        return jsonify(alunos[index])
    return jsonify({"erro": "Aluno não encontrado"}), 404



@app.route('/alunos/id/<int:id>', methods=['DELETE'])
def deletar_aluno_por_id(id):
    index = buscar_indice(alunos, id)
    if index is not None:
        removido = alunos.pop(index)
        return jsonify({"mensagem": "Aluno deletado com sucesso", "dados": removido})
    return jsonify({"erro": "Aluno não encontrado"}), 404



@app.route('/turmas', methods=['GET'])
def listar_turmas():
    return jsonify(turmas)

# LISTAR POR ID
@app.route('/turmas/id/<int:id>', methods=['GET'])
def listar_turma_por_id(id):
    turma = next((t for t in turmas if t["id"] == id), None)
    if turma:
        return jsonify(turma)
    return jsonify({"erro": "Turma não encontrada"}), 404



# Criar Turma
@app.route('/turmas', methods=['POST'])
def cadastrar_turma():
    dados = request.json
    novo_id = len(turmas) + 1
    nova_turma = {
        "id": novo_id,
        "nome": dados.get("nome", "Turma Sem Nome"),
        "professor_id": dados.get("professor_id", None),
        "alunos": dados.get("alunos", [])
    }
    turmas.append(nova_turma)
    return jsonify(nova_turma), 201

# Atualizar turma por ID
@app.route('/turmas/id/<int:id>', methods=['PUT'])
def atualizar_turma_id(id):
    turma = next((t for t in turmas if t["id"] == id), None)
    if turma:
        dados = request.json
        turma.update(dados)
        return jsonify(turma)
    return jsonify({"erro": "Turma não encontrada"}), 404


# Deletar Turma por ID
@app.route('/turmas/id/<int:id>', methods=['DELETE'])
def deletar_turma_id(id):
    global turmas
    turmas = [t for t in turmas if t["id"] != id]
    return jsonify({"mensagem": "Turma deletada com sucesso!"})




if __name__ == '__main__':
    app.run(debug=True)
