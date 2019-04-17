#!/usr/bin/python3
"""paramiko with SFTP and SSH | matthew.wamsley@verizon.com"""

#standard python lib
import warnings

##3 party libs
import paramiko


#filter the paramiko warning
warnings.filterwarnings(action='ignore',module='.*paramiko.*')


##define servers we want to connect to
usercreds = [{'un': 'bender', 'ip': '10.10.2.3'}, {'un': 'fry', 'ip': '10.10.2.4'}, {'un': 'zoidberg', 'ip': '10.10.2.5'}]


##loop through server we want to connect to
for fc in usercreds:
    #mytransport = paramiko.Transport(fc['ip'], 22)
    #mytransport.connect(username=fc['un'], password='alta3')
    #sftp = paramiko.SFTPClient.from_transport(mytransport)
    sshsession = paramiko.SSHClient()
    ##go grab an SSH key
    mykey = paramiko.RSAKey.from_private_key_file("/home/student/.ssh/id_rsa")
    ## Skips the warning that says "this fingerprint looks new" (authorized_hosts)
    sshsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    sshsession.connect(hostname=fc['ip'], username=fc['un'], pkey=mykey)

    sftp=sshsession.open_sftp()
    
    ## move mybash.sh to each server
    sftp.put('mybash.sh', '/tmp/mybash.sh')
    
    #sftp.close()
    #mytransport.close()

    #sshsession = paramiko.SSHClient()
    ##go grab an SSH key
    #mykey = paramiko.RSAKey.from_private_key_file("/home/student/.ssh/id_rsa")
    ## Skips the warning that says "this fingerprint looks new" (authorized_hosts)
    #sshsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #sshsession.connect(hostname=fc['ip'], username=fc['un'], pkey=mykey)
    
    ## exucute mybash.sh
    ssh_in, ssh_out, ssh_err = sshsession.exec_command('cd /tmp; bash mybash.sh')
    print(ssh_out.read().decode('utf-8'))

    ssh_in, ssh_out, ssh_err = sshsession.exec_command('cd /tmp; ls -la')
    print(ssh_out.read().decode('utf-8'))

    ##cat file to confirm working
    
    ## close connections
    sftp.close()
    sshsession.close()
