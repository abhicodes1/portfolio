#// The context processor must return a dictionary.
from .models import *
def get_notifications(request):
    print("In get notifs")
    Notifications = ""
    try:
        Notifications = notification.objects.filter(users=request.user)
        Notifications_count = notification.objects.filter(users=request.user, is_read=False).count()
        print("new notifications=",Notifications_count)
        print(Notifications)
        return {'notif': Notifications, "notif_c":Notifications_count}

    except:
        print("try did not work")  
        return {}
        
        
        
        
        
