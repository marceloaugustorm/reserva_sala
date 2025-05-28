from flask import Blueprint, request, jsonify
from Models.reserva_model import Reserva
from clients.gerenciamento_escola_client import turma_existe

reserva_bp = Blueprint("reserva_bp", __name__)

@reserva_bp.route("/reservas", methods=["POST"])
def criar_reserva():
    dados = request.json
    turma_id = dados.get("turma_id")

    if not turma_id or not turma_existe(turma_id):  
        return jsonify({"erro": "Turma não encontrada"}), 400

    reserva = Reserva.criar_reserva(dados)

    return jsonify({
        "mensagem": "Reserva criada com sucesso",
        "reserva": {
            "id": reserva.id,
            "turma_id": reserva.turma_id,
            "sala": reserva.sala,
            "data": reserva.data,
            "hora_inicio": reserva.hora_inicio,
            "hora_fim": reserva.hora_fim
        }
    }), 201

@reserva_bp.route("/reservas", methods=["GET"])
def listar_reservas():
    reservas = Reserva.listar_reservas()
    return jsonify([
        {
            "id": r.id,
            "turma_id": r.turma_id,
            "sala": r.sala,
            "data": r.data,
            "hora_inicio": r.hora_inicio,
            "hora_fim": r.hora_fim
        } for r in reservas
    ])
