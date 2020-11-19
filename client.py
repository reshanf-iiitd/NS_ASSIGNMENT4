import socket 
import os
import time
import datetime
import hashlib

HOST = '127.0.0.1'                        # The server's hostname or IP address
PORT = 41800                                  # The port used by the server
FILE = "upload_document.txt"                  # File to be sent to server
ENC_FILE = "upload_document.txt.enc"          # Name of received file with GMT and DS
# ENC_FILE = "gmt_ds1.txt"
FILE1 = "upload_document1.txt"   
FILE2= "verf.txt"

def date_time(gmt):
    temp = gmt.split(" ")
    temp1 = temp[0]
    # print(temp)
    datee = temp1.split("-")
    # print(datee)
    yy = int(datee[0])
    mm = int(datee[1])
    dd = int(datee[2])

    temp2 = temp[1]
    timee = temp2.split(":")
    hh= int(timee[0])
    minu = int(timee[1])
    
    return yy,mm,dd,hh,minu


def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


def helper_to_ver(FF):
    ## Getting the Recieved File Content after Decrypting
    with open(FF) as f:
        lines = [line.rstrip() for line in f]
    # print(lines)

    ## Getting the details of sent file 
    # with open("upload_document.txt") as f1:
    #     lines1 = [line.rstrip() for line in f1]

    gmt =datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    yy,mm,dd,hh,minu = date_time(gmt)
    # print(yy,mm,dd,minu,hh)

    yy1,mm1,dd1,hh1,minu1 = date_time(lines[2])

    f2 = open(FILE2,"w")
    f2.write("Name : Reshan Faraz")
    f2.write("\n")
    f2.write("Roll No : PhD19006")
    f2.write("\n")
    f2.write(lines[2])
    f2.close()

    hs = hash_file(FILE2)
    # print(hs)
    # print(lines)
    f=0
    if(yy == yy1 and mm == mm1 and dd==dd1 and hh==hh1 and abs(minu - minu1) <= 4):
        print("GMT Date and Time is right and recieved within time")
        print(lines[2])
        f=1
    f1 =0
    if(hs == lines[3]):
        print("Document Verified Succesfully Hashed Matched ")
        print(hs+ "=="+lines[3])
        f1=1

    if(f1 ==1 and f==1):
        print("************ VERIFIED SUCCESFULLY ******************")
        print("************ Document has correct GMT date/time Stamping ******************")

    if(f==0):
        print("Document Stamping is not valid because it was done 4 minute before")

    if(f1==0):
        print("Document Verfication fails because hashed not matched")




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to", s.getpeername())
    tosend = open(FILE,"rb")
    payload = tosend.read(1024)
    print("Sending file for Stamping")
    while(payload):
        s.send(payload)
        payload=tosend.read(1024)
    s.shutdown(socket.SHUT_WR)
    tosend.close()
    print("Done sending.\n")
    print("Waiting for file with digital signature and timestamping...")
    encfile = open(ENC_FILE,"wb")
    while True:
            data = s.recv(1024)
            print("Receiving upload_document with GMT date/time stamping and Digital Signature...")
            while(data):
                encfile.write(data)
                data=s.recv(1024)
                if not data:
                    print("File received.\n")
                    encfile.close()
                    break
            break

    # encfile = open(FILE2,"wb")
    # while True:
    #         data = s.recv(1024)
    #         print("Receiving upload_document with GMT and Digital Signature...")
    #         while(data):
    #             encfile.write(data)
    #             data=s.recv(1024)
    #             if not data:
    #                 print("File received.")
    #                 encfile.close()
    #                 break
    #         break   


    print("Decrypting file...")
    os.system("openssl rsautl -decrypt -inkey key.pem -in upload_document.txt.enc -out upload_document1.txt")
    

    helper_to_ver("upload_document1.txt")
    # os.system("openssl dgst -sha256 -verify public.pem -signature verf.txt upload_document1.txt ")
    print("Below is the content of the Recieved Document ...\n")

    ff=open('upload_document1.txt')
    print(ff.read())
    # print("Thanks a lot and Bye.")
    s.close()
