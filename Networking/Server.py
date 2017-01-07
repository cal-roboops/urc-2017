import socket
import cv2
import numpy
import sys

# Command line arg list
# [ip_port cam_name]

if len(sys.argv) < 2:
	print("Error not enough arguments!")
	exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', int(sys.argv[1])))
recv_len = 65536 	#32768 (Large enough for some cameras)

while True:
    try:
        msg = sock.recv(recv_len)
        data = numpy.fromstring(msg, dtype='uint8')
        decimg = cv2.imdecode(data,1)
        cv2.imshow(sys.argv[2], decimg)
        cv2.waitKey(1)
    except socket.error as e:
        print(e)

cv2.destroyAllWindows()
sock.close()