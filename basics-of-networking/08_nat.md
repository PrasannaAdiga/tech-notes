# Network Address Translation (NAT)
How the WAN sees your internal private devices

- We have all the devices is connected to the Internet. But the problem here remains, like, how can we get more than 4 billion devices on the Internet if we have a limit of IPV4? 
- One solution is IPV6, but nobody is bringing that up because supporting a new protocol is just you need to update all the routers and it's a huge job so people start using it before so it's there.
- But how do we expose my internal thousands of devices network, you know, keeping them private while still they can access the Internet, answer is the network address translation. This provides solution for the IPV4 limitation.
- And the goal of this is you can have one public IP address, which is your gateway, and all other devices like your MAC, phone, tablet, desktop etc will be connected to this gateway, so that all of those devices will be having one single public IP address which is gateway IP address.
- But now how do they differentiate each other? The nat table lives in the gateway or router and which maps the private IP addresses, which typically starts either 10.0.. or 192.168 or 172.16 along with their corresponding random port. So NAT act as both layer 3 and 4, since it knows both Ip and Port. And each of these private devices can make at most 65000 request to the same destination since those many random port it can use and have the corresponding records in nat table.
-  So all the outgoing request will have the source IP as router's public IP and all the incoming request has destination Ip as router's IP. And then this router forward the request to a particular internal private devices depdning on the mapping records it has in its nat table.
- IPv4 is limited only 4 billion
- Private vs Public IP Address
- E.g. 192.168.x.x , 10.0.0.x is private not routable in the Internet
- Internal hosts can be assigned private addresses
- Only your router need public IP address
- Router need to translate requests

## NAT Applications

- Private to Public translations
    - So we don't run out IPv4
- Port forwarding
    - Add a NAT entry in the router to forward packets to 80 to a machine in your LAN
    - No need to have root access to listen on port 80 on your device
    - Expose your local web server publicly
- Layer 4 Load Balancing
    - HAProxy NAT Mode - Your load balancer is your gateway
    - Clients send a request to a bogus service IP
    - Router intercepts that packet and replaces the service IP with a destination server
    - Layer 4 reverse proxying

## Port Forwarding
- A technique used to allow external devices access to computer services within a private network.
    - Example: Web server in your home network.
- Map an external IP address port number to a specific internal IP address and
port number.
    - Example: Forward all port 80 requests to your public router IP address to your web server in your home network.

## Access Control Lists (ACLs)
- Access Control Lists are a network security feature used to create allow/deny network rules to filter network traffic.
- They can be set for both incoming and outgoing traffic on a variety of devices, such as:
    - Routers 
    - Firewalls
    - Proxy Servers 
    - End-Devices

![stack_heap](images/nat.drawio.png "icon") 

