# VPC Connectivity Options

There are many ways where we can connect multiple VPCs, which are:
- VPC Endpoints & PrivateLink (To access other AWS services privately from your single VPC)
- VPC Peering connection (To access other VPCs privately from your VPC - One to One mapping)
- Transit Gateway (To access other VPCs privately from your VPC - One to Many mapping)
- Site-2-Site VPN (hybrid network - to connect on-premise network with AWS network)
- Client VPN (hybrid network - to connect single client machine with AWS network)
- Direct Connect

## VPC Endpoints(of type Gateway)

- Consider a scenario where we deployed on application in an EC2 instance which resides in one of the private subnet of VPC. So this instance can not talk to internet, since it resides inside a private subnet and also there is no NAT gateway/instance. 
- Now this application needs to process some data from S3 bucket which is a storage service for image/files/video, so it needs the access to S3 bucket which exists in the same region where VPC resides.
- Now the EC2 instance can not access this S3 bucket over the internet. One way it to have NAT gateway and Internet Gateway to access it over the internet. But since both S3 and EC2 instance resides in the AWS service, we can use VPC endpoint to access.

## VPC Endpoints(of type interface) or PrivateLink
- Now we can access other AWS services like SQS, SNS etc through VPC endpoint of type interface. This connectivity between VPC and AWS services is also called PrivateLink.
- Sometime we want to access some third party services, like may be some SaaS applications, or you are providing your services privately to your customers etc.
- Now one option is to expose these kind of applications over internet and other user can consume it over the internet.
- But lets say these services also resides inside AWS some other VPCs, and we have our own VPC which wants to consume this service. In these scenario, AWS provices a way to privately access these services, through VPC endpoint of type interface or private link.

## VPC Peering Connection
- From within same organization we might have different VPCs where different services are running which are managed by different teams. Also, if your customer deploys their applications in AWS, they also have their VPCs in AWS.
- Now these EC2 instances which are running in these VPCs needs to talk to each other. These VPCs may be in the same region or different region. One option is to expose these application over the internet by placing it in public subnet and IG, and then anybody can access it. But we dont want to do this, since these applications are private to company and can be accessible only by your company. 
- So by using VPC peering we can connect 2 VPC privately without exposing them to internet. As soon as we connect 2 VPCs any EC2 instances can communicate across these 2 VPCs by using private IP addresses of the instances. We dont need to have them in public subnet or have public IP addresses. 
- VPC peering are not transitive in nature, so only those VPCs which has direct VPC peering can communicate between each other.

## Transist Gateway
- VPC peering works well if there there are couple of VPCs. But if your org has many VPCs then usage of VPC peering is not effective since we need one VPC peering between each of the 2 VPCs.
- Instead we use one single transist gateway and all other VPCs will connect to this TG. By this way any instances can talk to each other accross these VPCs by using private IP of the instances.
- But there will be some additional cost for this TG
- TG is not just to connect VPCs. It has more options than this.
- We can connect VPN to a TG so that your On-premise network also can communicate with multiple VPCs. If there is no TG, and you want to access your VPC from on-premise network, then you would have to have multiple VPN connection to individual VPCs. But with the combination of TG and one single VPN we can greatly reduce our architecture. 
- And finally TG can also be peered across AWS regions. We can connect multiple TG which exists in different regions so that all the VPCs can talk to each other privately. So TG are regional router, which means TG can not connect to VPC in different regions, instead we can create another TG in other regions and peer them together. 

## Site to site VPN
- Site to site VPN is used as a hybrid network, which means to connect your on-premise network with AWS network. 
- If we have any application running in a private subnet and we dont want to expose them over the internet and we want to access this application in our on-premise network then we can use this site to site VPN connection and access these applications privately. This is like extending your on-premise network to AWS.

## Client to site VPN

- Site to site VPN is to connect 2 networks, where as client to site VPN is to connect your single client to AWS network privately. This also used as a hybrid network.
- For example, suppose you are working in home and you want to access the private resources which are inside your corporate network, then we need to connect to company VPN and access those resources. 
- Exactly we do in AWS, VPC is a private network and we create a `client VPN endpoint` and then connect to this endpoint from our client machine to access the resources privately.  

## Direct Connect
- It is a physical Layer1 network(not a virtual network) from AWS to your on-premise data center. If you want to access your AWS network from within on-primises network either you access it over the internet, or you access it over the site to site VPN connection. But this VPN connection also goes over the internet, just that the entire trafic is encrypted ans thats why it is secured. 
- But for the large organization they have huge workloads both in AWS and on-prmises, and they need a consistent and high bandwidth network between them. For this we need a dedicated network between them and Direct Connect is the solution for it.
- For this we need to work with Direct Connection partner where we setup physical connection between your data center and the `direct connect location` and there is already connectin established between `direct connect location` and AWS region in which we have our workloads.  

![stack_heap](images/vpc-connection-options.drawio.png "icon")
