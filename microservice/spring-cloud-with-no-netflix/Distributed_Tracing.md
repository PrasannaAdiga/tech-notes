## Distributed Tracing
By using Spring Cloud Sleuth and Zipkin

 - To trace microservices communication and to find out the slow microservices through analyzing their total time taken to process each request
 - Spring Cloud Sleuth will automatically add unique trace id and span id for each request which span across multiple microservices into log files. So logs can be aggregated and used to trace message easily across services 
 - Zipkin also provides an option to visualize the data flow between multiple microservice
 - Later zipkin will provide a graphical user interface where each of these request can be visualized
 - Trace id will be unique across the entire request/response flow, where span id will be unique between each microservice calls which represents a single unit of work
 - Add 'spring-cloud-sleuth-zipkin' dependency in each microservice including gateway server except the config and consul server
 - Sleuth can send all the data to Kafka instead of directly to Zipkin server, thus we can decouple both the sevices
 - Configure below settings in each microservice, which tells send the trace id and span id to mentioned Zipkin server URL over http protocol
 ```
 spring:
   zipkin:
     base-url: http://localhost:9411
     sender:
       type: web #Sendig the data through http protocol to zipkin
   sleuth:
     sampler:
       probability: 1 #How much percentage of data should send to zipkin
 ```
#### Zipkin server
 - Use the below docker command to run the Zipkin server locally:
 ```
 docker run -d -p 9411:9411 openzipkin/zipkin
 ```
 - Access the zipkin server at the url: http://localhost:9411 
