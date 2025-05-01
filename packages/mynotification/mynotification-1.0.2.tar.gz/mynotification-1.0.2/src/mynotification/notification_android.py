from jnius import autoclass


def send_notification(title: str, message: str):
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Context = autoclass("android.content.Context")
    NotificationBuilder = autoclass("android.app.Notification$Builder")
    NotificationManager = autoclass("android.app.NotificationManager")
    activity = PythonActivity.mActivity
    builder = NotificationBuilder(activity)
    builder.setContentTitle(title)
    builder.setContentText(message)
    builder.setSmallIcon(activity.getApplicationInfo().icon)
    notification = builder.build()
    service = activity.getSystemService(Context.NOTIFICATION_SERVICE)
    service.notify(0, notification)
