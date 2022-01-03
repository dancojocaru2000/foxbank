from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from ..db_utils import get_notifications, insert_notification, mark_notification_as_read, whose_notification
from ..decorators import ensure_logged_in
from ..models import Notification
from .. import decorators, returns

bp = Blueprint('notifications', __name__, description='Notifications operations')

@bp.post('/<int:notification_id>/mark_read')
@ensure_logged_in
@bp.response(401, returns.ErrorSchema, description='Login failure or not allowed')
@bp.doc(security=[{'Token': []}])
@bp.response(201, description='Successfully marked as read')
def mark_as_read(notification_id: int):
    """Mark notification as read"""
    if decorators.user_id != whose_notification(notification_id):
        return returns.abort(returns.UNAUTHORIZED)
    mark_notification_as_read(notification_id)


@bp.route('/')
class NotificationsList(MethodView):
    class NotificationsListPostParams(Schema):
        body = fields.Str(description='Text of the notification')
        read = fields.Bool(default=False, description='Whether the notification was read or not')

    class NotificationsListPostSchema(returns.SuccessSchema):
        notification = fields.Nested(Notification.NotificationSchema)

    @ensure_logged_in
    @bp.response(401, returns.ErrorSchema, description='Login failure')
    @bp.doc(security=[{'Token': []}])
    @bp.arguments(NotificationsListPostParams, as_kwargs=True)
    @bp.response(200, NotificationsListPostSchema)
    def post(self, body: str, read: bool = False):
        """Post a notification to the currently logged in user

        The usefulness of this endpoint is questionable besides debugging since it's a notification to self
        """
        now = datetime.now()
        notification = Notification.new_notification(body, now, read)
        insert_notification(decorators.user_id, notification)
        return returns.success(notification=notification)

    class NotificationsListGetSchema(returns.SuccessSchema):
        notifications = fields.List(fields.Nested(Notification.NotificationSchema))

    @ensure_logged_in
    @bp.response(401, returns.ErrorSchema, description='Login failure')
    @bp.doc(security=[{'Token': []}])
    @bp.response(200, NotificationsListGetSchema)
    def get(self):
        """Get all notifications for current user"""
        notifications = get_notifications(decorators.user_id)

        return returns.success(notifications=notifications)
