import socket
import cv2
import numpy
import sys

# Command line arg list
# [ip_addr ip_port cam_num]

if len(sys.argv) < 4:
	print("Error not enough arguments!")
	exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((sys.argv[1], int(sys.argv[2])))

capture = cv2.VideoCapture(int(sys.argv[3]))

while True:
    ret, frame = capture.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    try:
        sock.send(stringData);
    except socket.error as e:
    	print(e)

sock.close()