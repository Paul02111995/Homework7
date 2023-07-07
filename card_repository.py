
import psycopg2
import uuid


from card import Card


class CardRepository:
    def __init__(self, db_params):
        self.db_params = db_params
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.db_params['host'],
            port=self.db_params['port'],
            database=self.db_params['database'],
            user=self.db_params['user'],
            password=self.db_params['password']
        )

    def close(self):
        if self.connection:
            self.connection.close()

    def create_table(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id UUID PRIMARY KEY,
                pan TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                cvv TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        self.connection.commit()
        self.close()

    def save_card(self, card):
        self.connect()
        cursor = self.connection.cursor()

        card_id = uuid.uuid4()

        cursor.execute(
            '''
            INSERT INTO cards (id, pan, expiry_date, cvv, issue_date, owner_id, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''',
            (str(card_id), card.pan, card.expiry_date, card.cvv, card.issue_date, card.owner_id, card.status)
        )

        self.connection.commit()
        self.close()

        return str(card_id)

    def get_card_by_id(self, card_id):
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM cards WHERE id = %s', (card_id,))
        result = cursor.fetchone()

        self.close()

        if result:
            card_id, pan, expiry_date, cvv, issue_date, owner_id, status = result
            return Card(pan, expiry_date, cvv, issue_date, owner_id, status)

        return None