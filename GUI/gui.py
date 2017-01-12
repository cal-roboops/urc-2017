import atexit
from Tkinter import *
from PIL import Image, ImageTk
import socket
import cv2
import numpy
from threading import Thread
from time import sleep
import re


class Application(Frame):

    point_a = ()
    point_b = ()
    counter = 0
    coord_click_in = False

    dots = []
    lines = []

    prev_coord = ()

    def __init__(self, master=None):
        w = (root.winfo_screenwidth())
        h = root.winfo_screenheight()
        master.geometry("%dx%d+0+0" % (w, h))
        root.state('zoomed')
        Frame.__init__(self, master)
        self.grid()  # not necessary
        self.master.title("Rover GUI")
        self.master.title("Rover GUI")

        sock1, sock2, sock3 = None, None, None

        def exit_handler():
            cv2.destroyAllWindows()
            if sock1:
                sock1.close()
            if sock2:
                sock2.close()
            if sock3:
                sock3.close()

        for r in range(6):
            self.master.rowconfigure(r, weight=1)
        for c in range(12):
            self.master.columnconfigure(c, weight=1)

        Frame1 = Frame(master, bg="red", height=300, width=400)
        Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 4, sticky = W+E+N+S)
        Frame1.grid_propagate(False)
        Frame1.columnconfigure(0, weight=1)
        Frame2 = Frame(master, height=300, width=400)
        Frame2.grid_propagate(False)
        Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 4)
        e = Entry(Frame2)
        e.pack()
        e2 = Entry(Frame2)
        e2.pack()
        e3 = Entry(Frame2)
        e3.pack()
        Frame3 = Frame(master, height=300, width=400)
        Frame3.grid(row = 0, column = 4, rowspan = 3, columnspan = 4)
        Frame3.grid_propagate(False)
        Frame3.columnconfigure(0, weight=1)
        Frame4 = Frame(master, bg="purple", height=300, width=400)
        Frame4.grid(row = 3, column = 4, rowspan = 3, columnspan = 4, sticky = W+E+N+S)
        Frame4.grid_propagate(False)
        Frame5 = Frame(master, bg="white", height=300, width=400)
        Frame5.pack(fill=BOTH, expand=YES)
        Frame5.grid(row = 3, column = 8, rowspan = 3, columnspan = 4, sticky = W+E+N+S)
        Frame5.grid_propagate(False)
        Frame6 = Frame(master, bg="brown", height=300, width=400)
        Frame6.grid(row = 0, column = 8, rowspan = 3, columnspan = 4, sticky = W+E+N+S)
        Frame6.grid_propagate(False)

        c = Canvas(Frame5, bg='gray', width=0, height=0, bd=0)
        c.pack(fill=BOTH, expand=YES)

        def grid_template():
            c.create_line(c.winfo_width() / 2, 0, c.winfo_width() / 2, c.winfo_height())
            c.create_line(0, c.winfo_height() - (.15 * c.winfo_height()), c.winfo_width(),
                      c.winfo_height() - (.15 * c.winfo_height()))
            x = c.winfo_width() / 2
            y = c.winfo_height() - (.15 * c.winfo_height())
            x0 = x - 5
            y0 = y - 5
            x1 = x + 5
            y1 = y + 5
            oval = c.create_oval(x0, y0, x1, y1, fill="blue")
            Application.prev_coord = (x, y)
            Application.dots.append(oval)

        def reset():
            c.delete('all')
            Application.prev_coord = ()
            Application.dots = []
            Application.lines = []
            grid_template()
            e.delete(0, END)
            e.insert(END, '[Lat], [Lon] (Enter: press shift-up)')

        def undo():
            if len(Application.dots) > 1:
                c.delete(Application.dots[-1])
                Application.dots.pop()
                if len(Application.dots) > 0:
                    prev_dot = c.coords(Application.dots[-1])
                    Application.prev_coord = (prev_dot[0], prev_dot[1])
            if len(Application.lines) > 0:
                c.delete(Application.lines[-1])
                Application.lines.pop()
            if len(Application.dots) == 1:
                reset()

        def show_camera1():

            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.bind(('', 3000))
            recv_len = 32768

            display = Label(Frame1)
            display.pack(fill=None, expand=YES)

            while True:

                sleep(.01)

                try:
                    msg = sock1.recv(recv_len)
                    data = numpy.fromstring(msg, dtype='uint8')
                    decimg = cv2.imdecode(data, 1)
                    cv2image = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGBA)
                    image = Image.fromarray(cv2image)
                    image_resized = image.resize((root.winfo_width()/3 - 30, root.winfo_height()/2 - 30), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(image=image_resized)
                    display.img = img
                    display.configure(image=img)
                    cv2.waitKey(1)
                except socket.error:
                    print("Received Too Large")

        def show_camera2():

            sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock2.bind(('', 3001))
            recv_len = 32768

            display2 = Label(Frame3)
            display2.pack(fill=None, expand=YES)

            while True:

                sleep(.01)

                try:
                    msg = sock2.recv(recv_len)
                    data = numpy.fromstring(msg, dtype='uint8')
                    decimg = cv2.imdecode(data, 1)
                    cv2image = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGBA)
                    image = Image.fromarray(cv2image)
                    image_resized = image.resize((root.winfo_width() / 3 - 30, root.winfo_height() / 2 - 30),
                                                 Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(image=image_resized)
                    display2.img = img
                    display2.configure(image=img)
                    cv2.waitKey(1)
                except socket.error:
                    print("Received Too Large")

        def show_camera3():

            sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock3.bind(('', 3002))
            recv_len = 32768

            display3 = Label(Frame6)
            display3.pack(fill=None, expand=YES)

            while True:

                sleep(.01)

                try:
                    msg = sock3.recv(recv_len)
                    data = numpy.fromstring(msg, dtype='uint8')
                    decimg = cv2.imdecode(data, 1)
                    cv2image = cv2.cvtColor(decimg, cv2.COLOR_BGR2RGBA)
                    image = Image.fromarray(cv2image)
                    image_resized = image.resize((root.winfo_width() / 3 - 30, root.winfo_height() / 2 - 30),
                                                 Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(image= image_resized)
                    display3.img = img
                    display3.configure(image=img)
                    cv2.waitKey(1)
                except socket.error:
                    print("Received Too Large")

        def initiate_cameras():
            try:
                Thread(target=show_camera1).start()
                Thread(target=show_camera2).start()
                Thread(target=show_camera3).start()
            except Exception as e:
                print("Error: unable to start camera threads.")

        def coordinates(event):
            Application.coord_click_in = True


        def coords_submit(event):
            print('submission')
            valid_entry = True
            lat, lon = None, None
            result = e.get()
            i = 0
            if result == '[Lat], [Lon] (Enter: press shift-up)':
                print("Please enter values.")
                return
            values = re.findall(r"[-+]?\d*\.\d+|\d+", result)
            print(values)
            if not values or len(values) > 2:
                print("Latitude and Longitude not in the right format: [Lat], [Lat]")
                return
            try:
                lat, lon = float(values[0]), float(values[1])
            except Exception as error:
                print("Could not convert values in values array to floats. Error: " + error)
                return
            if Application.coord_click_in:
                e.delete(0, END)
                e.insert(0, '[Lat], [Lon] (Enter: press shift-up)')
                print('Coordinates submitted: ' + str(lat) + ", " + str(lon))
                # draw_destination(lat, lon)
                Application.coord_click_in = False
                # try:
                #     lat_lon = e.get()
                #     print(type(lat_lon))
                #     print(eval(lat_lon))
                # except Exception as error:
                #     print()

        # def convert_lat_lon(lat, lon):

        def draw_destination(lat, lon):
            x0 = lon - 5
            y0 = lat - 5
            x1 = lon + 5
            y1 = lat + 5
            dest = c.create_oval(x0, y0, x1, y1, fill="blue")

        Button(master, text="Button0").grid(row=6, column=0, sticky=E + W)
        Button(master, text="Button1").grid(row=6, column=1, sticky=E + W)
        Button(master, text="Button2").grid(row=6, column=2, sticky=E + W)
        Button(master, text="Button3").grid(row=6, column=3, sticky=E + W)
        Button(master, text="Button4").grid(row=6, column=4, sticky=E + W)
        Button(master, text="Button5").grid(row=6, column=5, sticky=E + W)
        Button(master, text="Button6").grid(row=6, column=6, sticky=E + W)
        Button(master, text="Button7").grid(row=6, column=7, sticky=E + W)
        Button(master, text="Undo", command=undo).grid(row=6, column=8, sticky=E + W)
        Button(master, text="Reset Grid", command=reset).grid(row=6, column=9, sticky=E + W)
        e = Entry(master, width=16)
        e.insert(END, '[Lat], [Lon] (Enter: press shift-up)')
        e.grid(row=6, column=10, sticky=E + W)
        Button(master, text="Start").grid(row=6, column=11, sticky=E + W)

        def motion(event):
            x, y = event.x, event.y
            oval = c.create_oval(x, y, x+4, y+4, fill="black")
            if len(Application.prev_coord) != 0 and len(Application.dots) != 0:
                line = c.create_line(Application.prev_coord[0], Application.prev_coord[1], x, y, fill='black')
                Application.lines.append(line)
            print('{}, {}'.format(x, y))
            print(Application.prev_coord[0], Application.prev_coord[1])
            Application.prev_coord = (x, y)
            Application.dots.append(oval)


        c.bind('<Button-1>', motion)
        e.bind('<Button-1>', coordinates)
        root.bind('<Shift-Up>', coords_submit)
        root.update()
        initiate_cameras()
        grid_template()
        atexit.register(exit_handler)


root = Tk()
app = Application(master=root)
app.mainloop()
