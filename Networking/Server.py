# import socket
# import sys
# import cv2
# import pickle
# import numpy
# import struct
# from PIL import Image, ImageTk
#
# def recvall(sock, count):
#     buf = b''
#     while count:
#         newbuf = sock.recv(count)
#         if not newbuf: return None
#         buf += newbuf
#         count -= len(newbuf)
#     return buf
#
# HOST = '127.0.0.1'
# PORT = 8083
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print 'Socket created'
#
# s.bind((HOST, PORT))
# print 'Socket bind complete'
# s.listen(10)
# print 'Socket now listening'
#
# conn, addr = s.accept()
#
# data = ""
# payload_size = struct.calcsize("L")
#
# while True:
#     # while len(data) < payload_size:
#     #     data += conn.recv(4096)
#     # packed_msg_size = data[:payload_size]
#     # data = data[payload_size:]
#     # msg_size = struct.unpack("L", packed_msg_size)[0]
#     # while len(data) < msg_size:
#     #     data += conn.recv (4096)
#     # frame_data = data[:msg_size]
#     # data = data[msg_size:]
#     #
#     # frame = pickle.loads(frame_data)
#     # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#     # img = Image.fromarray(cv2image)
#     # imgtk = ImageTk.PhotoImage(image=img)
#     data = s.recv()
#     print(data)
#     cv2.imshow('frame', data)
#
# s.close()

import socket
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = '0.0.0.0'
TCP_PORT = 5001

# HOST = '68.108.243.166'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
# s.connect((HOST, TCP_PORT))
s.listen(True)
conn, addr = s.accept()

while True:
    length = recvall(conn,16)
    stringData = recvall(conn, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    s.close()

    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER',decimg)
    cv2.waitKey(1)

cv2.destroyAllWindows()
