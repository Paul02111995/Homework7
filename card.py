class Card:
    def __init__(self, pan, expiry_date, cvv, issue_date, owner_id, status):
        self.pan = pan
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.issue_date = issue_date
        self.owner_id = owner_id
        self.status = status


    def activate(self):
        if self.status == "new":
            self.status = "active"
        elif self.status == "active":
            raise ValueError("The card is already blocked.")
        elif self.status == "blocked":
            raise ValueError("A blocked card cannot be activated.")


    def block(self):
        if self.status == "active":
            self.status = "blocked"
        elif self.status == "new":
            raise ValueError("The new card must be activated first.")
        elif self.status == "blocked":
            raise ValueError("The card is already blocked.")
