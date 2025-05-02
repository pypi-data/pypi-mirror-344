from jnius import autoclass
import traceback
import os


def send_notification(title: str, message: str):
    try:
        activity_host_class = os.getenv("MAIN_ACTIVITY_HOST_CLASS_NAME")
        assert activity_host_class
        activity_host = autoclass(activity_host_class)
        activity = activity_host.mActivity
        Context = autoclass("android.context.Context")
        NotificationManager = autoclass("android.app.NotificationManager")
        NotificationChannel = autoclass("android.app.NotificationChannel")
        Notification = autoclass("android.app.Notification")
        NotificationBuilder = autoclass("android.app.NotificationBuilder")
        notification_service = activity.getSystemService(Context.NOTIFICATION_SERVICE)
        channel_id = "my_notification_channel"
        channel_name = "Flet Notification Channel"
        importance = NotificationManager.IMPORTANCE_DEFAULT
        channel = NotificationChannel(channel_id, channel_name, importance)
        notification_service.createNotificationChannel(channel)
        builder = NotificationBuilder(activity, channel_id)
        builder.setContentTitle(title)
        builder.setContentText(message)
        builder.setSmallIcon(activity.getApplicationInfo().icon)
        builder.setAutoCancel(True)
        notification_id = 1
        notification = builder.build()
        notification_service.notify(notification_id, notification)
        print("Notification sent succesfully.")
        # status_text.collor = "green"

    except:
        pass
