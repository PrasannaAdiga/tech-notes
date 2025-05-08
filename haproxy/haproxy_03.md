## Access Control List (ACL)

Conditional we can call a backend based on true or false the condition results to. We can write ACL in two ways
- First way
```
acl is_static path -i -m beg /static/ # define a ACL condition
use_backend be_static if is_static # use the ACL, this will be executed if the condition is true
```
- Second way
```
use_backend be_static if { path -i -m beg /static/ } # anonymous access list
```

![stack_heap](images/08.drawio.png "icon")

### Examples
```
frontend  web_application
    acl web1 path_beg /campground
    acl web1 path_end 607e50e61030b115b6f92b30 # web1 is true if request path begins with `campground OR request path ends with `607e50e61030b115b6f92b30`
    

    acl web2 path_reg 196$
    acl web2 path_sub -i edit # web2 is true of request path begins with `campground OR request path ends with `607e50e61030b115b6f92b30`

    use_backend web2 if web2 # if web2 acl is true, use web2 backend
    use_backend web1 if web1 # if web1 acl is true, use web1 backend
    default_backend     web1 # if both of the acl does not match, then use web1 backend as default
    bind *:80

backend web1
    balance     roundrobin
    server      web1 10.0.1.20:3000 check 

backend web2
    balance     roundrobin
    server      web2 10.0.1.30:3000 check
```