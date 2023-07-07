from flask import Flask, request
from card import Card
from card_repository import CardRepository

app = Flask(__name__)

db_params = {
    'host': '127.0.0.1',
    'port': '5433',
    'database': 'Card',
    'user': 'Pavlo',
    'password': '12345'
}

card_repo = CardRepository(db_params)
card_repo.create_table()

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the Card Repository API!'

@app.route('/cards', methods=['GET'])
def create_card():
    pan = request.args.get('pan')
    expiry_date = request.args.get('expiry_date')
    cvv = request.args.get('cvv')
    issue_date = request.args.get('issue_date')
    owner_id = request.args.get('owner_id')
    status = request.args.get('status')

    card = Card(pan, expiry_date, cvv, issue_date, owner_id, status)
    card_id = card_repo.save_card(card)
    return f"Card created with ID: {card_id}"

@app.route('/cards/<card_id>', methods=['GET'])
def get_card(card_id):
    card = card_repo.get_card_by_id(card_id)
    if card:
        return {
            'pan': card.pan,
            'expiry_date': card.expiry_date,
            'cvv': card.cvv,
            'issue_date': card.issue_date,
            'owner_id': card.owner_id,
            'status': card.status
        }
    else:
        return f"Card with ID {card_id} not found"

if __name__ == '__main__':
    app.run(debug=True)
