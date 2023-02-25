from socket import *
from threading import Thread
import tkinter



def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            msg_list.insert(tkinter.END, msg)
        except Exception:  # если клиент ушел
            break



def send(event=None):
    msg = my_msg.get()
    my_msg.set("")  # Очищает поле ввода.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "<>":
        client_socket.close()
        top.quit()



def on_closing(event=None):
    """Эта функция должна вызываться при закрытии окна."""
    my_msg.set("<>")
    send()

top = tkinter.Tk()
top.title("Мой чат")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()# Для отправки сообщений.
my_msg.set("Введите ваше имя")
scrollbar = tkinter.Scrollbar(messages_frame)  # Для навигации по прошлым сообщениям.
# Далее будут сообщения.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
msg_list.configure(background='red',font=20,)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.configure(background="yellow",width=50,bd=5,font=30)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Отправить", command=send)
send_button.configure(background="green",width=20)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Теперь идет часть сокетов----
HOST = "127.0.0.1"
PORT = ""
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

ADDR = (HOST,PORT)

client_socket = socket()
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Запускает выполнение графического интерфейса.