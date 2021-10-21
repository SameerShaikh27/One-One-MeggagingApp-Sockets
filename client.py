import socket
import threading
from tkinter import *
from tkinter import scrolledtext
from tkinter import simpledialog

HOST = "127.0.0.1"
PORT = 1234


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # Popping up a message box to ask their name. After that only, we will show them a chat app.
        msg = Tk()
        msg.withdraw()

        self.name = simpledialog.askstring("Name", "Choose a name to connect", parent=msg)

        # Below code means that gui is not yet built.
        self.gui_done = False

        # Below code means that connections are running properly.
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    # We will use this function to built GUI
    def gui_loop(self):

        self.root = Tk()
        self.root.geometry("800x560")
        self.root.title("One-One Messaging App")
        # Giving the Background Color
        self.root.configure(background="white")

        # Frames MAIN, CENTER, and BOTTOM
        self.main_frame = Frame(self.root, relief=RIDGE, width=740, height=520, bd=12, pady=10, padx=10, bg="#787276")
        self.main_frame.grid(row=1, column=0, padx=20)

        self.label1 = Label(self.main_frame, text="Chat History", font="Cooper 15 bold", justify=CENTER, bg="#787276")
        self.label1.pack()

        self.center_frame = Frame(self.main_frame, bg="white", relief=RIDGE, width=680, height=320, bd=8)
        self.center_frame.pack(padx=10, pady=5)

        self.label2 = Label(self.main_frame, text="Message Box", font="Cooper 15 bold", justify=CENTER, bg="#787276")
        self.label2.pack()

        self.bottom_frame = Frame(self.main_frame, bg="#4d4c5c", relief=RIDGE, width=680, height=10, bd=8)
        self.bottom_frame.pack(side=BOTTOM, padx=5, anchor="w", pady=5)

        # MAIN FRAME
        # Creating scrolled textarea widget
        self.text_area = scrolledtext.ScrolledText(self.center_frame, wrap=WORD, width=70, height=15, font="arial 12", bd=3)
        self.text_area.grid(row=0, column=0, padx=5, pady=5)
        self.text_area.config(state="disabled")

        # BOTTOM FRAME # BOTTOM FRAME # BOTTOM FRAME # BOTTOM FRAME
        # Entry box to input answers
        self.e_messagebox = Text(self.bottom_frame, font="arial 15", width=50, bd=2, height=1)
        self.e_messagebox.grid(row=0, column=1, padx=10)

        # To submit answers
        self.b_send = Button(self.bottom_frame, text="Send", font="Cooper 12 bold", bg="#adadc9", bd=5, command=self.write)
        self.b_send.grid(row=0, column=2, pady=5, padx=10)

        self.gui_done = True

        self.root.protocol("WM_DELETE_WINDOW", self.stop)

        self.root.mainloop()

    def write(self):
        # Sending a message with a name
        message = f"{self.name}: {self.e_messagebox.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))

        # Clearing the input area after sending the message.
        self.e_messagebox.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.root.destroy()
        self.sock.close()
        exit(0)

    # This function is handling the connection and receiving the new messages from the server.
    def receive(self):
        while self.running:
            try:
                # Trying to receive a message from a server.
                message = self.sock.recv(1024).decode('utf-8')
                if message == "Name":
                    self.sock.send(self.name.encode('utf-8'))
                else:
                    if self.gui_done:
                        # Here, we are enabling the state of the textarea to input the message
                        self.text_area.config(state="normal")
                        # Inserting the message in the textarea at the end (Basically appending)
                        self.text_area.insert('end', message)
                        # Scrolling the textarea towards the 'end' which means down
                        self.text_area.yview('end')
                        # Here, we are disabling the state of the textarea after inputting the message
                        self.text_area.config(state="disabled")

            except ConnectionAbortedError:
                break
            except:
                print("General Error")
                self.sock.close()
                break


client = Client(HOST, PORT)
