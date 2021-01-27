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
####################################################################################################################
#!/usr/bin/env python3
import re
import paramiko
import time
import getpass
from os import system

system('clear')
Host_Name = 'UK-LON10-NNI01'
username = input('Enter Your Username to Login IHSM NNI Routers: ')
password = getpass.getpass()
print('=============Generating The Output Files From UK-LON10-NNI01 Router===================')
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


IHS_NAT_EUR = []
IHS_NAT_USA = []
IHS_NATIVE_EUR = []
IHS_NATIVE_USA = []
MARKIT_NAT_EUR = []
MARKIT_NAT_USA = []
MARKIT_NATIVE_EUR = []
MARKIT_NATIVE_USA = []

with open('Result_' + Host_Name) as f:
     for line in f:
         if 'ip prefix-list PL-IHS-NAT-EU' in line:
             IHS_NAT_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NAT-USA' in line:
               IHS_NAT_USA.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-EU' in line:
               IHS_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-USA' in line:
               IHS_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-EU' in line:
               MARKIT_NAT_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-USA' in line:
            MARKIT_NAT_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-EU' in line:
              MARKIT_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-USA' in line:
              MARKIT_NATIVE_USA.append(line)

Pre_NNI_RTR_IHS_NAT_EUR = []
Pre_NNI_RTR_IHS_NAT_USA = []
Pre_NNI_RTR_IHS_NATIVE_EUR = []
Pre_NNI_RTR_IHS_NATIVE_USA = []
Pre_NNI_RTR_MARKIT_NAT_EUR = []
Pre_NNI_RTR_MARKIT_NAT_USA = []
Pre_NNI_RTR_MARKIT_NATIVE_EUR = []
Pre_NNI_RTR_MARKIT_NATIVE_USA = []

for i in range(len(IHS_NAT_EUR)):
    Pre_NNI_RTR_IHS_NAT_EUR.append(IHS_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NAT_USA)):
    Pre_NNI_RTR_IHS_NAT_USA.append(IHS_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_EUR)):
    Pre_NNI_RTR_IHS_NATIVE_EUR.append(IHS_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_USA)):
    Pre_NNI_RTR_IHS_NATIVE_USA.append(IHS_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_EUR)):
    Pre_NNI_RTR_MARKIT_NAT_EUR.append(MARKIT_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_EUR)):
    Pre_NNI_RTR_MARKIT_NATIVE_EUR.append(MARKIT_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_USA)):
    Pre_NNI_RTR_MARKIT_NAT_USA.append(MARKIT_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_USA)):
    Pre_NNI_RTR_MARKIT_NATIVE_USA.append(MARKIT_NATIVE_USA[i].strip('\n').split(' ')[-1])

Pre_NNI_RTR_IHS_NAT_EUR_PL = []
Pre_NNI_RTR_IHS_NAT_USA_PL = []
Pre_NNI_RTR_IHS_NATIVE_EUR_PL = []
Pre_NNI_RTR_IHS_NATIVE_USA_PL = []
Pre_NNI_RTR_MARKIT_NAT_EUR_PL = []
Pre_NNI_RTR_MARKIT_NAT_USA_PL = []
Pre_NNI_RTR_MARKIT_NATIVE_EUR_PL = []
Pre_NNI_RTR_MARKIT_NATIVE_USA_PL = []

for line in Pre_NNI_RTR_IHS_NAT_EUR:
    if RE4.search(line):
       Pre_NNI_RTR_IHS_NAT_EUR_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_IHS_NAT_USA:
    if RE4.search(line):
       Pre_NNI_RTR_IHS_NAT_USA_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_IHS_NATIVE_EUR:
    if RE4.search(line):
       Pre_NNI_RTR_IHS_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_IHS_NATIVE_USA:
    if RE4.search(line):
       Pre_NNI_RTR_IHS_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_MARKIT_NAT_EUR:
    if RE4.search(line):
       Pre_NNI_RTR_MARKIT_NAT_EUR_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_MARKIT_NAT_USA:
    if RE4.search(line):
       Pre_NNI_RTR_MARKIT_NAT_USA_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_MARKIT_NATIVE_EUR:
    if RE4.search(line):
       Pre_NNI_RTR_MARKIT_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Pre_NNI_RTR_MARKIT_NATIVE_USA:
    if RE4.search(line):
       Pre_NNI_RTR_MARKIT_NATIVE_USA_PL.append(RE4.search(line).group())

#=========First Target Device===================================================
print('=============Generating The Output Files From UK-LON11-NNI01 Router===================')
print('\n')
Host_Name1  = 'UK-LON11-NNI01'
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

IHS_NAT_EUR.clear()
IHS_NAT_USA.clear()
IHS_NATIVE_EUR.clear()
IHS_NATIVE_USA.clear()
MARKIT_NAT_EUR.clear()
MARKIT_NAT_USA.clear()
MARKIT_NATIVE_EUR.clear()
MARKIT_NATIVE_USA.clear()

with open('Result_' + Host_Name1) as f:
     for line in f:
         if 'ip prefix-list PL-IHS-NAT-EU' in line:
             IHS_NAT_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NAT-USA' in line:
               IHS_NAT_USA.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-EU' in line:
               IHS_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-USA' in line:
               IHS_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-EU' in line:
               MARKIT_NAT_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-USA' in line:
            MARKIT_NAT_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-EU' in line:
              MARKIT_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-USA' in line:
              MARKIT_NATIVE_USA.append(line)

New_NNI_RTR_IHS_NAT_EUR = []
New_NNI_RTR_IHS_NAT_USA = []
New_NNI_RTR_IHS_NATIVE_EUR = []
New_NNI_RTR_IHS_NATIVE_USA = []
New_NNI_RTR_MARKIT_NAT_EUR = []
New_NNI_RTR_MARKIT_NAT_USA = []
New_NNI_RTR_MARKIT_NATIVE_EUR = []
New_NNI_RTR_MARKIT_NATIVE_USA = []

for i in range(len(IHS_NAT_EUR)):
    New_NNI_RTR_IHS_NAT_EUR.append(IHS_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NAT_USA)):
    New_NNI_RTR_IHS_NAT_USA.append(IHS_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_EUR)):
    New_NNI_RTR_IHS_NATIVE_EUR.append(IHS_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_USA)):
    New_NNI_RTR_IHS_NATIVE_USA.append(IHS_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_EUR)):
    New_NNI_RTR_MARKIT_NAT_EUR.append(MARKIT_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_EUR)):
    New_NNI_RTR_MARKIT_NATIVE_EUR.append(MARKIT_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_USA)):
    New_NNI_RTR_MARKIT_NAT_USA.append(MARKIT_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_USA)):
    New_NNI_RTR_MARKIT_NATIVE_USA.append(MARKIT_NATIVE_USA[i].strip('\n').split(' ')[-1])

New_NNI_RTR_IHS_NAT_EUR_PL = []
New_NNI_RTR_IHS_NAT_USA_PL = []
New_NNI_RTR_IHS_NATIVE_EUR_PL = []
New_NNI_RTR_IHS_NATIVE_USA_PL = []
New_NNI_RTR_MARKIT_NAT_EUR_PL = []
New_NNI_RTR_MARKIT_NAT_USA_PL = []
New_NNI_RTR_MARKIT_NATIVE_EUR_PL = []
New_NNI_RTR_MARKIT_NATIVE_USA_PL = []

for line in New_NNI_RTR_IHS_NAT_EUR:
    if RE4.search(line):
       New_NNI_RTR_IHS_NAT_EUR_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_IHS_NAT_USA:
    if RE4.search(line):
       New_NNI_RTR_IHS_NAT_USA_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_IHS_NATIVE_EUR:
    if RE4.search(line):
       New_NNI_RTR_IHS_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_IHS_NATIVE_USA:
    if RE4.search(line):
       New_NNI_RTR_IHS_NATIVE_USA_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_MARKIT_NAT_EUR:
    if RE4.search(line):
       New_NNI_RTR_MARKIT_NAT_EUR_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_MARKIT_NAT_USA:
    if RE4.search(line):
       New_NNI_RTR_MARKIT_NAT_USA_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_MARKIT_NATIVE_EUR:
    if RE4.search(line):
       New_NNI_RTR_MARKIT_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in New_NNI_RTR_MARKIT_NATIVE_USA:
    if RE4.search(line):
       New_NNI_RTR_MARKIT_NATIVE_USA_PL.append(RE4.search(line).group())
#========Second Target Device===================================================
print('=============Generating The Output Files From US-RIC01-NNI01 Router===================')
print('\n')

Host_Name2  = 'US-RIC01-NNI01'
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

IHS_NAT_EUR.clear()
IHS_NAT_USA.clear()
IHS_NATIVE_EUR.clear()
IHS_NATIVE_USA.clear()
MARKIT_NAT_EUR.clear()
MARKIT_NAT_USA.clear()
MARKIT_NATIVE_EUR.clear()
MARKIT_NATIVE_USA.clear()

with open('Result_' + Host_Name2) as f:
     for line in f:
         if 'ip prefix-list PL-IHS-NAT-EU' in line:
             IHS_NAT_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NAT-USA' in line:
               IHS_NAT_USA.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-EU' in line:
               IHS_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-USA' in line:
               IHS_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-EU' in line:
               MARKIT_NAT_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-USA' in line:
            MARKIT_NAT_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-EU' in line:
              MARKIT_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-USA' in line:
              MARKIT_NATIVE_USA.append(line)

Sec_NNI_RTR_IHS_NAT_EUR = []
Sec_NNI_RTR_IHS_NAT_USA = []
Sec_NNI_RTR_IHS_NATIVE_EUR = []
Sec_NNI_RTR_IHS_NATIVE_USA = []
Sec_NNI_RTR_MARKIT_NAT_EUR = []
Sec_NNI_RTR_MARKIT_NAT_USA = []
Sec_NNI_RTR_MARKIT_NATIVE_EUR = []
Sec_NNI_RTR_MARKIT_NATIVE_USA = []

for i in range(len(IHS_NAT_EUR)):
    Sec_NNI_RTR_IHS_NAT_EUR.append(IHS_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NAT_USA)):
    Sec_NNI_RTR_IHS_NAT_USA.append(IHS_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_EUR)):
    Sec_NNI_RTR_IHS_NATIVE_EUR.append(IHS_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_USA)):
    Sec_NNI_RTR_IHS_NATIVE_USA.append(IHS_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_EUR)):
    Sec_NNI_RTR_MARKIT_NAT_EUR.append(MARKIT_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_EUR)):
    Sec_NNI_RTR_MARKIT_NATIVE_EUR.append(MARKIT_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_USA)):
    Sec_NNI_RTR_MARKIT_NAT_USA.append(MARKIT_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_USA)):
    Sec_NNI_RTR_MARKIT_NATIVE_USA.append(MARKIT_NATIVE_USA[i].strip('\n').split(' ')[-1])

Sec_NNI_RTR_IHS_NAT_EUR_PL = []
Sec_NNI_RTR_IHS_NAT_USA_PL = []
Sec_NNI_RTR_IHS_NATIVE_EUR_PL = []
Sec_NNI_RTR_IHS_NATIVE_USA_PL = []
Sec_NNI_RTR_MARKIT_NAT_EUR_PL = []
Sec_NNI_RTR_MARKIT_NAT_USA_PL = []
Sec_NNI_RTR_MARKIT_NATIVE_EUR_PL = []
Sec_NNI_RTR_MARKIT_NATIVE_USA_PL = []

for line in Sec_NNI_RTR_IHS_NAT_EUR:
    if RE4.search(line):
       Sec_NNI_RTR_IHS_NAT_EUR_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_IHS_NAT_USA:
    if RE4.search(line):
       Sec_NNI_RTR_IHS_NAT_USA_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_IHS_NATIVE_EUR:
    if RE4.search(line):
       Sec_NNI_RTR_IHS_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_IHS_NATIVE_USA:
    if RE4.search(line):
       Sec_NNI_RTR_IHS_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_MARKIT_NAT_EUR:
    if RE4.search(line):
       Sec_NNI_RTR_MARKIT_NAT_EUR_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_MARKIT_NAT_USA:
    if RE4.search(line):
       Sec_NNI_RTR_MARKIT_NAT_USA_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_MARKIT_NATIVE_EUR:
    if RE4.search(line):
       Sec_NNI_RTR_MARKIT_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Sec_NNI_RTR_MARKIT_NATIVE_USA:
    if RE4.search(line):
       Sec_NNI_RTR_MARKIT_NATIVE_USA_PL.append(RE4.search(line).group())
#========Third Target Device===================================================
print('=============Generating The Output Files From US-WDC10-NNI01 Router===================')
print('\n')

Host_Name3  = 'US-WDC10-NNI01'
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

IHS_NAT_EUR.clear()
IHS_NAT_USA.clear()
IHS_NATIVE_EUR.clear()
IHS_NATIVE_USA.clear()
MARKIT_NAT_EUR.clear()
MARKIT_NAT_USA.clear()
MARKIT_NATIVE_EUR.clear()
MARKIT_NATIVE_USA.clear()

with open('Result_' + Host_Name3) as f:
     for line in f:
         if 'ip prefix-list PL-IHS-NAT-EU' in line:
             IHS_NAT_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NAT-USA' in line:
               IHS_NAT_USA.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-EU' in line:
               IHS_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-USA' in line:
               IHS_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-EU' in line:
               MARKIT_NAT_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-USA' in line:
            MARKIT_NAT_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-EU' in line:
              MARKIT_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-USA' in line:
              MARKIT_NATIVE_USA.append(line)

Thr_NNI_RTR_IHS_NAT_EUR = []
Thr_NNI_RTR_IHS_NAT_USA = []
Thr_NNI_RTR_IHS_NATIVE_EUR = []
Thr_NNI_RTR_IHS_NATIVE_USA = []
Thr_NNI_RTR_MARKIT_NAT_EUR = []
Thr_NNI_RTR_MARKIT_NAT_USA = []
Thr_NNI_RTR_MARKIT_NATIVE_EUR = []
Thr_NNI_RTR_MARKIT_NATIVE_USA = []

for i in range(len(IHS_NAT_EUR)):
    Thr_NNI_RTR_IHS_NAT_EUR.append(IHS_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NAT_USA)):
    Thr_NNI_RTR_IHS_NAT_USA.append(IHS_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_EUR)):
    Thr_NNI_RTR_IHS_NATIVE_EUR.append(IHS_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_USA)):
    Thr_NNI_RTR_IHS_NATIVE_USA.append(IHS_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_EUR)):
    Thr_NNI_RTR_MARKIT_NAT_EUR.append(MARKIT_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_EUR)):
    Thr_NNI_RTR_MARKIT_NATIVE_EUR.append(MARKIT_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_USA)):
    Thr_NNI_RTR_MARKIT_NAT_USA.append(MARKIT_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_USA)):
    Thr_NNI_RTR_MARKIT_NATIVE_USA.append(MARKIT_NATIVE_USA[i].strip('\n').split(' ')[-1])

Thr_NNI_RTR_IHS_NAT_EUR_PL = []
Thr_NNI_RTR_IHS_NAT_USA_PL = []
Thr_NNI_RTR_IHS_NATIVE_EUR_PL = []
Thr_NNI_RTR_IHS_NATIVE_USA_PL = []
Thr_NNI_RTR_MARKIT_NAT_EUR_PL = []
Thr_NNI_RTR_MARKIT_NAT_USA_PL = []
Thr_NNI_RTR_MARKIT_NATIVE_EUR_PL = []
Thr_NNI_RTR_MARKIT_NATIVE_USA_PL = []

for line in Thr_NNI_RTR_IHS_NAT_EUR:
    if RE4.search(line):
       Thr_NNI_RTR_IHS_NAT_EUR_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_IHS_NAT_USA:
    if RE4.search(line):
       Thr_NNI_RTR_IHS_NAT_USA_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_IHS_NATIVE_EUR:
    if RE4.search(line):
       Thr_NNI_RTR_IHS_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_IHS_NATIVE_USA:
    if RE4.search(line):
       Thr_NNI_RTR_IHS_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_MARKIT_NAT_EUR:
    if RE4.search(line):
       Thr_NNI_RTR_MARKIT_NAT_EUR_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_MARKIT_NAT_USA:
    if RE4.search(line):
       Thr_NNI_RTR_MARKIT_NAT_USA_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_MARKIT_NATIVE_EUR:
    if RE4.search(line):
       Thr_NNI_RTR_MARKIT_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Thr_NNI_RTR_MARKIT_NATIVE_USA:
    if RE4.search(line):
       Thr_NNI_RTR_MARKIT_NATIVE_USA_PL.append(RE4.search(line).group())
#=======================Comparison of Markit Side NNi Routers=======================================
print('=====Below output Based on Comparison of Markit Side NNI Routers=============================')

Missing_BGP_Routes=list(set(Pre_NNI_RTR_BGP_Routes).difference(set(New_NNI_RTR_BGP_Routes),set(Sec_NNI_RTR_BGP_Routes),set(Thr_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes1=list(set(New_NNI_RTR_BGP_Routes).difference(set(Pre_NNI_RTR_BGP_Routes),set(Sec_NNI_RTR_BGP_Routes),set(Thr_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes2=list(set(Sec_NNI_RTR_BGP_Routes).difference(set(Pre_NNI_RTR_BGP_Routes),set(New_NNI_RTR_BGP_Routes),set(Thr_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes3=list(set(Thr_NNI_RTR_BGP_Routes).difference(set(Pre_NNI_RTR_BGP_Routes),set(New_NNI_RTR_BGP_Routes),set(Sec_NNI_RTR_BGP_Routes)))

if len(Missing_BGP_Routes) == 0 and len(Missing_BGP_Routes1) == 0 and len(Missing_BGP_Routes2) == 0 and len(Missing_BGP_Routes3) == 0:
     print('='*95)
     print('BGP Routes are Same across all Markit NNI Routers!!!')
elif len(Missing_BGP_Routes) > 0:
     print('Missing BGP Routes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & '+ Host_Name3 + ' are below:')
     for i in range(len(Missing_BGP_Routes)):
         print(Missing_BGP_Routes[i])
elif len(Missing_BGP_Routes1) > 0:
     print('Missing BGP Routes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & '+ Host_Name3 + ' are below:')
     for i in range(len(Missing_BGP_Routes1)):
         print(Missing_BGP_Routes1[i])
elif len(Missing_BGP_Routes2) > 0:
     print('Missing BGP Routes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & '+ Host_Name3 + ' are below:')
     for i in range(len(Missing_BGP_Routes2)):
         print(Missing_BGP_Routes2[i])
elif len(Missing_BGP_Routes3) > 0:
     print('Missing BGP Routes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & '+ Host_Name2 + ' are below:')
     for i in range(len(Missing_BGP_Routes3)):
         print(Missing_BGP_Routes3[i])

##Below output will display BGP Route Count on Markit NNI Routers
print('\n'*1)
print('Below output will display BGP Route Count on all Markit NNI Routers:')
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
     print('Static Routes are Same across all Markit NNI Routers!!!')
elif len(Missing_Static_Routes) > 0:
     print('Missing Static Routes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Static_Routes)):
         print(Missing_Static_Routes[i])
elif len(Missing_Static_Routes1) > 0:
     print('Missing Static Routes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Static_Routes1)):
         print(Missing_Static_Routes1[i])
elif len(Missing_Static_Routes2) > 0:
     print('Missing Static Routes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Static_Routes2)):
         print(Missing_Static_Routes2[i])
elif len(Missing_Static_Routes3) > 0:
     print('Missing Static Routes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_Static_Routes3)):
         print(Missing_Static_Routes3[i])

##Below output will display Static Route Count on Markit NNI Routers
print('\n'*1)
print('Below output will display Static Route Count on all Markit NNI Routers:')
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
     print('Static Nats are Same across all Markit NNI Routers!!!')
elif len(Missing_Nats) > 0:
     print('Missing Static Nats of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Nats)):
         print(Missing_Nats[i])
elif len(Missing_Nats1) > 0:
     print('Missing Static Nats of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Nats1)):
         print(Missing_Nats1[i])
elif len(Missing_Nats2) > 0:
     print('Missing Static Nats of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_Nats2)):
         print(Missing_Nats2[i])
elif len(Missing_Nats3) > 0:
     print('Missing Static Nats of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_Nats3)):
         print(Missing_Nats3[i])

##Below output will display Static Nats Count on Markit NNI Routers
print('\n'*1)
print('Below output will display Static Nats Count on all Markit NNI Routers:')
print('='*95)
print("On " + Host_Name + " total no of Static Nats are :{}".format(len(Pre_NNI_RTR_Nats)))
print("On " + Host_Name1 + " total no of Static Nats are :{}".format(len(New_NNI_RTR_Nats)))
print("On " + Host_Name2 + " total no of Static Nats are :{}".format(len(Sec_NNI_RTR_Nats)))
print("On " + Host_Name3 + " total no of Static Nats are :{}".format(len(Thr_NNI_RTR_Nats)))
print('='*95)

#===============================================================================
Missing_IHS_NAT_EUR=list(set(Pre_NNI_RTR_IHS_NAT_EUR_PL).difference(set(New_NNI_RTR_IHS_NAT_EUR_PL),set(Sec_NNI_RTR_IHS_NAT_EUR_PL),set(Thr_NNI_RTR_IHS_NAT_EUR_PL)))
Missing_IHS_NAT_EUR1=list(set(New_NNI_RTR_IHS_NAT_EUR_PL).difference(set(Pre_NNI_RTR_IHS_NAT_EUR_PL),set(Sec_NNI_RTR_IHS_NAT_EUR_PL),set(Thr_NNI_RTR_IHS_NAT_EUR_PL)))
Missing_IHS_NAT_EUR2=list(set(Sec_NNI_RTR_IHS_NAT_EUR_PL).difference(set(Pre_NNI_RTR_IHS_NAT_EUR_PL),set(New_NNI_RTR_IHS_NAT_EUR_PL),set(Thr_NNI_RTR_IHS_NAT_EUR_PL)))
Missing_IHS_NAT_EUR3=list(set(Thr_NNI_RTR_IHS_NAT_EUR_PL).difference(set(Pre_NNI_RTR_IHS_NAT_EUR_PL),set(New_NNI_RTR_IHS_NAT_EUR_PL),set(Sec_NNI_RTR_IHS_NAT_EUR_PL)))

Missing_IHS_NAT_USA=list(set(Pre_NNI_RTR_IHS_NAT_USA_PL).difference(set(New_NNI_RTR_IHS_NAT_USA_PL),set(Sec_NNI_RTR_IHS_NAT_USA_PL),set(Thr_NNI_RTR_IHS_NAT_USA_PL)))
Missing_IHS_NAT_USA1=list(set(New_NNI_RTR_IHS_NAT_USA_PL).difference(set(Pre_NNI_RTR_IHS_NAT_USA_PL),set(Sec_NNI_RTR_IHS_NAT_USA_PL),set(Thr_NNI_RTR_IHS_NAT_USA_PL)))
Missing_IHS_NAT_USA2=list(set(Sec_NNI_RTR_IHS_NAT_USA_PL).difference(set(Pre_NNI_RTR_IHS_NAT_USA_PL),set(New_NNI_RTR_IHS_NAT_USA_PL),set(Thr_NNI_RTR_IHS_NAT_USA_PL)))
Missing_IHS_NAT_USA3=list(set(Thr_NNI_RTR_IHS_NAT_USA_PL).difference(set(Pre_NNI_RTR_IHS_NAT_USA_PL),set(New_NNI_RTR_IHS_NAT_USA_PL),set(Sec_NNI_RTR_IHS_NAT_USA_PL)))

Missing_IHS_NATIVE_EUR=list(set(Pre_NNI_RTR_IHS_NATIVE_EUR_PL).difference(set(New_NNI_RTR_IHS_NATIVE_EUR_PL),set(Sec_NNI_RTR_IHS_NATIVE_EUR_PL),set(Thr_NNI_RTR_IHS_NATIVE_EUR_PL)))
Missing_IHS_NATIVE_EUR1=list(set(New_NNI_RTR_IHS_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_IHS_NATIVE_EUR_PL),set(Sec_NNI_RTR_IHS_NATIVE_EUR_PL),set(Thr_NNI_RTR_IHS_NATIVE_EUR_PL)))
Missing_IHS_NATIVE_EUR2=list(set(Sec_NNI_RTR_IHS_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_IHS_NATIVE_EUR_PL),set(New_NNI_RTR_IHS_NATIVE_EUR_PL),set(Thr_NNI_RTR_IHS_NATIVE_EUR_PL)))
Missing_IHS_NATIVE_EUR3=list(set(Thr_NNI_RTR_IHS_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_IHS_NATIVE_EUR_PL),set(New_NNI_RTR_IHS_NATIVE_EUR_PL),set(Sec_NNI_RTR_IHS_NATIVE_EUR_PL)))

Missing_IHS_NATIVE_USA=list(set(Pre_NNI_RTR_IHS_NATIVE_USA_PL).difference(set(New_NNI_RTR_IHS_NATIVE_USA_PL),set(Sec_NNI_RTR_IHS_NATIVE_USA_PL),set(Thr_NNI_RTR_IHS_NATIVE_USA_PL)))
Missing_IHS_NATIVE_USA1=list(set(New_NNI_RTR_IHS_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_IHS_NATIVE_USA_PL),set(Sec_NNI_RTR_IHS_NATIVE_USA_PL),set(Thr_NNI_RTR_IHS_NATIVE_USA_PL)))
Missing_IHS_NATIVE_USA2=list(set(Sec_NNI_RTR_IHS_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_IHS_NATIVE_USA_PL),set(New_NNI_RTR_IHS_NATIVE_USA_PL),set(Thr_NNI_RTR_IHS_NATIVE_USA_PL)))
Missing_IHS_NATIVE_USA3=list(set(Thr_NNI_RTR_IHS_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_IHS_NATIVE_USA_PL),set(New_NNI_RTR_IHS_NATIVE_USA_PL),set(Sec_NNI_RTR_IHS_NATIVE_USA_PL)))

Missing_MARKIT_NAT_EUR=list(set(Pre_NNI_RTR_MARKIT_NAT_EUR_PL).difference(set(New_NNI_RTR_MARKIT_NAT_EUR_PL),set(Sec_NNI_RTR_MARKIT_NAT_EUR_PL),set(Thr_NNI_RTR_MARKIT_NAT_EUR_PL)))
Missing_MARKIT_NAT_EUR1=list(set(New_NNI_RTR_MARKIT_NAT_EUR_PL).difference(set(Pre_NNI_RTR_MARKIT_NAT_EUR_PL),set(Sec_NNI_RTR_MARKIT_NAT_EUR_PL),set(Thr_NNI_RTR_MARKIT_NAT_EUR_PL)))
Missing_MARKIT_NAT_EUR2=list(set(Sec_NNI_RTR_MARKIT_NAT_EUR_PL).difference(set(Pre_NNI_RTR_MARKIT_NAT_EUR_PL),set(New_NNI_RTR_MARKIT_NAT_EUR_PL),set(Thr_NNI_RTR_MARKIT_NAT_EUR_PL)))
Missing_MARKIT_NAT_EUR3=list(set(Thr_NNI_RTR_MARKIT_NAT_EUR_PL).difference(set(Pre_NNI_RTR_MARKIT_NAT_EUR_PL),set(New_NNI_RTR_MARKIT_NAT_EUR_PL),set(Sec_NNI_RTR_MARKIT_NAT_EUR_PL)))

Missing_MARKIT_NAT_USA=list(set(Pre_NNI_RTR_MARKIT_NAT_USA_PL).difference(set(New_NNI_RTR_MARKIT_NAT_USA_PL),set(Sec_NNI_RTR_MARKIT_NAT_USA_PL),set(Thr_NNI_RTR_MARKIT_NAT_USA_PL)))
Missing_MARKIT_NAT_USA1=list(set(New_NNI_RTR_MARKIT_NAT_USA_PL).difference(set(Pre_NNI_RTR_MARKIT_NAT_USA_PL),set(Sec_NNI_RTR_MARKIT_NAT_USA_PL),set(Thr_NNI_RTR_MARKIT_NAT_USA_PL)))
Missing_MARKIT_NAT_USA2=list(set(Sec_NNI_RTR_MARKIT_NAT_USA_PL).difference(set(Pre_NNI_RTR_MARKIT_NAT_USA_PL),set(New_NNI_RTR_MARKIT_NAT_USA_PL),set(Thr_NNI_RTR_MARKIT_NAT_USA_PL)))
Missing_MARKIT_NAT_USA3=list(set(Thr_NNI_RTR_MARKIT_NAT_USA_PL).difference(set(Pre_NNI_RTR_MARKIT_NAT_USA_PL),set(New_NNI_RTR_MARKIT_NAT_USA_PL),set(Sec_NNI_RTR_MARKIT_NAT_USA_PL)))

Missing_MARKIT_NATIVE_EUR=list(set(Pre_NNI_RTR_MARKIT_NATIVE_EUR_PL).difference(set(New_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Sec_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Thr_NNI_RTR_MARKIT_NATIVE_EUR_PL)))
Missing_MARKIT_NATIVE_EUR1=list(set(New_NNI_RTR_MARKIT_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Sec_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Thr_NNI_RTR_MARKIT_NATIVE_EUR_PL)))
Missing_MARKIT_NATIVE_EUR2=list(set(Sec_NNI_RTR_MARKIT_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(New_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Thr_NNI_RTR_MARKIT_NATIVE_EUR_PL)))
Missing_MARKIT_NATIVE_EUR3=list(set(Thr_NNI_RTR_MARKIT_NATIVE_EUR_PL).difference(set(Pre_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(New_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Sec_NNI_RTR_MARKIT_NATIVE_EUR_PL)))

Missing_MARKIT_NATIVE_USA=list(set(Pre_NNI_RTR_MARKIT_NATIVE_USA_PL).difference(set(New_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Sec_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Thr_NNI_RTR_MARKIT_NATIVE_USA_PL)))
Missing_MARKIT_NATIVE_USA1=list(set(New_NNI_RTR_MARKIT_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Sec_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Thr_NNI_RTR_MARKIT_NATIVE_USA_PL)))
Missing_MARKIT_NATIVE_USA2=list(set(Sec_NNI_RTR_MARKIT_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_MARKIT_NATIVE_USA_PL),set(New_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Thr_NNI_RTR_MARKIT_NATIVE_USA_PL)))
Missing_MARKIT_NATIVE_USA3=list(set(Thr_NNI_RTR_MARKIT_NATIVE_USA_PL).difference(set(Pre_NNI_RTR_MARKIT_NATIVE_USA_PL),set(New_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Sec_NNI_RTR_MARKIT_NATIVE_USA_PL)))

print('='*90)

if len(Missing_IHS_NAT_EUR) == 0 and len(Missing_IHS_NAT_EUR1) == 0 and len(Missing_IHS_NAT_EUR2) == 0 and len(Missing_IHS_NAT_EUR3) == 0:
     print('='*95)
     print('L-IHS NATTED Prefixes Of EU Region are Same across all Markit NNI Routers!!!')
elif len(Missing_IHS_NAT_EUR) > 0:
     print('Missing L-IHS EU Region NATTED Prefixes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NAT_EUR)):
         print(Missing_IHS_NAT_EUR[i])
elif len(Missing_IHS_NAT_EUR1) > 0:
     print('Missing L-IHS EU Region NATTED Prefixes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NAT_EUR1)):
         print(Missing_IHS_NAT_EUR1[i])
elif len(Missing_IHS_NAT_EUR2) > 0:
     print('Missing L-IHS EU Region NATTED Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NAT_EUR2)):
         print(Missing_IHS_NAT_EUR2[i])
elif len(Missing_IHS_NAT_EUR3) > 0:
     print('Missing L-IHS EU Region NATTED Prefixes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_IHS_NAT_EUR3)):
         print(Missing_IHS_NAT_EUR3[i])

if len(Missing_IHS_NAT_USA) == 0 and len(Missing_IHS_NAT_USA1) == 0 and len(Missing_IHS_NAT_USA2) == 0 and len(Missing_IHS_NAT_USA3) == 0:
     print('='*95)
     print('L-IHS NATTED Prefixes Of US Region are Same across all Markit NNI Routers!!!')
elif len(Missing_IHS_NAT_USA) > 0:
     print('Missing L-IHS US Region NATTED Prefixes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NAT_USA)):
         print(Missing_IHS_NAT_USA[i])
elif len(Missing_IHS_NAT_USA1) > 0:
     print('Missing L-IHS US Region NATTED Prefixes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NAT_USA1)):
         print(Missing_IHS_NAT_USA1[i])
elif len(Missing_IHS_NAT_USA2) > 0:
     print('Missing L-IHS US Region NATTED Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NAT_USA2)):
         print(Missing_IHS_NAT_USA2[i])
elif len(Missing_IHS_NAT_USA3) > 0:
     print('Missing L-IHS US Region NATTED Prefixes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_IHS_NAT_USA3)):
         print(Missing_IHS_NAT_USA3[i])

print('\n'*1)

if len(Missing_IHS_NATIVE_EUR) == 0 and len(Missing_IHS_NATIVE_EUR1) == 0 and len(Missing_IHS_NATIVE_EUR2) == 0 and len(Missing_IHS_NATIVE_EUR3) == 0:
     print('='*95)
     print('L-IHS NATIVE Prefixes Of EU Region are Same across all Markit NNI Routers!!!')
elif len(Missing_IHS_NATIVE_EUR) > 0:
     print('Missing L-IHS EU Region NATIVE Prefixes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_EUR)):
         print(Missing_IHS_NATIVE_EUR[i])
elif len(Missing_IHS_NATIVE_EUR1) > 0:
     print('Missing L-IHS EU Region NATIVE Prefixes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_EUR1)):
         print(Missing_IHS_NATIVE_EUR1[i])
elif len(Missing_IHS_NATIVE_EUR2) > 0:
     print('Missing L-IHS EU Region NATIVE Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_EUR2)):
         print(Missing_IHS_NATIVE_EUR2[i])
elif len(Missing_IHS_NATIVE_EUR3) > 0:
     print('Missing L-IHS EU Region NATIVE Prefixes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_EUR3)):
         print(Missing_IHS_NATIVE_EUR3[i])

if len(Missing_IHS_NATIVE_USA) == 0 and len(Missing_IHS_NATIVE_USA1) == 0 and len(Missing_IHS_NATIVE_USA2) == 0 and len(Missing_IHS_NATIVE_USA3) == 0:
     print('='*95)
     print('L-IHS NATIVE Prefixes Of US Region are Same across all Markit NNI Routers!!!')
elif len(Missing_IHS_NATIVE_USA) > 0:
     print('Missing L-IHS US Region NATIVE Prefixes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_USA)):
         print(Missing_IHS_NATIVE_USA[i])
elif len(Missing_IHS_NATIVE_USA1) > 0:
     print('Missing L-IHS US Region NATIVE Prefixes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_USA1)):
         print(Missing_IHS_NATIVE_USA1[i])
elif len(Missing_IHS_NATIVE_USA2) > 0:
     print('Missing L-IHS US Region NATIVE Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_USA2)):
         print(Missing_IHS_NATIVE_USA2[i])
elif len(Missing_IHS_NATIVE_USA3) > 0:
     print('Missing L-IHS US Region NATIVE Prefixes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_USA3)):
         print(Missing_IHS_NATIVE_USA3[i])

print('\n'*1)

if len(Missing_MARKIT_NAT_EUR) == 0 and len(Missing_MARKIT_NAT_EUR1) == 0 and len(Missing_MARKIT_NAT_EUR2) == 0 and len(Missing_MARKIT_NAT_EUR3) == 0:
     print('='*95)
     print('L-MARKIT NATTED Prefixes Of EU Region are Same across all MARKIT NNI Routers!!!')
elif len(Missing_MARKIT_NAT_EUR) > 0:
     print('Missing L-MARKIT EU Region NATTED Prefixes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_EUR)):
         print(Missing_MARKIT_NAT_EUR[i])
elif len(Missing_MARKIT_NAT_EUR1) > 0:
     print('Missing L-MARKIT EU Region NATTED Prefixes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_EUR1)):
         print(Missing_MARKIT_NAT_EUR1[i])
elif len(Missing_MARKIT_NAT_EUR2) > 0:
     print('Missing L-MARKIT EU Region NATTED Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_EUR2)):
         print(Missing_MARKIT_NAT_EUR2[i])
elif len(Missing_MARKIT_NAT_EUR3) > 0:
     print('Missing L-MARKIT EU Region NATTED Prefixes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_EUR3)):
         print(Missing_MARKIT_NAT_EUR3[i])


if len(Missing_MARKIT_NAT_USA) == 0 and len(Missing_MARKIT_NAT_USA1) == 0 and len(Missing_MARKIT_NAT_USA2) == 0 and len(Missing_MARKIT_NAT_USA3) == 0:
     print('='*95)
     print('L-MARKIT NATTED Prefixes Of US Region are Same across all MARKIT NNI Routers!!!')
elif len(Missing_MARKIT_NAT_USA) > 0:
     print('Missing L-MARKIT US Region NATTED Prefixes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_USA)):
         print(Missing_MARKIT_NAT_USA[i])
elif len(Missing_MARKIT_NAT_USA1) > 0:
     print('Missing L-MARKIT US Region NATTED Prefixes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_USA1)):
         print(Missing_MARKIT_NAT_USA1[i])
elif len(Missing_MARKIT_NAT_USA2) > 0:
     print('Missing L-MARKIT US Region NATTED Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_USA2)):
         print(Missing_MARKIT_NAT_USA2[i])
elif len(Missing_MARKIT_NAT_USA3) > 0:
     print('Missing L-MARKIT US Region NATTED Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_USA3)):
         print(Missing_MARKIT_NAT_USA3[i])

print('\n'*1)

if len(Missing_MARKIT_NATIVE_EUR) == 0 and len(Missing_MARKIT_NATIVE_EUR1) == 0 and len(Missing_MARKIT_NATIVE_EUR2) == 0 and len(Missing_MARKIT_NATIVE_EUR3) == 0:
     print('='*95)
     print('L-MARKIT NATIVE Prefixes Of EU Region are Same across all MARKIT NNI Routers!!!')
elif len(Missing_MARKIT_NATIVE_EUR) > 0:
     print('Missing L-MARKIT EU Region NATIVE Prefixes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_EUR)):
         print(Missing_MARKIT_NATIVE_EUR[i])
elif len(Missing_MARKIT_NATIVE_EUR1) > 0:
     print('Missing L-MARKIT EU Region NATIVE Prefixes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_EUR1)):
         print(Missing_MARKIT_NATIVE_EUR1[i])
elif len(Missing_MARKIT_NATIVE_EUR2) > 0:
     print('Missing L-MARKIT EU Region NATIVE Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_EUR2)):
         print(Missing_MARKIT_NATIVE_EUR2[i])
elif len(Missing_MARKIT_NATIVE_EUR3) > 0:
     print('Missing L-MARKIT EU Region NATIVE Prefixes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_EUR3)):
         print(Missing_MARKIT_NATIVE_EUR3[i])

if len(Missing_MARKIT_NATIVE_USA) == 0 and len(Missing_MARKIT_NATIVE_USA1) == 0 and len(Missing_MARKIT_NATIVE_USA2) == 0 and len(Missing_MARKIT_NATIVE_USA3) == 0:
     print('='*95)
     print('L-MARKIT NATIVE Prefixes Of US Region are Same across all MARKIT NNI Routers!!!')
elif len(Missing_MARKIT_NATIVE_USA) > 0:
     print('Missing L-MARKIT US Region NATIVE Prefixes of UK-LON10-NNI01 in ' + Host_Name1 + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_USA)):
         print(Missing_MARKIT_NATIVE_USA[i])
elif len(Missing_MARKIT_NATIVE_USA1) > 0:
     print('Missing L-MARKIT US Region NATIVE Prefixes of UK-LON11-NNI01 in ' + Host_Name + ' & ' + Host_Name2 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_USA1)):
         print(Missing_MARKIT_NATIVE_USA1[i])
elif len(Missing_MARKIT_NATIVE_USA2) > 0:
     print('Missing L-MARKIT US Region NATIVE Prefixes of US-RIC01-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name3 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_USA2)):
         print(Missing_MARKIT_NATIVE_USA2[i])
elif len(Missing_MARKIT_NATIVE_USA3) > 0:
     print('Missing L-MARKIT US Region NATIVE Prefixes of US-WDC10-NNI01 in ' + Host_Name + ' & ' + Host_Name1 + ' & ' + Host_Name2 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_USA3)):
         print(Missing_MARKIT_NATIVE_USA3[i])

print('='*90)
#======Files for L-IHS NNI Routers==============================================
#========Forth Target L-IHS Device===================================================
print('=============Generating The Output Files From UK-WOK01-NNI01 Router===================')
print('\n')

Host_Name4 = 'UK-WOK01-NNI01'

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


IHS_NAT_EUR = []
IHS_NAT_USA = []
IHS_NATIVE_EUR = []
IHS_NATIVE_USA = []
MARKIT_NAT_EUR = []
MARKIT_NAT_USA = []
MARKIT_NATIVE_EUR = []
MARKIT_NATIVE_USA = []

with open('Result_' + Host_Name4) as f:
     for line in f:
         if 'ip prefix-list PL-IHS-NAT-EU' in line:
             IHS_NAT_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NAT-USA' in line:
               IHS_NAT_USA.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-EU' in line:
               IHS_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-USA' in line:
               IHS_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-EU' in line:
               MARKIT_NAT_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-USA' in line:
            MARKIT_NAT_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-EU' in line:
              MARKIT_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-USA' in line:
              MARKIT_NATIVE_USA.append(line)

Forth_NNI_RTR_IHS_NAT_EUR = []
Forth_NNI_RTR_IHS_NAT_USA = []
Forth_NNI_RTR_IHS_NATIVE_EUR = []
Forth_NNI_RTR_IHS_NATIVE_USA = []
Forth_NNI_RTR_MARKIT_NAT_EUR = []
Forth_NNI_RTR_MARKIT_NAT_USA = []
Forth_NNI_RTR_MARKIT_NATIVE_EUR = []
Forth_NNI_RTR_MARKIT_NATIVE_USA = []

for i in range(len(IHS_NAT_EUR)):
    Forth_NNI_RTR_IHS_NAT_EUR.append(IHS_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NAT_USA)):
    Forth_NNI_RTR_IHS_NAT_USA.append(IHS_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_EUR)):
    Forth_NNI_RTR_IHS_NATIVE_EUR.append(IHS_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_USA)):
    Forth_NNI_RTR_IHS_NATIVE_USA.append(IHS_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_EUR)):
    Forth_NNI_RTR_MARKIT_NAT_EUR.append(MARKIT_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_EUR)):
    Forth_NNI_RTR_MARKIT_NATIVE_EUR.append(MARKIT_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_USA)):
    Forth_NNI_RTR_MARKIT_NAT_USA.append(MARKIT_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_USA)):
    Forth_NNI_RTR_MARKIT_NATIVE_USA.append(MARKIT_NATIVE_USA[i].strip('\n').split(' ')[-1])

Forth_NNI_RTR_IHS_NAT_EUR_PL = []
Forth_NNI_RTR_IHS_NAT_USA_PL = []
Forth_NNI_RTR_IHS_NATIVE_EUR_PL = []
Forth_NNI_RTR_IHS_NATIVE_USA_PL = []
Forth_NNI_RTR_MARKIT_NAT_EUR_PL = []
Forth_NNI_RTR_MARKIT_NAT_USA_PL = []
Forth_NNI_RTR_MARKIT_NATIVE_EUR_PL = []
Forth_NNI_RTR_MARKIT_NATIVE_USA_PL = []

for line in Forth_NNI_RTR_IHS_NAT_EUR:
    if RE4.search(line):
       Forth_NNI_RTR_IHS_NAT_EUR_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_IHS_NAT_USA:
    if RE4.search(line):
       Forth_NNI_RTR_IHS_NAT_USA_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_IHS_NATIVE_EUR:
    if RE4.search(line):
       Forth_NNI_RTR_IHS_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_IHS_NATIVE_USA:
    if RE4.search(line):
       Forth_NNI_RTR_IHS_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_MARKIT_NAT_EUR:
    if RE4.search(line):
       Forth_NNI_RTR_MARKIT_NAT_EUR_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_MARKIT_NAT_USA:
    if RE4.search(line):
       Forth_NNI_RTR_MARKIT_NAT_USA_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_MARKIT_NATIVE_EUR:
    if RE4.search(line):
       Forth_NNI_RTR_MARKIT_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Forth_NNI_RTR_MARKIT_NATIVE_USA:
    if RE4.search(line):
       Forth_NNI_RTR_MARKIT_NATIVE_USA_PL.append(RE4.search(line).group())
#========Fifth Target L-IHS Device===================================================
print('=============Generating The Output Files From UK-WOK01-NNI02 Router===================')
print('\n')

Host_Name5 = 'UK-WOK01-NNI02'
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


IHS_NAT_EUR = []
IHS_NAT_USA = []
IHS_NATIVE_EUR = []
IHS_NATIVE_USA = []
MARKIT_NAT_EUR = []
MARKIT_NAT_USA = []
MARKIT_NATIVE_EUR = []
MARKIT_NATIVE_USA = []

with open('Result_' + Host_Name5) as f:
     for line in f:
         if 'ip prefix-list PL-IHS-NAT-EU' in line:
             IHS_NAT_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NAT-USA' in line:
               IHS_NAT_USA.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-EU' in line:
               IHS_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-USA' in line:
               IHS_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-EU' in line:
               MARKIT_NAT_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-USA' in line:
            MARKIT_NAT_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-EU' in line:
              MARKIT_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-USA' in line:
              MARKIT_NATIVE_USA.append(line)

Fifth_NNI_RTR_IHS_NAT_EUR = []
Fifth_NNI_RTR_IHS_NAT_USA = []
Fifth_NNI_RTR_IHS_NATIVE_EUR = []
Fifth_NNI_RTR_IHS_NATIVE_USA = []
Fifth_NNI_RTR_MARKIT_NAT_EUR = []
Fifth_NNI_RTR_MARKIT_NAT_USA = []
Fifth_NNI_RTR_MARKIT_NATIVE_EUR = []
Fifth_NNI_RTR_MARKIT_NATIVE_USA = []

for i in range(len(IHS_NAT_EUR)):
    Fifth_NNI_RTR_IHS_NAT_EUR.append(IHS_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NAT_USA)):
    Fifth_NNI_RTR_IHS_NAT_USA.append(IHS_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_EUR)):
    Fifth_NNI_RTR_IHS_NATIVE_EUR.append(IHS_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_USA)):
    Fifth_NNI_RTR_IHS_NATIVE_USA.append(IHS_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_EUR)):
    Fifth_NNI_RTR_MARKIT_NAT_EUR.append(MARKIT_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_EUR)):
    Fifth_NNI_RTR_MARKIT_NATIVE_EUR.append(MARKIT_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_USA)):
    Fifth_NNI_RTR_MARKIT_NAT_USA.append(MARKIT_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_USA)):
    Fifth_NNI_RTR_MARKIT_NATIVE_USA.append(MARKIT_NATIVE_USA[i].strip('\n').split(' ')[-1])

Fifth_NNI_RTR_IHS_NAT_EUR_PL = []
Fifth_NNI_RTR_IHS_NAT_USA_PL = []
Fifth_NNI_RTR_IHS_NATIVE_EUR_PL = []
Fifth_NNI_RTR_IHS_NATIVE_USA_PL = []
Fifth_NNI_RTR_MARKIT_NAT_EUR_PL = []
Fifth_NNI_RTR_MARKIT_NAT_USA_PL = []
Fifth_NNI_RTR_MARKIT_NATIVE_EUR_PL = []
Fifth_NNI_RTR_MARKIT_NATIVE_USA_PL = []

for line in Fifth_NNI_RTR_IHS_NAT_EUR:
    if RE4.search(line):
       Fifth_NNI_RTR_IHS_NAT_EUR_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_IHS_NAT_USA:
    if RE4.search(line):
       Fifth_NNI_RTR_IHS_NAT_USA_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_IHS_NATIVE_EUR:
    if RE4.search(line):
       Fifth_NNI_RTR_IHS_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_IHS_NATIVE_USA:
    if RE4.search(line):
       Fifth_NNI_RTR_IHS_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_MARKIT_NAT_EUR:
    if RE4.search(line):
       Fifth_NNI_RTR_MARKIT_NAT_EUR_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_MARKIT_NAT_USA:
    if RE4.search(line):
       Fifth_NNI_RTR_MARKIT_NAT_USA_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_MARKIT_NATIVE_EUR:
    if RE4.search(line):
       Fifth_NNI_RTR_MARKIT_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Fifth_NNI_RTR_MARKIT_NATIVE_USA:
    if RE4.search(line):
       Fifth_NNI_RTR_MARKIT_NATIVE_USA_PL.append(RE4.search(line).group())
#========Sixth Target L-IHS Device===================================================
print('=============Generating The Output Files From US-VWC01-NNI01 Router===================')
print('\n')

Host_Name6 = 'US-VWC01-NNI01'

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


IHS_NAT_EUR = []
IHS_NAT_USA = []
IHS_NATIVE_EUR = []
IHS_NATIVE_USA = []
MARKIT_NAT_EUR = []
MARKIT_NAT_USA = []
MARKIT_NATIVE_EUR = []
MARKIT_NATIVE_USA = []

with open('Result_' + Host_Name6) as f:
     for line in f:
         if 'ip prefix-list PL-IHS-NAT-EU' in line:
             IHS_NAT_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NAT-USA' in line:
               IHS_NAT_USA.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-EU' in line:
               IHS_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-USA' in line:
               IHS_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-EU' in line:
               MARKIT_NAT_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-USA' in line:
            MARKIT_NAT_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-EU' in line:
              MARKIT_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-USA' in line:
              MARKIT_NATIVE_USA.append(line)

Sixth_NNI_RTR_IHS_NAT_EUR = []
Sixth_NNI_RTR_IHS_NAT_USA = []
Sixth_NNI_RTR_IHS_NATIVE_EUR = []
Sixth_NNI_RTR_IHS_NATIVE_USA = []
Sixth_NNI_RTR_MARKIT_NAT_EUR = []
Sixth_NNI_RTR_MARKIT_NAT_USA = []
Sixth_NNI_RTR_MARKIT_NATIVE_EUR = []
Sixth_NNI_RTR_MARKIT_NATIVE_USA = []

for i in range(len(IHS_NAT_EUR)):
    Sixth_NNI_RTR_IHS_NAT_EUR.append(IHS_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NAT_USA)):
    Sixth_NNI_RTR_IHS_NAT_USA.append(IHS_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_EUR)):
    Sixth_NNI_RTR_IHS_NATIVE_EUR.append(IHS_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_USA)):
    Sixth_NNI_RTR_IHS_NATIVE_USA.append(IHS_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_EUR)):
    Sixth_NNI_RTR_MARKIT_NAT_EUR.append(MARKIT_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_EUR)):
    Sixth_NNI_RTR_MARKIT_NATIVE_EUR.append(MARKIT_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_USA)):
    Sixth_NNI_RTR_MARKIT_NAT_USA.append(MARKIT_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_USA)):
    Sixth_NNI_RTR_MARKIT_NATIVE_USA.append(MARKIT_NATIVE_USA[i].strip('\n').split(' ')[-1])

Sixth_NNI_RTR_IHS_NAT_EUR_PL = []
Sixth_NNI_RTR_IHS_NAT_USA_PL = []
Sixth_NNI_RTR_IHS_NATIVE_EUR_PL = []
Sixth_NNI_RTR_IHS_NATIVE_USA_PL = []
Sixth_NNI_RTR_MARKIT_NAT_EUR_PL = []
Sixth_NNI_RTR_MARKIT_NAT_USA_PL = []
Sixth_NNI_RTR_MARKIT_NATIVE_EUR_PL = []
Sixth_NNI_RTR_MARKIT_NATIVE_USA_PL = []

for line in Sixth_NNI_RTR_IHS_NAT_EUR:
    if RE4.search(line):
       Sixth_NNI_RTR_IHS_NAT_EUR_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_IHS_NAT_USA:
    if RE4.search(line):
       Sixth_NNI_RTR_IHS_NAT_USA_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_IHS_NATIVE_EUR:
    if RE4.search(line):
       Sixth_NNI_RTR_IHS_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_IHS_NATIVE_USA:
    if RE4.search(line):
       Sixth_NNI_RTR_IHS_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_MARKIT_NAT_EUR:
    if RE4.search(line):
       Sixth_NNI_RTR_MARKIT_NAT_EUR_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_MARKIT_NAT_USA:
    if RE4.search(line):
       Sixth_NNI_RTR_MARKIT_NAT_USA_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_MARKIT_NATIVE_EUR:
    if RE4.search(line):
       Sixth_NNI_RTR_MARKIT_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Sixth_NNI_RTR_MARKIT_NATIVE_USA:
    if RE4.search(line):
       Sixth_NNI_RTR_MARKIT_NATIVE_USA_PL.append(RE4.search(line).group())
#========Seventh Target L-IHS Device===================================================
print('=============Generating The Output Files From US-VWC01-NNI02 Router===================')
print('\n')

Host_Name7 = 'US-VWC01-NNI02'

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


IHS_NAT_EUR = []
IHS_NAT_USA = []
IHS_NATIVE_EUR = []
IHS_NATIVE_USA = []
MARKIT_NAT_EUR = []
MARKIT_NAT_USA = []
MARKIT_NATIVE_EUR = []
MARKIT_NATIVE_USA = []

with open('Result_' + Host_Name7) as f:
     for line in f:
         if 'ip prefix-list PL-IHS-NAT-EU' in line:
             IHS_NAT_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NAT-USA' in line:
               IHS_NAT_USA.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-EU' in line:
               IHS_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-IHS-NATIVE-USA' in line:
               IHS_NATIVE_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-EU' in line:
               MARKIT_NAT_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NAT-USA' in line:
            MARKIT_NAT_USA.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-EU' in line:
              MARKIT_NATIVE_EUR.append(line)
         elif 'ip prefix-list PL-MARKIT-NATIVE-USA' in line:
              MARKIT_NATIVE_USA.append(line)

Seventh_NNI_RTR_IHS_NAT_EUR = []
Seventh_NNI_RTR_IHS_NAT_USA = []
Seventh_NNI_RTR_IHS_NATIVE_EUR = []
Seventh_NNI_RTR_IHS_NATIVE_USA = []
Seventh_NNI_RTR_MARKIT_NAT_EUR = []
Seventh_NNI_RTR_MARKIT_NAT_USA = []
Seventh_NNI_RTR_MARKIT_NATIVE_EUR = []
Seventh_NNI_RTR_MARKIT_NATIVE_USA = []

for i in range(len(IHS_NAT_EUR)):
    Seventh_NNI_RTR_IHS_NAT_EUR.append(IHS_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NAT_USA)):
    Seventh_NNI_RTR_IHS_NAT_USA.append(IHS_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_EUR)):
    Seventh_NNI_RTR_IHS_NATIVE_EUR.append(IHS_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(IHS_NATIVE_USA)):
    Seventh_NNI_RTR_IHS_NATIVE_USA.append(IHS_NATIVE_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_EUR)):
    Seventh_NNI_RTR_MARKIT_NAT_EUR.append(MARKIT_NAT_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_EUR)):
    Seventh_NNI_RTR_MARKIT_NATIVE_EUR.append(MARKIT_NATIVE_EUR[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NAT_USA)):
    Seventh_NNI_RTR_MARKIT_NAT_USA.append(MARKIT_NAT_USA[i].strip('\n').split(' ')[-1])

for i in range(len(MARKIT_NATIVE_USA)):
    Seventh_NNI_RTR_MARKIT_NATIVE_USA.append(MARKIT_NATIVE_USA[i].strip('\n').split(' ')[-1])

Seventh_NNI_RTR_IHS_NAT_EUR_PL = []
Seventh_NNI_RTR_IHS_NAT_USA_PL = []
Seventh_NNI_RTR_IHS_NATIVE_EUR_PL = []
Seventh_NNI_RTR_IHS_NATIVE_USA_PL = []
Seventh_NNI_RTR_MARKIT_NAT_EUR_PL = []
Seventh_NNI_RTR_MARKIT_NAT_USA_PL = []
Seventh_NNI_RTR_MARKIT_NATIVE_EUR_PL = []
Seventh_NNI_RTR_MARKIT_NATIVE_USA_PL = []

for line in Seventh_NNI_RTR_IHS_NAT_EUR:
    if RE4.search(line):
       Seventh_NNI_RTR_IHS_NAT_EUR_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_IHS_NAT_USA:
    if RE4.search(line):
       Seventh_NNI_RTR_IHS_NAT_USA_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_IHS_NATIVE_EUR:
    if RE4.search(line):
       Seventh_NNI_RTR_IHS_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_IHS_NATIVE_USA:
    if RE4.search(line):
       Seventh_NNI_RTR_IHS_NATIVE_USA_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_MARKIT_NAT_EUR:
    if RE4.search(line):
       Seventh_NNI_RTR_MARKIT_NAT_EUR_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_MARKIT_NAT_USA:
    if RE4.search(line):
       Seventh_NNI_RTR_MARKIT_NAT_USA_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_MARKIT_NATIVE_EUR:
    if RE4.search(line):
       Seventh_NNI_RTR_MARKIT_NATIVE_EUR_PL.append(RE4.search(line).group())

for line in Seventh_NNI_RTR_MARKIT_NATIVE_USA:
    if RE4.search(line):
       Seventh_NNI_RTR_MARKIT_NATIVE_USA_PL.append(RE4.search(line).group())
#=========================Comparison of L-IHS Side NNI Routers=======================================
Missing_BGP_Routes.clear()
Missing_BGP_Routes1.clear()
Missing_BGP_Routes2.clear()
Missing_BGP_Routes3.clear()

print('=====Below output Based on Comparison of L-IHS Side NNI Routers========================')
print('='*95)
Missing_BGP_Routes=list(set(Forth_NNI_RTR_BGP_Routes).difference(set(Fifth_NNI_RTR_BGP_Routes),set(Sixth_NNI_RTR_BGP_Routes),set(Seventh_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes1=list(set(Fifth_NNI_RTR_BGP_Routes).difference(set(Forth_NNI_RTR_BGP_Routes),set(Sixth_NNI_RTR_BGP_Routes),set(Seventh_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes2=list(set(Sixth_NNI_RTR_BGP_Routes).difference(set(Forth_NNI_RTR_BGP_Routes),set(Fifth_NNI_RTR_BGP_Routes),set(Seventh_NNI_RTR_BGP_Routes)))
Missing_BGP_Routes3=list(set(Seventh_NNI_RTR_BGP_Routes).difference(set(Forth_NNI_RTR_BGP_Routes),set(Fifth_NNI_RTR_BGP_Routes),set(Sixth_NNI_RTR_BGP_Routes)))

if len(Missing_BGP_Routes) == 0 and len(Missing_BGP_Routes1) == 0 and len(Missing_BGP_Routes2) == 0 and len(Missing_BGP_Routes3) == 0:
     print('='*95)
     print('BGP Routes are Same across all L-IHS NNI Routers!!!')
elif len(Missing_BGP_Routes) > 0:
     print('Missing BGP Routes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & '+ Host_Name7 + ' are below:')
     for i in range(len(Missing_BGP_Routes)):
         print(Missing_BGP_Routes[i])
elif len(Missing_BGP_Routes1) > 0:
     print('Missing BGP Routes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & '+ Host_Name7 + ' are below:')
     for i in range(len(Missing_BGP_Routes1)):
         print(Missing_BGP_Routes1[i])
elif len(Missing_BGP_Routes2) > 0:
     print('Missing BGP Routes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & '+ Host_Name7 + ' are below:')
     for i in range(len(Missing_BGP_Routes2)):
         print(Missing_BGP_Routes2[i])
elif len(Missing_BGP_Routes3) > 0:
     print('Missing BGP Routes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & '+ Host_Name6 + ' are below:')
     for i in range(len(Missing_BGP_Routes3)):
         print(Missing_BGP_Routes3[i])

##Below output will display BGP Route Count on L-IHS NNI Routers
print('\n'*1)
print('Below output will display BGP Route Count on all L-IHS NNI Routers:')
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
     print('Static Routes are Same across all L-IHS NNI Routers!!!')
elif len(Missing_Static_Routes) > 0:
     print('Missing Static Routes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Static_Routes)):
         print(Missing_Static_Routes[i])
elif len(Missing_Static_Routes1) > 0:
     print('Missing Static Routes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Static_Routes1)):
         print(Missing_Static_Routes1[i])
elif len(Missing_Static_Routes2) > 0:
     print('Missing Static Routes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Static_Routes2)):
         print(Missing_Static_Routes2[i])
elif len(Missing_Static_Routes3) > 0:
     print('Missing Static Routes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_Static_Routes3)):
         print(Missing_Static_Routes3[i])

##Below output will display Static Route Count on L-IHS NNI Routers
print('\n'*1)
print('Below output will display Static Route Count on all L-IHS NNI Routers:')
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
     print('Static Nats are Same across all L-IHS NNI Routers!!!')
elif len(Missing_Nats) > 0:
     print('Missing Static Nats of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Nats)):
         print(Missing_Nats[i])
elif len(Missing_Nats1) > 0:
     print('Missing Static Nats of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Nats1)):
         print(Missing_Nats1[i])
elif len(Missing_Nats2) > 0:
     print('Missing Static Nats of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_Nats2)):
         print(Missing_Nats2[i])
elif len(Missing_Nats3) > 0:
     print('Missing Static Nats of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_Nats3)):
         print(Missing_Nats3[i])

##Below output will display Static Nats Count on L-IHS NNI Routers
print('\n'*1)
print('Below output will display Static Nats Count on all L-IHS NNI Routers:')
print('='*95)
print("On " + Host_Name + " total no of Static Nats are :{}".format(len(Forth_NNI_RTR_Nats)))
print("On " + Host_Name5 + " total no of Static Nats are :{}".format(len(Fifth_NNI_RTR_Nats)))
print("On " + Host_Name6 + " total no of Static Nats are :{}".format(len(Sixth_NNI_RTR_Nats)))
print("On " + Host_Name7 + " total no of Static Nats are :{}".format(len(Seventh_NNI_RTR_Nats)))
print('='*95)

#===============================================================================
Missing_IHS_NAT_EUR.clear()
Missing_IHS_NAT_EUR1.clear()
Missing_IHS_NAT_EUR2.clear()
Missing_IHS_NAT_EUR3.clear()

Missing_IHS_NAT_USA.clear()
Missing_IHS_NAT_USA1.clear()
Missing_IHS_NAT_USA2.clear()
Missing_IHS_NAT_USA3.clear()

Missing_IHS_NATIVE_EUR.clear()
Missing_IHS_NATIVE_EUR1.clear()
Missing_IHS_NATIVE_EUR2.clear()
Missing_IHS_NATIVE_EUR3.clear()

Missing_IHS_NATIVE_USA.clear()
Missing_IHS_NATIVE_USA1.clear()
Missing_IHS_NATIVE_USA2.clear()
Missing_IHS_NATIVE_USA3.clear()

Missing_MARKIT_NAT_EUR.clear()
Missing_MARKIT_NAT_EUR1.clear()
Missing_MARKIT_NAT_EUR2.clear()
Missing_MARKIT_NAT_EUR3.clear()

Missing_MARKIT_NAT_USA.clear()
Missing_MARKIT_NAT_USA1.clear()
Missing_MARKIT_NAT_USA2.clear()
Missing_MARKIT_NAT_USA3.clear()

Missing_MARKIT_NATIVE_EUR.clear()
Missing_MARKIT_NATIVE_EUR1.clear()
Missing_MARKIT_NATIVE_EUR2.clear()
Missing_MARKIT_NATIVE_EUR3.clear()

Missing_MARKIT_NATIVE_USA.clear()
Missing_MARKIT_NATIVE_USA1.clear()
Missing_MARKIT_NATIVE_USA2.clear()
Missing_MARKIT_NATIVE_USA3.clear()


Missing_IHS_NAT_EUR=list(set(Forth_NNI_RTR_IHS_NAT_EUR_PL).difference(set(Fifth_NNI_RTR_IHS_NAT_EUR_PL),set(Sixth_NNI_RTR_IHS_NAT_EUR_PL),set(Seventh_NNI_RTR_IHS_NAT_EUR_PL)))
Missing_IHS_NAT_EUR1=list(set(Fifth_NNI_RTR_IHS_NAT_EUR_PL).difference(set(Forth_NNI_RTR_IHS_NAT_EUR_PL),set(Sixth_NNI_RTR_IHS_NAT_EUR_PL),set(Seventh_NNI_RTR_IHS_NAT_EUR_PL)))
Missing_IHS_NAT_EUR2=list(set(Sixth_NNI_RTR_IHS_NAT_EUR_PL).difference(set(Forth_NNI_RTR_IHS_NAT_EUR_PL),set(Fifth_NNI_RTR_IHS_NAT_EUR_PL),set(Seventh_NNI_RTR_IHS_NAT_EUR_PL)))
Missing_IHS_NAT_EUR3=list(set(Seventh_NNI_RTR_IHS_NAT_EUR_PL).difference(set(Forth_NNI_RTR_IHS_NAT_EUR_PL),set(Fifth_NNI_RTR_IHS_NAT_EUR_PL),set(Sixth_NNI_RTR_IHS_NAT_EUR_PL)))

Missing_IHS_NAT_USA=list(set(Forth_NNI_RTR_IHS_NAT_USA_PL).difference(set(Fifth_NNI_RTR_IHS_NAT_USA_PL),set(Sixth_NNI_RTR_IHS_NAT_USA_PL),set(Seventh_NNI_RTR_IHS_NAT_USA_PL)))
Missing_IHS_NAT_USA1=list(set(Fifth_NNI_RTR_IHS_NAT_USA_PL).difference(set(Forth_NNI_RTR_IHS_NAT_USA_PL),set(Sixth_NNI_RTR_IHS_NAT_USA_PL),set(Seventh_NNI_RTR_IHS_NAT_USA_PL)))
Missing_IHS_NAT_USA2=list(set(Sixth_NNI_RTR_IHS_NAT_USA_PL).difference(set(Forth_NNI_RTR_IHS_NAT_USA_PL),set(Fifth_NNI_RTR_IHS_NAT_USA_PL),set(Seventh_NNI_RTR_IHS_NAT_USA_PL)))
Missing_IHS_NAT_USA3=list(set(Seventh_NNI_RTR_IHS_NAT_USA_PL).difference(set(Forth_NNI_RTR_IHS_NAT_USA_PL),set(Fifth_NNI_RTR_IHS_NAT_USA_PL),set(Sixth_NNI_RTR_IHS_NAT_USA_PL)))

Missing_IHS_NATIVE_EUR=list(set(Forth_NNI_RTR_IHS_NATIVE_EUR_PL).difference(set(Fifth_NNI_RTR_IHS_NATIVE_EUR_PL),set(Sixth_NNI_RTR_IHS_NATIVE_EUR_PL),set(Seventh_NNI_RTR_IHS_NATIVE_EUR_PL)))
Missing_IHS_NATIVE_EUR1=list(set(Fifth_NNI_RTR_IHS_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_IHS_NATIVE_EUR_PL),set(Sixth_NNI_RTR_IHS_NATIVE_EUR_PL),set(Seventh_NNI_RTR_IHS_NATIVE_EUR_PL)))
Missing_IHS_NATIVE_EUR2=list(set(Sixth_NNI_RTR_IHS_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_IHS_NATIVE_EUR_PL),set(Fifth_NNI_RTR_IHS_NATIVE_EUR_PL),set(Seventh_NNI_RTR_IHS_NATIVE_EUR_PL)))
Missing_IHS_NATIVE_EUR3=list(set(Seventh_NNI_RTR_IHS_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_IHS_NATIVE_EUR_PL),set(Fifth_NNI_RTR_IHS_NATIVE_EUR_PL),set(Sixth_NNI_RTR_IHS_NATIVE_EUR_PL)))

Missing_IHS_NATIVE_USA=list(set(Forth_NNI_RTR_IHS_NATIVE_USA_PL).difference(set(Fifth_NNI_RTR_IHS_NATIVE_USA_PL),set(Sixth_NNI_RTR_IHS_NATIVE_USA_PL),set(Seventh_NNI_RTR_IHS_NATIVE_USA_PL)))
Missing_IHS_NATIVE_USA1=list(set(Fifth_NNI_RTR_IHS_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_IHS_NATIVE_USA_PL),set(Sixth_NNI_RTR_IHS_NATIVE_USA_PL),set(Seventh_NNI_RTR_IHS_NATIVE_USA_PL)))
Missing_IHS_NATIVE_USA2=list(set(Sixth_NNI_RTR_IHS_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_IHS_NATIVE_USA_PL),set(Fifth_NNI_RTR_IHS_NATIVE_USA_PL),set(Seventh_NNI_RTR_IHS_NATIVE_USA_PL)))
Missing_IHS_NATIVE_USA3=list(set(Seventh_NNI_RTR_IHS_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_IHS_NATIVE_USA_PL),set(Fifth_NNI_RTR_IHS_NATIVE_USA_PL),set(Sixth_NNI_RTR_IHS_NATIVE_USA_PL)))

Missing_MARKIT_NAT_EUR=list(set(Forth_NNI_RTR_MARKIT_NAT_EUR_PL).difference(set(Fifth_NNI_RTR_MARKIT_NAT_EUR_PL),set(Sixth_NNI_RTR_MARKIT_NAT_EUR_PL),set(Seventh_NNI_RTR_MARKIT_NAT_EUR_PL)))
Missing_MARKIT_NAT_EUR1=list(set(Fifth_NNI_RTR_MARKIT_NAT_EUR_PL).difference(set(Forth_NNI_RTR_MARKIT_NAT_EUR_PL),set(Sixth_NNI_RTR_MARKIT_NAT_EUR_PL),set(Seventh_NNI_RTR_MARKIT_NAT_EUR_PL)))
Missing_MARKIT_NAT_EUR2=list(set(Sixth_NNI_RTR_MARKIT_NAT_EUR_PL).difference(set(Forth_NNI_RTR_MARKIT_NAT_EUR_PL),set(Fifth_NNI_RTR_MARKIT_NAT_EUR_PL),set(Seventh_NNI_RTR_MARKIT_NAT_EUR_PL)))
Missing_MARKIT_NAT_EUR3=list(set(Seventh_NNI_RTR_MARKIT_NAT_EUR_PL).difference(set(Forth_NNI_RTR_MARKIT_NAT_EUR_PL),set(Fifth_NNI_RTR_MARKIT_NAT_EUR_PL),set(Sixth_NNI_RTR_MARKIT_NAT_EUR_PL)))

Missing_MARKIT_NAT_USA=list(set(Forth_NNI_RTR_MARKIT_NAT_USA_PL).difference(set(Fifth_NNI_RTR_MARKIT_NAT_USA_PL),set(Sixth_NNI_RTR_MARKIT_NAT_USA_PL),set(Seventh_NNI_RTR_MARKIT_NAT_USA_PL)))
Missing_MARKIT_NAT_USA1=list(set(Fifth_NNI_RTR_MARKIT_NAT_USA_PL).difference(set(Forth_NNI_RTR_MARKIT_NAT_USA_PL),set(Sixth_NNI_RTR_MARKIT_NAT_USA_PL),set(Seventh_NNI_RTR_MARKIT_NAT_USA_PL)))
Missing_MARKIT_NAT_USA2=list(set(Sixth_NNI_RTR_MARKIT_NAT_USA_PL).difference(set(Forth_NNI_RTR_MARKIT_NAT_USA_PL),set(Fifth_NNI_RTR_MARKIT_NAT_USA_PL),set(Seventh_NNI_RTR_MARKIT_NAT_USA_PL)))
Missing_MARKIT_NAT_USA3=list(set(Seventh_NNI_RTR_MARKIT_NAT_USA_PL).difference(set(Forth_NNI_RTR_MARKIT_NAT_USA_PL),set(Fifth_NNI_RTR_MARKIT_NAT_USA_PL),set(Sixth_NNI_RTR_MARKIT_NAT_USA_PL)))

Missing_MARKIT_NATIVE_EUR=list(set(Forth_NNI_RTR_MARKIT_NATIVE_EUR_PL).difference(set(Fifth_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Sixth_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Seventh_NNI_RTR_MARKIT_NATIVE_EUR_PL)))
Missing_MARKIT_NATIVE_EUR1=list(set(Fifth_NNI_RTR_MARKIT_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Sixth_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Seventh_NNI_RTR_MARKIT_NATIVE_EUR_PL)))
Missing_MARKIT_NATIVE_EUR2=list(set(Sixth_NNI_RTR_MARKIT_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Fifth_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Seventh_NNI_RTR_MARKIT_NATIVE_EUR_PL)))
Missing_MARKIT_NATIVE_EUR3=list(set(Seventh_NNI_RTR_MARKIT_NATIVE_EUR_PL).difference(set(Forth_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Fifth_NNI_RTR_MARKIT_NATIVE_EUR_PL),set(Sixth_NNI_RTR_MARKIT_NATIVE_EUR_PL)))

Missing_MARKIT_NATIVE_USA=list(set(Forth_NNI_RTR_MARKIT_NATIVE_USA_PL).difference(set(Fifth_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Sixth_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Seventh_NNI_RTR_MARKIT_NATIVE_USA_PL)))
Missing_MARKIT_NATIVE_USA1=list(set(Fifth_NNI_RTR_MARKIT_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Sixth_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Seventh_NNI_RTR_MARKIT_NATIVE_USA_PL)))
Missing_MARKIT_NATIVE_USA2=list(set(Sixth_NNI_RTR_MARKIT_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Fifth_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Seventh_NNI_RTR_MARKIT_NATIVE_USA_PL)))
Missing_MARKIT_NATIVE_USA3=list(set(Seventh_NNI_RTR_MARKIT_NATIVE_USA_PL).difference(set(Forth_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Fifth_NNI_RTR_MARKIT_NATIVE_USA_PL),set(Sixth_NNI_RTR_MARKIT_NATIVE_USA_PL)))

print('='*90)

if len(Missing_IHS_NAT_EUR) == 0 and len(Missing_IHS_NAT_EUR1) == 0 and len(Missing_IHS_NAT_EUR2) == 0 and len(Missing_IHS_NAT_EUR3) == 0:
     print('='*95)
     print('L-IHS NATTED Prefixes Of EU Region are Same across all L-IHS NNI Routers!!!')
elif len(Missing_IHS_NAT_EUR) > 0:
     print('Missing L-IHS EU Region NATTED Prefixes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NAT_EUR)):
         print(Missing_IHS_NAT_EUR[i])
elif len(Missing_IHS_NAT_EUR1) > 0:
     print('Missing L-IHS EU Region NATTED Prefixes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NAT_EUR1)):
         print(Missing_IHS_NAT_EUR1[i])
elif len(Missing_IHS_NAT_EUR2) > 0:
     print('Missing L-IHS EU Region NATTED Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NAT_EUR2)):
         print(Missing_IHS_NAT_EUR2[i])
elif len(Missing_IHS_NAT_EUR3) > 0:
     print('Missing L-IHS EU Region NATTED Prefixes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_IHS_NAT_EUR3)):
         print(Missing_IHS_NAT_EUR3[i])

if len(Missing_IHS_NAT_USA) == 0 and len(Missing_IHS_NAT_USA1) == 0 and len(Missing_IHS_NAT_USA2) == 0 and len(Missing_IHS_NAT_USA3) == 0:
     print('='*95)
     print('L-IHS NATTED Prefixes Of US Region are Same across all L-IHS NNI Routers!!!')
elif len(Missing_IHS_NAT_USA) > 0:
     print('Missing L-IHS US Region NATTED Prefixes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NAT_USA)):
         print(Missing_IHS_NAT_USA[i])
elif len(Missing_IHS_NAT_USA1) > 0:
     print('Missing L-IHS US Region NATTED Prefixes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NAT_USA1)):
         print(Missing_IHS_NAT_USA1[i])
elif len(Missing_IHS_NAT_USA2) > 0:
     print('Missing L-IHS US Region NATTED Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NAT_USA2)):
         print(Missing_IHS_NAT_USA2[i])
elif len(Missing_IHS_NAT_USA3) > 0:
     print('Missing L-IHS US Region NATTED Prefixes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_IHS_NAT_USA3)):
         print(Missing_IHS_NAT_USA3[i])

print('\n'*1)

if len(Missing_IHS_NATIVE_EUR) == 0 and len(Missing_IHS_NATIVE_EUR1) == 0 and len(Missing_IHS_NATIVE_EUR2) == 0 and len(Missing_IHS_NATIVE_EUR3) == 0:
     print('='*95)
     print('L-IHS NATIVE Prefixes Of EU Region are Same across all L-IHS NNI Routers!!!')
elif len(Missing_IHS_NATIVE_EUR) > 0:
     print('Missing L-IHS EU Region NATIVE Prefixes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_EUR)):
         print(Missing_IHS_NATIVE_EUR[i])
elif len(Missing_IHS_NATIVE_EUR1) > 0:
     print('Missing L-IHS EU Region NATIVE Prefixes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_EUR1)):
         print(Missing_IHS_NATIVE_EUR1[i])
elif len(Missing_IHS_NATIVE_EUR2) > 0:
     print('Missing L-IHS EU Region NATIVE Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_EUR2)):
         print(Missing_IHS_NATIVE_EUR2[i])
elif len(Missing_IHS_NATIVE_EUR3) > 0:
     print('Missing L-IHS EU Region NATIVE Prefixes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_EUR3)):
         print(Missing_IHS_NATIVE_EUR3[i])

if len(Missing_IHS_NATIVE_USA) == 0 and len(Missing_IHS_NATIVE_USA1) == 0 and len(Missing_IHS_NATIVE_USA2) == 0 and len(Missing_IHS_NATIVE_USA3) == 0:
     print('='*95)
     print('L-IHS NATIVE Prefixes Of US Region are Same across all L-IHS NNI Routers!!!')
elif len(Missing_IHS_NATIVE_USA) > 0:
     print('Missing L-IHS US Region NATIVE Prefixes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_USA)):
         print(Missing_IHS_NATIVE_USA[i])
elif len(Missing_IHS_NATIVE_USA1) > 0:
     print('Missing L-IHS US Region NATIVE Prefixes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_USA1)):
         print(Missing_IHS_NATIVE_USA1[i])
elif len(Missing_IHS_NATIVE_USA2) > 0:
     print('Missing L-IHS US Region NATIVE Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_USA2)):
         print(Missing_IHS_NATIVE_USA2[i])
elif len(Missing_IHS_NATIVE_USA3) > 0:
     print('Missing L-IHS US Region NATIVE Prefixes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_IHS_NATIVE_USA3)):
         print(Missing_IHS_NATIVE_USA3[i])

print('\n'*1)

if len(Missing_MARKIT_NAT_EUR) == 0 and len(Missing_MARKIT_NAT_EUR1) == 0 and len(Missing_MARKIT_NAT_EUR2) == 0 and len(Missing_MARKIT_NAT_EUR3) == 0:
     print('='*95)
     print('Markit NATTED Prefixes Of EU Region are Same across all L-IHS NNI Routers!!!')
elif len(Missing_MARKIT_NAT_EUR) > 0:
     print('Missing MARKIT EU Region NATTED Prefixes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_EUR)):
         print(Missing_MARKIT_NAT_EUR[i])
elif len(Missing_MARKIT_NAT_EUR1) > 0:
     print('Missing MARKIT EU Region NATTED Prefixes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_L-IHS_NAT_EUR1)):
         print(Missing_MARKIT_NAT_EUR1[i])
elif len(Missing_MARKIT_NAT_EUR2) > 0:
     print('Missing MARKIT EU Region NATTED Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_EUR2)):
         print(Missing_MARKIT_NAT_EUR2[i])
elif len(Missing_MARKIT_NAT_EUR3) > 0:
     print('Missing MARKIT EU Region NATTED Prefixes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_EUR3)):
         print(Missing_MARKIT_NAT_EUR3[i])


if len(Missing_MARKIT_NAT_USA) == 0 and len(Missing_MARKIT_NAT_USA1) == 0 and len(Missing_MARKIT_NAT_USA2) == 0 and len(Missing_MARKIT_NAT_USA3) == 0:
     print('='*95)
     print('MARKIT NATTED Prefixes Of US Region are Same across all MARKIT NNI Routers!!!')
elif len(Missing_MARKIT_NAT_USA) > 0:
     print('Missing MARKIT US Region NATTED Prefixes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_USA)):
         print(Missing_MARKIT_NAT_USA[i])
elif len(Missing_MARKIT_NAT_USA1) > 0:
     print('Missing MARKIT US Region NATTED Prefixes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_USA1)):
         print(Missing_MARKIT_NAT_USA1[i])
elif len(Missing_MARKIT_NAT_USA2) > 0:
     print('Missing MARKIT US Region NATTED Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_USA2)):
         print(Missing_MARKIT_NAT_USA2[i])
elif len(Missing_MARKIT_NAT_USA3) > 0:
     print('Missing MARKIT US Region NATTED Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_MARKIT_NAT_USA3)):
         print(Missing_MARKIT_NAT_USA3[i])

print('\n'*1)

if len(Missing_MARKIT_NATIVE_EUR) == 0 and len(Missing_MARKIT_NATIVE_EUR1) == 0 and len(Missing_MARKIT_NATIVE_EUR2) == 0 and len(Missing_MARKIT_NATIVE_EUR3) == 0:
     print('='*95)
     print('MARKIT NATIVE Prefixes Of EU Region are Same across all MARKIT NNI Routers!!!')
elif len(Missing_MARKIT_NATIVE_EUR) > 0:
     print('Missing MARKIT EU Region NATIVE Prefixes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_EUR)):
         print(Missing_MARKIT_NATIVE_EUR[i])
elif len(Missing_MARKIT_NATIVE_EUR1) > 0:
     print('Missing MARKIT EU Region NATIVE Prefixes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_EUR1)):
         print(Missing_MARKIT_NATIVE_EUR1[i])
elif len(Missing_MARKIT_NATIVE_EUR2) > 0:
     print('Missing MARKIT EU Region NATIVE Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_EUR2)):
         print(Missing_MARKIT_NATIVE_EUR2[i])
elif len(Missing_MARKIT_NATIVE_EUR3) > 0:
     print('Missing MARKIT EU Region NATIVE Prefixes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_EUR3)):
         print(Missing_MARKIT_NATIVE_EUR3[i])
print('='*90)

if len(Missing_MARKIT_NATIVE_USA) == 0 and len(Missing_MARKIT_NATIVE_USA1) == 0 and len(Missing_MARKIT_NATIVE_USA2) == 0 and len(Missing_MARKIT_NATIVE_USA3) == 0:
     print('='*95)
     print('MARKIT NATIVE Prefixes Of US Region are Same across all MARKIT NNI Routers!!!')
elif len(Missing_MARKIT_NATIVE_USA) > 0:
     print('Missing MARKIT US Region NATIVE Prefixes of UK-WOK01-NNI01 in ' + Host_Name5 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_USA)):
         print(Missing_MARKIT_NATIVE_USA[i])
elif len(Missing_MARKIT_NATIVE_USA1) > 0:
     print('Missing MARKIT US Region NATIVE Prefixes of UK-WOK01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name6 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_USA1)):
         print(Missing_MARKIT_NATIVE_USA1[i])
elif len(Missing_MARKIT_NATIVE_USA2) > 0:
     print('Missing MARKIT US Region NATIVE Prefixes of US-VWC01-NNI01 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name7 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_USA2)):
         print(Missing_MARKIT_NATIVE_USA2[i])
elif len(Missing_MARKIT_NATIVE_USA3) > 0:
     print('Missing MARKIT US Region NATIVE Prefixes of US-VWC01-NNI02 in ' + Host_Name4 + ' & ' + Host_Name5 + ' & ' + Host_Name6 + ' are below:')
     for i in range(len(Missing_MARKIT_NATIVE_USA3)):
         print(Missing_MARKIT_NATIVE_USA3[i])

print('='*90)
