## HAProxy

### Install HAProxy in MAC M1

1. Install homebrew
2. Install haproxy through homebrew '`brew install haproxy`
3. It installs the haproxy under the directory `/opt/homebrew/opt/haproxy`


### Configure and Test HAProxy
1. create a new file `haproxy.cfg` file under the path `/opt/homebrew/etc`
2. Add the below content into the above haproxy.cfg file
```
defaults
    mode http
    timeout client 10s
    timeout connect 5s
    timeout server 10s
    timeout http-request 10s
frontend my_frontend
    bind 127.0.0.1:80
    default_backend my_backend
backend my_backend
    balance roundrobin
    server server1 127.0.0.1:8001
    server server2 127.0.0.1:8002
```
3. Open 2 separate terminal window and run  below 2 simple servers through python 
```
python3 -m http.server 8001 --bind 127.0.0.1
```
```
python3 -m http.server 8002 --bind 127.0.0.1
```
4. Run haproxy through command `sudo haproxy -f haproxy.cfg`

5. In a third terminal window, send a request to haproxy listener port(i.e 80) confirm the connection works. Or open a browser and make a call to `localhost`
```
curl 127.0.0.1
```
6. Run the above curl command multiple times and check the logs of both python server. Request will be evenly distributed between these 2 available servers. 


### Links
- https://phoenixnap.com/kb/haproxy-load-balancer
- https://serversforhackers.com/c/load-balancing-with-haproxy
- https://ahmedyusuf.medium.com/installing-haproxy-on-osx-mojave-e49b048d063c