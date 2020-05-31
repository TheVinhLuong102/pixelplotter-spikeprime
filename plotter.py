from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import time
hub = PrimeHub() 

# paper resolution
vert_move = 80;
horiz_move = 80;

filename = "doug.txt"

# Python2 compatibility variables
false = 0
true = 1

buf = ""
def writebuf(text):
    global buf
    buf = buf+text

def printbuf():
    global buf
    print(buf)
    buf=""

# define motors and use brake mode

def waitformotor(motor):
    xxx = 0

paper = Motor("E")
pen1 = Motor("B")
#pen2 = ev3.MediumMotor('outD')
head = Motor("D")

pen1.set_stop_action("brake")
#pen2.stop_action = "brake"
head.set_stop_action("brake")
paper.set_stop_action("brake")
head.set_degrees_counted(0)
pen1.set_degrees_counted(0)
#pen2.reset()
paper.set_degrees_counted(0)


#move paper until color sensor recieves >50 reading

#paper.speed_regulation_enabled=u'on'
pen1.run_for_degrees(30,40)
#pen2.run_to_rel_pos(speed_sp=400, position_sp=53)
pen1.set_degrees_counted(0)
#pen2.reset()
print("Init printer motors")
print("Pixel Plotter v4.1 code v1.0 spike")


def resetMotors():
    paper.run_to_degrees_counted(0,-100)
    head.run_to_degrees_counted(0,-100)
#    pen1.run_to_abs_pos(position_sp=0, speed_sp=1000)
#    pen2.run_to_abs_pos(position_sp=0, speed_sp=1000)
#    waitformotor(pen1)
#    waitformotor(pen2)

#make a function to make a dot on the page
def makedot(pen,dir):
    pen.run_for_degrees(30,-80)
    waitformotor(pen) #double check if motor is stopped before raising pen
    pen.run_for_degrees(29,80)
    waitformotor(pen) #double check if motor is stopped before raising pen

#resize and flip image
#filename = sys.argv[1]

def processPic(img,width,height):
    r_array = []
    g_array = []
    b_array = []
    bl_array = []
    e4col = false
    lastRow = 0
    w = width-1
    h = 0
    e4col=false
    xd = 0
    yd = 0
    while yd < height:
        line = img.readline()
        while xd < width:
            if int(line[xd]) == 0: #is pixel black?
                writebuf("D") #print block if black pixel
                # lower and raise pen
                # move pen left
            else:
                writebuf(" ")
                #move pen left
            xd = xd + 1
        yd = yd + 1
        xd = width-1
        xd = 0
        printbuf()
    return (r_array,g_array,b_array,bl_array,e4col,lastRow)


def runPrinter(img,width,height):
    initial = time.time()
    xd = 0
    yd = 0
    xda = 0
    while yd < height:
        line = img.readline()
        while xd < width:
            if int(line[xd]) == 0: #is pixel black?
                writebuf("D") #print block if black pixel
                head.run_to_degrees_counted(horiz_move*xd, 100)
                waitformotor(head)
                # lower and raise pen
                makedot(pen1,1)
                # move pen left
            else:
                writebuf(" ")
                #move pen left
            xd = xd + 1
            xda = xda + 1
        yd = yd + 1
        xd = width-1
        xd = 0
        paper.run_to_degrees_counted(vert_move*(yd), -100)
        writebuf("             PCT: "+str(int(100*xda/(width*height)))+"% ; Time Remaining: "+str(int((100-100*xda/(width*height))*(time.time()-initial)/(100*xda/(width*height))))+"s")
        printbuf()
        # reset pen location
        waitformotor(paper)

def printer(filename):
    img = open(filename)
    width=int(img.readline())
    height=int(img.readline())

    print(width," x ",height)

    #r_array, g_array, b_array, bl_array, e4col, lastRow = processPic(img, width, height)
    
    print('Is this picture ok? Press left to print black...') #wait for dialogue to be answered then start printing

    hub.left_button.wait_until_pressed()

    print("Starting")

    img = open(filename)
    width = int(img.readline())
    height = int(img.readline())
    runPrinter(img, width, height)
    resetMotors()

printer(filename)
