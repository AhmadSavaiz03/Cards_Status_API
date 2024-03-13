from config import DevelopmentConfig, TestingConfig, ProductionConfig
import unittest
from app import app, db
from models.card import Card
from datetime import datetime

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
            sample_card = Card(card_id="ZYW1234", user_phone="971234567", status="Delivered", last_updated=datetime.utcnow())
            db.session.add(sample_card)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_card_status(self):
        # Test by card_id
        response = self.client.get('/get_card_status?card_id=ZYW1234')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Delivered', response.get_data(as_text=True))
        print(response.get_data(as_text=True))  

        # Test by user_phone
        response = self.client.get('/get_card_status?user_phone=971234567')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Delivered', response.get_data(as_text=True))
        print(response.get_data(as_text=True)) 

    def test_card_lifecycle(self):
        with app.app_context():
            new_card = Card(card_id="GEN123", user_phone="9712345678", status="Generated", last_updated=datetime.utcnow(), delivery_attempts=0)
            db.session.add(new_card)
            db.session.commit()

            # Manual
            card = db.session.get(Card, "GEN123")
            card.delivery_attempts = 3 
            card.status = 'Returned'
            db.session.commit()

        response = self.client.get('/get_card_status?card_id=GEN123')
        self.assertIn('Returned', response.get_data(as_text=True), "Card status should be 'Returned' after exceeding delivery attempts.")


if __name__ == '__main__':
    unittest.main()
