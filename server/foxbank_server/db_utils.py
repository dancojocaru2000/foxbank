from functools import wraps
import json
import sys
from types import ModuleType

from . import db as _db
from . import models

_db_global: None | tuple[_db.get_return, int] = None


def get_db(fn):
    @wraps(fn)
    def wrapper(*args, **kargs):
        global _db_global
        if _db_global is None:
            _db_global = _db.get(), 1
        else:
            _db_global = _db_global[0], _db_global[1] + 1
        result = fn(*args, **kargs)
        _db_global = _db_global[0], _db_global[1] - 1
        if _db_global[1] == 0:
            _db_global = None
        return result

    return wrapper


class Module(ModuleType):
    @property
    def db(self) -> _db.get_return:
        if _db_global is None:
            raise Exception('Function not wrapped with @get_db, db unavailable')
        return _db_global[0]


    @get_db
    def get_user(self, username: str | None = None, user_id: int | None = None) -> models.User | None:
        cur = self.db.cursor()
        if username is not None:
            cur.execute('select * from users where username=?', (username,))
        elif user_id is not None:
            cur.execute('select * from users where id=?', (user_id,))
        else:
            raise Exception('Neither username or user_id passed')
        result = cur.fetchone()
        if result is None:
            return None
        return models.User.from_query(result)


    @get_db
    def insert_user(self, user: models.User):
        # Prepare user
        if not user.otp:
            from pyotp import random_base32
            user.otp = random_base32()

        cur = self.db.cursor()
        cur.execute(
            'insert into users(username, email, otp, fullname) values (?, ?, ?, ?)',
            (user.username, user.email, user.otp, user.fullname),
        )

        cur.execute(
            'select id from users where username = ? and email = ? and otp = ? and fullname = ?',
            (user.username, user.email, user.otp, user.fullname),
        )

        user.id = cur.fetchone()['id']


    @get_db
    def get_accounts(self, user_id: int | None = None) -> list[models.Account]:
        """
        Get all accounts.
        If `user_id` is provided, get only the accounts for the matching user.
        """
        cur = self.db.cursor()
        if user_id:
            cur.execute('''
                select id, iban, currency, account_type, custom_name from accounts
                inner join users_accounts
                    on accounts.id = users_accounts.account_id
                where users_accounts.user_id = ?
            ''', (user_id,))
        else:
            cur.execute('select id, iban, currency, account_type, custom_name from accounts')
        accounts = [models.Account.from_query(q) for q in cur.fetchall()]

        for account in accounts:
            cur.execute(
                'select balance from V_account_balance where account_id = ?',
                (account.id,),
            )

            result = cur.fetchone()
            if result is not None:
                account.balance = result['balance']

        return accounts


    @get_db
    def get_account(self, account_id: int | None = None, iban: str | None = None) -> models.Account | None:
        cur = self.db.cursor()
        if account_id is not None:
            cur.execute(
                'select * from accounts where id=?',
                (account_id,),
            )
        elif iban is not None:
            cur.execute(
                'select * from accounts where iban=?',
                (iban,),
            )
        else:
            raise Exception('Neither username or user_id passed')
        result = cur.fetchone()
        if result is None:
            return None
        account = models.Account.from_query(result)

        cur.execute(
            'select balance from V_account_balance where account_id = ?',
            (account.id,),
        )

        result = cur.fetchone()
        if result is not None:
            account.balance = result['balance']

        return account


    @get_db
    def whose_account(self, account: int | models.Account) -> int | None:
        try:
            account_id = account.id
        except AttributeError:
            account_id = account

        cur = self.db.cursor()
        cur.execute('select user_id from users_accounts where account_id = ?', (account_id,))
        result = cur.fetchone()
        if not result:
            return None
        return result['user_id']


    @get_db
    def insert_account(self, user_id: int, account: models.Account):
        # Prepare account
        ibans = [acc.iban for acc in self.get_accounts(user_id)]
        if not account.iban:
            from random import randint
            while True:
                iban = 'RO00FOXB0' + account.currency
                iban += str(randint(10, 10 ** 12 - 1)).rjust(12, '0')
                from .utils.iban import gen_check_digits
                iban = gen_check_digits(iban)
                if iban not in ibans:
                    break
            account.iban = iban

        cur = self.db.cursor()
        cur.execute(
            'insert into accounts(iban, currency, account_type, custom_name) values (?, ?, ?, ?)',
            (account.iban, account.currency, account.account_type, account.custom_name),
        )

        cur.execute(
            'select id from accounts where iban = ?',
            (account.iban,),
        )
        account.id = cur.fetchone()['id']

        cur.execute(
            'insert into users_accounts(user_id, account_id) VALUES (?, ?)',
            (user_id, account.id)
        )

        self.db.commit()

    @get_db
    def get_transactions(self, account_id: int) -> list[models.Transaction]:
        cur = self.db.cursor()
        cur.execute(
            'select transaction_id from accounts_transactions where account_id = ?',
            (account_id,),
        )

        transactions = []
        for tid in (row['transaction_id'] for row in cur.fetchall()):
            cur.execute(
                'select * from transactions where id = ?',
                (tid,),
            )

            db_res = cur.fetchone()
            if db_res is None:
                continue
            transactions.append(models.Transaction.from_query(db_res))

        return transactions

    @get_db
    def insert_transaction(self, account_id: int, transaction: models.Transaction):
        cur = self.db.cursor()
        cur.execute(
            'insert into transactions(datetime, other_party, status, type, extra) values (?, ?, ?, ?, ?)',
            (
                transaction.date_time.isoformat(),
                json.dumps(transaction.other_party),
                transaction.status,
                transaction.transaction_type,
                json.dumps(transaction.extra),
            ),
        )

        cur.execute(
            'select id from transactions where datetime = ? and other_party = ? and status = ? and type = ? and extra = ?',
            (
                transaction.date_time.isoformat(),
                json.dumps(transaction.other_party),
                transaction.status,
                transaction.transaction_type,
                json.dumps(transaction.extra),
            ),
        )
        transaction.id = cur.fetchone()['id']

        cur.execute(
            'insert into accounts_transactions(account_id, transaction_id) values (?, ?)',
            (account_id, transaction.id),
        )

        self.db.commit()

    @get_db
    def get_notifications(self, user_id: int) -> list[models.Notification]:
        cur = self.db.cursor()

        cur.execute(
            '''
            select n.id, n.body, n.datetime, n.read
            from notifications as n
            inner join users_notifications on n.id = users_notifications.notification_id
            where users_notifications.user_id = ?
            ''',
            (user_id,),
        )

        return [models.Notification.from_query(q) for q in cur.fetchall()]

    @get_db
    def insert_notification(self, user_id: int, notification: models.Notification):
        cur = self.db.cursor()

        cur.execute(
            'insert into notifications(body, datetime, read) values (?, ?, ?)',
            (
                notification.body,
                notification.date_time.isoformat(),
                1 if notification.read else 0,
            ),
        )

        cur.execute(
            'select id from notifications where body = ? and datetime = ? and read = ?',
            (
                notification.body,
                notification.date_time.isoformat(),
                1 if notification.read else 0,
            ),
        )
        notification.id = cur.fetchone()['id']

        cur.execute(
            'insert into users_notifications values (?, ?)',
            (user_id, notification.id,),
        )

        self.db.commit()

    @get_db
    def whose_notification(self, notification: int | models.Notification) -> int | None:
        try:
            notification_id = notification.id
        except AttributeError:
            notification_id = notification

        cur = self.db.cursor()
        cur.execute('select user_id from users_notifications where notification_id = ?', (notification_id,))
        result = cur.fetchone()
        if not result:
            return None
        return result[0]

    @get_db
    def mark_notification_as_read(self, notification_id: int):
        cur = self.db.cursor()
        cur.execute(
            'update notifications set read = 1 where id = ?',
            (notification_id,),
        )
        self.db.commit()

    @get_db
    def get_forex_rate(self, from_currency: str, to_currency: str) -> float | None:
        if from_currency == to_currency:
            return 1.0

        cur = self.db.cursor()

        if from_currency == 'RON' or to_currency == 'RON':
            currency_pairs = [(from_currency, to_currency)]
        else:
            currency_pairs = [(from_currency, 'RON'), ('RON', to_currency)]

        amount = 1.0
        for currency_pair in currency_pairs:
            to_select = 'to_ron'
            if currency_pair[0] == 'RON':
                to_select = 'from_ron'
            cur.execute(
                f'select {to_select} from exchange where currency = ?',
                (currency_pair[1] if currency_pair[0] == 'RON' else currency_pair[0],),
            )
            rate = cur.fetchone()
            if rate is None:
                amount = None
                break
            rate = rate[0]
            amount *= rate

        return amount


sys.modules[__name__] = Module(__name__)
