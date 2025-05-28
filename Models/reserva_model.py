from database import db

class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, nullable=False)
    sala = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    hora_inicio = db.Column(db.String(5), nullable=False)
    hora_fim = db.Column(db.String(5), nullable=False)

    @classmethod
    def criar_reserva(cls, dados):
        reserva = cls(
            turma_id=dados.get("turma_id"),
            sala=dados.get("sala"),
            data=dados.get("data"),
            hora_inicio=dados.get("hora_inicio"),
            hora_fim=dados.get("hora_fim")
        )
        db.session.add(reserva)
        db.session.commit()
        return reserva

    @classmethod
    def listar_reservas(cls):
        return cls.query.all()
