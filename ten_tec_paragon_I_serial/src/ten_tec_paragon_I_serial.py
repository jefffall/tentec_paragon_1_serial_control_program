import serial
import time
import sys
from datetime import datetime
from datetime import date

'''
screen /dev/cu.usbserial-A10M60PN 1200,cs8,parenb,-parodd,-cstopb
'''

ser = serial.Serial('/dev/cu.usbserial-A10M60PN', 1200, timeout=0,parity=serial.PARITY_NONE, rtscts=0)
ser.flush()
#print (ser)


def set_frequency(num_freq):
    
    
    if int(num_freq) > 29:
        return("most signficant > 29")
    freq = str(num_freq)
    my_len = len(freq)
    if "." not in freq:
        if my_len > 6.0:
            return ("freq len > 6")
        for x in range(0, my_len):
            ser.write(bytes(freq[x], 'utf-8'))
            time.sleep(.1)
        ser.write(b'@')
        return ("DONE")
    else:
        if my_len > 7:
            return ("freq len > 7")
        for x in range(0, my_len):
            if freq[x] == ".":
                ser.write(b'W')
                time.sleep(.1)
            ser.write(bytes(freq[x], 'utf-8'))
            time.sleep(.1)
        ser.write(b'@')
        return ("DONE")


    
        

'''
FREQUENCY
Status bytes
0 10 MHZ
1 1 MHZ
2 100 KHZ
3 10 KHZ
4 1 KHZ
5 100 HZ
6 10 HZ

32 BIT DRIVER IC

7
 BIT 7 - FAST LED
 BIT 6 - RTTY OUTPUT LINE
 BIT 5 - FM OUTPUT LINE
 BIT 4 - AM OUTPUT LINE
 BIT 3 - LSB OUTPUT LINE
 BIT 2 - USB OUTPUT LINE
 BIT 1 - CW OUTPUT LINE
 BIT 0 - TUNE OUTPUT LINE
'''
FAST_LED = 0x80
RTTY_OUTPUT_LINE = 0x40
FM_OUTPUT_LINE = 0x20
AM_OUTPUT_LINE = 0x10
LSB_OUTPUT_LINE = 0x08
USB_OUTPUT_LINE = 0x04
CW_OUTPUT_LINE = 0x02
TUNE_OUTPUT_LINE = 0x01
'''
8
 BIT 7 6.0 KHZ FILTER OUTPUT 
 BIT 6 2.4 KHZ FILTER OUTPUT
 BIT 5 1.8 KHZ FILTER OUTPUT
 BIT 4 .50 KHZ FILTER OUTPUT
 BIT 3 .25 KHZ FILTER OUTPUT
 BIT 2 RX OFFSET LED OUTPUT
 BIT 1 TX OFFSET LED OUTPUT
 BIT 0 LOCK LED OUTPUT
'''
my_6_KHZ_FILTER_OUTPUT = 0x80
my_2dot4_KHZ_FILTER_OUTPUT = 0x40
my_1dot8_KHZ_FILTER_OUTPUT = 0x20
my_dot50_KHZ_FILTER_OUTPUT = 0x10
my_dot25_KHZ_FILTER_OUTPUT = 0x08
RX_OFFSET_LED_OUTPUT = 0x04
TX_OFFSET_LED_OUTPUT = 0x02
LOCK_LED_OUTPUT = 0x01
'''
9
 BIT 7 DATE LED OUTPUT
 BIT 6 TIME LED OUTPUT
 BIT 5 OFFSET LED OUTPUT
 BIT 4 MEMORY LED OUTPUT
 BIT 3 VFO A LED OUTPUT
 BIT 2 VFO B LED OUTPUT
 BIT 1 SPLIT LED OUTPUT
 BIT 0 TAG LED OUTPUT
'''
DATE_LED_OUTPUT = 0x80
TIME_LED_OUTPUT = 0x40
OFFSET_LED_OUTPUT = 0x20
MEMORY_LED_OUTPUT = 0x10
VFO_A_LED_OUTPUT = 0x08
VFO_B_LED_OUTPUT = 0x04
SPLIT_LED_OUTPUT = 0x02
TAG_LED_OUTPUT = 0x01
'''
 
10
 BIT 7 BAND RELAY #8 ( 22-30 MHZ)
 BIT 6 BAND RELAY #7 ( 15-22 MHZ)
 BIT 5 BAND RELAY #6 ( 10.5-15 MHZ)
 BIT 4 BAND RELAY #5 ( 6.5-10.5 MHZ)
 BIT 3 BAND RELAY #4 ( 4-6.5 MHZ)
 BIT 2 BAND RELAY #3 ( 2.5-4 MHZ)
 BIT 1 BAND RELAY #2 ( 1.7-2.5 MHZ)
 BIT 0 BAND RELAY #1 ( 0.1-1.7 MHZ)
'''
BAND_RELAY_8 = 0x80
BAND_RELAY_7 = 0x40
BAND_RELAY_6 = 0x20
BAND_RELAY_5 = 0x10
BAND_RELAY_4 = 0x08
BAND_RELAY_3 = 0x04
BAND_RELAY_2 = 0x02
BAND_RELAY_1 = 0x01
'''
11 MEMORY CHANNEL (63 IF NOT IN MEMORY MODE)
 
12 TUNING STEP SIZE
   00 - 10 HZ
   01 - 20 HZ
   02 - 50 HZ
   03 - 100 HZ
   04 - 500 HZ
   
13 - 17 OFFSET

13 OFFSET NEGATIVE IF > 1
14 10 KHZ
15 1 KHZ
16 100 HZ
17 10 HZ

18 - 24 TAG IN ASCII

25 MONTH

26 DAY OF MONTH

27 HOURS IN 24 HOUR FORMAT

28 MINUTES 00 TO 59

29 SECONDS 00 TO 59
'''


 
def get_status(ser):
    LED = {}
    ser.write(b'\\')
    time.sleep(.5)
    my_bytes = ser.read(30)
    time.sleep(.01)
    ser.flush()
    my_byte_arr = bytearray(my_bytes)
    
    freq = ""    
    for x in range(0,6):
        freq = freq + str(my_byte_arr[x])
        
        
    if my_byte_arr[7] & FAST_LED:
        LED['FAST'] = 1
    else:
        LED['FAST'] = 0
    if my_byte_arr[7] & RTTY_OUTPUT_LINE:
        LED['RTTY'] = 1
    else:
        LED['RTTY'] = 0
    if my_byte_arr[7] & FM_OUTPUT_LINE:
        LED['FM'] = 1
    else:
        LED['FM'] = 0
    if my_byte_arr[7] & AM_OUTPUT_LINE:
        LED['AM'] = 1
    else:
        LED['AM'] = 0
    if my_byte_arr[7] & LSB_OUTPUT_LINE:
        LED['LSB'] = 1
    else:
        LED['LSB'] = 0
    if my_byte_arr[7] & USB_OUTPUT_LINE:
        LED['USB'] = 1
    else:
        LED['USB'] = 0
    if my_byte_arr[7] & CW_OUTPUT_LINE:
        LED['CW'] = 1
    else:
        LED['CW'] = 0
    if my_byte_arr[7] & TUNE_OUTPUT_LINE:
        LED['TUNE'] = 1
    else:
        LED['TUNE'] = 0
        
######################################################################
        
    if my_byte_arr[8] & my_6_KHZ_FILTER_OUTPUT:
        LED['6KHZ'] = 1
    else:
        LED['6KHZ'] = 0
    if my_byte_arr[8] & my_2dot4_KHZ_FILTER_OUTPUT:
        LED['2.4KHZ'] = 1
    else:
        LED['2.4KHZ'] = 0
    if my_byte_arr[8] & my_1dot8_KHZ_FILTER_OUTPUT:
        LED['1.8KHZ'] = 1
    else:
        LED['1.8KHZ'] = 0
    if my_byte_arr[8] & my_dot50_KHZ_FILTER_OUTPUT:
        LED['.5KHZ'] = 1
    else:
        LED['.5KHZ'] = 0
    if my_byte_arr[8] & my_dot25_KHZ_FILTER_OUTPUT:
        LED['.25KHZ'] = 1
    else:
        LED['.25KHZ'] = 0
    if my_byte_arr[8] & RX_OFFSET_LED_OUTPUT:
        LED['RX_OFFSET'] = 1
    else:
        LED['RX_OFFSET'] = 0
    if my_byte_arr[8] & TX_OFFSET_LED_OUTPUT:
        LED['TX_OFFSET'] = 1
    else:
        LED['TX_OFFSET'] = 0
    if my_byte_arr[8] & LOCK_LED_OUTPUT:
        LED['LOCK'] = 1
    else:
        LED['LOCK'] = 0
        
##############################################################################
            
    if my_byte_arr[9] & DATE_LED_OUTPUT:
        LED['DATE'] = 1
    else:
        LED['DATE'] = 0
    if my_byte_arr[9] & TIME_LED_OUTPUT:
        LED['TIME'] = 1
    else:
        LED['TIME'] = 0
    if my_byte_arr[9] & OFFSET_LED_OUTPUT:
        LED['OFFSET'] = 1
    else:
        LED['OFFSET'] = 0
    if my_byte_arr[9] & MEMORY_LED_OUTPUT:
        LED['MEMORY'] = 1
    else:
        LED['MEMORY'] = 0
    if my_byte_arr[9] & VFO_A_LED_OUTPUT:
        LED['VFO_A'] = 1
    else:
        LED['VFO_A'] = 0
    if my_byte_arr[9] & VFO_B_LED_OUTPUT:
        LED['VFO_B'] = 1
    else:
        LED['VFO_B'] = 0
    if my_byte_arr[9] & SPLIT_LED_OUTPUT:
        LED['SPLIT'] = 1
    else:
        LED['SPLIT'] = 0
    if my_byte_arr[9] & TAG_LED_OUTPUT:
        LED['TAG'] = 1
    else:
        LED['TAG'] = 0
            
################################################################################
 
    if my_byte_arr[10] & BAND_RELAY_8:
        LED['BAND_22-30_MHZ'] = 1
    else:
        LED['BAND_22-30_MHZ'] = 0
    if my_byte_arr[10] & BAND_RELAY_7:
        LED['BAND_15-22_MHZ'] = 1
    else:
        LED['BAND_15-22_MHZ'] = 0
    if my_byte_arr[10] & BAND_RELAY_6:
        LED['BAND_10.5-15_MHZ'] = 1
    else:
        LED['BAND_10.5-15_MHZ'] = 0
    if my_byte_arr[10] & BAND_RELAY_5:
        LED['BAND_6.5-10.5_MHZ'] = 1
    else:
        LED['BAND_6.5-10.5_MHZ'] = 0
    if my_byte_arr[10] & BAND_RELAY_4:
        LED['BAND_4-6.5_MHZ'] = 1
    else:
        LED['BAND_4-6.5_MHZ'] = 0
    if my_byte_arr[10] & BAND_RELAY_3:
        LED['BAND_2.5-4_MHZ'] = 1
    else:
        LED['BAND_2.5-4_MHZ'] = 0
    if my_byte_arr[9] & BAND_RELAY_2:
        LED['BAND_1.7-2.5_MHZ'] = 1
    else:
        LED['BAND_1.7-2.5_MHZ'] = 0
    if my_byte_arr[10] & BAND_RELAY_1:
        LED['BAND_0.1-1.7_MHZ'] = 1
    else:
        LED['BAND_0.1-1.7_MHZ'] = 0
        
    LED['MEMORY_CHAN'] = my_byte_arr[11]
    
    # In Hertz - assigns step in HZ
    if my_byte_arr[12] == 0:
        LED['TUNING_STEP_SIZE'] = "10"
    elif my_byte_arr[12] == 1:
        LED['TUNING_STEP_SIZE'] = "50"
    elif my_byte_arr[12] == 2:
        LED['TUNING_STEP_SIZE'] = "100"
    else:
        LED['TUNING_STEP_SIZE'] = "500"
        
   
    offset = int(my_byte_arr[14]) * 10000
    offset = offset + int(my_byte_arr[15]) * 1000
    offset = offset + int(my_byte_arr[16]) * 100
    offset = offset + int(my_byte_arr[17]) * 10
    offset_float = offset / 1000
    if int(my_byte_arr[13]) > 1:
        offset_float = offset_float * -1.0
    LED['OFFSET'] = str(offset_float) + " KHz"
    
    mydate = str(my_byte_arr[25]) + "/" + str(my_byte_arr[26])
    
    mytime = hex(my_byte_arr[27]).lstrip("0x") + ":"
    my_min = hex(my_byte_arr[28]).lstrip("0x")
    if len(my_min) == 1:
        my_min = "0" + my_min
    my_sec = hex(my_byte_arr[29]).lstrip("0x")
    if len(my_sec) == 1:
        my_sec = "0" + my_sec
        
    mytime = mytime + my_min + ":" + my_sec
    
    LED['freq'] = freq
    LED['date'] = mydate
    LED['time'] = mytime
        
    return (LED)

def set_mode(mode):
    if mode == "FM" or mode == "fm":
        ser.write(b'L')
    elif mode == "AM" or mode == "am":
        ser.write(b'M')
    elif mode == "LSB" or mode == "lsb":
        ser.write(b'N')
    elif mode == "USB" or mode == "usb":
        ser.write(b'O')
    elif mode == "CW" or mode == "cw":
        ser.write(b'P')
    elif mode == "TUNE" or mode == "tune":
        ser.write(b'Q')
    time.sleep(.1)
    
def tune_up():
    ser.write(b'[')
    time.sleep(.01)
    
def scan_band(steps):
    time.sleep(1)
    for x in range(0,steps):
        #print ("tune")
        tune_up()
        
def get_tuning_steps(bandwidth):
    my_status = get_status(ser)
    tuning_step = my_status['TUNING_STEP_SIZE']
    bandwidth_hz = int(round(bandwidth * 1000000, 0))
    print (bandwidth_hz)
    print (int(tuning_step))
    tuning_steps = bandwidth_hz // int(tuning_step)
    print(tuning_steps)
    return(tuning_steps)


      
def scan_band_80m():
    set_mode("LSB")
    bandwidth = 4.0 - 3.5
    set_frequency(3.5)
    time.sleep(.1)
    scan_band(get_tuning_steps(bandwidth))
    ser.flush()
    
def scan_band_60m():
    set_mode("USB")
    set_frequency(5.3305)
    time.sleep(2)
    set_frequency(5.3465)
    time.sleep(2)
    set_frequency(5.357)
    time.sleep(2)
    set_frequency(5.3715)
    time.sleep(2)
    set_frequency(5.4035)
    time.sleep(2)
    ser.flush()
    

def scan_band_40m():
    set_mode("LSB")
    bandwidth = 7.3 - 7.2
    set_frequency(7.2)
    time.sleep(.1)
    scan_band(get_tuning_steps(bandwidth))
    
def scan_band_30m():
    set_mode("USB")
    bandwidth = 10.15 - 10.1
    set_frequency(10.1)
    time.sleep(.1)
    scan_band(get_tuning_steps(bandwidth))
    ser.flush()
  
def scan_band_20m():
    set_mode("USB")
    bandwidth = 14.35 - 14.0
    set_frequency(14)
    time.sleep(.1)
    scan_band(get_tuning_steps(bandwidth))
    ser.flush()
    
def scan_band_17m():
    set_mode("USB")
    bandwidth = 18.168 - 18.068 
    set_frequency(18.068)
    time.sleep(.1)
    scan_band(get_tuning_steps(bandwidth))
    
def scan_band_15m():
    set_mode("USB")
    bandwidth = 21.45 - 21.0
    set_frequency(21)
    time.sleep(.1)
    scan_band(get_tuning_steps(bandwidth))
    ser.flush()
    
def scan_band_12m():
    set_mode("USB")
    bandwidth = 24.99 - 24.89
    set_frequency(24.89)
    time.sleep(.1)
    scan_band(get_tuning_steps(bandwidth))
    
def scan_band_10m():
    set_mode("USB")
    bandwidth = 29.7 - 28.0
    set_frequency(28)
    time.sleep(.1)
    scan_band(get_tuning_steps(bandwidth))
    ser.flush()

def set_memory(mem):
    mem = str(mem)
    ser.write(b'<')
    time.sleep(.1)
    ser.write(bytes(mem[:-1],'utf-8'))
    time.sleep(.1)
    ser.write(bytes(mem[1:],'utf-8'))
    time.sleep(.1)
    
def enter_tag(tag):
    ser.write(b'X') #SHIFT
    time.sleep(.1)
    ser.write(b';') #SET
    for x in range(0, len(tag)):
        ser.write(bytes(tag[x],'ascii'))
        time.sleep(.1)
    ser.write(b'@') # ENTER
    time.sleep(1)
    
def set_filter(filter):
    if filter == 6:
        ser.write(b'R')
    else:
        ser.write(b'S')
    time.sleep(.1)
    
def set_date():
  
    months = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]
    mydate = date.today()
    parts = str(mydate).split("-")
    month = int(parts[1])
    day = int(parts[2])
    for y in range(1,3): # Get into date mode on LED
        led_lit = get_status(ser)
        time.sleep(.1)
        if led_lit['DATE'] == 1:
            time.sleep(1)
            break
        else:
            ser.write(b'B') #press disp kay
            time.sleep(.5)
    ser.write(b'X')
    time.sleep(.1)
    ser.write(b';')
    time.sleep(.1)
    # The month after reset starts as NOV
    for x in range (1,int(months[month])):
        ser.write(b'Z')
        ser.flush()
        time.sleep(.1)
    ser.write(b'@')
    time.sleep(.1)
    # The Day starts as 20
    if day < 20:
        for x in range(20,day,-1): #decrement the day sending a down command
            ser.write(b'Y')
            time.sleep(.1)
    elif day > 20:
        for x in range(20,day): #decrement the day sending a down command
            ser.write(b'Z')
            time.sleep(.1)
    ser.write(b'@')
   
def set_time():
    time.sleep(1)
    myobj = datetime.now()
    hour = str(myobj.hour)
    min = str(myobj.minute)
    if len(hour) == 1:
        hour = "0" + hour
    if len(min) == 1:
        min = "0" + min
    for y in range(1,3): # Get into date mode on LED
        led_lit = get_status(ser)
        time.sleep(.1)
        if led_lit['TIME'] == 1:
            time.sleep(1)
            break
        else:
            ser.write(b'B') #press disp kay
            time.sleep(.5)
    # Now LED on Paragon must show TIME
    # Set the time        
    ser.write(b'X')
    time.sleep(.1)
    ser.write(b';')
    time.sleep(.1)
    # Enter the HOUR
    for x in range(0,2):
        ser.write(bytes(hour[x],'ascii'))
        ser.flush()
        time.sleep(.2)
    # Enter the minutes
    for x in range(0,2):
        ser.write(bytes(min[x],'ascii'))
        ser.flush()
        time.sleep(.2)
    # enter as we are done.    
    # ser.write(b'@')
    time.sleep(1)
    
    
     
        
    
'''
A = L
B = M
C = N
D = O
E = P
F = Q
G = R
H = S
I = T
J = U
K = V
L = H
M = I
N = B
O = >
P = C
Q = ?
R = D
S = ;
T = E
U = <
W = F
V = :
X = A
Y = K
Z = J
space = G
'''
    
    
    
def load_memories():

    time.sleep(1)
    # MEM | FREQ | MODE | TAG
    mem = [
    "01 1.84 USB 1160GQE8",
    "02 2.5 AM FFF:",
    "03 3.33 AM NNS<",
    "04 3.573 USB 880IGQE8",
    "05 5 AM FFF:",
    "06 5.357 USB 660IGQE8",
    "07 7.074 USB 440IGQE8",
    "08 7.85 AM NNS<",
    "09 10 AM FFF:",
    "10 10.136 USB 330IGQE8",
    "11 14.074 USB 220IGQE8",
    "12 14.670 AM NNS<",
    "13 15 AM FFF:",
    "14 18.100 USB 117IGQE8",
    "15 20 AM FFF:",
    "16 21.074 USB 115IGQE8",
    "17 24.914 USB 112IGQE8",
    "18 25 AM FFF:",
    "19 28.074 USB 110IGQE8"   
    ]
    
    for y in range(1,3): # Get into date mode on LED
        led_lit = get_status(ser)
        time.sleep(.1)
        if led_lit['TAG'] == 1:
            time.sleep(1)
            break
        else:
            ser.write(b'B') #press disp kay
            time.sleep(.5)
  
    set_filter(6)
    for inp in mem:
        col = inp.split(" ")
        set_frequency(float(col[1]))
        time.sleep(.1)
        set_mode(col[2])
        time.sleep(.1)
        set_memory(col[0])
        time.sleep(.1)
        # TAG
        enter_tag(col[3])
        time.sleep(1)
        
def was_paragon_reset():
    status = get_status(ser) 
    if status['date'] == "17/32":
        mytime = str(status['time'])
        if "12::" in mytime:
            print ("Setting Paragon Date and time...")
            set_date()
            set_time()
            load_memories()
        else:
            parts = mytime.split(":")
            hours = int(parts[0])
            minutes = int(parts[1])
            if hours == 12 and minutes < 11:
                print ("Setting Paragon Date and time...")
                set_date()
                set_time()
                load_memories()
    else:
        print ("Paragon I was not reset so not setting time and date") 
 
##############################################################################################
# main
#print(set_frequency(10.))

#load_memories()

was_paragon_reset()
scan_band_20m()
#load_memories()
exit(0)



status = get_status(ser)
print (status)
exit(0)
if status['DATE'] == "17/32":
    mytime = str(status['TIME'])
    if "12::" in mytime:
        set_date()
        set_time
    else:
        parts = mytime.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        if hours == 12 and minutes < 11:
            set_date()
            set_time
        
exit(0)



while True:
    #scan_band_60m()
    #scan_band_40m()
    #time.sleep(2)
    #scan_band_30m()
    #time.sleep(2)
    scan_band_20m()
    exit(0)
    ##ime.sleep(2)
    scan_band_10m()
    time.sleep(2)


print( get_status(ser))

#set_frequency(7.2)
#scan_band()


