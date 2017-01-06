# import cv2
# import numpy as np
# import socket
# import sys
# import pickle
# import struct
# import errno
#
# HOST = '127.0.0.1'
# PORT = 8083
#
#
# cap = cv2.VideoCapture(0)
#
#
# clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # clientsocket.connect((HOST, PORT))
#
# clientsocket.bind((HOST, PORT))
#
# clientsocket.listen(10)
#
# while True:
#     client, address = clientsocket.accept()
#     ret, frame = cap.read()
#     if ret:
#         frame = frame.flatten()
#         data = frame.tostring()
#         clientsocket.send(data)
#     # data = pickle.dumps(frame)
#     # clientsocket.sendall(struct.pack("L", len(data)) + data)
#
# clientsocket.close()


import socket
import cv2
import numpy

TCP_IP = '0.0.0.0'
TCP_PORT = 5001

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

capture = cv2.VideoCapture(1)

while True:
    ret, frame = capture.read()
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    sock.send( str(len(stringData)).ljust(16));
    sock.send(stringData);

sock.close()

decimg=cv2.imdecode(data,1)
cv2.imshow('CLIENT',decimg)
cv2.waitKey(0)
cv2.destroyAllWindows()