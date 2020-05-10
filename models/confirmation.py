from uuid import uuid4
import time

from db import db


CONFIRMATION_EXPIRATION_DELTA = 1800  # 30 min


class ConfirmationModel(db.Model):
    __tablename__ = 'confirmations'

    id = db.Column(db.String(50), primary_key=True)  # TOKEN ID
    expire_at = db.Column(db.Integer, nullable=False)  # EPOCH TIME
    confirmed = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel')

    def __int__(self, user_id: str, **kwargs):
        super().__int__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time.time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = False

    @classmethod
    def find_by_id(cls, _id: int) -> 'ConfirmationModel':
        return cls.query.filter_by(id=_id).first()

    @property
    def expired(self) -> bool:
        return time.time() > self.expire_at

    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(time.time())
            self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
