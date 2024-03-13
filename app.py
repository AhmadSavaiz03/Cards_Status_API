from config import DevelopmentConfig, TestingConfig, ProductionConfig
from celeryconfig import make_celery

from flask import Flask, render_template, url_for, request, redirect
from extensions import db, migrate
import os

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:an3909@localhost/zywa'
db.init_app(app)
migrate.init_app(app, db)

from api.routes import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/')

def process_csv_files():
    from utils import csv_processor  # avoid circular imports

    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(current_dir, 'resources', 'csv_files')

    pickup_csv_path = os.path.join(csv_dir, 'Sample Card Status Info - Pickup.csv')
    delivery_exceptions_csv_path = os.path.join(csv_dir, 'Sample Card Status Info - Delivery exceptions.csv')
    delivered_csv_path = os.path.join(csv_dir, 'Sample Card Status Info - Delivered.csv')
    returned_csv_path = os.path.join(csv_dir, 'Sample Card Status Info - Returned.csv')

    csv_processor.process_pickup_csv(pickup_csv_path)
    csv_processor.process_delivery_exceptions_csv(delivery_exceptions_csv_path)
    csv_processor.process_delivered_csv(delivered_csv_path)
    csv_processor.process_returned_csv(returned_csv_path)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        card_content = request.form['content']
        new_task = Card(content=card_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error Input'
    else:
        cards = Card.query.order_by(Card.last_updated).all()
        print(cards)
        return render_template('index.html', card=cards)

if __name__ == '__main__':
    from models.card import Card # avoid circular imports
    with app.app_context():
        process_csv_files()
    app.run(debug=True)