import socket
import cv2
import numpy
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(('127.0.0.1', 3000))

capture = cv2.VideoCapture(1)

while True:
    ret, frame = capture.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),50]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    try:
        sock.send(stringData);
    except socket.error:
        print("Too Large: " + str(len(stringData)))

sock.close()