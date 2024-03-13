import unittest
from app import app, db 
from models.card import Card
from datetime import datetime

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        
        # insert a sample record
        with app.app_context():
            # working on actual database
            db.create_all()
            sample_card = Card(card_id="TEST_ZYW1234", user_phone="971234567", status="Delivered", last_updated=datetime.utcnow())
            db.session.add(sample_card)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            # clean testing
            test_card = Card.query.filter_by(card_id="TEST_ZYW1234").first()
            if test_card:
                db.session.delete(test_card)
                db.session.commit()
            # db.drop_all()

    def test_get_card_status_valid_card_id(self):
        print(f"Requesting with card_id=TEST_ZYW1234")
        response = self.client.get('/get_card_status?card_id=TEST_ZYW1234')
        print(response.get_data(as_text=True)) 
        self.assertEqual(response.status_code, 200)



    def test_get_card_status_valid_user_phone(self):
        response = self.client.get('/get_card_status?user_phone=971234567')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Delivered', response.get_data(as_text=True))

    def test_get_card_status_invalid_card_id(self):
        response = self.client.get('/get_card_status?card_id=InvalidID')
        self.assertEqual(response.status_code, 400)

    def test_get_card_status_invalid_user_phone(self): 
        response = self.client.get('/get_card_status?user_phone=InvalidPhone')
        self.assertEqual(response.status_code, 400)

    def test_get_card_status_missing_parameters(self):
        response = self.client.get('/get_card_status')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()