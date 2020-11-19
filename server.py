import socket 
import os
import time
import datetime
import hashlib



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






HOST = '127.0.0.1'  
PORT = 41800            
FILEE = "gmt_ds.txt"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Waiing for connections...")
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        f = open(FILEE,'wb')
        while True:
            data = conn.recv(1024)
            print("Receiving file...")
            while(data):
                f.write(data)
                # print(f.line())
                data=conn.recv(1024)
            print("File received.")
            f.close()

            # x = input("Enter 1 to time stamp a Document")
            f1 = open(FILEE,'a')
            f1.write("\n")
            gmt =datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            f1.write(gmt)
            f1.close()
            ha = hash_file(FILEE)
            f2 = open(FILEE,'a')
            # os.system("openssl dgst -sha256 -sign key.pem -out gmt.txt gmt_ds.txt")
            f2.write("\n")
            f2.write(ha)

            f2.close()
            print("Encrypting file...")
            os.system("openssl rsautl -encrypt -pubin -inkey public.pem -in gmt_ds.txt -out gmt_ds.txt.enc")
            
            time.sleep(2)
            tosend = open("gmt_ds.txt.enc","rb")
            payload = tosend.read(1024)
            print("Sending file with GMT date/time Stamping with Digital signature.")
            while(payload):
                conn.send(payload)
                payload=tosend.read(1024)
            print("File sent.")
            break

            # tosend = open("gmt.txt","rb")
            # payload = tosend.read(1024)
            # while(payload):
            #     conn.send(payload)
            #     payload=tosend.read(1024)
            # print("Sig sent.")
            # break
        ######################
        ###################### DELETING THE FILE AFTER SENDING TO MEET POINT 3 IN QUESTION
        ###################### SO THAT SERVER DOES NOT ANY COPY OF THE DOCUMENT
        os.system("del gmt_ds.txt")
        print('Disconnecting ', addr)
        conn.close()




