# John Taube
# 4/17/2020
# CIS 457-20
# This is the host side code for the chat application
import socket  # import sockets for TCP communication
import threading  # import threading for multiple threads of action
from tkinter import *  # import all tkinter for GUI

# close socket early, before connection
def notifClose():
    sock.close()

# connection notification
def connNotif():
    notif = Tk() # create window for connection notification
    lbl = Label(notif, text="Waiting for connection...", font=("Arial", 12)) # notify user of wait
    lbl.pack()
    notif.protocol("WM_DELETE_WINDOW", notifClose)  # on notification close, run function
    while not connStatus:  # run GUI update while window is open
        if(earlyEnd):  # if window closed before connection
            break  # break out of GUI update loop
        else:
            notif.update()
    notif.quit()  # quit window

# message receive
def inMsg():
    while True:  # thread will always run, until program is killed
        try:
            msg = conn.recv(BUFFER_SIZE).decode()  # get and decode message
            if msg == "{ExitApp}":
                msgLst.insert(END, "Notification: Friend has left.")  # place notification in chat history
                break  # break from loop
            else:
                msgLst.insert(END, "Friend: " + msg)  # place notification in chat history
        except OSError:  # Host may have left chat
            break  # break from loop

# message send
def outMsg():
    msg = msgField.get()  # get message from message entry box
    msgE = msg.encode()  # encode message (required to send)
    try:
        conn.sendall(msgE)  # send message
        msgLst.insert(END, "You: " + msg)  # insert message in chat history
    except OSError:
        msgLst.insert(END, "Notification: No Connection.")  # place notification in chat history

def onClose():
    msg = "{ExitApp}"  # tell client program that host has left
    msgE = msg.encode()  # encode message (required to send)
    try:
        conn.sendall(msgE)  # send message
    except OSError:
        pass
    conn.close()  # close connection
    window.quit()  # close window



window = Tk()  # initialize window
window.title("ChatAppH")  # give window title
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

BUFFER_SIZE = 5000  # Set buffer size
ADDR = ("localhost", 5005)  # preset address info
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # prep socket
sock.bind(ADDR)  # open socket
sock.listen(1)  # listen for connections
connStatus = False  # connection status for connection wait notification
earlyEnd = False  # early terminate boolean for connection
notifThread = threading.Thread(target=connNotif)  # set up connection wait notification thread
notifThread.start()  # start connection wait notification thread
try:  # try to accept connections
    conn, conAddr = sock.accept()  # accept connection, blocks while waiting
    connStatus = True  # change connection status, to close the connection wait notification thread
    rcvThread = threading.Thread(target=inMsg)
    rcvThread.start()
    msgLst.insert(END, "Notification: Connection established!")
    window.protocol("WM_DELETE_WINDOW", onClose)  # run function on close
    mainloop()  # update GUI, blocking
    quit()  # quit program, when GUI update passes block
except OSError:
    earlyEnd = True  # if accept failed, user has terminated early, close connection wait notification
    quit()  # quit program



