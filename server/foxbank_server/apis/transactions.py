from datetime import date, datetime
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

import re

from ..decorators import ensure_logged_in
from ..db_utils import get_transactions, get_account, get_accounts, insert_transaction, whose_account
from ..models import Account, Transaction
from ..utils.iban import check_iban
from .. import decorators, returns

bp = Blueprint('transactions', __name__, description='Bank transfers and other transactions')

@bp.route('/')
class TransactionsList(MethodView):
    class TransactionsParams(Schema):
        account_id = fields.Int(min=1)

    class TransactionsGetResponse(returns.SuccessSchema):
        transactions = fields.List(fields.Nested(Transaction.TransactionSchema))

    @ensure_logged_in
    @bp.response(401, returns.ErrorSchema, description='Login failure or not allowed')
    @bp.doc(security=[{'Token': []}])
    @bp.arguments(TransactionsParams, as_kwargs=True, location='query')
    @bp.response(200, TransactionsGetResponse)
    def get(self, account_id: int):
        """Get transactions for a certain account"""
        if whose_account(account_id) != decorators.user_id:
            return returns.abort(returns.UNAUTHORIZED)

        # return returns.success(
        #     transactions=[t.to_json() for t in get_transactions(account_id)]
        # )
        return returns.success(
            transactions=get_transactions(account_id)
        )

    class TransactionsCreateParams(Schema):
        account_id = fields.Int(min=1)
        destination_iban = fields.Str()
        amount = fields.Int(min=1)
        description = fields.Str(default='')

    class TransactionsCreateResponse(returns.SuccessSchema):
        transaction = fields.Nested(Transaction.TransactionSchema)

    @ensure_logged_in
    @bp.response(401, returns.ErrorSchema, description='Login failure or not allowed')
    @bp.response(404, returns.ErrorSchema, description='Destination account not found')
    @bp.response(422, returns.ErrorSchema, description='Invalid account')
    @bp.doc(security=[{'Token': []}])
    @bp.arguments(TransactionsCreateParams, as_kwargs=True)
    @bp.response(200, TransactionsCreateResponse)
    def post(self, account_id: int, destination_iban: str, amount: int, description: str = ''):
        """Create a send_transfer transaction"""
        if whose_account(account_id) != decorators.user_id:
            return returns.abort(returns.UNAUTHORIZED)

        account: Account = get_account(account_id=account_id)

        if account is None:
            return returns.abort(returns.invalid_argument('account_id'))

        amount = -1 * abs(amount)

        if account.balance + amount < 0:
            return returns.abort(returns.NO_BALANCE)

        # Check if IBAN is valid
        destination_iban = re.sub(r'\s', '', destination_iban)

        if not check_iban(destination_iban):
            return returns.abort(returns.INVALID_IBAN)

        date = datetime.now()

        # Check if transaction is to another FoxBank account
        reverse_transaction = None
        if destination_iban[4:8] == 'FOXB':
            for acc in get_accounts():
                if destination_iban == acc.iban:
                    reverse_transaction = Transaction.new_transaction(
                        date_time=date,
                        transaction_type='receive_transfer',
                        status='processed',
                        other_party={'iban': account.iban,},
                        extra={'currency': account.currency, 'amount': -amount,},
                    )
                    insert_transaction(acc.id, reverse_transaction)
                    break
            else:
                return returns.abort(returns.NOT_FOUND)

        transaction = Transaction.new_transaction(
            date_time=date,
            transaction_type='send_transfer',
            status=('processed' if reverse_transaction is not None else 'pending'),
            other_party={'iban': destination_iban,},
            extra={
                'currency': account.currency,
                'amount': amount,
                'description': description,
            },
        )

        insert_transaction(account_id, transaction)

        return returns.success(transaction=transaction)
