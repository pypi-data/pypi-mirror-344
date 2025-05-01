class Notification:
    def init(self, title, message, platform):
        self.title = title
        self.message = message
        self.platform = platform

    def send_mynotification(self):
        desktop = ["linux", "windows", "macos"]
        if self.platform == "android":
            from src.mynotification.notification_android import send_notification

            send_notification(title=self.title, message=self.message)
        if self.platform in desktop:
            from src.mynotification.notification_android import send_notification

            send_notification(title=self.title, message=self.message)
