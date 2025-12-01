import traceback
from rest_framework.views import exception_handler
from rest_framework.response import Response
from apps.shared.utils.telegram_alerts import send_alert
from apps.shared.exceptions.custom_exceptions import CustomException
from apps.shared.utils.custom_response import CustomResponse
from apps.shared.utils.custom_current_host import get_client_ip

def custom_exception_handler(exc, context):
    """
    Handles all exceptions in DRF, sends alerts to Telegram,
    and returns a structured JSON response.
    """
    request = context.get('request')
    view = context.get('view')

    # Build message info
    view_name = view.__class__.__name__ if view else 'UnknownView'
    path = getattr(request, 'path', 'unknown') if request else 'unknown'
    method = getattr(request, 'method', 'unknown') if request else 'unknown'
    client_ip = get_client_ip(request) if request else 'unknown'
    port = request.META.get('REMOTE_PORT', 'unknown') if request else 'unknown'

    # Full traceback
    tb = traceback.format_exc()
    tb = tb[-2000:] if tb else "No traceback available"

    # Format Telegram message
    message = (
        f"❌ <b>Exception Alert</b> ❌\n\n"
        f"<b>View:</b> {view_name}\n"
        f"<b>Path & Method:</b> {method} {path}\n"
        f"<b>Client IP/Port:</b> {client_ip}:{port}\n\n"
    )

    if isinstance(exc, CustomException):
        message += f"<b>CustomException Message:</b> {exc.message_key}\n"
        if exc.context:
            message += f"<b>Context:</b> {exc.context}\n"
        send_alert(message)
        return CustomResponse.error(message_key=exc.message_key, request=request, context=exc.context)

    # Call default DRF handler first
    response = exception_handler(exc, context)

    # If unknown exception or not handled by DRF, send alert
    if response is None:
        message += f"<b>Exception:</b> {str(exc)}\n"
        message += f"<b>Traceback:</b> {tb}\n"
        send_alert(message)
        return CustomResponse.error(message_key="UNKNOWN_ERROR", request=request, context={'exc': str(exc)})

    # For DRF-handled exceptions, optionally alert (comment if too noisy)
    send_alert(message + f"<b>DRF Exception:</b> {str(exc)}")
    return response
