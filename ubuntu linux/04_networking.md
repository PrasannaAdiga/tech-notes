# Networking, Services and System updates

## Network components
- IP
- Subnet mask
- Gateway
- Static vs. DHCP
- Interface
- Interface MAC

## Network Files and Commands
- Interface Detection
- Assigning an IP address
- Interface configuration files
    - /etc/nsswitch.conf
    - /etc/hostname => tiny version of DNS, this file contains IP address and the corresponding hostname. So when we ping the hostname, it actually ping its corresponding IP address
    - /etc/sysconfig/network
    - /etc/sysconfig/network-scripts/ifcfg-nic 
    - /etc/resolv.conf
- NetworkCommands 
    - ping
    - ifconfig => Tells what all the interfaces defined
    - ifup or ifdown => to stop or start interfaces
    - netstat
    - tcpdump
- To get NIC information
    - ethtool enp0s3

## Download Files or Apps
- wget command
- Example: wget http://website.com/filename

## curl and ping Commands
- curl to make http request to a server which is running on some IP and Port
- ping is to check whether request can reach a specific IP
- curl http://website.com/filename
- curl –O http://website.com/filename
- ping www.google.com

## File Transfer Protocol

The File Transfer Protocol is a standard network protocol used for the transfer of computer files between a client and server on a computer network. FTP is built on a client-server model architecture using separate control and data connections between the client and the server. Default FTP Port = 21

## Secure Copy Protocol (SCP)

The Secure Copy Protocol or “SCP” helps to transfer computer files securely from a local to a remote host. It is somewhat similar to the File Transfer Protocol “FTP”, but it adds security and authentication. Default SCP Port = 22 (same as SSH).

## Remote Synchronization (rsync)

- rsync is a utility for efficiently transferring and synchronizing files within the same computer or to a remote computer by comparing the modification times and sizes of files
- rsync is a lot faster than ftp or scp
- This utility is mostly used to backup the files and directories from one server to another and can be run as a cron task
- Default rsync Port = 22 (same as SSH)

## System Updates and Repos
- yum (CentOS) => can download and install the packages over the internet
- apt-get (other Linux) => can download and install the packages over the internet
- rpm (Redhat Package Manager) => Can install the package only. Can not download. So it can be used in an env where it does not have internet access.

### Package Management
- Install a package: yum install ksh OR sudo apt-get install ksh
- Remove a package: rpm remove ksh OR sudo apt-get remove ksh
- Check for a package: rpm -qa | grep ksh(RedHat) => qa means query all OR dpkg -l | grep ksh(UBUNTU)
- To list all the configuration files of a package: rpm -qc ksh
- To check which package a command is uses: which ksh => /usr/bin/ksh
- To check whether a packge is running: systemctl status ksh
- To cehck whether a process is running: ps -aux | grep ksh

## System Upgrade/Patch Management
- Two type of upgrades happens in Linux, to update it OS
    - Major version = 5, 6, 7
    - Minor version = 7.3 to 7.4
- Example: yum update –y
- yum update vs. upgrade
    - upgrade = delete packages
    - update = preserve

## Rollback Updates and Patches
- Rollback a package or patch
    - yum install <package-name> 
    - yum history undo <id>    

## SSH and Telnet
To connect to a server system
- Telnet = Un-secured connection between computers 
- SSH = Secured

## Domain Name System (DNS)
- Hostname to IP - A Record
- IP to Hostname - PTR Record
- Hostname to Hostname - CNAME Record
- Files
    - /etc/named.conf
    - /var/named
- Service
    - systemctl restart named
- Commands used for DNS lookup  
    - nslookup
    - dig      


## Network Time Protocol(NTP)

The purpose of this service is to synchronize your computer's time to another server in case you lose your time. So in corporate environment, it becomes very very imperative that you have all your servers synchronized with one clock so the time won't shift.

- File
    - /etc/ntp.conf
- Service
    - systemctl restart ntpd
- Command 
    - ntpq

## chronyd
Latest release to replace NTP

- Purpose = Time synchronization
- Package name = chronyd
- Configuration file = /etc/chronyd.conf
- Log file = /var/log/chrony
- Service = systemctl start/restart chronyd 
- Program command = chronyd.

## sendmail

- Purpose = Send and receive emails
- Files 
    - /etc/mail/sendmail.mc
    - /etc/mail/sendmail.cf
    - /etc/mail
- Service
    - systemctl restart sendmail
- Command
    - mail –s "subject line" email@mydomain.com

## WebServer (Apache - HTTP)
- Purpose = Serve webpages
- Install = sudo apt-get install httpd
- Service or Package name = httpd
- Files 
    - /etc/httpd/conf/httpd.conf
    - /var/www/html/index.html
- Log Files = /var/log/httpd/
- Service
    - systemctl restart httpd
    - systemctl enable httpd    

## Central Logger (rsyslog)
- Purpose = Generate logs or collect logs from other servers or clients
- Service or package name = rsyslog
- Configuration file = /etc/rsyslog.conf
- Service
    - systemctl restart rsyslog 
    - systemctl enable rsyslog

## Linux OS Hardening
- User Account
- Remove un-wanted packages
- Stop un-used Services
- Check on Listening Ports
- Secure SSH Configuration
- Enable Firewall (iptables/firewalld)
- Change Listening Services Port Numbers
- Keep your OS up to date (security patching)













