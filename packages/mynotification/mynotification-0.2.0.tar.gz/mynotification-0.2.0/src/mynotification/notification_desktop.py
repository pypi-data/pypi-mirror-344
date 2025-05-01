from notifypy import Notify


def send_notification(title, message):
    notification = Notify()
    notification.title = "Cool Title"
    notification.message = "Even cooler message."
    notification.send()
