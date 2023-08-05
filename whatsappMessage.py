import webbrowser
import pyautogui
import time

contact = {
    "sam": "+91**********",
    "john": "+91**********"
}
def send_whatsapp_message(reciver, message):
    phone_number = ""
    found = False
    for name, number in contact.items():
        if name == reciver:
            phone_number = number
            found = True
            break
    if not found:
        return f"No contact named {reciver}"
    formatted_phone_number = "".join(filter(str.isdigit, phone_number))
    whatsapp_link = f"https://wa.me/{formatted_phone_number}?text={message}"
    webbrowser.open(whatsapp_link)
    time.sleep(5)
    pyautogui.press('enter')
    return "Message sent!"


