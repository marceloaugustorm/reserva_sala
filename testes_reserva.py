import unittest
from flask import Flask
from database import db
from Models.reserva_model import Reserva
from Controllers.reserva_route import reserva_bp

# Mock para simular a existência da turma
def turma_existe_mock(turma_id):
    return turma_id == 1  # Só a turma 1 existe

# Substituir a função original pela mockada
import clients.gerenciamento_escola_client
clients.gerenciamento_escola_client.turma_existe = turma_existe_mock

class ReservaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(self.app)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        self.app.register_blueprint(reserva_bp)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_criar_reserva_sucesso(self):
        response = self.client.post("/reservas", json={
            "turma_id": 1,
            "sala": "101",
            "data": "2025-06-01",
            "hora_inicio": "08:00",
            "hora_fim": "10:00"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("mensagem", data)
        self.assertEqual(data["reserva"]["turma_id"], 1)

    def test_criar_reserva_turma_invalida(self):
        response = self.client.post("/reservas", json={
            "turma_id": 999,  # inexistente no mock
            "sala": "102",
            "data": "2025-06-01",
            "hora_inicio": "10:00",
            "hora_fim": "12:00"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("erro", data)

    def test_listar_reservas(self):
        # Cria uma reserva antes de testar o GET
        self.client.post("/reservas", json={
            "turma_id": 1,
            "sala": "201",
            "data": "2025-06-02",
            "hora_inicio": "14:00",
            "hora_fim": "16:00"
        })

        response = self.client.get("/reservas")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

if __name__ == "__main__":
    unittest.main()
