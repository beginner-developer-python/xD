import tkinter as tk
from PIL import Image, ImageTk
import socket
import io
import pyautogui
from win10toast import ToastNotifier
import threading

class Sender:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.ip_address, self.port))

    def send_message(self, message):
        message_bytes = message.encode()
        self.socket.sendall(len(message_bytes).to_bytes(4, byteorder="big"))
        self.socket.sendall(message_bytes)

    def send_image(self, image_path):
        with open(image_path, "rb") as f:
            img_bytes = f.read()

        self.socket.sendall(len(img_bytes).to_bytes(4, byteorder="big"))
        self.socket.sendall(img_bytes)

    def close(self):
        self.socket.close()

class Receiver:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.socket.bind((self.ip_address, self.port))

    def listen(self):
        self.socket.listen()

    def accept(self):
        conn, addr = self.socket.accept()
        return conn, addr

    def receive_message(self, conn):
        message_length_bytes = conn.recv(4)
        message_length = int.from_bytes(message_length_bytes, byteorder="big")
        message_bytes = conn.recv(message_length)
        message = message_bytes.decode()
        return message

    def receive_image(self, conn):
        img_length_bytes = conn.recv(4)
        img_length = int.from_bytes(img_length_bytes, byteorder="big")
        img_bytes = b""

        while len(img_bytes) < img_length:
            chunk = conn.recv(img_length - len(img_bytes))
            if not chunk:
                break
            img_bytes += chunk

        img = Image.open(io.BytesIO(img_bytes))
        return img

    def close(self):
        self.socket.close()

sender_ip = ''
class GuiUpdater:
    def __init__(self, root):
        self.root = root
        self.image_label = tk.Label(self.root)
        self.image_label.pack()
        self.text_box = tk.Text(self.root, height=2, width=20)
        self.text_box.pack()
        self.button = tk.Button(self.root, text="Send Text", command=self.send_text)
        self.button.pack()

    def update_image(self, img):
        photo = ImageTk.PhotoImage(img)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
    
    def send_text(self):
        # Get the text from the text box
        text = self.text_box.get("1.0", "end-1c")
        # Create a Sender instance with the IP address and port of the receiver
        print(sender_ip, type(sender_ip))
        sender = Sender(sender_ip[0], 5001)
        try:
            sender.connect()
            sender.send_message(text)
            sender.close()
            # Close the existing root window
            self.image_label.configure(image=None)
            self.image_label.image = None
            self.root.iconify()
            # Create a new instance of Tkinter and restart the GUI

        except ConnectionRefusedError:
            print(f"Could not connect to {self.ip}.")


def send(ip_addresses, img):
    for ip_address in ip_addresses:
        sender = Sender(ip_address, 5000)
        try:
            sender.connect()
        except ConnectionRefusedError:
            print(f"Could not connect to {ip_address}.")
            continue
        
        sender.send_message("Hello, this is a popup message!")
        sender.send_image(img)
        sender.close()

        receiver = Receiver("", 5001)
        receiver.bind()
        receiver.listen()
        conn, ads = receiver.accept()
        message = receiver.receive_message(conn)
        receiver.close()
        return message

def listen_for_connections(gui_updater):
    receiver = Receiver("", 5000)
    receiver.bind()
    receiver.listen()

    while True:
        conn, Ip = receiver.accept()
        sender = Sender(Ip, 5001)
        message = receiver.receive_message(conn)
        img = receiver.receive_image(conn)
        w, h = pyautogui.size() 
        w = w / 2
        h = h / 2 
        img = img.resize([int(w), int(h)])
        global sender_ip
        sender_ip = Ip
        # Update the GUI using the GuiUpdater instance
        gui_updater.update_image(img)
        # Send notification and handle the rest of the connection as before
        send_notification("PokeMMO Captcha", "PokeMMO Captcha")
        sender.close()

def send_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PokeMMO Captcha")

    # Set the IP address of the receiver
    gui_updater = GuiUpdater(root)
    gui_updater.ip = ''

    # Start the separate thread for listening to incoming connections
    connection_thread = threading.Thread(target=listen_for_connections, args=(gui_updater,))
    connection_thread.start()

    # Start the Tkinter event loop
    root.mainloop()
