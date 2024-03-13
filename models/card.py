from extensions import db
from sqlalchemy.dialects.postgresql import TIMESTAMP

class Card(db.Model):
    __tablename__ = 'cards'

    card_id = db.Column(db.String(), primary_key=True)
    user_phone = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    last_updated = db.Column(TIMESTAMP, nullable=False)
    delivery_attempts = db.Column(db.Integer, default=0)