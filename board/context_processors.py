from board.models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        notification_recipient= request.user
        notifications = Notification.objects.filter(
            recipient = notification_recipient
            ).filter(
                is_read = False,
            )
        context = {'notifications_count': notifications.count(), 'notifications': notifications}
    else:
        context = {'notifications_count': 0, 'notifications': {}}

    return context
