#Get configuration files
import paramiko
import time

#Create connection variables
user = 'cisco'
password = 'cisco'
enable_password = 'cisco1'
port = 22

#Define pathes for backups and file with list of devices
folderconf = "c:\\temp\\conf\\"
devicelist = "devices.txt"

#Open file with device
input_file = open( folderconf + devicelist, "r")

#Loop through device list and execute
for ip in input_file.readlines():
    ipaddr = ip.strip()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipaddr, port, user, password, look_for_keys=False, allow_agent=False)
    chan = ssh.invoke_shell()
    time.sleep(2)
    chan.send('enable\n')
    chan.send(enable_password +'\n')
    time.sleep(1)
    chan.send('term len 0\n')
    time.sleep(1)
    chan.send('sh run\n')
    time.sleep(20)
    output = chan.recv(999999)
    filename = folderconf + ipaddr + ".cfg"
    f1 = open(filename, 'a')
    f1.write(output.decode("utf-8") )
    f1.close()
    ssh.close() 
    input_file.close()
