from http import HTTPStatus
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields

import re

from ..decorators import ensure_logged_in
from ..models import Account
from ..utils.iban import IBAN_BANKS, check_iban
from .. import decorators
from .. import db_utils
from .. import returns

bp = Blueprint('accounts', __name__, description='Bank Accounts operations')

VALID_CURRENCIES = ['RON', 'EUR', 'USD']
ACCOUNT_TYPES = ['Checking', 'Savings']

class MetaCurrenciesSchema(returns.SuccessSchema):
    currencies = fields.List(fields.Str())

class MetaAccountTypesSchema(returns.SuccessSchema):
    account_types = fields.List(fields.Str(), data_key='accountTypes')

class MetaValidateIbanParams(Schema):
    iban = fields.Str(example='RO15RZBR0000060021338765')

class MetaValidateIbanSchema(returns.SuccessSchema):
    valid = fields.Bool()
    formatted_iban = fields.Str(data_key='formattedIban', optional=True)
    bank_name = fields.Str(data_key='bankName', optional=True, description='Known bank for IBAN')

@bp.get('/meta/currencies')
@bp.response(200, MetaCurrenciesSchema)
def get_valid_currencies():
    """Get valid account currencies"""
    return returns.success(currencies=VALID_CURRENCIES)


@bp.get('/meta/account_types')
@bp.response(200, MetaAccountTypesSchema)
def get_valid_account_types():
    """Get valid account types"""
    return returns.success(account_types=ACCOUNT_TYPES)


@bp.get('/meta/validate_iban')
@bp.arguments(MetaValidateIbanParams, location='query', as_kwargs=True)
@bp.response(200, MetaValidateIbanSchema)
def get_validate_iban(iban: str):
    """Validate IBAN"""
    iban = re.sub(r'\s', '', iban)
    valid = len(iban) > 8 and re.match(r'^[A-Z]{2}[0-9]{2}', iban) is not None and check_iban(iban)
    bank_name = None
    if iban[0:2] in IBAN_BANKS:
        if iban[4:8] in IBAN_BANKS[iban[0:2]]:
            bank_name = IBAN_BANKS[iban[0:2]][iban[4:8]]

    return returns.success(
        valid=valid,
        formatted_iban=re.sub(r'(.{4})', r'\1 ', iban).strip() if valid else None,
        bank_name=bank_name if valid else None,
    )


class AccountResponseSchema(returns.SuccessSchema):
    account = fields.Nested(Account.AccountSchema)


@bp.get('/<int:account_id>')
@ensure_logged_in
@bp.response(401, returns.ErrorSchema, description='Login failure or not allowed')
@bp.doc(security=[{'Token': []}])
@bp.response(200, AccountResponseSchema)
def get_account_id(account_id: int):
    """Get account by id"""
    account = db_utils.get_account(account_id=account_id)
    if account is None:
        return returns.abort(returns.NOT_FOUND)
    if decorators.user_id != db_utils.whose_account(account):
        return returns.abort(returns.UNAUTHORIZED)
    # account = account.to_json()
    return returns.success(account=account)


@bp.get('/IBAN_<iban>')
@ensure_logged_in
@bp.response(401, returns.ErrorSchema, description='Login failure')
@bp.doc(security=[{'Token': []}])
@bp.response(200, AccountResponseSchema)
def get_account_iban(iban: str):
    """Get account by IBAN"""
    account = db_utils.get_account(iban=iban)
    if account is None:
        return returns.abort(returns.NOT_FOUND)
    if decorators.user_id != db_utils.whose_account(account):
        return returns.abort(returns.UNAUTHORIZED)
    # account = account.to_json()
    return returns.success(account=account)


@bp.route('/')
class AccountsList(MethodView):
    class CreateAccountParams(Schema):
        currency = fields.String(example='RON')
        account_type = fields.String(data_key='accountType', example='Checking')
        custom_name = fields.String(data_key='customName', example='Daily Spending')

    class CreateAccountResponseSchema(returns.SuccessSchema):
        account = fields.Nested(Account.AccountSchema)

    @ensure_logged_in
    @bp.response(401, returns.ErrorSchema, description='Login failure')
    @bp.doc(security=[{'Token': []}])
    @bp.arguments(CreateAccountParams, as_kwargs=True)
    @bp.response(200, CreateAccountResponseSchema)
    @bp.response(422, returns.ErrorSchema, description='Invalid currency or account type')
    def post(self, currency: str, account_type: str, custom_name: str):
        """Create account"""
        if currency not in VALID_CURRENCIES:
            return returns.abort(returns.invalid_argument('currency'))
        if account_type not in ACCOUNT_TYPES:
            return returns.abort(returns.invalid_argument('account_type'))

        account = Account(-1, '', currency, account_type, custom_name or '')
        db_utils.insert_account(decorators.user_id, account)
        # return returns.success(account=account.to_json())
        return returns.success(account=account)

    class AccountsResponseSchema(returns.SuccessSchema):
        accounts = fields.List(fields.Nested(Account.AccountSchema))

    @ensure_logged_in
    @bp.response(401, returns.ErrorSchema, description='Login failure')
    @bp.doc(security=[{'Token': []}])
    @bp.response(200, AccountsResponseSchema)
    def get(self):
        """Get all accounts of user"""
        return returns.success(accounts=db_utils.get_accounts(decorators.user_id))

