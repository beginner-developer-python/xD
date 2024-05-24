
from win10toast import ToastNotifier
def send_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=10)
send_notification("PokeMMO Captcha", "PokeMMO Captcha")
send_notification("PokeMMO Captcha", "PokeMMO Captcha")