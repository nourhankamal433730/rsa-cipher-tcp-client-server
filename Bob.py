import socket
import pickle
import random
import tkinter as tk
from tkinter import messagebox
from threading import Thread

def is_probably_prime(n, k=5):
    """Test if a number is probably prime using Miller-Rabin test."""
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_rsa_keypair(bit_length=512):
    """Generate a RSA key pair using random prime numbers."""
    while True:
        p = random.getrandbits(bit_length)
        if is_probably_prime(p):
            break

    while True:
        q = random.getrandbits(bit_length)
        if is_probably_prime(q) and q != p:
            break

    n = p * q
    totient = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, totient)

    return n, totient, e, d

def string_to_int(s):
    """Convert a string to an integer using ASCII encoding."""
    result = 0
    for letter in s:
        result = result * 128 + ord(letter)
    return result

def int_to_string(n):
    """Convert an integer to a string using ASCII encoding."""
    result = ""
    while n > 0:
        result = chr(n % 128) + result
        n = n // 128
    return result

def print_ciphertext(ciphertext):
    #messagebox.showinfo("Ciphertext Received", f"Ciphertext: {ciphertext}")
    print(f"Ciphertext received: {ciphertext}")

def start_server():
    #we use "127.0.0.1" because the client and server are on the same machine,
    HOST = "127.0.0.1"
    PORT = 5005

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        update_status(f"Server Listening for connections on {HOST}:{PORT}...")

        conn, addr = s.accept()
        with conn:
            update_status(f"Connected by {addr}")

            n, totient, e, d = generate_rsa_keypair()
            public_key = (n, e)
            serialized_key = pickle.dumps(public_key)
            conn.sendall(serialized_key)

            ciphertext = pickle.loads(conn.recv(1024))
            print_ciphertext(ciphertext)

            plaintext = int_to_string(pow(ciphertext, d, n))
            update_status(f"Message received: {plaintext}")

def send_message():
    HOST = "127.0.0.1"
    PORT = 5005

    message = message_entry.get()
    message = string_to_int(message)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        data = s.recv(1024)
        received_key = pickle.loads(data)
        print(f"Received public key: {received_key}")

        n, e = received_key

        if len(bin(message)[2:]) < n.bit_length():
            ciphertext = pow(message, e, n)
            serialized_ciphertext = pickle.dumps(ciphertext)
            s.sendall(serialized_ciphertext)
            messagebox.showinfo("Success", "Message sent successfully")
        else:
            messagebox.showerror("Error", "Message is too large for encryption")

def update_status(message):
    status_label.config(text=message)

def clear_status():
    # Clear the status after the delay
    status_label.config(text="")

# GUI for Bob
bob_window = tk.Tk()
bob_window.title("Bob - Client")

# Background image
bg_image = tk.PhotoImage(file="D:/network securiity project/rsa-cipher-tcp-client-server-main/images/WhatsApp-Image-2024-05-10-at-11.29.07_24c46b23.png")  # Change the filename to your image file
bg_label = tk.Label(bob_window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

message_label = tk.Label(bob_window, text="Enter your message:",font=("Arial", 11))
message_label.pack(pady=10)
message_label.pack()

message_entry = tk.Entry(bob_window, font=("Arial", 12))
message_entry.pack(pady=5)
message_entry.pack()

send_button = tk.Button(bob_window, text="Send Message", command=send_message,
                        font=("Arial", 12), bg="purple", fg="white", activebackground="darkblue", padx=10, pady=5)
send_button.pack(pady=12)
send_button.pack()

status_label = tk.Label(bob_window, text="Server not started",font=("Arial", 12), padx=100, pady=100)
status_label.pack()

start_button = tk.Button(bob_window, text="Start Server", command=lambda: Thread(target=start_server).start(),
                         font=("Arial", 12), bg="purple", fg="white", activebackground="darkgreen", padx=10, pady=5)
start_button.pack(pady=16)
start_button.pack()

bob_window.mainloop()























