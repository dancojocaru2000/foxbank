from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields
from .. import returns, ram_db, decorators
from ..db_utils import get_user
from ..models import User
from ..decorators import ensure_logged_in

from pyotp import TOTP

bp = Blueprint('login', __name__, description='Login operations')

class LoginParams(Schema):
    username = fields.String()
    code = fields.String()

class LoginResult(returns.SuccessSchema):
    token = fields.String()

class LoginSuccessSchema(returns.SuccessSchema):
    token = fields.String()

@bp.route('/')
class Login(MethodView):
    @bp.arguments(LoginParams, as_kwargs=True)
    @bp.response(401, returns.ErrorSchema, description='Login failure')
    @bp.response(200, LoginSuccessSchema)
    def post(self, username: str, code: str):
        user: User | None = get_user(username=username)
        if user is None:
            return returns.INVALID_DETAILS

        otp = TOTP(user.otp)
        if not otp.verify(code, valid_window=1):
            return returns.INVALID_DETAILS

        token = ram_db.login_user(user.id)
        return returns.success(token=token)

@bp.route('/whoami')
class WhoAmI(MethodView):
    class WhoAmISchema(returns.SuccessSchema):
        user = fields.Nested(User.UserSchema)

    @bp.response(401, returns.ErrorSchema, description='Login failure')
    @bp.response(200, WhoAmISchema)
    @bp.doc(security=[{'Token': []}])
    @ensure_logged_in
    def get(self):
        user: User | None = get_user(user_id=decorators.user_id)
        if user is not None:
            user = user.to_json()

        return returns.success(user=user)
