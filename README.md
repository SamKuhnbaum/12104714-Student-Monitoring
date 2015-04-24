# 12104714-Student-Monitoring
Student Monitoring Program -- 
In order to edit the program different modules are required - py2win, pyHook, PIL, MIME and pycrypto for IDLE
After editing - py2exe must be used in order for the program to work on other machines without the above modules
needing to be installed. The way you do this is through the cmd line, you change the code in 'setup' to represent
the file you wish to run, and find the setup file through cmd file using 'cd' and type 'python setup.py install' and
'python setup.py py2exe'- This creates a .exe file with the separate modules as dlls (check Monitor_KL2 folder for more details)

In order to run the program, just click on the separate .exe files inside Monitor_KL2 and Decryptor.

KL2 - This is the overall monitoring software - 
There is an options list which tells you exactly what to do upon starting the program.
It uses pyHook and pythoncom to find and record keystrokes.
PIL to take screenshots.
Pycrypto to encrypt the monitoring file using AES-CBC.
MIME to send the files through email - to access the files after the process is complete go to gmail and log in with 

Username: - mmukeylogger@gmail.co.uk
Password: - keylogged

KLDecrypt - This is a separate decryption program -
Download the files from the email and put the enkeylog.txt file into the same folder as the KLDecrypt.exe file
dekeylog.txt will appear showing the original text.

The code can be viewed by either opening the separate .py programs using IDLE, Notepad, Notepad++ or Visual Basic.

Preferably, IDLE 2.7 with the separate modules installed, a download list is shown below -
py2exe - http://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/
pywin32 - http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/
pyHook - http://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/
pycrypto - https://pypi.python.org/pypi/pycrypto/2.0.1
PIL - http://www.pythonware.com/products/pil/








