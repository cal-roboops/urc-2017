import socket
import cv2
import numpy

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 3000))
recv_len = 32768

while True:
    try:
        msg = sock.recv(recv_len)
        data = numpy.fromstring(msg, dtype='uint8')
        decimg = cv2.imdecode(data,1)
        cv2.imshow('SERVER', decimg)
        cv2.waitKey(1)
    except socket.error:
        print("Received Too Large")

cv2.destroyAllWindows()
sock.close()