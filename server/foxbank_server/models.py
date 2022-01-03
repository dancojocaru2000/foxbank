from dataclasses import dataclass, field
from marshmallow import Schema, fields
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    email: str
    otp: str
    fullname: str

    class UserSchema(Schema):
        id = fields.Int(required=False)
        username = fields.String()
        email = fields.String()
        otp = fields.String(load_only=True, required=False)
        fullname = fields.String()

    @staticmethod
    def new_user(username: str, email: str, fullname: str) -> 'User':
        return User(
            id=-1,
            username=username,
            email=email,
            otp='',
            fullname=fullname,
        )

    def to_json(self, include_otp=False, include_id=False):
        result = {
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname,
        }
        if include_id:
            result['id'] = self.id
        if include_otp:
            result['otp'] = self.otp
        return result

    @classmethod
    def from_query(cls, query_result):
        return cls(*query_result)


@dataclass
class Account:
    id: int
    iban: str
    currency: str
    account_type: str
    custom_name: str
    balance: int = field(default=0)

    class AccountSchema(Schema):
        id = fields.Int(required=False)
        iban = fields.Str()
        currency = fields.Str()
        account_type = fields.Str(data_key='accountType')
        custom_name = fields.Str(data_key='customName')
        balance = fields.Int()

    @staticmethod
    def new_account(currency: str, account_type: str, custom_name: str = '') -> 'Account':
        return Account(
            id=-1,
            iban='',
            currency=currency,
            account_type=account_type,
            custom_name=custom_name,
        )

    def to_json(self, include_id=True):
        result = {
            'iban': self.iban,
            'currency': self.currency,
            'accountType': self.account_type,
            'customName': self.custom_name,
            'balance': self.balance,
        }
        if include_id:
            result['id'] = self.id
        return result

    @classmethod
    def from_query(cls, query_result):
        return cls(*query_result)


@dataclass
class Transaction:
    id: int
    date_time: datetime
    other_party: str
    status: str
    transaction_type: str
    extra: str

    class TransactionSchema(Schema):
        id = fields.Int(required=False)
        date_time = fields.DateTime(data_key='datetime')
        other_party = fields.Dict(keys=fields.Str(), values=fields.Raw(), data_key='otherParty')
        status = fields.Str()
        transaction_type = fields.Str(data_key='transactionType')
        extra = fields.Dict(keys=fields.Str(), values=fields.Raw())

    @staticmethod
    def new_transaction(date_time: datetime, other_party: str, status: str, transaction_type: str, extra: str = '') -> 'Transaction':
        return Transaction(
            id=-1,
            date_time=date_time,
            other_party=other_party,
            status=status,
            transaction_type=transaction_type,
            extra=extra,
        )

    def to_json(self, include_id=True):
        result = {
            'datetime': self.date_time.isoformat(),
            'otherParty': self.other_party,
            'status': self.status,
            'transactionType': self.transaction_type,
            'extra': self.extra,
        }
        if include_id:
            result['id'] = self.id
        return result

    @classmethod
    def from_query(cls, query_result):
        import json

        query_result = list(query_result)
        if type(query_result[1]) is str:
            query_result[1] = datetime.fromisoformat(query_result[1])
        if type(query_result[2]) is str:
            query_result[2] = json.loads(query_result[2])
        if type(query_result[5]) is str:
            query_result[5] = json.loads(query_result[5])

        return cls(*query_result)

@dataclass
class Notification:
    id: int
    body: str
    date_time: datetime
    read: bool

    class NotificationSchema(Schema):
        id = fields.Int(required=False)
        body = fields.Str()
        date_time = fields.DateTime(data_key='datetime')
        read = fields.Bool()

    @staticmethod
    def new_notification(body: str, date_time: datetime, read: bool = False) -> 'Notification':
        return Notification(
            id=-1,
            body=body,
            date_time=date_time,
            read=read,
        )

    @classmethod
    def from_query(cls, query_result):
        query_result = list(query_result)
        if type(query_result[2]) is str:
            query_result[2] = datetime.fromisoformat(query_result[2])
        if type(query_result[3]) is not bool:
            query_result[3] = bool(query_result[3])

        return cls(*query_result)
