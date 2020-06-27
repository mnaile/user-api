from extensions.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(),unique=True, nullable=False)
    password = db.Column(db.String(),nullable=False)
    filename = db.Column(db.String())

    def set_password(self):
        self.password = generate_password_hash(self.password)
    
    def check_password(self, password_hash):
        return check_password_hash(self.password, password_hash)


    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key,val)
        self.save_db()

class UserBooks(db.Model):
    __tablename__ = "user_books"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

    def save_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update_db(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key,val)
        self.save_db()
