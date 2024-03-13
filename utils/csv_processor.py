import pandas as pd
from extensions import db
from models.card import Card
from datetime import datetime

import logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def standardize_phone(phone):
    phone_str = str(phone).strip('"')
    return phone_str[-9:]

def convert_timestamp(timestamp_str, fmt=None):
    formats = [fmt] + ["%Y-%m-%dT%H:%M:%SZ", "%d-%m-%Y %H:%M", "%d-%m-%Y %I:%M%p", "%d-%m-%Y %I:%M %p"] if fmt else ["%Y-%m-%dT%H:%M:%SZ", "%d-%m-%Y %H:%M", "%d-%m-%Y %I:%M%p", "%d-%m-%Y %I:%M %p"]
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    logger.warning(f"Timestamp format not recognized: {timestamp_str}")
    return None

def update_card_status(card_id, user_phone, status, timestamp):
    card = Card.query.get(card_id)
    if card:
        # Update only if the new timestamp is earlier
        if card.last_updated < timestamp:
            card.status = status
            card.last_updated = timestamp
    else:
        card = Card(card_id=card_id, user_phone=user_phone, status=status, last_updated=timestamp)
        db.session.add(card)
    db.session.commit()

def process_delivered_csv(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        user_phone = standardize_phone(row['User contact'])
        timestamp = convert_timestamp(row['Timestamp'])
        update_card_status(row['Card ID'], user_phone, 'Delivered', timestamp)

def process_pickup_csv(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        user_phone = standardize_phone(str(row['User Mobile']))
        timestamp = convert_timestamp(row['Timestamp'])
        update_card_status(row['Card ID'], user_phone, 'Picked Up', timestamp)

def process_delivery_exceptions_csv(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        card_id = row['Card ID']
        user_phone = standardize_phone(row['User contact'])
        timestamp = convert_timestamp(row['Timestamp'], "%d-%m-%Y %H:%M")

        card = Card.query.get(card_id)
        if card:
            card.delivery_attempts += 1

            if card.delivery_attempts > 2:
                card.status = 'Returned'
            else:
                card.status = 'Delivery Exception'

            card.last_updated = timestamp
            db.session.commit()
        else:
            # If the card doesn't exist, it might be the first record of it.
            pass

def process_returned_csv(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        user_phone = standardize_phone(row['User contact'])
        timestamp = convert_timestamp(row['Timestamp'], "%d-%m-%Y %H:%M%p")
        update_card_status(row['Card ID'], user_phone, 'Returned', timestamp)