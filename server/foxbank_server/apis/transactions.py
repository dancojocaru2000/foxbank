from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from ..decorators import ensure_logged_in
from ..models import Transaction
from ..db_utils import get_transactions
from .. import returns

bp = Blueprint('transactions', __name__, description='Bank transfers and other transactions')

@bp.route('/')
class TransactionsList(MethodView):
    class TransactionsParams(Schema):
        account_id = fields.Int(min=1)

    class TransactionsGetResponse(returns.SuccessSchema):
        transactions = fields.List(fields.Nested(Transaction.TransactionSchema))

    @ensure_logged_in
    @bp.response(401, returns.ErrorSchema, description='Login failure')
    @bp.doc(security=[{'Token': []}])
    @bp.arguments(TransactionsParams, as_kwargs=True, location='query')
    @bp.response(200, TransactionsGetResponse)
    def get(self, account_id: int):
        """Get transactions for a certain account"""
        return returns.success(
            transactions=[t.to_json() for t in get_transactions(account_id)]
        )

    class TransactionsCreateParams(Schema):
        account_id = fields.Int(min=1)
        destination_iban = fields.Str()
        amount = fields.Int(min=1)

    class TransactionsCreateResponse(returns.SuccessSchema):
        transaction = fields.Nested(Transaction.TransactionSchema)

    @ensure_logged_in
    @bp.response(401, returns.ErrorSchema, description='Login failure')
    @bp.doc(security=[{'Token': []}])
    @bp.arguments(TransactionsCreateParams)
    @bp.response(200, TransactionsCreateResponse)
    def post(self, account_id: int, destination_iban: str, amount: int):
        """Create a send_transfer transaction"""
        raise NotImplementedError()
