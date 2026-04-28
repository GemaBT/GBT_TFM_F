"""from api.models import AuthLog

def log_event(user, action, status, request):
    ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')

    AuthLog.objects.create(
        user=user,
        action=action,
        status=status,
        ip_address=ip,
        user_agent=user_agent
    )
    """
from api.models import AuthLog

def log_event(user, action, status, request):
    AuthLog.objects.create(
        user=user,  # 👈 aquí va el objeto, no el id
        action=action,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
        status=status
    )