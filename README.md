![image](https://github.com/planetxort/Buffer-Overflow-Guide/blob/master/buffer-overflow-attacks.png)
# Buffer Overflow Guide
This is a Bufferflow Guide, inspired by TheCyberMentor's Buffer Overflow tutorial: [Buffer Overflows Made Easy](https://www.youtube.com/watch?v=qSnPayW6F7U&list=PLLKT__MCUeix3O0DPbmuaRuR_4Hxo4m3G) 

# Background:
This repository is meant to be supplemental information based on TheCyberMentor's walkthrough. I created this guide with the intent to provide step-by-step written instructions, and hopefully provide greater insight or additional confidence in your pursuit to learn this technique. I believe that notetaking can be a difficult for many individuals, therefore the goal of this repository is to consolidate steps into a reference sheet, and provide the scripts used in TheCyberMentor's video series. All credit for the scripts go to TheCyberMentor. The only changes I made to the scripts were morale-building naming conventions and providing an additional script for Linux buffer-overflows. The beauty of this repository is that it can be cloned to your linux machine (removing the need for manually typing out python scripts), and utilized as a reference if you forget any of the steps in TheCyberMentor's Walkthrough (or cloned before watching his video series)

# Assumed Knowledge
1. Lab Setup
2. An understanding of Network adapters and communication between Windows/Linux
3. Basic understanding of Metasploit, Python and Shells
4. You have at least watched TheCyberMentor's Video Series, or you have a baseline level of buffer overflow understanding
5. Enumeration Methodology (Linux and Windows)
6. Basic Usage of Immunity Debugger

# Tools needed:
1. Kali Linux
2. Windows System with Immunity Debugger installed, *NOTE*: You do **not** have to put in real information to download this. ([Immunity Debugger](https://debugger.immunityinc.com/ID_register.py))
3. Vulnserver: [Download Link](https://sites.google.com/site/lupingreycorner/vulnserver.zip?attredirects=0) (if you're following along with TheCyberMentor's video series)

# Additional Setup Considerations
1. Ensure you have permisson to run executable files as Administrator on Windows.
2. Download or Copy the code of [Mona.py](https://github.com/corelan/mona/blob/master/mona.py), you will need this for module functionality in Immunity Debugger.
3. Place the Mona.py file in the following directory: C:/Program Files(x86)/Immunity Inc/Immunity Debugger/PyCommands
4. One last consideration: Ensure you have connectivity between your Lab Environment (do a ping from your linux host to your windows host) ping x.x.x.x - If you don't, please read guides on understanding Network Adapter Settings for your specific virtialization software.

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
The typical Buffer Overflow scenario relies on Reverse Engineering an executable file. Before you attempt to Spike, etc, you're going to want to find an executable file. In the instance of Vulnserver, you will be given an executable file. In a realistic scenario, you're going to want to perform enumeration methodology and look for an executable file to download. These are typically hosted via SMB Shares, FTP Servers, Exposed Web Directories, etc. Use best practice regarding enumeration and continue with this guide when you have an executable file.

# 2. Spiking
Spiking is all about identifying what command is vulnerable (observed by the program breaking in Immunity)

Steps:
1. Connect to a port or a program that allows you to send specific commands, for instance, you may see that the system you're trying to exploit has a service on port 9999.
Command: nc -nv 9999
2. Observe the commands that can be utilized on the service, in TheCyberMentor video, the vulnerable service command was "TRUN" but in reality, you will likely have to use the provided script on multiple commands until the program breaks.
3. Run Immunity as Admin.
4. Run the executable you found. (or downloaded for practice)
5. Attach to the executable process.
6. Click the "Play" button in Immunity, ensure it says Running on the bottom right hand corner.
7. Use the provided command.spk file, ensuring that you edit the 'STATS' command with whatever command you're attempting to test.
Command: generic_send_tcp ip port command.spk 0 0
8. After you utilize the command.spk, look to see if there's an Access Violation in Immunity, if there is not, edit the command within the command.spk to a different one and retest.

# 3. Fuzzing
The process of fuzzing is to attempt to narrow down the amount of bytes it took to crash the program.

1. Edit the provided fuzz.py script. Replace the IP, PORT, and TRUN command with the IP, port and command that you want to test.
Command: python fuzz.py
2. Try to use CTRL+C to stop the script exactly when you see an Access Violation pop-up in Immunity. This will ensure you can more accurately estimate the bytes it took to crash it.
3. Write down the amount of bytes it took to crash the program

# 4. Finding the Offset
The correct identification of the offset will help ensure that the shellcode you generate will not immediately crash the program.

1. Generate pattern code, replacing the number in the command with the number of bytes it took to crash the program (found in step 3)
Command: /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2000
2. Copy the output of the pattern_create command and edit the offset.py script provided in this repository. Replace the existing offset value portion of the script with the pattern that you generated from the command.
3. Close out Immunity + the executable program.
4. Repeat the process of relaunching Immunity and attaching to the executable program.
5. Run the script
Command: python offset.py
6. Go into Immunity and look for a number written in the EIP space.
7. If there is not a number written into the EIP space, the amount of bytes you identified in your Fuzz may be off. Go back to step 1 and regenerate pattern code, using a number higher than whatever you had written to the script. For instance, if you used 700, try 1000, or 1200. If you are unsuccessful, you may have messed up during Fuzzing. Go back to the Fuzzing section and try to stop the script faster when you see the Access Violation in Immunity.
8. When you find a number written to the EIP, write this number down somewhere. Use the following command, replacing the -l switch value with your identified fuzz-bytes number from step 1, and replace the -q switch with the number that was written into the EIP.
Command: /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 2500 -q 386F4337
9. If everything is correct, when you run the above command, you should get an exact offset match that looks like this:
 **[*] Exact match at offset 2003**
10. Ensure that you write down this offset match.

# 5. Overwriting the EIP
1. 
