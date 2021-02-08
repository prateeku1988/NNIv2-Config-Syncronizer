#################################################################################################################
##
## Author : Prateek Upadhyay
##
## Title  : Cisco IOS-XE NNI routers Routing , NAT entries & IP Prefix Lists comparison
##
## Date   : 06.11.2020
##
##
## Version Control : 1.0
## Here A is one Organization & B is Different Organization whose IPspaces are clashing
####################################################################################################################
#!/usr/bin/env python3
import re
import paramiko
import time
import getpass
from os import system

system('clear')
Host_Name = 'XXXX'
username = input('Enter Your Username to Login NNI Routers: ')
password = getpass.getpass()
print('=============Generating The Output Files From XXXX Router===================')
print('\n')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(Host_Name, 22, username, password)

remote_session = client.invoke_shell()

output = remote_session.send('\n')
output = remote_session.send('ter len 0\n')
output = remote_session.send('sh ip route bgp\n')
output = remote_session.send('sh ip route static\n')
output = remote_session.send('sh run | i ip nat\n')
output = remote_session.send('sh run | i ip prefix-list\n')

time.sleep(15)

output = remote_session.recv(85535)
client.close()


with open('Result_' + Host_Name, 'w') as f:
    f.write(output.decode('utf-8'))

RE = re.compile('S\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE1 = re.compile('B\*?\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE3 = re.compile('(\d+\.\d+\.\d+\.\d+\s){2}\/[0-9]{2}')
RE4 = re.compile('(\d+\.\d+\.\d+\.\d+)\/[0-9]{2}')

Pre_NNI_RTR_Raw=[]
Pre_NNI_RTR_Static_Routes=[]

with open('Result_' + Host_Name) as f:
     for line in f:
         if RE.search(line):
            Pre_NNI_RTR_Raw.append(RE.search(line).group())

for i in range(len(Pre_NNI_RTR_Raw)):
    Pre_NNI_RTR_Static_Routes.append(Pre_NNI_RTR_Raw[i].split(' ')[-1])

#print(Pre_NNI_RTR_Static_Routes)
Pre_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name) as f:
     for line in f:
         if RE1.search(line):
            Pre_NNI_RTR_Raw.append(RE1.search(line).group())

Pre_NNI_RTR_BGP_Routes=[]

for i in range(len(Pre_NNI_RTR_Raw)):
    Pre_NNI_RTR_BGP_Routes.append(Pre_NNI_RTR_Raw[i].split(' ')[-1])

Pre_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name) as f:
     for line in f:
         if RE3.search(line):
            Pre_NNI_RTR_Raw.append(RE3.search(line).group())

Pre_NNI_RTR_Nats=[]

for i in range(len(Pre_NNI_RTR_Raw)):
    Pre_NNI_RTR_Nats.append(Pre_NNI_RTR_Raw[i])


A_NAT_EUR = []
A_NAT_USA = []
A_NATIVE_EUR = []
A_NATIVE_USA = []
B_NAT_EUR = []
B_NAT_USA = []
B_NATIVE_EUR = []
B_NATIVE_USA = []

with open('Result_' + Host_Name) as f:
     for line in f:
         if 'ip prefix-list PL-A-NAT-EU' in line:
             A_NAT_EUR.append(line)
         elif 'ip prefix-list PL-A-NAT-USA' in line:
               A_NAT_USA.append(line)
         elif 'ip prefix-list PL-A-NATIVE-EU' in line:
               A_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-A-NATIVE-USA' in line:
               A_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-B-NAT-EU' in line:
               B_NAT_EUR.append(line)
         elif 'ip prefix-list PL-B-NAT-USA' in line:
            B_NAT_USA.append(line)
         elif 'ip prefix-list PL-B-NATIVE-EU' in line:
              B_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-B-NATIVE-USA' in line:
              B_NATIVE_USA.append(line)

Pre_NNI_RTR_A_NAT_EUR = []
Pre_NNI_RTR_A_NAT_USA = []
Pre_NNI_RTR_A_NATIVE_EUR = []
Pre_NNI_RTR_A_NATIVE_USA = []
Pre_NNI_RTR_B_NAT_EUR = []
Pre_NNI_RTR_B_NAT_USA = []
Pre_NNI_RTR_B_NATIVE_EUR = []
Pre_NNI_RTR_B_NATIVE_USA = []

for i in range(len(A_NAT_EUR)):
    Pre_NNI_RTR_A_NAT_EUR.append(A_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NAT_USA)):
    Pre_NNI_RTR_A_NAT_USA.append(A_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_EUR)):
    Pre_NNI_RTR_A_NATIVE_EUR.append(A_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_USA)):
    Pre_NNI_RTR_A_NATIVE_USA.append(A_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_EUR)):
    Pre_NNI_RTR_B_NAT_EUR.append(B_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_EUR)):
    Pre_NNI_RTR_B_NATIVE_EUR.append(B_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_USA)):
    Pre_NNI_RTR_B_NAT_USA.append(B_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_USA)):
    Pre_NNI_RTR_B_NATIVE_USA.append(B_NATIVE_USA[i].strip('\n').split(' ')[-1])

Pre_NNI_RTR_A_NAT_EUR_PL = []
Pre_NNI_RTR_A_NAT_USA_PL = []
Pre_NNI_RTR_A_NATIVE_EUR_PL = []
Pre_NNI_RTR_A_NATIVE_USA_PL = []
Pre_NNI_RTR_B_NAT_EUR_PL = []
Pre_NNI_RTR_B_NAT_USA_PL = []
Pre_NNI_RTR_B_NATIVE_EUR_PL = []
Pre_NNI_RTR_B_NATIVE_USA_PL = []

for line in Pre_NNI_RTR_A_NAT_EUR:
    if RE4.search(line):
       Pre_NNI_RTR_A_NAT_EUR_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_A_NAT_USA:
    if RE4.search(line):
       Pre_NNI_RTR_A_NAT_USA_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_A_NATIVE_EUR:
    if RE4.search(line):
       Pre_NNI_RTR_A_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_A_NATIVE_USA:
    if RE4.search(line):
       Pre_NNI_RTR_A_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_B_NAT_EUR:
    if RE4.search(line):
       Pre_NNI_RTR_B_NAT_EUR_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_B_NAT_USA:
    if RE4.search(line):
       Pre_NNI_RTR_B_NAT_USA_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_B_NATIVE_EUR:
    if RE4.search(line):
       Pre_NNI_RTR_B_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_B_NATIVE_USA:
    if RE4.search(line):
       Pre_NNI_RTR_B_NATIVE_USA_PL.append(RE4.search(line).group())

#=========First Target Device===================================================
print('=============Generating The Output Files From XXXX Router===================')
print('\n')
Host_Name1  = 'XXXX'
#username = input('Enter Username: ')
#password = getpass.getpass()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(Host_Name1, 22, username, password)

remote_session = client.invoke_shell()

output = remote_session.send('\n')
output = remote_session.send('ter len 0\n')
output = remote_session.send('sh ip route bgp\n')
output = remote_session.send('sh ip route static\n')
output = remote_session.send('sh run | i ip nat\n')
output = remote_session.send('sh run | i ip prefix-list\n')

time.sleep(15)

output = remote_session.recv(85535)
#print(output.decode('utf-8'))
client.close()

with open('Result_' + Host_Name1, 'w') as f:
    f.write(output.decode('utf-8'))

New_NNI_RTR_Raw=[]
New_NNI_RTR_Static_Routes=[]

with open('Result_' + Host_Name1) as f:
     for line in f:
         if RE.search(line):
            New_NNI_RTR_Raw.append(RE.search(line).group())

for i in range(len(New_NNI_RTR_Raw)):
    New_NNI_RTR_Static_Routes.append(New_NNI_RTR_Raw[i].split(' ')[-1])

#print(New_NNI_RTR_Static_Routes)
New_NNI_RTR_Raw.clear()


with open('Result_' + Host_Name1) as f:
     for line in f:
         if RE1.search(line):
            New_NNI_RTR_Raw.append(RE1.search(line).group())

New_NNI_RTR_BGP_Routes=[]

for i in range(len(New_NNI_RTR_Raw)):
    New_NNI_RTR_BGP_Routes.append(New_NNI_RTR_Raw[i].split(' ')[-1])

New_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name1) as f:
     for line in f:
         if RE3.search(line):
            New_NNI_RTR_Raw.append(RE3.search(line).group())

New_NNI_RTR_Nats=[]

for i in range(len(New_NNI_RTR_Raw)):
    New_NNI_RTR_Nats.append(New_NNI_RTR_Raw[i])

A_NAT_EUR.clear()
A_NAT_USA.clear()
A_NATIVE_EUR.clear()
A_NATIVE_USA.clear()
B_NAT_EUR.clear()
B_NAT_USA.clear()
B_NATIVE_EUR.clear()
B_NATIVE_USA.clear()

with open('Result_' + Host_Name1) as f:
     for line in f:
         if 'ip prefix-list PL-A-NAT-EU' in line:
             A_NAT_EUR.append(line)
         elif 'ip prefix-list PL-A-NAT-USA' in line:
               A_NAT_USA.append(line)
         elif 'ip prefix-list PL-A-NATIVE-EU' in line:
               A_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-A-NATIVE-USA' in line:
               A_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-B-NAT-EU' in line:
               B_NAT_EUR.append(line)
         elif 'ip prefix-list PL-B-NAT-USA' in line:
            B_NAT_USA.append(line)
         elif 'ip prefix-list PL-B-NATIVE-EU' in line:
              B_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-B-NATIVE-USA' in line:
              B_NATIVE_USA.append(line)

New_NNI_RTR_A_NAT_EUR = []
New_NNI_RTR_A_NAT_USA = []
New_NNI_RTR_A_NATIVE_EUR = []
New_NNI_RTR_A_NATIVE_USA = []
New_NNI_RTR_B_NAT_EUR = []
New_NNI_RTR_B_NAT_USA = []
New_NNI_RTR_B_NATIVE_EUR = []
New_NNI_RTR_B_NATIVE_USA = []

for i in range(len(A_NAT_EUR)):
    New_NNI_RTR_A_NAT_EUR.append(A_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NAT_USA)):
    New_NNI_RTR_A_NAT_USA.append(A_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_EUR)):
    New_NNI_RTR_A_NATIVE_EUR.append(A_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_USA)):
    New_NNI_RTR_A_NATIVE_USA.append(A_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_EUR)):
    New_NNI_RTR_B_NAT_EUR.append(B_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_EUR)):
    New_NNI_RTR_B_NATIVE_EUR.append(B_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_USA)):
    New_NNI_RTR_B_NAT_USA.append(B_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_USA)):
    New_NNI_RTR_B_NATIVE_USA.append(B_NATIVE_USA[i].strip('\n').split(' ')[-1])

New_NNI_RTR_A_NAT_EUR_PL = []
New_NNI_RTR_A_NAT_USA_PL = []
New_NNI_RTR_A_NATIVE_EUR_PL = []
New_NNI_RTR_A_NATIVE_USA_PL = []
New_NNI_RTR_B_NAT_EUR_PL = []
New_NNI_RTR_B_NAT_USA_PL = []
New_NNI_RTR_B_NATIVE_EUR_PL = []
New_NNI_RTR_B_NATIVE_USA_PL = []

for line in New_NNI_RTR_A_NAT_EUR:
    if RE4.search(line):
       New_NNI_RTR_A_NAT_EUR_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_A_NAT_USA:
    if RE4.search(line):
       New_NNI_RTR_A_NAT_USA_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_A_NATIVE_EUR:
    if RE4.search(line):
       New_NNI_RTR_A_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_A_NATIVE_USA:
    if RE4.search(line):
       New_NNI_RTR_A_NATIVE_USA_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_B_NAT_EUR:
    if RE4.search(line):
       New_NNI_RTR_B_NAT_EUR_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_B_NAT_USA:
    if RE4.search(line):
       New_NNI_RTR_B_NAT_USA_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_B_NATIVE_EUR:
    if RE4.search(line):
       New_NNI_RTR_B_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_B_NATIVE_USA:
    if RE4.search(line):
       New_NNI_RTR_B_NATIVE_USA_PL.append(RE4.search(line).group())
#========Second Target Device===================================================
print('=============Generating The Output Files From XXXX Router===================')
print('\n')

Host_Name2  = 'XXXX'
#username = input('Enter Username: ')
#password = getpass.getpass()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(Host_Name2, 22, username, password)

remote_session = client.invoke_shell()

output = remote_session.send('\n')
output = remote_session.send('ter len 0\n')
output = remote_session.send('sh ip route bgp\n')
output = remote_session.send('sh ip route static\n')
output = remote_session.send('sh run | i ip nat\n')
output = remote_session.send('sh run | i ip prefix-list\n')

time.sleep(15)

output = remote_session.recv(85535)
#print(output.decode('utf-8'))
client.close()

with open('Result_' + Host_Name2, 'w') as f:
    f.write(output.decode('utf-8'))

Sec_NNI_RTR_Raw=[]
Sec_NNI_RTR_Static_Routes=[]

with open('Result_' + Host_Name2) as f:
     for line in f:
         if RE.search(line):
            Sec_NNI_RTR_Raw.append(RE.search(line).group())

for i in range(len(Sec_NNI_RTR_Raw)):
    Sec_NNI_RTR_Static_Routes.append(Sec_NNI_RTR_Raw[i].split(' ')[-1])

#print(Sec_NNI_RTR_Static_Routes)
Sec_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name2) as f:
     for line in f:
         if RE1.search(line):
            Sec_NNI_RTR_Raw.append(RE1.search(line).group())

Sec_NNI_RTR_BGP_Routes=[]

for i in range(len(Sec_NNI_RTR_Raw)):
    Sec_NNI_RTR_BGP_Routes.append(Sec_NNI_RTR_Raw[i].split(' ')[-1])

Sec_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name2) as f:
     for line in f:
         if RE3.search(line):
            Sec_NNI_RTR_Raw.append(RE3.search(line).group())

Sec_NNI_RTR_Nats=[]

for i in range(len(Sec_NNI_RTR_Raw)):
    Sec_NNI_RTR_Nats.append(Sec_NNI_RTR_Raw[i])

A_NAT_EUR.clear()
A_NAT_USA.clear()
A_NATIVE_EUR.clear()
A_NATIVE_USA.clear()
B_NAT_EUR.clear()
B_NAT_USA.clear()
B_NATIVE_EUR.clear()
B_NATIVE_USA.clear()

with open('Result_' + Host_Name2) as f:
     for line in f:
         if 'ip prefix-list PL-A-NAT-EU' in line:
             A_NAT_EUR.append(line)
         elif 'ip prefix-list PL-A-NAT-USA' in line:
               A_NAT_USA.append(line)
         elif 'ip prefix-list PL-A-NATIVE-EU' in line:
               A_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-A-NATIVE-USA' in line:
               A_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-B-NAT-EU' in line:
               B_NAT_EUR.append(line)
         elif 'ip prefix-list PL-B-NAT-USA' in line:
            B_NAT_USA.append(line)
         elif 'ip prefix-list PL-B-NATIVE-EU' in line:
              B_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-B-NATIVE-USA' in line:
              B_NATIVE_USA.append(line)

Sec_NNI_RTR_A_NAT_EUR = []
Sec_NNI_RTR_A_NAT_USA = []
Sec_NNI_RTR_A_NATIVE_EUR = []
Sec_NNI_RTR_A_NATIVE_USA = []
Sec_NNI_RTR_B_NAT_EUR = []
Sec_NNI_RTR_B_NAT_USA = []
Sec_NNI_RTR_B_NATIVE_EUR = []
Sec_NNI_RTR_B_NATIVE_USA = []

for i in range(len(A_NAT_EUR)):
    Sec_NNI_RTR_A_NAT_EUR.append(A_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NAT_USA)):
    Sec_NNI_RTR_A_NAT_USA.append(A_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_EUR)):
    Sec_NNI_RTR_A_NATIVE_EUR.append(A_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_USA)):
    Sec_NNI_RTR_A_NATIVE_USA.append(A_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_EUR)):
    Sec_NNI_RTR_B_NAT_EUR.append(B_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_EUR)):
    Sec_NNI_RTR_B_NATIVE_EUR.append(B_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_USA)):
    Sec_NNI_RTR_B_NAT_USA.append(B_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_USA)):
    Sec_NNI_RTR_B_NATIVE_USA.append(B_NATIVE_USA[i].strip('\n').split(' ')[-1])

Sec_NNI_RTR_A_NAT_EUR_PL = []
Sec_NNI_RTR_A_NAT_USA_PL = []
Sec_NNI_RTR_A_NATIVE_EUR_PL = []
Sec_NNI_RTR_A_NATIVE_USA_PL = []
Sec_NNI_RTR_B_NAT_EUR_PL = []
Sec_NNI_RTR_B_NAT_USA_PL = []
Sec_NNI_RTR_B_NATIVE_EUR_PL = []
Sec_NNI_RTR_B_NATIVE_USA_PL = []

for line in Sec_NNI_RTR_A_NAT_EUR:
    if RE4.search(line):
       Sec_NNI_RTR_A_NAT_EUR_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_A_NAT_USA:
    if RE4.search(line):
       Sec_NNI_RTR_A_NAT_USA_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_A_NATIVE_EUR:
    if RE4.search(line):
       Sec_NNI_RTR_A_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_A_NATIVE_USA:
    if RE4.search(line):
       Sec_NNI_RTR_A_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_B_NAT_EUR:
    if RE4.search(line):
       Sec_NNI_RTR_B_NAT_EUR_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_B_NAT_USA:
    if RE4.search(line):
       Sec_NNI_RTR_B_NAT_USA_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_B_NATIVE_EUR:
    if RE4.search(line):
       Sec_NNI_RTR_B_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_B_NATIVE_USA:
    if RE4.search(line):
       Sec_NNI_RTR_B_NATIVE_USA_PL.append(RE4.search(line).group())
#========Third Target Device===================================================
print('=============Generating The Output Files From XXXX Router===================')
print('\n')

Host_Name3  = 'XXXX'
#username = input('Enter Username: ')
#password = getpass.getpass()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(Host_Name3, 22, username, password)

remote_session = client.invoke_shell()

output = remote_session.send('\n')
output = remote_session.send('ter len 0\n')
output = remote_session.send('sh ip route bgp\n')
output = remote_session.send('sh ip route static\n')
output = remote_session.send('sh run | i ip nat\n')
output = remote_session.send('sh run | i ip prefix-list\n')

time.sleep(15)

output = remote_session.recv(85535)
#print(output.decode('utf-8'))
client.close()

with open('Result_' + Host_Name3, 'w') as f:
    f.write(output.decode('utf-8'))

Thr_NNI_RTR_Raw=[]
Thr_NNI_RTR_Static_Routes=[]

with open('Result_' + Host_Name3) as f:
     for line in f:
         if RE.search(line):
            Thr_NNI_RTR_Raw.append(RE.search(line).group())

for i in range(len(Thr_NNI_RTR_Raw)):
    Thr_NNI_RTR_Static_Routes.append(Thr_NNI_RTR_Raw[i].split(' ')[-1])

#print(Thr_NNI_RTR_Static_Routes)
Thr_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name3) as f:
     for line in f:
         if RE1.search(line):
            Thr_NNI_RTR_Raw.append(RE1.search(line).group())

Thr_NNI_RTR_BGP_Routes=[]

for i in range(len(Thr_NNI_RTR_Raw)):
    Thr_NNI_RTR_BGP_Routes.append(Thr_NNI_RTR_Raw[i].split(' ')[-1])

Thr_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name3) as f:
     for line in f:
         if RE3.search(line):
            Thr_NNI_RTR_Raw.append(RE3.search(line).group())

Thr_NNI_RTR_Nats=[]

for i in range(len(Thr_NNI_RTR_Raw)):
    Thr_NNI_RTR_Nats.append(Thr_NNI_RTR_Raw[i])

A_NAT_EUR.clear()
A_NAT_USA.clear()
A_NATIVE_EUR.clear()
A_NATIVE_USA.clear()
B_NAT_EUR.clear()
B_NAT_USA.clear()
B_NATIVE_EUR.clear()
B_NATIVE_USA.clear()

with open('Result_' + Host_Name3) as f:
     for line in f:
         if 'ip prefix-list PL-A-NAT-EU' in line:
             A_NAT_EUR.append(line)
         elif 'ip prefix-list PL-A-NAT-USA' in line:
               A_NAT_USA.append(line)
         elif 'ip prefix-list PL-A-NATIVE-EU' in line:
               A_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-A-NATIVE-USA' in line:
               A_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-B-NAT-EU' in line:
               B_NAT_EUR.append(line)
         elif 'ip prefix-list PL-B-NAT-USA' in line:
            B_NAT_USA.append(line)
         elif 'ip prefix-list PL-B-NATIVE-EU' in line:
              B_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-B-NATIVE-USA' in line:
              B_NATIVE_USA.append(line)

Thr_NNI_RTR_A_NAT_EUR = []
Thr_NNI_RTR_A_NAT_USA = []
Thr_NNI_RTR_A_NATIVE_EUR = []
Thr_NNI_RTR_A_NATIVE_USA = []
Thr_NNI_RTR_B_NAT_EUR = []
Thr_NNI_RTR_B_NAT_USA = []
Thr_NNI_RTR_B_NATIVE_EUR = []
Thr_NNI_RTR_B_NATIVE_USA = []

for i in range(len(A_NAT_EUR)):
    Thr_NNI_RTR_A_NAT_EUR.append(A_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NAT_USA)):
    Thr_NNI_RTR_A_NAT_USA.append(A_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_EUR)):
    Thr_NNI_RTR_A_NATIVE_EUR.append(A_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_USA)):
    Thr_NNI_RTR_A_NATIVE_USA.append(A_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_EUR)):
    Thr_NNI_RTR_B_NAT_EUR.append(B_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_EUR)):
    Thr_NNI_RTR_B_NATIVE_EUR.append(B_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_USA)):
    Thr_NNI_RTR_B_NAT_USA.append(B_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_USA)):
    Thr_NNI_RTR_B_NATIVE_USA.append(B_NATIVE_USA[i].strip('\n').split(' ')[-1])

Thr_NNI_RTR_A_NAT_EUR_PL = []
Thr_NNI_RTR_A_NAT_USA_PL = []
Thr_NNI_RTR_A_NATIVE_EUR_PL = []
Thr_NNI_RTR_A_NATIVE_USA_PL = []
Thr_NNI_RTR_B_NAT_EUR_PL = []
Thr_NNI_RTR_B_NAT_USA_PL = []
Thr_NNI_RTR_B_NATIVE_EUR_PL = []
Thr_NNI_RTR_B_NATIVE_USA_PL = []

for line in Thr_NNI_RTR_A_NAT_EUR:
    if RE4.search(line):
       Thr_NNI_RTR_A_NAT_EUR_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_A_NAT_USA:
    if RE4.search(line):
       Thr_NNI_RTR_A_NAT_USA_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_A_NATIVE_EUR:
    if RE4.search(line):
       Thr_NNI_RTR_A_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_A_NATIVE_USA:
    if RE4.search(line):
       Thr_NNI_RTR_A_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_B_NAT_EUR:
    if RE4.search(line):
       Thr_NNI_RTR_B_NAT_EUR_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_B_NAT_USA:
    if RE4.search(line):
       Thr_NNI_RTR_B_NAT_USA_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_B_NATIVE_EUR:
    if RE4.search(line):
       Thr_NNI_RTR_B_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_B_NATIVE_USA:
    if RE4.search(line):
       Thr_NNI_RTR_B_NATIVE_USA_PL.append(RE4.search(line).group())
#=======================Comparison of B Side NNi Routers=======================================
print('=====Below output Based on Comparison of B Side NNI Routers=============================')

Missing_BGP_Routes=list(set(Pre_NNI_RTR_BGP_Routes).difference(set(New_NNI_RTR_BGP_Routes),set(Sec_NNI_RTR_BGP_Routes),set(Thr_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes1=list(set(New_NNI_RTR_BGP_Routes).difference(set(Pre_NNI_RTR_BGP_Routes),set(Sec_NNI_RTR_BGP_Routes),set(Thr_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes2=list(set(Sec_NNI_RTR_BGP_Routes).difference(set(Pre_NNI_RTR_BGP_Routes),set(New_NNI_RTR_BGP_Routes),set(Thr_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes3=list(set(Thr_NNI_RTR_BGP_Routes).difference(set(Pre_NNI_RTR_BGP_Routes),set(New_NNI_RTR_BGP_Routes),set(Sec_NNI_RTR_BGP_Routes)))

if len(Missing_BGP_Routes) == 0 and len(Missing_BGP_Routes1) == 0 and len(Missing_BGP_Routes2) == 0 and len(Missing_BGP_Routes3) == 0:
     print('='*95)
     print('BGP Routes are Same across all B NNI Routers!!!')
elif len(Missing_BGP_Routes) > 0:
     print('Missing BGP Routes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & '+ Host_Name3 + ' are below:')
     for i in range(len(Missing_BGP_Routes)):
         print(Missing_BGP_Routes[i])
elif len(Missing_BGP_Routes1) > 0:
     print('Missing BGP Routes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & '+ Host_Name3 + ' are below:')
     for i in range(len(Missing_BGP_Routes1)):
         print(Missing_BGP_Routes1[i])
elif len(Missing_BGP_Routes2) > 0:
     print('Missing BGP Routes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & '+ Host_Name3 + ' are below:')
     for i in range(len(Missing_BGP_Routes2)):
         print(Missing_BGP_Routes2[i])
elif len(Missing_BGP_Routes3) > 0:
     print('Missing BGP Routes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & '+ Host_Name2 + ' are below:')
     for i in range(len(Missing_BGP_Routes3)):
         print(Missing_BGP_Routes3[i])

##Below output will display BGP Route Count on B NNI Routers
print('\n'*1)
print('Below output will display BGP Route Count on all B NNI Routers:')
print('='*95)
print("On " + Host_Name + " total no of BGP routes are :{}".format(len(Pre_NNI_RTR_BGP_Routes)))
print("On " + Host_Name1 + " total no of BGP routes are :{}".format(len(New_NNI_RTR_BGP_Routes)))
print("On " + Host_Name2 + " total no of BGP routes are :{}".format(len(Sec_NNI_RTR_BGP_Routes)))
print("On " + Host_Name3 + " total no of BGP routes are :{}".format(len(Thr_NNI_RTR_BGP_Routes)))
print('='*95)
#===============================================================================
Missing_Static_Routes=list(set(Pre_NNI_RTR_Static_Routes).difference(set(New_NNI_RTR_Static_Routes),set(Sec_NNI_RTR_Static_Routes),set(Thr_NNI_RTR_Static_Routes)))
Missing_Static_Routes1=list(set(New_NNI_RTR_Static_Routes).difference(set(Pre_NNI_RTR_Static_Routes),set(Sec_NNI_RTR_Static_Routes),set(Thr_NNI_RTR_Static_Routes)))
Missing_Static_Routes2=list(set(Sec_NNI_RTR_Static_Routes).difference(set(Pre_NNI_RTR_Static_Routes),set(New_NNI_RTR_Static_Routes),set(Thr_NNI_RTR_Static_Routes)))
Missing_Static_Routes3=list(set(Thr_NNI_RTR_Static_Routes).difference(set(Pre_NNI_RTR_Static_Routes),set(New_NNI_RTR_Static_Routes),set(Sec_NNI_RTR_Static_Routes)))

if len(Missing_Static_Routes) == 0 and len(Missing_Static_Routes1) == 0 and len(Missing_Static_Routes2) == 0 and len(Missing_Static_Routes3) == 0:
     print('='*95)
     print('Static Routes are Same across all B NNI Routers!!!')
elif len(Missing_Static_Routes) > 0:
     print('Missing Static Routes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Static_Routes)):
         print(Missing_Static_Routes[i])
elif len(Missing_Static_Routes1) > 0:
     print('Missing Static Routes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Static_Routes1)):
         print(Missing_Static_Routes1[i])
elif len(Missing_Static_Routes2) > 0:
     print('Missing Static Routes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Static_Routes2)):
         print(Missing_Static_Routes2[i])
elif len(Missing_Static_Routes3) > 0:
     print('Missing Static Routes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_Static_Routes3)):
         print(Missing_Static_Routes3[i])

##Below output will display Static Route Count on B NNI Routers
print('\n'*1)
print('Below output will display Static Route Count on all B NNI Routers:')
print('='*95)
print("On " + Host_Name + " total no of Static routes are :{}".format(len(Pre_NNI_RTR_Static_Routes)))
print("On " + Host_Name1 + " total no of Static routes are :{}".format(len(New_NNI_RTR_Static_Routes)))
print("On " + Host_Name2 + " total no of Static routes are :{}".format(len(Sec_NNI_RTR_Static_Routes)))
print("On " + Host_Name3 + " total no of Static routes are :{}".format(len(Thr_NNI_RTR_Static_Routes)))
print('='*95)
#===============================================================================
Missing_Nats=list(set(Pre_NNI_RTR_Nats).difference(set(New_NNI_RTR_Nats),set(Sec_NNI_RTR_Nats),set(Thr_NNI_RTR_Nats)))
Missing_Nats1=list(set(New_NNI_RTR_Nats).difference(set(Pre_NNI_RTR_Nats),set(Sec_NNI_RTR_Nats),set(Sec_NNI_RTR_Nats)))
Missing_Nats2=list(set(Sec_NNI_RTR_Nats).difference(set(Pre_NNI_RTR_Nats),set(New_NNI_RTR_Nats),set(Sec_NNI_RTR_Nats)))
Missing_Nats3=list(set(Thr_NNI_RTR_Nats).difference(set(Pre_NNI_RTR_Nats),set(New_NNI_RTR_Nats),set(Sec_NNI_RTR_Nats)))

if len(Missing_Nats) == 0 and len(Missing_Nats1) == 0 and len(Missing_Nats2) == 0 and len(Missing_Nats3) == 0:
     print('='*95)
     print('Static Nats are Same across all B NNI Routers!!!')
elif len(Missing_Nats) > 0:
     print('Missing Static Nats of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Nats)):
         print(Missing_Nats[i])
elif len(Missing_Nats1) > 0:
     print('Missing Static Nats of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Nats1)):
         print(Missing_Nats1[i])
elif len(Missing_Nats2) > 0:
     print('Missing Static Nats of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Nats2)):
         print(Missing_Nats2[i])
elif len(Missing_Nats3) > 0:
     print('Missing Static Nats of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_Nats3)):
         print(Missing_Nats3[i])

##Below output will display Static Nats Count on B NNI Routers
print('\n'*1)
print('Below output will display Static Nats Count on all B NNI Routers:')
print('='*95)
print("On " + Host_Name + " total no of Static Nats are :{}".format(len(Pre_NNI_RTR_Nats)))
print("On " + Host_Name1 + " total no of Static Nats are :{}".format(len(New_NNI_RTR_Nats)))
print("On " + Host_Name2 + " total no of Static Nats are :{}".format(len(Sec_NNI_RTR_Nats)))
print("On " + Host_Name3 + " total no of Static Nats are :{}".format(len(Thr_NNI_RTR_Nats)))
print('='*95)

#===============================================================================
Missing_A_NAT_EUR=list(set(Pre_NNI_RTR_A_NAT_EUR_PL).difference(set(New_NNI_RTR_A_NAT_EUR_PL),set(Sec_NNI_RTR_A_NAT_EUR_PL),set(Thr_NNI_RTR_A_NAT_EUR_PL)))
Missing_A_NAT_EUR1=list(set(New_NNI_RTR_A_NAT_EUR_PL).difference(set(Pre_NNI_RTR_A_NAT_EUR_PL),set(Sec_NNI_RTR_A_NAT_EUR_PL),set(Thr_NNI_RTR_A_NAT_EUR_PL)))
Missing_A_NAT_EUR2=list(set(Sec_NNI_RTR_A_NAT_EUR_PL).difference(set(Pre_NNI_RTR_A_NAT_EUR_PL),set(New_NNI_RTR_A_NAT_EUR_PL),set(Thr_NNI_RTR_A_NAT_EUR_PL)))
Missing_A_NAT_EUR3=list(set(Thr_NNI_RTR_A_NAT_EUR_PL).difference(set(Pre_NNI_RTR_A_NAT_EUR_PL),set(New_NNI_RTR_A_NAT_EUR_PL),set(Sec_NNI_RTR_A_NAT_EUR_PL)))

Missing_A_NAT_USA=list(set(Pre_NNI_RTR_A_NAT_USA_PL).difference(set(New_NNI_RTR_A_NAT_USA_PL),set(Sec_NNI_RTR_A_NAT_USA_PL),set(Thr_NNI_RTR_A_NAT_USA_PL)))
Missing_A_NAT_USA1=list(set(New_NNI_RTR_A_NAT_USA_PL).difference(set(Pre_NNI_RTR_A_NAT_USA_PL),set(Sec_NNI_RTR_A_NAT_USA_PL),set(Thr_NNI_RTR_A_NAT_USA_PL)))
Missing_A_NAT_USA2=list(set(Sec_NNI_RTR_A_NAT_USA_PL).difference(set(Pre_NNI_RTR_A_NAT_USA_PL),set(New_NNI_RTR_A_NAT_USA_PL),set(Thr_NNI_RTR_A_NAT_USA_PL)))
Missing_A_NAT_USA3=list(set(Thr_NNI_RTR_A_NAT_USA_PL).difference(set(Pre_NNI_RTR_A_NAT_USA_PL),set(New_NNI_RTR_A_NAT_USA_PL),set(Sec_NNI_RTR_A_NAT_USA_PL)))

Missing_A_NATIVE_EUR=list(set(Pre_NNI_RTR_A_NATIVE_EUR_PL).difference(set(New_NNI_RTR_A_NATIVE_EUR_PL),set(Sec_NNI_RTR_A_NATIVE_EUR_PL),set(Thr_NNI_RTR_A_NATIVE_EUR_PL)))
Missing_A_NATIVE_EUR1=list(set(New_NNI_RTR_A_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_A_NATIVE_EUR_PL),set(Sec_NNI_RTR_A_NATIVE_EUR_PL),set(Thr_NNI_RTR_A_NATIVE_EUR_PL)))
Missing_A_NATIVE_EUR2=list(set(Sec_NNI_RTR_A_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_A_NATIVE_EUR_PL),set(New_NNI_RTR_A_NATIVE_EUR_PL),set(Thr_NNI_RTR_A_NATIVE_EUR_PL)))
Missing_A_NATIVE_EUR3=list(set(Thr_NNI_RTR_A_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_A_NATIVE_EUR_PL),set(New_NNI_RTR_A_NATIVE_EUR_PL),set(Sec_NNI_RTR_A_NATIVE_EUR_PL)))

Missing_A_NATIVE_USA=list(set(Pre_NNI_RTR_A_NATIVE_USA_PL).difference(set(New_NNI_RTR_A_NATIVE_USA_PL),set(Sec_NNI_RTR_A_NATIVE_USA_PL),set(Thr_NNI_RTR_A_NATIVE_USA_PL)))
Missing_A_NATIVE_USA1=list(set(New_NNI_RTR_A_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_A_NATIVE_USA_PL),set(Sec_NNI_RTR_A_NATIVE_USA_PL),set(Thr_NNI_RTR_A_NATIVE_USA_PL)))
Missing_A_NATIVE_USA2=list(set(Sec_NNI_RTR_A_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_A_NATIVE_USA_PL),set(New_NNI_RTR_A_NATIVE_USA_PL),set(Thr_NNI_RTR_A_NATIVE_USA_PL)))
Missing_A_NATIVE_USA3=list(set(Thr_NNI_RTR_A_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_A_NATIVE_USA_PL),set(New_NNI_RTR_A_NATIVE_USA_PL),set(Sec_NNI_RTR_A_NATIVE_USA_PL)))

Missing_B_NAT_EUR=list(set(Pre_NNI_RTR_B_NAT_EUR_PL).difference(set(New_NNI_RTR_B_NAT_EUR_PL),set(Sec_NNI_RTR_B_NAT_EUR_PL),set(Thr_NNI_RTR_B_NAT_EUR_PL)))
Missing_B_NAT_EUR1=list(set(New_NNI_RTR_B_NAT_EUR_PL).difference(set(Pre_NNI_RTR_B_NAT_EUR_PL),set(Sec_NNI_RTR_B_NAT_EUR_PL),set(Thr_NNI_RTR_B_NAT_EUR_PL)))
Missing_B_NAT_EUR2=list(set(Sec_NNI_RTR_B_NAT_EUR_PL).difference(set(Pre_NNI_RTR_B_NAT_EUR_PL),set(New_NNI_RTR_B_NAT_EUR_PL),set(Thr_NNI_RTR_B_NAT_EUR_PL)))
Missing_B_NAT_EUR3=list(set(Thr_NNI_RTR_B_NAT_EUR_PL).difference(set(Pre_NNI_RTR_B_NAT_EUR_PL),set(New_NNI_RTR_B_NAT_EUR_PL),set(Sec_NNI_RTR_B_NAT_EUR_PL)))

Missing_B_NAT_USA=list(set(Pre_NNI_RTR_B_NAT_USA_PL).difference(set(New_NNI_RTR_B_NAT_USA_PL),set(Sec_NNI_RTR_B_NAT_USA_PL),set(Thr_NNI_RTR_B_NAT_USA_PL)))
Missing_B_NAT_USA1=list(set(New_NNI_RTR_B_NAT_USA_PL).difference(set(Pre_NNI_RTR_B_NAT_USA_PL),set(Sec_NNI_RTR_B_NAT_USA_PL),set(Thr_NNI_RTR_B_NAT_USA_PL)))
Missing_B_NAT_USA2=list(set(Sec_NNI_RTR_B_NAT_USA_PL).difference(set(Pre_NNI_RTR_B_NAT_USA_PL),set(New_NNI_RTR_B_NAT_USA_PL),set(Thr_NNI_RTR_B_NAT_USA_PL)))
Missing_B_NAT_USA3=list(set(Thr_NNI_RTR_B_NAT_USA_PL).difference(set(Pre_NNI_RTR_B_NAT_USA_PL),set(New_NNI_RTR_B_NAT_USA_PL),set(Sec_NNI_RTR_B_NAT_USA_PL)))

Missing_B_NATIVE_EUR=list(set(Pre_NNI_RTR_B_NATIVE_EUR_PL).difference(set(New_NNI_RTR_B_NATIVE_EUR_PL),set(Sec_NNI_RTR_B_NATIVE_EUR_PL),set(Thr_NNI_RTR_B_NATIVE_EUR_PL)))
Missing_B_NATIVE_EUR1=list(set(New_NNI_RTR_B_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_B_NATIVE_EUR_PL),set(Sec_NNI_RTR_B_NATIVE_EUR_PL),set(Thr_NNI_RTR_B_NATIVE_EUR_PL)))
Missing_B_NATIVE_EUR2=list(set(Sec_NNI_RTR_B_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_B_NATIVE_EUR_PL),set(New_NNI_RTR_B_NATIVE_EUR_PL),set(Thr_NNI_RTR_B_NATIVE_EUR_PL)))
Missing_B_NATIVE_EUR3=list(set(Thr_NNI_RTR_B_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_B_NATIVE_EUR_PL),set(New_NNI_RTR_B_NATIVE_EUR_PL),set(Sec_NNI_RTR_B_NATIVE_EUR_PL)))

Missing_B_NATIVE_USA=list(set(Pre_NNI_RTR_B_NATIVE_USA_PL).difference(set(New_NNI_RTR_B_NATIVE_USA_PL),set(Sec_NNI_RTR_B_NATIVE_USA_PL),set(Thr_NNI_RTR_B_NATIVE_USA_PL)))
Missing_B_NATIVE_USA1=list(set(New_NNI_RTR_B_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_B_NATIVE_USA_PL),set(Sec_NNI_RTR_B_NATIVE_USA_PL),set(Thr_NNI_RTR_B_NATIVE_USA_PL)))
Missing_B_NATIVE_USA2=list(set(Sec_NNI_RTR_B_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_B_NATIVE_USA_PL),set(New_NNI_RTR_B_NATIVE_USA_PL),set(Thr_NNI_RTR_B_NATIVE_USA_PL)))
Missing_B_NATIVE_USA3=list(set(Thr_NNI_RTR_B_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_B_NATIVE_USA_PL),set(New_NNI_RTR_B_NATIVE_USA_PL),set(Sec_NNI_RTR_B_NATIVE_USA_PL)))

print('='*90)

if len(Missing_A_NAT_EUR) == 0 and len(Missing_A_NAT_EUR1) == 0 and len(Missing_A_NAT_EUR2) == 0 and len(Missing_A_NAT_EUR3) == 0:
     print('='*95)
     print('L-A NATTED Prefixes Of EU Region are Same across all B NNI Routers!!!')
elif len(Missing_A_NAT_EUR) > 0:
     print('Missing L-A EU Region NATTED Prefixes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NAT_EUR)):
         print(Missing_A_NAT_EUR[i])
elif len(Missing_A_NAT_EUR1) > 0:
     print('Missing L-A EU Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NAT_EUR1)):
         print(Missing_A_NAT_EUR1[i])
elif len(Missing_A_NAT_EUR2) > 0:
     print('Missing L-A EU Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NAT_EUR2)):
         print(Missing_A_NAT_EUR2[i])
elif len(Missing_A_NAT_EUR3) > 0:
     print('Missing L-A EU Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_A_NAT_EUR3)):
         print(Missing_A_NAT_EUR3[i])

if len(Missing_A_NAT_USA) == 0 and len(Missing_A_NAT_USA1) == 0 and len(Missing_A_NAT_USA2) == 0 and len(Missing_A_NAT_USA3) == 0:
     print('='*95)
     print('L-A NATTED Prefixes Of US Region are Same across all B NNI Routers!!!')
elif len(Missing_A_NAT_USA) > 0:
     print('Missing L-A US Region NATTED Prefixes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NAT_USA)):
         print(Missing_A_NAT_USA[i])
elif len(Missing_A_NAT_USA1) > 0:
     print('Missing L-A US Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NAT_USA1)):
         print(Missing_A_NAT_USA1[i])
elif len(Missing_A_NAT_USA2) > 0:
     print('Missing L-A US Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NAT_USA2)):
         print(Missing_A_NAT_USA2[i])
elif len(Missing_A_NAT_USA3) > 0:
     print('Missing L-A US Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_A_NAT_USA3)):
         print(Missing_A_NAT_USA3[i])

print('\n'*1)

if len(Missing_A_NATIVE_EUR) == 0 and len(Missing_A_NATIVE_EUR1) == 0 and len(Missing_A_NATIVE_EUR2) == 0 and len(Missing_A_NATIVE_EUR3) == 0:
     print('='*95)
     print('L-A NATIVE Prefixes Of EU Region are Same across all B NNI Routers!!!')
elif len(Missing_A_NATIVE_EUR) > 0:
     print('Missing L-A EU Region NATIVE Prefixes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NATIVE_EUR)):
         print(Missing_A_NATIVE_EUR[i])
elif len(Missing_A_NATIVE_EUR1) > 0:
     print('Missing L-A EU Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NATIVE_EUR1)):
         print(Missing_A_NATIVE_EUR1[i])
elif len(Missing_A_NATIVE_EUR2) > 0:
     print('Missing L-A EU Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NATIVE_EUR2)):
         print(Missing_A_NATIVE_EUR2[i])
elif len(Missing_A_NATIVE_EUR3) > 0:
     print('Missing L-A EU Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_A_NATIVE_EUR3)):
         print(Missing_A_NATIVE_EUR3[i])

if len(Missing_A_NATIVE_USA) == 0 and len(Missing_A_NATIVE_USA1) == 0 and len(Missing_A_NATIVE_USA2) == 0 and len(Missing_A_NATIVE_USA3) == 0:
     print('='*95)
     print('L-A NATIVE Prefixes Of US Region are Same across all B NNI Routers!!!')
elif len(Missing_A_NATIVE_USA) > 0:
     print('Missing L-A US Region NATIVE Prefixes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NATIVE_USA)):
         print(Missing_A_NATIVE_USA[i])
elif len(Missing_A_NATIVE_USA1) > 0:
     print('Missing L-A US Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NATIVE_USA1)):
         print(Missing_A_NATIVE_USA1[i])
elif len(Missing_A_NATIVE_USA2) > 0:
     print('Missing L-A US Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_A_NATIVE_USA2)):
         print(Missing_A_NATIVE_USA2[i])
elif len(Missing_A_NATIVE_USA3) > 0:
     print('Missing L-A US Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_A_NATIVE_USA3)):
         print(Missing_A_NATIVE_USA3[i])

print('\n'*1)

if len(Missing_B_NAT_EUR) == 0 and len(Missing_B_NAT_EUR1) == 0 and len(Missing_B_NAT_EUR2) == 0 and len(Missing_B_NAT_EUR3) == 0:
     print('='*95)
     print('L-B NATTED Prefixes Of EU Region are Same across all B NNI Routers!!!')
elif len(Missing_B_NAT_EUR) > 0:
     print('Missing L-B EU Region NATTED Prefixes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NAT_EUR)):
         print(Missing_B_NAT_EUR[i])
elif len(Missing_B_NAT_EUR1) > 0:
     print('Missing L-B EU Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NAT_EUR1)):
         print(Missing_B_NAT_EUR1[i])
elif len(Missing_B_NAT_EUR2) > 0:
     print('Missing L-B EU Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NAT_EUR2)):
         print(Missing_B_NAT_EUR2[i])
elif len(Missing_B_NAT_EUR3) > 0:
     print('Missing L-B EU Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_B_NAT_EUR3)):
         print(Missing_B_NAT_EUR3[i])


if len(Missing_B_NAT_USA) == 0 and len(Missing_B_NAT_USA1) == 0 and len(Missing_B_NAT_USA2) == 0 and len(Missing_B_NAT_USA3) == 0:
     print('='*95)
     print('L-B NATTED Prefixes Of US Region are Same across all B NNI Routers!!!')
elif len(Missing_B_NAT_USA) > 0:
     print('Missing L-B US Region NATTED Prefixes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NAT_USA)):
         print(Missing_B_NAT_USA[i])
elif len(Missing_B_NAT_USA1) > 0:
     print('Missing L-B US Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NAT_USA1)):
         print(Missing_B_NAT_USA1[i])
elif len(Missing_B_NAT_USA2) > 0:
     print('Missing L-B US Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NAT_USA2)):
         print(Missing_B_NAT_USA2[i])
elif len(Missing_B_NAT_USA3) > 0:
     print('Missing L-B US Region NATTED Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_B_NAT_USA3)):
         print(Missing_B_NAT_USA3[i])

print('\n'*1)

if len(Missing_B_NATIVE_EUR) == 0 and len(Missing_B_NATIVE_EUR1) == 0 and len(Missing_B_NATIVE_EUR2) == 0 and len(Missing_B_NATIVE_EUR3) == 0:
     print('='*95)
     print('L-B NATIVE Prefixes Of EU Region are Same across all B NNI Routers!!!')
elif len(Missing_B_NATIVE_EUR) > 0:
     print('Missing L-B EU Region NATIVE Prefixes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NATIVE_EUR)):
         print(Missing_B_NATIVE_EUR[i])
elif len(Missing_B_NATIVE_EUR1) > 0:
     print('Missing L-B EU Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NATIVE_EUR1)):
         print(Missing_B_NATIVE_EUR1[i])
elif len(Missing_B_NATIVE_EUR2) > 0:
     print('Missing L-B EU Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NATIVE_EUR2)):
         print(Missing_B_NATIVE_EUR2[i])
elif len(Missing_B_NATIVE_EUR3) > 0:
     print('Missing L-B EU Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_B_NATIVE_EUR3)):
         print(Missing_B_NATIVE_EUR3[i])

if len(Missing_B_NATIVE_USA) == 0 and len(Missing_B_NATIVE_USA1) == 0 and len(Missing_B_NATIVE_USA2) == 0 and len(Missing_B_NATIVE_USA3) == 0:
     print('='*95)
     print('L-B NATIVE Prefixes Of US Region are Same across all B NNI Routers!!!')
elif len(Missing_B_NATIVE_USA) > 0:
     print('Missing L-B US Region NATIVE Prefixes of XXXX in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NATIVE_USA)):
         print(Missing_B_NATIVE_USA[i])
elif len(Missing_B_NATIVE_USA1) > 0:
     print('Missing L-B US Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NATIVE_USA1)):
         print(Missing_B_NATIVE_USA1[i])
elif len(Missing_B_NATIVE_USA2) > 0:
     print('Missing L-B US Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_B_NATIVE_USA2)):
         print(Missing_B_NATIVE_USA2[i])
elif len(Missing_B_NATIVE_USA3) > 0:
     print('Missing L-B US Region NATIVE Prefixes of XXXX in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_B_NATIVE_USA3)):
         print(Missing_B_NATIVE_USA3[i])

print('='*90)
#======Files for L-A NNI Routers==============================================
#========Forth Target L-A Device===================================================
print('=============Generating The Output Files From XXXX Router===================')
print('\n')

Host_Name4 = 'XXXX'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(Host_Name4, 22, username, password)

remote_session = client.invoke_shell()

output = remote_session.send('\n')
output = remote_session.send('ter len 0\n')
output = remote_session.send('sh ip route bgp\n')
output = remote_session.send('sh ip route static\n')
output = remote_session.send('sh run | i ip nat\n')
output = remote_session.send('sh run | i ip prefix-list\n')

time.sleep(15)

output = remote_session.recv(85535)
#print(output.decode('utf-8'))
client.close()


with open('Result_' + Host_Name4, 'w') as f:
    f.write(output.decode('utf-8'))

RE = re.compile('S\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE1 = re.compile('B\*?\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE3 = re.compile('(\d+\.\d+\.\d+\.\d+\s){2}\/[0-9]{2}')
RE4 = re.compile('(\d+\.\d+\.\d+\.\d+)\/[0-9]{2}')

Forth_NNI_RTR_Raw=[]
Forth_NNI_RTR_Static_Routes=[]

with open('Result_' + Host_Name4) as f:
     for line in f:
         if RE.search(line):
            Forth_NNI_RTR_Raw.append(RE.search(line).group())

for i in range(len(Forth_NNI_RTR_Raw)):
    Forth_NNI_RTR_Static_Routes.append(Forth_NNI_RTR_Raw[i].split(' ')[-1])

#print(Forth_NNI_RTR_Static_Routes)
Forth_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name4) as f:
     for line in f:
         if RE1.search(line):
            Forth_NNI_RTR_Raw.append(RE1.search(line).group())

Forth_NNI_RTR_BGP_Routes=[]

for i in range(len(Forth_NNI_RTR_Raw)):
    Forth_NNI_RTR_BGP_Routes.append(Forth_NNI_RTR_Raw[i].split(' ')[-1])

Forth_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name4) as f:
     for line in f:
         if RE3.search(line):
            Forth_NNI_RTR_Raw.append(RE3.search(line).group())

Forth_NNI_RTR_Nats=[]

for i in range(len(Forth_NNI_RTR_Raw)):
    Forth_NNI_RTR_Nats.append(Forth_NNI_RTR_Raw[i])


A_NAT_EUR = []
A_NAT_USA = []
A_NATIVE_EUR = []
A_NATIVE_USA = []
B_NAT_EUR = []
B_NAT_USA = []
B_NATIVE_EUR = []
B_NATIVE_USA = []

with open('Result_' + Host_Name4) as f:
     for line in f:
         if 'ip prefix-list PL-A-NAT-EU' in line:
             A_NAT_EUR.append(line)
         elif 'ip prefix-list PL-A-NAT-USA' in line:
               A_NAT_USA.append(line)
         elif 'ip prefix-list PL-A-NATIVE-EU' in line:
               A_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-A-NATIVE-USA' in line:
               A_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-B-NAT-EU' in line:
               B_NAT_EUR.append(line)
         elif 'ip prefix-list PL-B-NAT-USA' in line:
            B_NAT_USA.append(line)
         elif 'ip prefix-list PL-B-NATIVE-EU' in line:
              B_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-B-NATIVE-USA' in line:
              B_NATIVE_USA.append(line)

Forth_NNI_RTR_A_NAT_EUR = []
Forth_NNI_RTR_A_NAT_USA = []
Forth_NNI_RTR_A_NATIVE_EUR = []
Forth_NNI_RTR_A_NATIVE_USA = []
Forth_NNI_RTR_B_NAT_EUR = []
Forth_NNI_RTR_B_NAT_USA = []
Forth_NNI_RTR_B_NATIVE_EUR = []
Forth_NNI_RTR_B_NATIVE_USA = []

for i in range(len(A_NAT_EUR)):
    Forth_NNI_RTR_A_NAT_EUR.append(A_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NAT_USA)):
    Forth_NNI_RTR_A_NAT_USA.append(A_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_EUR)):
    Forth_NNI_RTR_A_NATIVE_EUR.append(A_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_USA)):
    Forth_NNI_RTR_A_NATIVE_USA.append(A_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_EUR)):
    Forth_NNI_RTR_B_NAT_EUR.append(B_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_EUR)):
    Forth_NNI_RTR_B_NATIVE_EUR.append(B_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_USA)):
    Forth_NNI_RTR_B_NAT_USA.append(B_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_USA)):
    Forth_NNI_RTR_B_NATIVE_USA.append(B_NATIVE_USA[i].strip('\n').split(' ')[-1])

Forth_NNI_RTR_A_NAT_EUR_PL = []
Forth_NNI_RTR_A_NAT_USA_PL = []
Forth_NNI_RTR_A_NATIVE_EUR_PL = []
Forth_NNI_RTR_A_NATIVE_USA_PL = []
Forth_NNI_RTR_B_NAT_EUR_PL = []
Forth_NNI_RTR_B_NAT_USA_PL = []
Forth_NNI_RTR_B_NATIVE_EUR_PL = []
Forth_NNI_RTR_B_NATIVE_USA_PL = []

for line in Forth_NNI_RTR_A_NAT_EUR:
    if RE4.search(line):
       Forth_NNI_RTR_A_NAT_EUR_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_A_NAT_USA:
    if RE4.search(line):
       Forth_NNI_RTR_A_NAT_USA_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_A_NATIVE_EUR:
    if RE4.search(line):
       Forth_NNI_RTR_A_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_A_NATIVE_USA:
    if RE4.search(line):
       Forth_NNI_RTR_A_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_B_NAT_EUR:
    if RE4.search(line):
       Forth_NNI_RTR_B_NAT_EUR_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_B_NAT_USA:
    if RE4.search(line):
       Forth_NNI_RTR_B_NAT_USA_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_B_NATIVE_EUR:
    if RE4.search(line):
       Forth_NNI_RTR_B_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_B_NATIVE_USA:
    if RE4.search(line):
       Forth_NNI_RTR_B_NATIVE_USA_PL.append(RE4.search(line).group())
#========Fifth Target L-A Device===================================================
print('=============Generating The Output Files From XXXX Router===================')
print('\n')

Host_Name5 = 'XXXX'
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(Host_Name5, 22, username, password)

remote_session = client.invoke_shell()

output = remote_session.send('\n')
output = remote_session.send('ter len 0\n')
output = remote_session.send('sh ip route bgp\n')
output = remote_session.send('sh ip route static\n')
output = remote_session.send('sh run | i ip nat\n')
output = remote_session.send('sh run | i ip prefix-list\n')

time.sleep(15)

output = remote_session.recv(85535)
#print(output.decode('utf-8'))
client.close()


with open('Result_' + Host_Name5, 'w') as f:
    f.write(output.decode('utf-8'))

RE = re.compile('S\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE1 = re.compile('B\*?\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE3 = re.compile('(\d+\.\d+\.\d+\.\d+\s){2}\/[0-9]{2}')
RE4 = re.compile('(\d+\.\d+\.\d+\.\d+)\/[0-9]{2}')

Fifth_NNI_RTR_Raw=[]
Fifth_NNI_RTR_Static_Routes=[]

with open('Result_' + Host_Name5) as f:
     for line in f:
         if RE.search(line):
            Fifth_NNI_RTR_Raw.append(RE.search(line).group())

for i in range(len(Fifth_NNI_RTR_Raw)):
    Fifth_NNI_RTR_Static_Routes.append(Fifth_NNI_RTR_Raw[i].split(' ')[-1])

#print(Fifth_NNI_RTR_Static_Routes)
Fifth_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name5) as f:
     for line in f:
         if RE1.search(line):
            Fifth_NNI_RTR_Raw.append(RE1.search(line).group())

Fifth_NNI_RTR_BGP_Routes=[]

for i in range(len(Fifth_NNI_RTR_Raw)):
    Fifth_NNI_RTR_BGP_Routes.append(Fifth_NNI_RTR_Raw[i].split(' ')[-1])

Fifth_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name5) as f:
     for line in f:
         if RE3.search(line):
            Fifth_NNI_RTR_Raw.append(RE3.search(line).group())

Fifth_NNI_RTR_Nats=[]

for i in range(len(Fifth_NNI_RTR_Raw)):
    Fifth_NNI_RTR_Nats.append(Fifth_NNI_RTR_Raw[i])


A_NAT_EUR = []
A_NAT_USA = []
A_NATIVE_EUR = []
A_NATIVE_USA = []
B_NAT_EUR = []
B_NAT_USA = []
B_NATIVE_EUR = []
B_NATIVE_USA = []

with open('Result_' + Host_Name5) as f:
     for line in f:
         if 'ip prefix-list PL-A-NAT-EU' in line:
             A_NAT_EUR.append(line)
         elif 'ip prefix-list PL-A-NAT-USA' in line:
               A_NAT_USA.append(line)
         elif 'ip prefix-list PL-A-NATIVE-EU' in line:
               A_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-A-NATIVE-USA' in line:
               A_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-B-NAT-EU' in line:
               B_NAT_EUR.append(line)
         elif 'ip prefix-list PL-B-NAT-USA' in line:
            B_NAT_USA.append(line)
         elif 'ip prefix-list PL-B-NATIVE-EU' in line:
              B_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-B-NATIVE-USA' in line:
              B_NATIVE_USA.append(line)

Fifth_NNI_RTR_A_NAT_EUR = []
Fifth_NNI_RTR_A_NAT_USA = []
Fifth_NNI_RTR_A_NATIVE_EUR = []
Fifth_NNI_RTR_A_NATIVE_USA = []
Fifth_NNI_RTR_B_NAT_EUR = []
Fifth_NNI_RTR_B_NAT_USA = []
Fifth_NNI_RTR_B_NATIVE_EUR = []
Fifth_NNI_RTR_B_NATIVE_USA = []

for i in range(len(A_NAT_EUR)):
    Fifth_NNI_RTR_A_NAT_EUR.append(A_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NAT_USA)):
    Fifth_NNI_RTR_A_NAT_USA.append(A_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_EUR)):
    Fifth_NNI_RTR_A_NATIVE_EUR.append(A_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_USA)):
    Fifth_NNI_RTR_A_NATIVE_USA.append(A_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_EUR)):
    Fifth_NNI_RTR_B_NAT_EUR.append(B_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_EUR)):
    Fifth_NNI_RTR_B_NATIVE_EUR.append(B_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_USA)):
    Fifth_NNI_RTR_B_NAT_USA.append(B_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_USA)):
    Fifth_NNI_RTR_B_NATIVE_USA.append(B_NATIVE_USA[i].strip('\n').split(' ')[-1])

Fifth_NNI_RTR_A_NAT_EUR_PL = []
Fifth_NNI_RTR_A_NAT_USA_PL = []
Fifth_NNI_RTR_A_NATIVE_EUR_PL = []
Fifth_NNI_RTR_A_NATIVE_USA_PL = []
Fifth_NNI_RTR_B_NAT_EUR_PL = []
Fifth_NNI_RTR_B_NAT_USA_PL = []
Fifth_NNI_RTR_B_NATIVE_EUR_PL = []
Fifth_NNI_RTR_B_NATIVE_USA_PL = []

for line in Fifth_NNI_RTR_A_NAT_EUR:
    if RE4.search(line):
       Fifth_NNI_RTR_A_NAT_EUR_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_A_NAT_USA:
    if RE4.search(line):
       Fifth_NNI_RTR_A_NAT_USA_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_A_NATIVE_EUR:
    if RE4.search(line):
       Fifth_NNI_RTR_A_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_A_NATIVE_USA:
    if RE4.search(line):
       Fifth_NNI_RTR_A_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_B_NAT_EUR:
    if RE4.search(line):
       Fifth_NNI_RTR_B_NAT_EUR_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_B_NAT_USA:
    if RE4.search(line):
       Fifth_NNI_RTR_B_NAT_USA_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_B_NATIVE_EUR:
    if RE4.search(line):
       Fifth_NNI_RTR_B_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_B_NATIVE_USA:
    if RE4.search(line):
       Fifth_NNI_RTR_B_NATIVE_USA_PL.append(RE4.search(line).group())
#========Sixth Target L-A Device===================================================
print('=============Generating The Output Files From XXXX Router===================')
print('\n')

Host_Name6 = 'XXXX'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(Host_Name6, 22, username, password)

remote_session = client.invoke_shell()

output = remote_session.send('\n')
output = remote_session.send('ter len 0\n')
output = remote_session.send('sh ip route bgp\n')
output = remote_session.send('sh ip route static\n')
output = remote_session.send('sh run | i ip nat\n')
output = remote_session.send('sh run | i ip prefix-list\n')

time.sleep(15)

output = remote_session.recv(85535)
#print(output.decode('utf-8'))
client.close()


with open('Result_' + Host_Name6, 'w') as f:
    f.write(output.decode('utf-8'))

RE = re.compile('S\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE1 = re.compile('B\*?\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE3 = re.compile('(\d+\.\d+\.\d+\.\d+\s){2}\/[0-9]{2}')
RE4 = re.compile('(\d+\.\d+\.\d+\.\d+)\/[0-9]{2}')

Sixth_NNI_RTR_Raw=[]
Sixth_NNI_RTR_Static_Routes=[]

with open('Result_' + Host_Name6) as f:
     for line in f:
         if RE.search(line):
            Sixth_NNI_RTR_Raw.append(RE.search(line).group())

for i in range(len(Sixth_NNI_RTR_Raw)):
    Sixth_NNI_RTR_Static_Routes.append(Sixth_NNI_RTR_Raw[i].split(' ')[-1])

#print(Sixth_NNI_RTR_Static_Routes)
Sixth_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name6) as f:
     for line in f:
         if RE1.search(line):
            Sixth_NNI_RTR_Raw.append(RE1.search(line).group())

Sixth_NNI_RTR_BGP_Routes=[]

for i in range(len(Sixth_NNI_RTR_Raw)):
    Sixth_NNI_RTR_BGP_Routes.append(Sixth_NNI_RTR_Raw[i].split(' ')[-1])

Sixth_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name6) as f:
     for line in f:
         if RE3.search(line):
            Sixth_NNI_RTR_Raw.append(RE3.search(line).group())

Sixth_NNI_RTR_Nats=[]

for i in range(len(Sixth_NNI_RTR_Raw)):
    Sixth_NNI_RTR_Nats.append(Sixth_NNI_RTR_Raw[i])


A_NAT_EUR = []
A_NAT_USA = []
A_NATIVE_EUR = []
A_NATIVE_USA = []
B_NAT_EUR = []
B_NAT_USA = []
B_NATIVE_EUR = []
B_NATIVE_USA = []

with open('Result_' + Host_Name6) as f:
     for line in f:
         if 'ip prefix-list PL-A-NAT-EU' in line:
             A_NAT_EUR.append(line)
         elif 'ip prefix-list PL-A-NAT-USA' in line:
               A_NAT_USA.append(line)
         elif 'ip prefix-list PL-A-NATIVE-EU' in line:
               A_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-A-NATIVE-USA' in line:
               A_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-B-NAT-EU' in line:
               B_NAT_EUR.append(line)
         elif 'ip prefix-list PL-B-NAT-USA' in line:
            B_NAT_USA.append(line)
         elif 'ip prefix-list PL-B-NATIVE-EU' in line:
              B_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-B-NATIVE-USA' in line:
              B_NATIVE_USA.append(line)

Sixth_NNI_RTR_A_NAT_EUR = []
Sixth_NNI_RTR_A_NAT_USA = []
Sixth_NNI_RTR_A_NATIVE_EUR = []
Sixth_NNI_RTR_A_NATIVE_USA = []
Sixth_NNI_RTR_B_NAT_EUR = []
Sixth_NNI_RTR_B_NAT_USA = []
Sixth_NNI_RTR_B_NATIVE_EUR = []
Sixth_NNI_RTR_B_NATIVE_USA = []

for i in range(len(A_NAT_EUR)):
    Sixth_NNI_RTR_A_NAT_EUR.append(A_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NAT_USA)):
    Sixth_NNI_RTR_A_NAT_USA.append(A_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_EUR)):
    Sixth_NNI_RTR_A_NATIVE_EUR.append(A_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_USA)):
    Sixth_NNI_RTR_A_NATIVE_USA.append(A_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_EUR)):
    Sixth_NNI_RTR_B_NAT_EUR.append(B_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_EUR)):
    Sixth_NNI_RTR_B_NATIVE_EUR.append(B_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_USA)):
    Sixth_NNI_RTR_B_NAT_USA.append(B_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_USA)):
    Sixth_NNI_RTR_B_NATIVE_USA.append(B_NATIVE_USA[i].strip('\n').split(' ')[-1])

Sixth_NNI_RTR_A_NAT_EUR_PL = []
Sixth_NNI_RTR_A_NAT_USA_PL = []
Sixth_NNI_RTR_A_NATIVE_EUR_PL = []
Sixth_NNI_RTR_A_NATIVE_USA_PL = []
Sixth_NNI_RTR_B_NAT_EUR_PL = []
Sixth_NNI_RTR_B_NAT_USA_PL = []
Sixth_NNI_RTR_B_NATIVE_EUR_PL = []
Sixth_NNI_RTR_B_NATIVE_USA_PL = []

for line in Sixth_NNI_RTR_A_NAT_EUR:
    if RE4.search(line):
       Sixth_NNI_RTR_A_NAT_EUR_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_A_NAT_USA:
    if RE4.search(line):
       Sixth_NNI_RTR_A_NAT_USA_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_A_NATIVE_EUR:
    if RE4.search(line):
       Sixth_NNI_RTR_A_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_A_NATIVE_USA:
    if RE4.search(line):
       Sixth_NNI_RTR_A_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_B_NAT_EUR:
    if RE4.search(line):
       Sixth_NNI_RTR_B_NAT_EUR_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_B_NAT_USA:
    if RE4.search(line):
       Sixth_NNI_RTR_B_NAT_USA_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_B_NATIVE_EUR:
    if RE4.search(line):
       Sixth_NNI_RTR_B_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_B_NATIVE_USA:
    if RE4.search(line):
       Sixth_NNI_RTR_B_NATIVE_USA_PL.append(RE4.search(line).group())
#========Seventh Target L-A Device===================================================
print('=============Generating The Output Files From XXXX Router===================')
print('\n')

Host_Name7 = 'XXXX'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(Host_Name7, 22, username, password)

remote_session = client.invoke_shell()

output = remote_session.send('\n')
output = remote_session.send('ter len 0\n')
output = remote_session.send('sh ip route bgp\n')
output = remote_session.send('sh ip route static\n')
output = remote_session.send('sh run | i ip nat\n')
output = remote_session.send('sh run | i ip prefix-list\n')

time.sleep(15)

output = remote_session.recv(85535)
#print(output.decode('utf-8'))
client.close()


with open('Result_' + Host_Name7, 'w') as f:
    f.write(output.decode('utf-8'))

RE = re.compile('S\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE1 = re.compile('B\*?\s+\d+\.\d+\.\d+\.\d+\/\d+')
RE3 = re.compile('(\d+\.\d+\.\d+\.\d+\s){2}\/[0-9]{2}')
RE4 = re.compile('(\d+\.\d+\.\d+\.\d+)\/[0-9]{2}')

Seventh_NNI_RTR_Raw=[]
Seventh_NNI_RTR_Static_Routes=[]

with open('Result_' + Host_Name7) as f:
     for line in f:
         if RE.search(line):
            Seventh_NNI_RTR_Raw.append(RE.search(line).group())

for i in range(len(Seventh_NNI_RTR_Raw)):
    Seventh_NNI_RTR_Static_Routes.append(Seventh_NNI_RTR_Raw[i].split(' ')[-1])

#print(Seventh_NNI_RTR_Static_Routes)
Seventh_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name7) as f:
     for line in f:
         if RE1.search(line):
            Seventh_NNI_RTR_Raw.append(RE1.search(line).group())

Seventh_NNI_RTR_BGP_Routes=[]

for i in range(len(Seventh_NNI_RTR_Raw)):
    Seventh_NNI_RTR_BGP_Routes.append(Seventh_NNI_RTR_Raw[i].split(' ')[-1])

Seventh_NNI_RTR_Raw.clear()

with open('Result_' + Host_Name7) as f:
     for line in f:
         if RE3.search(line):
            Seventh_NNI_RTR_Raw.append(RE3.search(line).group())

Seventh_NNI_RTR_Nats=[]

for i in range(len(Seventh_NNI_RTR_Raw)):
    Seventh_NNI_RTR_Nats.append(Seventh_NNI_RTR_Raw[i])


A_NAT_EUR = []
A_NAT_USA = []
A_NATIVE_EUR = []
A_NATIVE_USA = []
B_NAT_EUR = []
B_NAT_USA = []
B_NATIVE_EUR = []
B_NATIVE_USA = []

with open('Result_' + Host_Name7) as f:
     for line in f:
         if 'ip prefix-list PL-A-NAT-EU' in line:
             A_NAT_EUR.append(line)
         elif 'ip prefix-list PL-A-NAT-USA' in line:
               A_NAT_USA.append(line)
         elif 'ip prefix-list PL-A-NATIVE-EU' in line:
               A_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-A-NATIVE-USA' in line:
               A_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-B-NAT-EU' in line:
               B_NAT_EUR.append(line)
         elif 'ip prefix-list PL-B-NAT-USA' in line:
            B_NAT_USA.append(line)
         elif 'ip prefix-list PL-B-NATIVE-EU' in line:
              B_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-B-NATIVE-USA' in line:
              B_NATIVE_USA.append(line)

Seventh_NNI_RTR_A_NAT_EUR = []
Seventh_NNI_RTR_A_NAT_USA = []
Seventh_NNI_RTR_A_NATIVE_EUR = []
Seventh_NNI_RTR_A_NATIVE_USA = []
Seventh_NNI_RTR_B_NAT_EUR = []
Seventh_NNI_RTR_B_NAT_USA = []
Seventh_NNI_RTR_B_NATIVE_EUR = []
Seventh_NNI_RTR_B_NATIVE_USA = []

for i in range(len(A_NAT_EUR)):
    Seventh_NNI_RTR_A_NAT_EUR.append(A_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NAT_USA)):
    Seventh_NNI_RTR_A_NAT_USA.append(A_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_EUR)):
    Seventh_NNI_RTR_A_NATIVE_EUR.append(A_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(A_NATIVE_USA)):
    Seventh_NNI_RTR_A_NATIVE_USA.append(A_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_EUR)):
    Seventh_NNI_RTR_B_NAT_EUR.append(B_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_EUR)):
    Seventh_NNI_RTR_B_NATIVE_EUR.append(B_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(B_NAT_USA)):
    Seventh_NNI_RTR_B_NAT_USA.append(B_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(B_NATIVE_USA)):
    Seventh_NNI_RTR_B_NATIVE_USA.append(B_NATIVE_USA[i].strip('\n').split(' ')[-1])

Seventh_NNI_RTR_A_NAT_EUR_PL = []
Seventh_NNI_RTR_A_NAT_USA_PL = []
Seventh_NNI_RTR_A_NATIVE_EUR_PL = []
Seventh_NNI_RTR_A_NATIVE_USA_PL = []
Seventh_NNI_RTR_B_NAT_EUR_PL = []
Seventh_NNI_RTR_B_NAT_USA_PL = []
Seventh_NNI_RTR_B_NATIVE_EUR_PL = []
Seventh_NNI_RTR_B_NATIVE_USA_PL = []

for line in Seventh_NNI_RTR_A_NAT_EUR:
    if RE4.search(line):
       Seventh_NNI_RTR_A_NAT_EUR_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_A_NAT_USA:
    if RE4.search(line):
       Seventh_NNI_RTR_A_NAT_USA_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_A_NATIVE_EUR:
    if RE4.search(line):
       Seventh_NNI_RTR_A_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_A_NATIVE_USA:
    if RE4.search(line):
       Seventh_NNI_RTR_A_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_B_NAT_EUR:
    if RE4.search(line):
       Seventh_NNI_RTR_B_NAT_EUR_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_B_NAT_USA:
    if RE4.search(line):
       Seventh_NNI_RTR_B_NAT_USA_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_B_NATIVE_EUR:
    if RE4.search(line):
       Seventh_NNI_RTR_B_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_B_NATIVE_USA:
    if RE4.search(line):
       Seventh_NNI_RTR_B_NATIVE_USA_PL.append(RE4.search(line).group())
#=========================Comparison of L-A Side NNI Routers=======================================
Missing_BGP_Routes.clear()
Missing_BGP_Routes1.clear()
Missing_BGP_Routes2.clear()
Missing_BGP_Routes3.clear()

print('=====Below output Based on Comparison of L-A Side NNI Routers========================')
print('='*95)
Missing_BGP_Routes=list(set(Forth_NNI_RTR_BGP_Routes).difference(set(Fifth_NNI_RTR_BGP_Routes),set(Sixth_NNI_RTR_BGP_Routes),set(Seventh_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes1=list(set(Fifth_NNI_RTR_BGP_Routes).difference(set(Forth_NNI_RTR_BGP_Routes),set(Sixth_NNI_RTR_BGP_Routes),set(Seventh_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes2=list(set(Sixth_NNI_RTR_BGP_Routes).difference(set(Forth_NNI_RTR_BGP_Routes),set(Fifth_NNI_RTR_BGP_Routes),set(Seventh_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes3=list(set(Seventh_NNI_RTR_BGP_Routes).difference(set(Forth_NNI_RTR_BGP_Routes),set(Fifth_NNI_RTR_BGP_Routes),set(Sixth_NNI_RTR_BGP_Routes)))

if len(Missing_BGP_Routes) == 0 and len(Missing_BGP_Routes1) == 0 and len(Missing_BGP_Routes2) == 0 and len(Missing_BGP_Routes3) == 0:
     print('='*95)
     print('BGP Routes are Same across all L-A NNI Routers!!!')
elif len(Missing_BGP_Routes) > 0:
     print('Missing BGP Routes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & '+ Host_Name7 + ' are below:')
     for i in range(len(Missing_BGP_Routes)):
         print(Missing_BGP_Routes[i])
elif len(Missing_BGP_Routes1) > 0:
     print('Missing BGP Routes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & '+ Host_Name7 + ' are below:')
     for i in range(len(Missing_BGP_Routes1)):
         print(Missing_BGP_Routes1[i])
elif len(Missing_BGP_Routes2) > 0:
     print('Missing BGP Routes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & '+ Host_Name7 + ' are below:')
     for i in range(len(Missing_BGP_Routes2)):
         print(Missing_BGP_Routes2[i])
elif len(Missing_BGP_Routes3) > 0:
     print('Missing BGP Routes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & '+ Host_Name6 + ' are below:')
     for i in range(len(Missing_BGP_Routes3)):
         print(Missing_BGP_Routes3[i])

##Below output will display BGP Route Count on L-A NNI Routers
print('\n'*1)
print('Below output will display BGP Route Count on all L-A NNI Routers:')
print('='*95)
print("On " + Host_Name4 + " total no of BGP routes are :{}".format(len(Forth_NNI_RTR_BGP_Routes)))
print("On " + Host_Name5 + " total no of BGP routes are :{}".format(len(Fifth_NNI_RTR_BGP_Routes)))
print("On " + Host_Name6 + " total no of BGP routes are :{}".format(len(Sixth_NNI_RTR_BGP_Routes)))
print("On " + Host_Name7 + " total no of BGP routes are :{}".format(len(Seventh_NNI_RTR_BGP_Routes)))
print('='*95)
#===============================================================================
Missing_Static_Routes.clear()
Missing_Static_Routes1.clear()
Missing_Static_Routes2.clear()
Missing_Static_Routes3.clear()

Missing_Static_Routes=list(set(Forth_NNI_RTR_Static_Routes).difference(set(Fifth_NNI_RTR_Static_Routes),set(Sixth_NNI_RTR_Static_Routes),set(Seventh_NNI_RTR_Static_Routes)))
Missing_Static_Routes1=list(set(Fifth_NNI_RTR_Static_Routes).difference(set(Forth_NNI_RTR_Static_Routes),set(Sixth_NNI_RTR_Static_Routes),set(Seventh_NNI_RTR_Static_Routes)))
Missing_Static_Routes2=list(set(Sixth_NNI_RTR_Static_Routes).difference(set(Forth_NNI_RTR_Static_Routes),set(Fifth_NNI_RTR_Static_Routes),set(Seventh_NNI_RTR_Static_Routes)))
Missing_Static_Routes3=list(set(Seventh_NNI_RTR_Static_Routes).difference(set(Forth_NNI_RTR_Static_Routes),set(Fifth_NNI_RTR_Static_Routes),set(Sixth_NNI_RTR_Static_Routes)))

if len(Missing_Static_Routes) == 0 and len(Missing_Static_Routes1) == 0 and len(Missing_Static_Routes2) == 0 and len(Missing_Static_Routes3) == 0:
     print('='*95)
     print('Static Routes are Same across all L-A NNI Routers!!!')
elif len(Missing_Static_Routes) > 0:
     print('Missing Static Routes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Static_Routes)):
         print(Missing_Static_Routes[i])
elif len(Missing_Static_Routes1) > 0:
     print('Missing Static Routes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Static_Routes1)):
         print(Missing_Static_Routes1[i])
elif len(Missing_Static_Routes2) > 0:
     print('Missing Static Routes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Static_Routes2)):
         print(Missing_Static_Routes2[i])
elif len(Missing_Static_Routes3) > 0:
     print('Missing Static Routes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_Static_Routes3)):
         print(Missing_Static_Routes3[i])

##Below output will display Static Route Count on L-A NNI Routers
print('\n'*1)
print('Below output will display Static Route Count on all L-A NNI Routers:')
print('='*95)
print("On " + Host_Name4 + " total no of Static routes are :{}".format(len(Forth_NNI_RTR_Static_Routes)))
print("On " + Host_Name5 + " total no of Static routes are :{}".format(len(Fifth_NNI_RTR_Static_Routes)))
print("On " + Host_Name6 + " total no of Static routes are :{}".format(len(Sixth_NNI_RTR_Static_Routes)))
print("On " + Host_Name7 + " total no of Static routes are :{}".format(len(Seventh_NNI_RTR_Static_Routes)))
print('='*95)
#===============================================================================
Missing_Nats.clear()
Missing_Nats1.clear()
Missing_Nats2.clear()
Missing_Nats3.clear()


Missing_Nats=list(set(Forth_NNI_RTR_Nats).difference(set(Fifth_NNI_RTR_Nats),set(Sixth_NNI_RTR_Nats),set(Seventh_NNI_RTR_Nats)))
Missing_Nats1=list(set(Fifth_NNI_RTR_Nats).difference(set(Forth_NNI_RTR_Nats),set(Sixth_NNI_RTR_Nats),set(Sixth_NNI_RTR_Nats)))
Missing_Nats2=list(set(Sixth_NNI_RTR_Nats).difference(set(Forth_NNI_RTR_Nats),set(Fifth_NNI_RTR_Nats),set(Sixth_NNI_RTR_Nats)))
Missing_Nats3=list(set(Seventh_NNI_RTR_Nats).difference(set(Forth_NNI_RTR_Nats),set(Fifth_NNI_RTR_Nats),set(Sixth_NNI_RTR_Nats)))

if len(Missing_Nats) == 0 and len(Missing_Nats1) == 0 and len(Missing_Nats2) == 0 and len(Missing_Nats3) == 0:
     print('='*95)
     print('Static Nats are Same across all L-A NNI Routers!!!')
elif len(Missing_Nats) > 0:
     print('Missing Static Nats of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Nats)):
         print(Missing_Nats[i])
elif len(Missing_Nats1) > 0:
     print('Missing Static Nats of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Nats1)):
         print(Missing_Nats1[i])
elif len(Missing_Nats2) > 0:
     print('Missing Static Nats of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Nats2)):
         print(Missing_Nats2[i])
elif len(Missing_Nats3) > 0:
     print('Missing Static Nats of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_Nats3)):
         print(Missing_Nats3[i])

##Below output will display Static Nats Count on L-A NNI Routers
print('\n'*1)
print('Below output will display Static Nats Count on all L-A NNI Routers:')
print('='*95)
print("On " + Host_Name + " total no of Static Nats are :{}".format(len(Forth_NNI_RTR_Nats)))
print("On " + Host_Name5 + " total no of Static Nats are :{}".format(len(Fifth_NNI_RTR_Nats)))
print("On " + Host_Name6 + " total no of Static Nats are :{}".format(len(Sixth_NNI_RTR_Nats)))
print("On " + Host_Name7 + " total no of Static Nats are :{}".format(len(Seventh_NNI_RTR_Nats)))
print('='*95)

#===============================================================================
Missing_A_NAT_EUR.clear()
Missing_A_NAT_EUR1.clear()
Missing_A_NAT_EUR2.clear()
Missing_A_NAT_EUR3.clear()

Missing_A_NAT_USA.clear()
Missing_A_NAT_USA1.clear()
Missing_A_NAT_USA2.clear()
Missing_A_NAT_USA3.clear()

Missing_A_NATIVE_EUR.clear()
Missing_A_NATIVE_EUR1.clear()
Missing_A_NATIVE_EUR2.clear()
Missing_A_NATIVE_EUR3.clear()

Missing_A_NATIVE_USA.clear()
Missing_A_NATIVE_USA1.clear()
Missing_A_NATIVE_USA2.clear()
Missing_A_NATIVE_USA3.clear()

Missing_B_NAT_EUR.clear()
Missing_B_NAT_EUR1.clear()
Missing_B_NAT_EUR2.clear()
Missing_B_NAT_EUR3.clear()

Missing_B_NAT_USA.clear()
Missing_B_NAT_USA1.clear()
Missing_B_NAT_USA2.clear()
Missing_B_NAT_USA3.clear()

Missing_B_NATIVE_EUR.clear()
Missing_B_NATIVE_EUR1.clear()
Missing_B_NATIVE_EUR2.clear()
Missing_B_NATIVE_EUR3.clear()

Missing_B_NATIVE_USA.clear()
Missing_B_NATIVE_USA1.clear()
Missing_B_NATIVE_USA2.clear()
Missing_B_NATIVE_USA3.clear()


Missing_A_NAT_EUR=list(set(Forth_NNI_RTR_A_NAT_EUR_PL).difference(set(Fifth_NNI_RTR_A_NAT_EUR_PL),set(Sixth_NNI_RTR_A_NAT_EUR_PL),set(Seventh_NNI_RTR_A_NAT_EUR_PL)))
Missing_A_NAT_EUR1=list(set(Fifth_NNI_RTR_A_NAT_EUR_PL).difference(set(Forth_NNI_RTR_A_NAT_EUR_PL),set(Sixth_NNI_RTR_A_NAT_EUR_PL),set(Seventh_NNI_RTR_A_NAT_EUR_PL)))
Missing_A_NAT_EUR2=list(set(Sixth_NNI_RTR_A_NAT_EUR_PL).difference(set(Forth_NNI_RTR_A_NAT_EUR_PL),set(Fifth_NNI_RTR_A_NAT_EUR_PL),set(Seventh_NNI_RTR_A_NAT_EUR_PL)))
Missing_A_NAT_EUR3=list(set(Seventh_NNI_RTR_A_NAT_EUR_PL).difference(set(Forth_NNI_RTR_A_NAT_EUR_PL),set(Fifth_NNI_RTR_A_NAT_EUR_PL),set(Sixth_NNI_RTR_A_NAT_EUR_PL)))

Missing_A_NAT_USA=list(set(Forth_NNI_RTR_A_NAT_USA_PL).difference(set(Fifth_NNI_RTR_A_NAT_USA_PL),set(Sixth_NNI_RTR_A_NAT_USA_PL),set(Seventh_NNI_RTR_A_NAT_USA_PL)))
Missing_A_NAT_USA1=list(set(Fifth_NNI_RTR_A_NAT_USA_PL).difference(set(Forth_NNI_RTR_A_NAT_USA_PL),set(Sixth_NNI_RTR_A_NAT_USA_PL),set(Seventh_NNI_RTR_A_NAT_USA_PL)))
Missing_A_NAT_USA2=list(set(Sixth_NNI_RTR_A_NAT_USA_PL).difference(set(Forth_NNI_RTR_A_NAT_USA_PL),set(Fifth_NNI_RTR_A_NAT_USA_PL),set(Seventh_NNI_RTR_A_NAT_USA_PL)))
Missing_A_NAT_USA3=list(set(Seventh_NNI_RTR_A_NAT_USA_PL).difference(set(Forth_NNI_RTR_A_NAT_USA_PL),set(Fifth_NNI_RTR_A_NAT_USA_PL),set(Sixth_NNI_RTR_A_NAT_USA_PL)))

Missing_A_NATIVE_EUR=list(set(Forth_NNI_RTR_A_NATIVE_EUR_PL).difference(set(Fifth_NNI_RTR_A_NATIVE_EUR_PL),set(Sixth_NNI_RTR_A_NATIVE_EUR_PL),set(Seventh_NNI_RTR_A_NATIVE_EUR_PL)))
Missing_A_NATIVE_EUR1=list(set(Fifth_NNI_RTR_A_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_A_NATIVE_EUR_PL),set(Sixth_NNI_RTR_A_NATIVE_EUR_PL),set(Seventh_NNI_RTR_A_NATIVE_EUR_PL)))
Missing_A_NATIVE_EUR2=list(set(Sixth_NNI_RTR_A_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_A_NATIVE_EUR_PL),set(Fifth_NNI_RTR_A_NATIVE_EUR_PL),set(Seventh_NNI_RTR_A_NATIVE_EUR_PL)))
Missing_A_NATIVE_EUR3=list(set(Seventh_NNI_RTR_A_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_A_NATIVE_EUR_PL),set(Fifth_NNI_RTR_A_NATIVE_EUR_PL),set(Sixth_NNI_RTR_A_NATIVE_EUR_PL)))

Missing_A_NATIVE_USA=list(set(Forth_NNI_RTR_A_NATIVE_USA_PL).difference(set(Fifth_NNI_RTR_A_NATIVE_USA_PL),set(Sixth_NNI_RTR_A_NATIVE_USA_PL),set(Seventh_NNI_RTR_A_NATIVE_USA_PL)))
Missing_A_NATIVE_USA1=list(set(Fifth_NNI_RTR_A_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_A_NATIVE_USA_PL),set(Sixth_NNI_RTR_A_NATIVE_USA_PL),set(Seventh_NNI_RTR_A_NATIVE_USA_PL)))
Missing_A_NATIVE_USA2=list(set(Sixth_NNI_RTR_A_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_A_NATIVE_USA_PL),set(Fifth_NNI_RTR_A_NATIVE_USA_PL),set(Seventh_NNI_RTR_A_NATIVE_USA_PL)))
Missing_A_NATIVE_USA3=list(set(Seventh_NNI_RTR_A_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_A_NATIVE_USA_PL),set(Fifth_NNI_RTR_A_NATIVE_USA_PL),set(Sixth_NNI_RTR_A_NATIVE_USA_PL)))

Missing_B_NAT_EUR=list(set(Forth_NNI_RTR_B_NAT_EUR_PL).difference(set(Fifth_NNI_RTR_B_NAT_EUR_PL),set(Sixth_NNI_RTR_B_NAT_EUR_PL),set(Seventh_NNI_RTR_B_NAT_EUR_PL)))
Missing_B_NAT_EUR1=list(set(Fifth_NNI_RTR_B_NAT_EUR_PL).difference(set(Forth_NNI_RTR_B_NAT_EUR_PL),set(Sixth_NNI_RTR_B_NAT_EUR_PL),set(Seventh_NNI_RTR_B_NAT_EUR_PL)))
Missing_B_NAT_EUR2=list(set(Sixth_NNI_RTR_B_NAT_EUR_PL).difference(set(Forth_NNI_RTR_B_NAT_EUR_PL),set(Fifth_NNI_RTR_B_NAT_EUR_PL),set(Seventh_NNI_RTR_B_NAT_EUR_PL)))
Missing_B_NAT_EUR3=list(set(Seventh_NNI_RTR_B_NAT_EUR_PL).difference(set(Forth_NNI_RTR_B_NAT_EUR_PL),set(Fifth_NNI_RTR_B_NAT_EUR_PL),set(Sixth_NNI_RTR_B_NAT_EUR_PL)))

Missing_B_NAT_USA=list(set(Forth_NNI_RTR_B_NAT_USA_PL).difference(set(Fifth_NNI_RTR_B_NAT_USA_PL),set(Sixth_NNI_RTR_B_NAT_USA_PL),set(Seventh_NNI_RTR_B_NAT_USA_PL)))
Missing_B_NAT_USA1=list(set(Fifth_NNI_RTR_B_NAT_USA_PL).difference(set(Forth_NNI_RTR_B_NAT_USA_PL),set(Sixth_NNI_RTR_B_NAT_USA_PL),set(Seventh_NNI_RTR_B_NAT_USA_PL)))
Missing_B_NAT_USA2=list(set(Sixth_NNI_RTR_B_NAT_USA_PL).difference(set(Forth_NNI_RTR_B_NAT_USA_PL),set(Fifth_NNI_RTR_B_NAT_USA_PL),set(Seventh_NNI_RTR_B_NAT_USA_PL)))
Missing_B_NAT_USA3=list(set(Seventh_NNI_RTR_B_NAT_USA_PL).difference(set(Forth_NNI_RTR_B_NAT_USA_PL),set(Fifth_NNI_RTR_B_NAT_USA_PL),set(Sixth_NNI_RTR_B_NAT_USA_PL)))

Missing_B_NATIVE_EUR=list(set(Forth_NNI_RTR_B_NATIVE_EUR_PL).difference(set(Fifth_NNI_RTR_B_NATIVE_EUR_PL),set(Sixth_NNI_RTR_B_NATIVE_EUR_PL),set(Seventh_NNI_RTR_B_NATIVE_EUR_PL)))
Missing_B_NATIVE_EUR1=list(set(Fifth_NNI_RTR_B_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_B_NATIVE_EUR_PL),set(Sixth_NNI_RTR_B_NATIVE_EUR_PL),set(Seventh_NNI_RTR_B_NATIVE_EUR_PL)))
Missing_B_NATIVE_EUR2=list(set(Sixth_NNI_RTR_B_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_B_NATIVE_EUR_PL),set(Fifth_NNI_RTR_B_NATIVE_EUR_PL),set(Seventh_NNI_RTR_B_NATIVE_EUR_PL)))
Missing_B_NATIVE_EUR3=list(set(Seventh_NNI_RTR_B_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_B_NATIVE_EUR_PL),set(Fifth_NNI_RTR_B_NATIVE_EUR_PL),set(Sixth_NNI_RTR_B_NATIVE_EUR_PL)))

Missing_B_NATIVE_USA=list(set(Forth_NNI_RTR_B_NATIVE_USA_PL).difference(set(Fifth_NNI_RTR_B_NATIVE_USA_PL),set(Sixth_NNI_RTR_B_NATIVE_USA_PL),set(Seventh_NNI_RTR_B_NATIVE_USA_PL)))
Missing_B_NATIVE_USA1=list(set(Fifth_NNI_RTR_B_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_B_NATIVE_USA_PL),set(Sixth_NNI_RTR_B_NATIVE_USA_PL),set(Seventh_NNI_RTR_B_NATIVE_USA_PL)))
Missing_B_NATIVE_USA2=list(set(Sixth_NNI_RTR_B_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_B_NATIVE_USA_PL),set(Fifth_NNI_RTR_B_NATIVE_USA_PL),set(Seventh_NNI_RTR_B_NATIVE_USA_PL)))
Missing_B_NATIVE_USA3=list(set(Seventh_NNI_RTR_B_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_B_NATIVE_USA_PL),set(Fifth_NNI_RTR_B_NATIVE_USA_PL),set(Sixth_NNI_RTR_B_NATIVE_USA_PL)))

print('='*90)

if len(Missing_A_NAT_EUR) == 0 and len(Missing_A_NAT_EUR1) == 0 and len(Missing_A_NAT_EUR2) == 0 and len(Missing_A_NAT_EUR3) == 0:
     print('='*95)
     print('L-A NATTED Prefixes Of EU Region are Same across all L-A NNI Routers!!!')
elif len(Missing_A_NAT_EUR) > 0:
     print('Missing L-A EU Region NATTED Prefixes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NAT_EUR)):
         print(Missing_A_NAT_EUR[i])
elif len(Missing_A_NAT_EUR1) > 0:
     print('Missing L-A EU Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NAT_EUR1)):
         print(Missing_A_NAT_EUR1[i])
elif len(Missing_A_NAT_EUR2) > 0:
     print('Missing L-A EU Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NAT_EUR2)):
         print(Missing_A_NAT_EUR2[i])
elif len(Missing_A_NAT_EUR3) > 0:
     print('Missing L-A EU Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_A_NAT_EUR3)):
         print(Missing_A_NAT_EUR3[i])

if len(Missing_A_NAT_USA) == 0 and len(Missing_A_NAT_USA1) == 0 and len(Missing_A_NAT_USA2) == 0 and len(Missing_A_NAT_USA3) == 0:
     print('='*95)
     print('L-A NATTED Prefixes Of US Region are Same across all L-A NNI Routers!!!')
elif len(Missing_A_NAT_USA) > 0:
     print('Missing L-A US Region NATTED Prefixes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NAT_USA)):
         print(Missing_A_NAT_USA[i])
elif len(Missing_A_NAT_USA1) > 0:
     print('Missing L-A US Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NAT_USA1)):
         print(Missing_A_NAT_USA1[i])
elif len(Missing_A_NAT_USA2) > 0:
     print('Missing L-A US Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NAT_USA2)):
         print(Missing_A_NAT_USA2[i])
elif len(Missing_A_NAT_USA3) > 0:
     print('Missing L-A US Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_A_NAT_USA3)):
         print(Missing_A_NAT_USA3[i])

print('\n'*1)

if len(Missing_A_NATIVE_EUR) == 0 and len(Missing_A_NATIVE_EUR1) == 0 and len(Missing_A_NATIVE_EUR2) == 0 and len(Missing_A_NATIVE_EUR3) == 0:
     print('='*95)
     print('L-A NATIVE Prefixes Of EU Region are Same across all L-A NNI Routers!!!')
elif len(Missing_A_NATIVE_EUR) > 0:
     print('Missing L-A EU Region NATIVE Prefixes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NATIVE_EUR)):
         print(Missing_A_NATIVE_EUR[i])
elif len(Missing_A_NATIVE_EUR1) > 0:
     print('Missing L-A EU Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NATIVE_EUR1)):
         print(Missing_A_NATIVE_EUR1[i])
elif len(Missing_A_NATIVE_EUR2) > 0:
     print('Missing L-A EU Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NATIVE_EUR2)):
         print(Missing_A_NATIVE_EUR2[i])
elif len(Missing_A_NATIVE_EUR3) > 0:
     print('Missing L-A EU Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_A_NATIVE_EUR3)):
         print(Missing_A_NATIVE_EUR3[i])

if len(Missing_A_NATIVE_USA) == 0 and len(Missing_A_NATIVE_USA1) == 0 and len(Missing_A_NATIVE_USA2) == 0 and len(Missing_A_NATIVE_USA3) == 0:
     print('='*95)
     print('L-A NATIVE Prefixes Of US Region are Same across all L-A NNI Routers!!!')
elif len(Missing_A_NATIVE_USA) > 0:
     print('Missing L-A US Region NATIVE Prefixes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NATIVE_USA)):
         print(Missing_A_NATIVE_USA[i])
elif len(Missing_A_NATIVE_USA1) > 0:
     print('Missing L-A US Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NATIVE_USA1)):
         print(Missing_A_NATIVE_USA1[i])
elif len(Missing_A_NATIVE_USA2) > 0:
     print('Missing L-A US Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_A_NATIVE_USA2)):
         print(Missing_A_NATIVE_USA2[i])
elif len(Missing_A_NATIVE_USA3) > 0:
     print('Missing L-A US Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_A_NATIVE_USA3)):
         print(Missing_A_NATIVE_USA3[i])

print('\n'*1)

if len(Missing_B_NAT_EUR) == 0 and len(Missing_B_NAT_EUR1) == 0 and len(Missing_B_NAT_EUR2) == 0 and len(Missing_B_NAT_EUR3) == 0:
     print('='*95)
     print('B NATTED Prefixes Of EU Region are Same across all L-A NNI Routers!!!')
elif len(Missing_B_NAT_EUR) > 0:
     print('Missing B EU Region NATTED Prefixes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NAT_EUR)):
         print(Missing_B_NAT_EUR[i])
elif len(Missing_B_NAT_EUR1) > 0:
     print('Missing B EU Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_L-A_NAT_EUR1)):
         print(Missing_B_NAT_EUR1[i])
elif len(Missing_B_NAT_EUR2) > 0:
     print('Missing B EU Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NAT_EUR2)):
         print(Missing_B_NAT_EUR2[i])
elif len(Missing_B_NAT_EUR3) > 0:
     print('Missing B EU Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_B_NAT_EUR3)):
         print(Missing_B_NAT_EUR3[i])


if len(Missing_B_NAT_USA) == 0 and len(Missing_B_NAT_USA1) == 0 and len(Missing_B_NAT_USA2) == 0 and len(Missing_B_NAT_USA3) == 0:
     print('='*95)
     print('B NATTED Prefixes Of US Region are Same across all B NNI Routers!!!')
elif len(Missing_B_NAT_USA) > 0:
     print('Missing B US Region NATTED Prefixes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NAT_USA)):
         print(Missing_B_NAT_USA[i])
elif len(Missing_B_NAT_USA1) > 0:
     print('Missing B US Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NAT_USA1)):
         print(Missing_B_NAT_USA1[i])
elif len(Missing_B_NAT_USA2) > 0:
     print('Missing B US Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NAT_USA2)):
         print(Missing_B_NAT_USA2[i])
elif len(Missing_B_NAT_USA3) > 0:
     print('Missing B US Region NATTED Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_B_NAT_USA3)):
         print(Missing_B_NAT_USA3[i])

print('\n'*1)

if len(Missing_B_NATIVE_EUR) == 0 and len(Missing_B_NATIVE_EUR1) == 0 and len(Missing_B_NATIVE_EUR2) == 0 and len(Missing_B_NATIVE_EUR3) == 0:
     print('='*95)
     print('B NATIVE Prefixes Of EU Region are Same across all B NNI Routers!!!')
elif len(Missing_B_NATIVE_EUR) > 0:
     print('Missing B EU Region NATIVE Prefixes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NATIVE_EUR)):
         print(Missing_B_NATIVE_EUR[i])
elif len(Missing_B_NATIVE_EUR1) > 0:
     print('Missing B EU Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NATIVE_EUR1)):
         print(Missing_B_NATIVE_EUR1[i])
elif len(Missing_B_NATIVE_EUR2) > 0:
     print('Missing B EU Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NATIVE_EUR2)):
         print(Missing_B_NATIVE_EUR2[i])
elif len(Missing_B_NATIVE_EUR3) > 0:
     print('Missing B EU Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_B_NATIVE_EUR3)):
         print(Missing_B_NATIVE_EUR3[i])
print('='*90)

if len(Missing_B_NATIVE_USA) == 0 and len(Missing_B_NATIVE_USA1) == 0 and len(Missing_B_NATIVE_USA2) == 0 and len(Missing_B_NATIVE_USA3) == 0:
     print('='*95)
     print('B NATIVE Prefixes Of US Region are Same across all B NNI Routers!!!')
elif len(Missing_B_NATIVE_USA) > 0:
     print('Missing B US Region NATIVE Prefixes of XXXX in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NATIVE_USA)):
         print(Missing_B_NATIVE_USA[i])
elif len(Missing_B_NATIVE_USA1) > 0:
     print('Missing B US Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NATIVE_USA1)):
         print(Missing_B_NATIVE_USA1[i])
elif len(Missing_B_NATIVE_USA2) > 0:
     print('Missing B US Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_B_NATIVE_USA2)):
         print(Missing_B_NATIVE_USA2[i])
elif len(Missing_B_NATIVE_USA3) > 0:
     print('Missing B US Region NATIVE Prefixes of XXXX in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_B_NATIVE_USA3)):
         print(Missing_B_NATIVE_USA3[i])

print('='*90)
