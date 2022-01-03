from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from ..db_utils import get_forex_rate
from .. import returns

bp = Blueprint('forex', __name__, description='Foreign Exchange information')

class GetExchangeResult(returns.SuccessSchema):
    rate = fields.Float(optional=True)

@bp.get('/<from_currency>/<to_currency>')
@bp.response(422, returns.ErrorSchema, description='Invalid currency')
@bp.response(200, GetExchangeResult)
def get_exchange(from_currency: str, to_currency: str):
    """Get exchange rate between two currencies"""
    if from_currency == to_currency:
        rate = 1
    else:
        rate = get_forex_rate(from_currency, to_currency)

    if rate is None:
        return returns.abort(returns.invalid_argument('currency'))

    return returns.success(rate=rate)
