# John Taube
# 4/17/2020
# CIS 457-20
# This is the client side code for the chat application
import socket  # import sockets for TCP communication
import threading  # import threading for multiple threads of action
from tkinter import *  # import all tkinter for GUI

# message receive
def inMsg():
    while True:  # thread will always run, until program is killed
        try:
            msg = sock.recv(BUFFER_SIZE).decode()  # get and decode message
            if msg == "{ExitApp}":
                msgLst.insert(END, "Notification: Friend has left.")  # place notification in chat history
                break
            else:
                msgLst.insert(END, "Friend: " + msg)
        except OSError:  # Client may have left chat
            break

# message send
def outMsg():
    msg = msgField.get()  # get message from message entry box
    msgE = msg.encode()  # encode message (required to send)
    try:
        sock.sendall(msgE)  # send message
        msgLst.insert(END, "You: " + msg)  # place message in chat history
    except OSError:  # if message send fails, no connection
        msgLst.insert(END, "Notification: No Connection.")  # place message in chat history

# when window closes
def onClose():
    msg = "{ExitApp}"  # tell host program that client has left
    msgE = msg.encode()  # encode message (required to send)
    try:
        sock.sendall(msgE)  # send message
    except OSError:
        pass
    sock.close()  # close connection
    window.quit() # close window


window = Tk()  # initialize window
window.title("ChatAppC")  # give window title
window.geometry('640x480')  # give window geometry
msgFr = Frame(window)  # message frame
scrollbar = Scrollbar(msgFr)  # navigate through other messages
msgLst = Listbox(msgFr, height=15, width=80, yscrollcommand=scrollbar.set, font=("Arial", 12))  # add message history
scrollbar.pack(side=RIGHT, fill=Y)
msgLst.pack(side=LEFT, fill=BOTH)
msgLst.pack()
msgFr.pack()
msgField = Entry(window, width=30, font=("Arial", 12))  # add entry field
msgField.pack()
sendBtn = Button(window, text="Send", command=outMsg)  # add send button
sendBtn.pack()
window.protocol("WM_DELETE_WINDOW", onClose)  # run function on close

BUFFER_SIZE = 5000  # Set buffer size
ADDR = ("localhost", 5005)  # preset address info
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # prep socket
try:
    sock.connect(ADDR)  # try to connect to address
    msgLst.insert(END, "Notification: Connection established!")  # place notification in chat history
    rcvThread = threading.Thread(target=inMsg)  # set up receiving thread
    rcvThread.start()  # start receiving thread
except OSError:  # on connection fail
    msgLst.insert(END, "Notification: Can't connect")  # place notification in chat history
mainloop()  # update GUI, blocking
quit()  # quit program, when GUI update passes block
