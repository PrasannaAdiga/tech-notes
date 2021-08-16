# Spring Cloud
Provides the tools to quickly build some common patterns in distributed systems 

## Configuration management
By using Spring Cloud Config Server and Config Client

Register Config Server with Consul
#### Config Server
 - Add the dependency 'spring-cloud-config-server' and 'spring-cloud-starter-consul-all'
 - Add the annotation '@EnableConfigServer' into main application
 ```
 @SpringBootApplication
 @EnableConfigServer
 public class BookstoreConfigServerApplication {
 }
 ```
 - Add below configuration details to bootstrap.yml
 ```
 spring:
   cloud:
     config:
       server:
         #git:
         #uri: #Provide Git URI here if we use to connect to Git Repo
         native:
           searchLocations: classpath:/config-repo
     cloud:
       consul:
         discovery:
           instance-id: ${spring.application.name}:${random.int[1,999999]}
 ```
 - Create a new folder 'config-repo' under the path 'src/main/resources' and create different yml files for each of the microservice with corresponding microservice's application name as file name. Keep all configurations related to different profile here.
 - Also, create a common 'application.yml' file and add all the configuration details which are unique for all microservices
  
#### Config Client
 - Add the dependency 'spring-cloud-starter-config' and 'spring-retry' in each of the microservices which needs to connect to Config Server
 - Add the below configuration details in each microservice 'bootstrap.yml' file in order to connect to Config Server while booting up along with spring retry configuration(Required to make microservice to wait until config server is up and running).
 ```
 cloud:
   config:
     uri: http://localhost:8888
     fail-fast: true
     retry:
       initial-interval: 60000
       multiplier: 1.5
       max-attempts: 1000
       max-interval: 5000
 ```
 - Also, add below details in 'bootstrap.yml'. These configuration details will fetch all the available properties for the mentioned application name and profile name.
 ```
 spring:
   application:
     name: bookstore-product-service
   profiles:
     active: ${SPRING_PROFILES_ACTIVE:local_zone1}
 ```

## Service Discovery 
By Using Consul

#### Consul Server
To Create Consul Cluster using Docker follow the below steps:
 - Create a new network 'docker network create bookstore'
 - Type the command ‘docker run -d --name consul-1 -p 8500:8500 --network=bookstore -e CONSUL_BIND_INTERFACE=eth0 consul’. Here we use the common network 'bookstore' where other container also runs like Prometheus so that communication between containers will be easy by using only the container name
 - Type the command ‘docker inspect consul-1’. Copy the IP address.
 - Type the command ‘docker run -d --name consul-2 -e CONSUL_BIND_INTERFACE=eth0 -p 8501:8500 consul agent -dev -join=172.17.0.2<REPLACE THIS BY PREVIOUSLY COPIED IP ADDRESS>’
 - Type the command ‘docker run -d --name consul-3 -e CONSUL_BIND_INTERFACE=eth0 -p 8502:8500 consul agent -dev -join=172.17.0.2<REPLACE THIS BY PREVIOUSLY COPIED IP ADDRESS>’
 - Test the Consul Cluster by typing the command: ‘docker exec -t consul-1 consul members’. This will list down details of all 3 Consul nodes.
 - Access the Consul UI: http://localhost:8500/
 - Refer: https://piotrminkowski.com/2019/11/06/microservices-with-spring-boot-spring-cloud-gateway-and-consul-cluster/

#### Microservices as Consul Client
By using Spring Cloud Consul

 - Add the dependency 'spring-cloud-starter-consul-all' --> This includes both spring-cloud-consul-discovery and spring-cloud-consul-config
 - Add the below configuration in bootstrap.yml
 ```
 spring:
   application:
     name: bookstore-cart-service
 ```
- Add the below configurations in application.yml
 ```
  server:
    port: 0 -> To launch multiple instances of this microservice
      name: bookstore-cart-service

  spring:
    cloud:
      consul:
        discovery:
          instance-id: ${spring.application.name}:${random.int[1,999999]}
          health-check-path: /actuator/health -> By default this url will be selected by spring clud consul if actuator is in classpath.
                                                 We need to set permitAll permission to this endpoint if spring security is in classpath
  ```
  - Check for registered information of this service in Consul by access the Consul URL: http://localhost:8500

#### To Enable Zone Affinity Mechanism in Consul
 - Define below 2 different spring profile in each application, one for zone1 and another for zone2
 ```
 spring:
   profiles: zone1
   cloud:
     consul:
       discovery:
         instanceZone: zone1
 ---
 spring:
   profiles: zone2
   cloud:
     consul:
       discovery:
         instanceZone: zone2
 ```
- Run multiple instances of each microservice by passing environment variable '-Dspring.profiles.active' as either zone1 or zone2. This will register each microservice in their respective zones by adding the corresponding tags as zone1 or zone2 in Consul.

## API Gateway 
By using Spring Cloud Gateway

 - Spring cloud Gateway provides various functionalities like, SpringDoc OpenAPI support, Timeouts and Retries, Rate Limiting with Redis, Circuit Breaker with Resilience4j. 
 - Use API Gateway server to expose each microservice on a static port to an external client applications, as microservices will be running on random ports
 - We don’t need to register gateway in Consul discovery, because it is not accessed internally. But, we integrate Gateway server to Consul discovery as Gateway server needs to get details of running microservice instances
 - The API gateway, which is built on top of Spring Cloud Gateway uses Netty as an embedded server and is based on reactive Spring WebFlux. Also, Springdoc OpenAPI is compatible with OpenAPI 3, and supports Spring WebFlux, while SpringFox is not.
 - If the Zone Affinity Mechanism in Consul is enabled, then we can run multiple instances of API Gateway in each zones
 - Add the dependencies 'spring-cloud-starter-gateway', 'spring-cloud-starter-consul-all' and 'spring-boot-starter-actuator'. If we add spring-boot-actuator, there will be new endpoint '/actuator/gateway' added by spring-cloud-gateway.
 - We can define multiple spring profiles corresponding to each zone in API Gateway
 ```
 spring:
   profiles: zone1
   cloud:
     consul:
       discovery:
         instanceZone: zone1
         register: false
         registerHealthCheck: false
         tags: zone=zone1
 server:  
   port: ${PORT:8080}
 ```
 - To enable integration with Consul discovery, set the below property
 ```
 spring:
   cloud:
     gateway:
       discovery:
         locator:
           enabled: true
 ```
 - Then we can define multiple Route definition for each microservice. By default, Spring Cloud Gateway uses Spring Cloud Load Balancer for load balancing.
 - Run multiple instances of gateway server by passing environment variable '-Dspring.profiles.active' as either zone1 or zone2. This will create different gateway server in their respective zones by adding the corresponding tags as zone1 or zone2 in Consul.
 - Now we can be sure that each incoming request to gateway server started in zone1 would be forwarded to only those microservices which are also having the tag of 'zone1'. And the same for Zone2.
 - To access gateway server running on port 8080(zone1)/9080(zone2): http://localhost:<port>/<service-name-defined-in-gateway-server>/<service-path>
 - To support the CORS in API Gateway, add the below configuration in the application.yml file. With this configuration, client applications can call any of the back end REST APIs through API Gateway Server
 ```
 spring:
   cloud:
     gateway:
       globalcors:
         cors-configurations:
           '[/**]':
             allowedOrigins: "*"
             allowedHeaders:
               - x-requested-with
               - authorization
               - Content-Type
               - Content-Length
               - Authorization
               - credential
               - X-XSRF-TOKEN
             allowedMethods:
               - GET
               - POST
               - PUT
               - DELETE
               - OPTIONS
               - PATCH
             maxAge: 7200
 ```

#### Gateway Actuator Endpoint
 - If we add the dependency 'spring-boot-starter-actuator', cloud gateway will provide additional endpoint '/gateway/routes'
 - To enable this, add the below property in application yml file along with other endpoint names:
 ```
 management:
   endpoints:
     web:
       exposure:
         include: gateway
 ```
 - This endpoint provides information on the configured route, uri, predicate, filter definitions
 
#### SpringDoc OpenAPI
 - It is possible to group all available micro services OpenAPI documentations in Spring Cloud Gateway and show all of them under a single service endpoint.
 - For that, add the dependencies 'springdoc-openapi-webflux-ui' in cloud gateway project
 - Add a new Route definition for the path '/v3/api-docs/**' in application yml file
 ```
 - id: openapi
   uri: http://localhost:${server.port}
   predicates:
     - Path=/v3/api-docs/**
   filters:
     - RewritePath=/v3/api-docs/(?<path>.*), /$\{path}/v3/api-docs
 ```
 - Finally, create a new Bean, which will provide the list of GroupedOpenApi. In this Bean configuration, we loop through Route definition of each micro service and add their corresponding spring doc open api rest endpoints into a list of GroupedOpenApi. Add this list into Swagger UI as a Group which will display a dropdown from where we can select any one of the microservice name and see their corresponding api docs.
 ```
 @Configuration
 public class OpenAPIResourceConfig {
     @Autowired
     RouteDefinitionLocator locator;
     @Bean
     public List<GroupedOpenApi> apis(SwaggerUiConfigParameters swaggerUiConfigParameters, RouteDefinitionLocator locator) {
         List<GroupedOpenApi> groups = new ArrayList<>();
         List<RouteDefinition> definitions = locator.getRouteDefinitions().collectList().block();
         definitions.stream().filter(routeDefinition -> routeDefinition.getId().matches(".*-service") &&
                 !routeDefinition.getId().contains("DiscoveryClient")).forEach(routeDefinition -> {
             String name = routeDefinition.getId().replaceAll("-service", "");
             swaggerUiConfigParameters.addGroup(name);
             groups.add(GroupedOpenApi.builder().pathsToMatch("/" + name + "/**").group(name).build());
         });
         return groups;
     }
 }
 ```

#### Timeouts and Retries in Gateway
##### Retry
 - By default, spring cloud gateway provides Retry filter. To activate this filter, provide either default or custom filter for each microservice in the route config definition
 ```
 filters:
   - RewritePath=/bookstore-address/(?<path>.*), /$\{path}
   - name: Retry (name of the filer)
     args:
       retries: 3 (number of retries)
       series: SERVER_ERROR (For 3XX, 4XX or 5XX series of error)
       statuses: SERVICE_UNAVAILABLE,GATEWAY_TIMEOUT,BAD_GATEWAY (For specific error status)
       exceptions: (For specific exception classes)
         - org.springframework.cloud.gateway.support.NotFoundException
         - org.springframework.cloud.gateway.support.TimeoutException
         - IOException
       methods: GET,POST,PUT,DELETE,PATCH (For specific method)
       backoff: (Delay while calling the api for each retry)
         firstBackoff: 10ms
         maxBackoff: 50ms
         factor: 2
         basedOnPreviousValue: false
 ```
 - If we mention '-name: Retry', then default Mechanism will be applied
##### Timeout
 - To set the global http call timeouts, use the below configurations in the application yml file
 ```
 spring:
   cloud:
     gateway:
       httpclient:
         connect-timeout: 1000
         response-timeout: 5s 
 ```   
 - To configure, per each route definition use the below setting
 ```
 - id: per_route_timeouts
   metadata:
     response-timeout: 200
     connect-timeout: 200
 ```

#### Circuit Breaker in Gateway

#### Rate Limiting in Gateway with Redis

#### Logging filter in Gateway

#### Validate JWT Access token in Gateway

  
## Inter Service Communication 
Along with Client Side Load Balancer, Circuit Breaker and Retry

By Using Spring Cloud OpenFeign with Spring Cloud LoadBalancer(as a Load Balancer) and spring-cloud-starter-circuitbreaker-resilience4j(as a Circuit Breaker)  

 - Add the dependency 'spring-cloud-starter-openfeign', 'spring-cloud-loadbalancer'
 - If Circuit Breaker functionality is needed add the dependency 'spring-cloud-starter-circuitbreaker-resilience4j'. Also, aadd the dependency 'resilience4j-micrometer' along with 'spring-boot-actuator', which will provide additional metrics related to resilience4j.
 - The OpenFeign will auto-integrate with service discovery like Consul, if 'spring-cloud-starter-consul-all' is in the classpath to get the details of running micro service instances
 - To use it we need to declare an interface with required methods for communication. Method signature must be similar to the one which is defined in the actual microservice.
 - The interface has to be annotated with @FeignClient that points to the service using its discovery name as registered in Consul.
 ```
 @FeignClient("bookstore-address-service")
 public interface AddressFeignClient { 
     @GetMapping("/v1/billing-addresses/{id}")
     BillingAddressResponse getBillingAddressById(@PathVariable("id") String id);
 }
 ```
 - Also, we can define the User Access token as a Request Parameter in Feign Interface Definition Methods. And then pass the actual user access token when we call this API from any services. 
 ```
 ProductResponse getProductById(@RequestHeader(value = "Authorization", required = true) String accessToken, @PathVariable("id") String id);
 ```
 - Also, we can write custom exception for Feign Exception and global handler for the same.
 - We can keep all the properties of this library in Config Server
 - Note that, if we add Circuit Breaker support, then Retry and ErrorDecoder functionality of Open Feign will not work with the current Open Feign version since, Circuit Breaker will break the call without retrying the call and respond with dummy data which is implemented in the Fallback Handler methods. So, do not use Circuit Breaker if we need to have Open Feign Retry and Error Handler mechanism.

### Load Balancer
 - Spring Cloud OpenFeign can use Spring Cloud LoadBalance as a client side load balancer, if it exists in the classpath, and the ribbon load balancer disabled.
 ```
 spring:
   cloud:
     loadbalancer:
       ribbon:
         enabled: false
 ```

### Circuit Breaker
 - Spring Cloud OpenFeign uses Resilience4j as Circuit Breaker if 'spring-cloud-starter-circuitbreaker-resilience4j' is in the classpath, Hystrix is disabled and the below configuration set:
 ```
 feign:
   circuitbreaker:
     enabled: true
   hystrix:
     enabled: false
 ```
 - To implement Fallback method for Circuit Breaker, the above plugin provides FallbackFactory interface, which can be implemented to provide default handler and can catch and throw the Actual Cause of the Client Calls
 - Below is such Custom FallbackFactory classes and Handlers:
 ```
 @Component
 public class ProductClientFactory implements FallbackFactory<ProductClientHandler> {
     @Override
     public ProductClientHandler create(Throwable cause) {
         return new ProductClientHandler();
     }
 }

 public class ProductClientHandler implements ProductFeignClient {
     @Override
     public ProductResponse getProductById(String id) {
         return ProductResponse.builder()
                 .availableCount(10)
                 .build();
     }
 }
 ```
 - And, finally tell Feign Client to use this Fallback method on failure:
 ```
 @FeignClient(name = "${address.service.name:bookstore-address-service}",
         fallbackFactory = AddressClientFactory.class)
 public interface AddressFeignClient {
 }
 ```

### Retry
 - To implement retry mechanism for the failure calls for a specific number of times, if the target service is down or unable to respond.
 - For that, create a custom Retry class and configure it as below:
 ```
 package com.learning.bookstore.retry;
 @Component
 public class FeignClientRetry extends Retryer.Default {
     public FeignClientRetry() {
         super();
     }
 }
 ----------------
 application.yml:
 feign:
   client:
     config:
       default:
         retryer: com.learning.bookstore.retry.FeignClientRetry
 ``` 
 - Here we are using Default Retry which retries 5 number of times for failed client calls, and if all retry fails then calls the fallback process to handle the failure 
 
### Error Decoder
 - We can also, write custom error decoder where, we can extract the status code of the error and then accordingly throw RetryableException exception which will trigger Retry mechanism or else can bubble the exception which will be finally handled by Fallback Handlers.
 ```
 @Component
 public class FeignClientErrorDecoder implements ErrorDecoder {
     private final ErrorDecoder defaultErrorDecoder = new Default();
     @Override
     public Exception decode(String s, Response response) {
         Exception exception = defaultErrorDecoder.decode(s, response);
         if(response.status() == HttpStatus.INTERNAL_SERVER_ERROR.value()){
            return new RetryableException(HttpStatus.INTERNAL_SERVER_ERROR.value(), "500 Internal Server error",
                   response.request().httpMethod(), null, null );
         }
         return exception;
     }
 }
 ----------------
  application.yml:
  feign:
    client:
      config:
        default:
          retryer: com.learning.bookstore.decoder.FeignClientErrorDecoder
 ``` 

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

##Distributed Log Aggregator
To aggregate the logger data from different micro services into one place for analyzing purpose

 - Use the tools like Logstash-logback-encoder, logback-access-spring-boot-starter, Logstash, Elastic Search and Kibana
 
#### Logstash-logback-encoder 
To store the logback log information which are defined in the application logic, into a physical log file, in a structured format lke JSON or to append the log data into Console in a specific pattern
 - If 'logstash-logback-encoder' plugin is in the classpath, it will read the appender details to Logstash which are defined in the 'logback-spring.xml' file and generates a local physical file which contains all the logs data of the application, in a specific format which is required by Logstash
 - Further, details of the 'logback-spring.xml' file provided in the below logback section

#### logback-access-spring-boot-starter
To store the logback application access information into a physical log file, in a structured format lke JSON or to append the log data into Console in a specific pattern
 - This plugin provides HTTP logging capability through logback-access module.
 - logback-access integrates to the servlet container of an application (Tomcat or Jetty), catches the HTTP calls and turns them into log items
 - Add the dependency 'logback-access-spring-boot-starter'
 - Create a new XML configuration file 'logback-access.xml' under the path src/resources which will be read automatically by this plugin
 - By reading this config file, 'logback-access-spring-boot-starter' plugin will add details on request data, response data, request url, response status, request and response status etc into the console or the physical file which later can be sent to Logstash 
 - Also, in this configuration file we can define some filter, which can skip adding access information of the mentioned URLs like /health API which will be called by Consul automatically for every one minute
 - Such a sample 'logback-access.xml' file can be configured as below:
 ```
 <appender name="Console" class="ch.qos.logback.core.ConsoleAppender">
     <encoder>
         <pattern>combined</pattern>
     </encoder>
 </appender>
 <appender name="LogStash" class="ch.qos.logback.core.FileAppender">
     <file>${LOGS}/${applicationName}.log</file>
     <filter class="ch.qos.logback.core.filter.EvaluatorFilter">
         <evaluator class="ch.qos.logback.access.net.URLEvaluator">
             <URL>/health</URL>
         </evaluator>
         <OnMismatch>NEUTRAL</OnMismatch>
         <OnMatch>DENY</OnMatch>
     </filter>
     <encoder class="net.logstash.logback.encoder.LogstashAccessEncoder">
         <fieldNames>
             <requestHeaders>request_headers</requestHeaders>
             <responseHeaders>response_headers</responseHeaders>
         </fieldNames>
         <lowerCaseHeaderNames>true</lowerCaseHeaderNames>
     </encoder>
 </appender>
 <appender-ref ref="Console" />
 <appender-ref ref="LogStash" />
 ```

#### Logstash
To Collect, Filter and Transform the log data

 - We can define the configuration in the logstash.conf file of Logstash
 - This file basically has three sections input, filter and output
 - Input: here we can define the path of the physical log file which is created for a microservice
 ```
 input {
   file {
     type => "bookstore-address-service-log"
     path => "/Users/prasannaadiga/Learning/Project/spring-cloud/bookstore-app/bookstore-address-service/logs/bookstore-address-service.log"
   }
 }
 ```
 - Filter: If we use logstash-logback-encoder plugin we automatically send JSOn format of log details to logsatsh. so no need to define any formatting logic in filter section. else, we can use Grok filter to split, agrreagate and transform unstructured log data to structured JSON format. 
 - And, inorder to split each key value of a JSON object into a separate data, so that later in Kibana we can see each of these data separately instead of whole json as single field and can apply better filter use the below JSON filter in filter section:
 ```
 filter {
   json {
     source => "message"
   }
 }
 ```
 - Output: This section defines host address of elastic search, and the new index details specific for this microservice logs, so that all the filtered logs can be send to Elastic seach and stored in the specific index as mentioned
 ```
 output {
   if [type] == "bookstore-address-service-log" {
     elasticsearch {
       hosts => ["https://bc4315f93c074ac995953bb0696639a9.eastus2.azure.elastic-cloud.com:9243"]
       index => "bookstore-address-service-%{+YYYY.MM.dd}"
       user => "<user name of elastic cloud of we use>"
       password => "<password of elastic cloud if we use>"
     }
   }
   stdout { codec => rubydebug }
 }
 ```
 - Logstash can be started in docker or local executable. To run in local, go to bin directory and use the command './logstash -f <full path for logstash.conf>'

#### Elastic Search
Search Engine to store and search all the log file records for analysis purpose

#### Kibana
A visual interface to search and visualize log file records, which are read from Elastic Search

## Distributed Alert and Monitoring system
To provide alert and monitoring support for all microservices
 - Use the plugins or tools like Spring-boot-actuator, Micrometer, Prometheus, Grafana
 - Metric is a measurement of a value from within the application
 - The value can be current memory usage, the number of HTTP requests, how long the HTTP requests took (latency), the number of threads in use etc

#### Monitoring System
 - Add the dependencies 'micrometer-registry-prometheus' and 'spring-boot-starter-actuator' in each micro service application
 - Add the below configurations in application.yml
 ```
 management:
   endpoints:
     web:
       base-path: /actuator
       exposure.include: prometheus
       path-mapping.prometheus: metrics
   endpoint:
     prometheus:
       cache:
         time-to-live: 1ms
 ```
 - With the above config, now we can access the metrics details at http://<host>:<port>/actuator/metrics
 - An example metric looks like: metric_name{labe1Name="label1Value",label2Name="label2Value",...}
 - Now, we have metrics exposed by our application, we need a way to pull them and keep a history of them through Prometheus, in order that: we can see historical data, we can see the data over time to calculate measures such as rates, we can query the data in an easy way

##### Prometheus 
 - Prometheus provides us functions to run more elaborate queries like rate(http_server_requests_seconds_count{uri="/doit"}[5m])
 - Prometheus can be run locally through exe file or in docker container through docker-compose file
 - To run in a docker-compose file use the below one. Here we
 ```
 version: '3.7'
 services:
   prometheus:
     image: prom/prometheus:${PROMETHEUS_VERSION:-latest}
     hostname: prometheus
     ports:
       - 9090:9090
     volumes:
       - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
       - ./prometheus:/prometheus
     networks:
       - bookstore
 networks:
   bookstore:
     name: bookstore #Run this server in the same network 'bookstore' where consul also running
 ```
 - In order to scrape/pull metrics details from each microservice we need to have 'prometheus.yml' config file.
 - In this config file we can define multiple jobs to scrape metrics from multiple microservice. like:
 ```
 scrape_configs:
   - job_name: 'bookstore-order-service'
     metrics_path: '/actuator/metrics'
     scrape_interval: 1m
     static_configs:
       - targets: ['consul-1:8080'] #Here give the conatiner name of the consul as both of these services are running in the same netwrok 'bookstore' and one container can access another through just container name
 ```
 - Or, if we use Consul as a Service Registry, then instead of defining scrape configuration for each microservice we can define Consul endpoint through 'consul_sd_configs', which will scrape automatically metrics details of all microservice which are registered in Consul 
 ```
 scrape_configs:
   - job_name: 'prometheus'
     scrape_interval: 1m
     static_configs:
       - targets: ['localhost:9090']
   - job_name: 'grafana'
     scrape_interval: 1m
     metrics_path: '/metrics'
     static_configs:
       - targets: ['grafana:3000']
   - job_name: 'consul'
     metrics_path: '/actuator/metrics'
     consul_sd_configs:
       - server: '172.17.0.1:8500'
         services: []
 ``` 
 - Finally, we can access Prometheus at the url http://localhost:9090 and see all the metrics which are scraped from each microservice

##### Grafana
 - Grafana can be run locally through exe file or in docker container through docker-compose file
 - To run in a docker-compose file use the below one. Here we
   ```
   version: '3.7'
   services:
     grafana:
       image: grafana/grafana:${GRAFANA_VERSION:-latest}
       hostname: grafana
       ports:
         - 3000:3000
       volumes:
         - ./grafana:/var/lib/grafana
       environment:
         - GF_SECURITY_ADMIN_USER=admin
         - GF_SECURITY_ADMIN_PASSWORD=admin
       networks:
         - bookstore
   networks:
     bookstore:
       name: bookstore #Run this server in the same network 'bookstore' where Prometheus and Consul running
   ```
 - Once Grafana is running, access it through the url: http://localhost:3000 
 - Connect to Prometheus DB through its IP address or domain name 'prometheus' if we run both Prometheus and Grafana in docker container
 - Finally, create multiple dashboards for each metric details or use any popular existing Grafana Dashboard available in the market 

#### Alerting System
To report an alarm message to configured destination through AlertManager

 - Configure certain rules in Prometheus on the metrics data which are collected, and if the configured rules are broken, then send an alert message to either Slack, Gmail etc. Here are some examples:
 - Memory usage greater than 95%, Number of 404 errors greater than 10% of all requests, Average response time greater than 500 ms
 - Prometheus gives us an easy way to configure rules, which when broken will create an alert via another tool call AlertManager
 - A rule is simply a metric, with a condition. If we wanted to create an alert for when our application has a request rate greater than 0, the rules.yml config would be:
 ```
 groups:
   - name: default
     rules:
       - alert: RequestRate
         expr:  rate(http_server_requests_seconds_count{uri="/doit"}[5m]) > 0
         for: 1m
         labels:
           severity: high
         annotations:
           summary: Application receiving too many requests
 ```
 - Create a new config file alertmanager.yml which contains config details about Email or Slack
 ```
 route:
   receiver: emailer
 receivers:
 - name: emailer
   email_configs:
   - to: <gmail-email-address>
     from:  <gmail-email-address> 
     smarthost: smtp.gmail.com:587 
     auth_username: <gmail-email-address>  
     auth_identity: <gmail-email-address>  
     auth_password: <gmail-app-password>  
 ```
 - To run AlertManager through docker-compose use the below config
 ```
 version: "3"
   services:
     alertmanager:
         image: prom/alertmanager:latest
         ports:
           - 9093:9093
         volumes:
           - ./config/alertmanager.yml:/etc/alertmanager/alertmanager.yml #Pass the alert maanger config file path here
 ```
 - Add the details of rules.yml and configuration detail of AlertManager in prometheus.yml file
 ```
 scrape_configs:
   rule_files:
     - rules.yml
   alerting:
      alertmanagers:
        - static_configs: 
            - targets:
                - alertmanager:9093 
 ```
 - Finally, access the AlertManager URL at http://localhost:9093
 - Access the url http://localhost:9090/alerts of Prometheus. Here the new alert definition will be listed and initially its status will be 'inactive'. When we hit the mentioned API, an alert will be raised from Prometheus, so the status will be moved from inactive to pending. After the configured waiting period status will be changed to 'firing', where Prometheus will send the alert details to AlertManager, from where this message will be sent to configured destination. 
 - So we need 3 configurations file. One for adding Prometheous scrape details, another for defineing rules for alert and final one for destination endpoint details for AlertManager
 - Refer https://tomgregory.com/monitoring-a-spring-boot-application-part-3-rules-and-alerting/
 
---

# Oauth2 and OpenID Connect 
By Using Keycloak - As a OAuth2 Authorization Server

 - Keycloak is an OAuth2 Authorization Server which will implement both OAuth2 and OpenId Connect protocols to provide access and id tokens for OAuth2 Client applications. 
 - These tokens will contains user identity and access/role related information
 - Later OAuth2 client applications will use these tokens to access any protected resources from OAuth2 Resource Server.
 - In this product, we have used Embedded Keycloak along with customized themes as mentioned in the series of article in the link: https://www.baeldung.com/tag/keycloak/ 
 - By following the above link, we can implement an Embedded Keycloak Authorization server with build in support for the user registration, user login, Forgot Password, Remember Me, SSO, custom Themes and Pages etc
 - bookstore-realm.json file contains all the configuration in the json form, to create Keycloak Realm(Bookstore), Client(product-service), Roles(Admin, Buyer), Users(Admin User, Buyer User) with a password and mapped roles etc.

---

# Spring Boot
To create stand-alone, production-grade Spring based Java Micro Service Applications
 
 - Each spring boot micro service applications are registered/connected to below spring cloud related servers:
    - Configuration Management Server - Spring Cloud Config with Github
    - Discovery Server - Spring Cloud Consul
    - API Gateway - Spring Cloud Gateway
 - Multiple instances of each micro service applications will be running to provide High Availability
 - Use version control system for code base like SVN or Git
 - Use version control system for database like Liquibase or Flyway
 - Use Dependency, automation and Build Management tool like Maven or Gradle
 - Configuration: Each microservice application's basic configuration are keeping in bootstrap.yml and rest of the configuration's values will be fetched dynamically through Spring cloud config server while application boots up. For configurations related to multiple environment use the tool like Spring Profile
 - Use tools like Lombok to eliminate boilerplate codes
 - Always code to interfaces instead of implementation
 - Use Project architecture like Layered architecture, hexagonal architecture or onion architecture
 - Write immutable domain objects and business logic only with getters or builders
 - To eliminate Null Pointer exceptions use Java Stream and Optional API in every business logic
 - Use separate model for communications at each layer or share the common models across different layers. Use tools like 'Model Mapper' to convert data from type to other in the immutable ways
 - Use Facade design pattern to write the REST API Controller layer
 - CQRS: Use Command Query Response Segregation pattern while implementing REST APIs 
 - Use the different annotations provided by Spring MVC to implement the REST API Controller layer 
 - Logging: Add the proper Log details of types error, info, debug, warning  across the applications by using plugins like 'logstash-logback-encode' along with 'logback-spring.xml' configuration file
 - Authentication: Convert the spring project into a OAuth2 Resource Server by using the plugin 'spring-boot-starter-oauth2-resource-server' which internally provides required security through 'spring-security' and JWT Access Token which can be obtained from OAuth2 Authorization server. Also, create a custom 'WebSecurityConfigurerAdapter' class to enable required spring beans
 - JWT Access Token: JWT access token contains User details, and his assigned role details, which can be extracted and uses across the application
 - Authorization: Above authentication configuration by default provides the authorization support as well. Annotate the REST API controller classes with @PreAuthorize along with right access logic through HasAuthority, HasRole or HasPermission methods provided by Spring Security
 - Exception Handling: Implement and through custom exceptions in the business logic and handle those in the Spring Security Global Exception handler(through @RestControllerAdvice annotation) which will return a meaningful message to user
 - Data Validation: Add data validation logic at each request objects and hibernate entities before doing any business logic on them by using plugins like 'spring-boot-starter-validation' which internally contains 'javax.validation' support
 - Versioning: Use the proper versioning while designing REST APIs
 - API Documentation: Use the tools like Swagger or Spring REST Docs to create the documentation of external REST APIs
 - ORM Tool: To map any Java Entities to Database colums use tools like Hibernate and define Entities along with required annotations and mappings
 - Data Access: Use tools like Hibernate or Spring Data JPA to reduce the boilerplate codes while accessing any DB along with custom native or spring data JPA queries
 - Audit: Implement auditing functionality for hibernate database entities to keep track of created/updated user and time information
 - Data History: use the tool like Hibernate Enver to maintain history of record for each data operation
 - Monitoring: Use the tools like Micrometer and Spring boot actuator which by default, provides many applications or infrastructure related metric informations. Also, we can use 'micrometer-registry-prometheus' plugin which will provide metric data which are required to send and store in Prometheus DB, and the same can be later visualized in Grafana
 - Alert: Use AlertManager component of Prometheus to send an alert message to operators if the defined Prometheus rules are broken
 - Inter Service Communication - Synchronous: To communicate from one micro service to another use the direct synchronous communication approach either by using Spring MVC Rest Template, Spring WebFlux WebClient or Spring Cloud Open Feign tools. In synchronous communication, use patterns like Cicruit Breaker, Retry, Error Decoder, Time Limiting, Rate Limiting, Load Balancer by using tools like Spring Cloud Circuit Breaker, Spring Cloud Open Feign, Resilience4j, Spring CLoud Load Balancer etc
 - Inter Service Communication - Asynchronous: To communicate between micro services asynchronously use SAGA pattern or Event Driven Architecture by using Distributed Messaging Platform like Kafka or Distributed Queueing platform like RabbitMQ

### Java Doc
 - Add the below configuration in build.gradle file
 ```
 javadoc {
    options.addBooleanOption('html5', true)
 }
 ``` 
 - Run the gradle 'javadoc' command from IntelliJ, which will generates the package information of that specific project 
 - html format of the documentation will be available under the path build -> docs -> javadoc in the root directory of the project
 
### Logback
To customize and send application logs in to a console or file
  - By default, spring boot support logback for logs and provides the logback XML configuration file 'logback-spring.xml' which can be placed in the application resource path to store the application logs into a local physical file or can be sent to console or to Logstash after converting into a Structured format like JSON
  - Add the dependency 'logstash-logback-encoder', which will read the configuration defined in 'logback-spring.xml' file and converts the text format application logs to json format which is required for the Logstash
  Note: Use the absolute path for the file location instead of relative path
  - Sample such logback-spring.xml
  ```
  <property name="LOGS" value="/Users/prasannaadiga/Learning/Project/spring-cloud/bookstore-app/bookstore-payment-service/logs" />
      <springProperty scope="context" name="applicationName" source="spring.application.name"/>
      <appender name="Console" class="ch.qos.logback.core.ConsoleAppender">
          <layout class="ch.qos.logback.classic.PatternLayout">
              <Pattern>
                  %black(%d{ISO8601}) %highlight(%-5level) [%blue(%t)] %yellow(%C{1.}): %msg%n%throwable
              </Pattern>
          </layout>
      </appender>
      <appender name="RollingFile" class="ch.qos.logback.core.rolling.RollingFileAppender">
          <file>${LOGS}/${applicationName}.log</file>
          <encoder class="net.logstash.logback.encoder.LogstashEncoder">
          </encoder>
          <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
              <fileNamePattern>${LOGS}/archived/spring-boot-logger-%d{yyyy-MM-dd}.%i.log
              </fileNamePattern>
              <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                  <maxFileSize>10MB</maxFileSize>
              </timeBasedFileNamingAndTriggeringPolicy>
          </rollingPolicy>
      </appender>
  ```
 - Also, Logback provides support for profile based log configuration for each package or frameworks, which can be define in the same logback-spring.xml file
 ```
 <springProfile name="local_zone1,local_zone2">
     <root level="info">
         <appender-ref ref="LogStash" />
         <appender-ref ref="Console" />
     </root>
     <logger name="org.springframework.*" level="debug" additivity="false">
         <appender-ref ref="LogStash" />
         <appender-ref ref="Console" />
     </logger>
 </springProfile>
 <springProfile name="docker">
     <root level="error">
         <appender-ref ref="LogStash" />
         <appender-ref ref="Console" />
     </root>
     <logger name="com.learning.bookstore" level="warn" additivity="false">
         <appender-ref ref="LogStash" />
         <appender-ref ref="Console" />
     </logger>
 </springProfile>
 ```

### Logging
  - Use the Lombok annotation @Slf4j in each java classes wherever we need to write logs
  - Use log level 'debug' only when we need to log values of some variable in a complex logic
  - Use the log level 'info' whenever some new logic is started or finished with proper input or output values. Also, to log request/response values whenever system calls any external servers
  - Use the log level 'warning' in situations where the code execution might cause some side effect later
  - Use the log level 'error' in catch blocks
  - By default, set the log level as 'error' for the ROOT log for production
  - Also set the log level as info for application's root package, if there are not so many info logs exists in code
  - Note that, by default if we activate the endpoint 'logger' of spring boot actuator, then the actuator provides a REST endpoint through which we can chang the log level of any package or plugin without restarting the server. We can make this just by executing the API with required data.
  - To set different log levels for each package use below configurations. This can also configure in 'logback-spring.xml' file
  ```
  logging.level.org.springframework.web: DEBUG
  logging.level.org.hibernate: ERROR
  ```
  - Also, do not use message formatting, instead use structured arguments. Which helps for better search criteria support in ELK 
  ```
  Dont use this:
    log.info("Processing company {} of {}", companyIndex, companyCount);
  Use this:
    log.info("Processing company", v("companyIndex", companyIndex), v("companyCount", companyCount));
  ```
  - Finally, use the Logback plugin which is provided by default in spring boot. Write a custom 'logback-spring.xml' file which will append all the provided log details into a console, or a file(In a JSON format which later can send to Logstash)
  
### Validation and Exception Handling
  - Use validator annotations like @NotEmpty, @NotNull, @NotBlank, @Size, @Min, @Max, @Positive etc in the domain/entity classes along with proper exception message details for the user to read
  - In the RestController use the annotation @Validated at the controller level and @Valid at the method level
  - So Hibernate validator will call the validation logic once the API is called and then throws the corresponding exception if the validation fails
  - We can also create custom validations by creating custom annotation which uses a class which implements ConstraintValidator and provides the required validation logic
  - Create a class with @RestControllerAdvice which extends the ResponseEntityExceptionHandler 
  - The above class will work as GlobalExceptionHandler where we can override any existing spring exception handling logic to provide custom logic, or we can write handler logic for our Custom User Defined exceptions, by annotating a class with @RestControllerAdvice
  - Here we can create exception message object with a meaningful message along with proper error code send it back to user

### Entity Audit and History
For managing audit information for entities
  - Add the dependency 'spring-boot-starter-data-jpa'
  - Create an abstract entity class with annotation '@MappedSuperclass', which contains the fields CreatedBy, CreatedDate, LastModifiedBy and LastModifiedDate
  - Create a spring boot configuration class with annotation '@EnableJpaAuditing' and other configuration as mentioned in the link: http://progressivecoder.com/spring-boot-jpa-auditing-example-with-auditoraware-interface/

For managing history information for entities
  - Add the dependency 'hibernate-envers'
  - Add the annotation '@Audited' to each entity for which history information needs to be maintained
  - This will creates bunch of extra tables for each entity to maintain its history. Refer te link: http://progressivecoder.com/setting-hibernate-envers-spring-boot/
 
### Designing REST APIs
  - Use @RestController, @RequestMapping, @PathVariable, @RequestParam, @RequestBody, @GetMapping, @PostMapping, @PutMapping, @DeleteMapping annotations wherever required
  - Use validation related annotations on method arguments, parameters or variables to check the validations
  - Use proper log details by using @Slf4j annotation and handle the global and custom exception messages
  - Use the annotation @RequiredArgsConstructor annotation with private final fields to automatically inject the required beans by spring
  - GET Request: Mainly used for filtering or sorting or searching. To fetch all available records in the pagination format or fetch a record by its id or fetch few records by list of their ids in the pagination format. Response status will be 200 - Ok.
  - Post Request: Post method is used to create a record. Response will be 201 - Created with empty body. Also, return the id of the newly created record as a location header
  - Put Request: Used to update an existing record. Response will be 200 - Ok with empty body.
  - Delete Request: Used to delete an existing record. Response will be 204 - No Content.

### Filters and Interceptors in Spring
 - Filters which resides basically in a web/servlet containers, are used to filter any request or response which flows between a client, and a servlet which is mapped to a specific URL
 - In case of spring, where we will be having spring IoC container, filters are used between the client and spring MVC dispatcher servlet which is running inside spring container
 - Interceptors are used between spring MVC dispatcher servlet and a specific controllers
 - So Basically Filters are used in a web container outside of spring containers and Interceptors are used inside a spring container. So Interceptor can have complete access on spring context to perform complex logic.
 - Use the spring provided filter OncePerRequestFilter if we want to log any request/response which comes to our application from outside clients. This filter also used to add any custom header to request/response, to deny certain request before it reaches dispatcher servlet, to add authentication check, to log request/response details etc.
 - Use the spring provided interceptor ClientHttpRequestInterceptor if we want to log any request/response which triggers from our application to outside clients by using RestTemplate. Through this interceptor we can also add any custom header to request/response, to deny certain request, to add authentication check, to log request/response objects header, body etc (https://howtodoinjava.com/spring-boot2/resttemplate/clienthttprequestinterceptor/ for reference)
 - If we use Feign to make outside client calls and to log the request and response object details we can use the below Feign bean configuration 
    ```
      @Bean
      Logger.Level feignLoggerLevel() {
          if(log.isDebugEnabled()) {
              return Logger.Level.FULL;
          } else {
              return Logger.Level.BASIC;
          }
      }
    ```
 - Use the spring provided interceptor HandlerInterceptor to get the complete access over any request before it reaches a controller, or after controller return a response and before it render view, or after the view rendered completely. We can usually set start time in the preHandle method and check for the end time in afterCompletion method to find total time taken for an REST API to execute.Also, we can set unique traceId for each request in the preHandle method and later in the afterCompletion method we can remove these traceId
 - Interceptor to work, it must registered in InterceptorRegistry. For this spring provides a Configurer class WebMvcConfigurer, addInterceptor method where new interceptors can be registered in the order.
 - Each Interceptor can also configure to get activated only for specific set of URL's
 - ClientHttpRequestInterceptor to work, it must be set as interceptor to RestTemplate by using restTemplate.setInterceptor method
 - OncePerRequestFilter to work, it must be set as filter to FilterRegistrationBean by using its setFilter method

### Spring Security
To provide authentication, authorization
 - Add the dependency 'spring-boot-starter-security'
 - By default, spring security generates a password while running the server. The default username is 'user'. Both of these can be configured through a property file.
 - Also, by default spring security enables form based and http basic authentication based authentication flow
 - The above behaviour can be customized by extending the WebSecurityConfigurerAdapter class and overriding it's methods
 - In the above custom class, we can configure Authentication Manager to read the user credentials and roles either from in memory or from databases through custom UserDetailsService and UserDetail classes
 - Also, we can configure which all APIs can be permitted to access and which all APIs are restricted to access
 - APIs which are restricted to access, needs a valid username and password to access. 
 - Once Authentication is successful, we can restrict accessing each APIs only through a valid Role. This process is called authorization.
 - We can configure authorization either in the configuration class or at each class/method level through @PreAuthorize or other annotations provide by spring security. To use these annotations we need to set '@EnableGlobalMethodSecurity(prePostEnabled = true)' in the configuration file.
 - Also, we can write custom exception handler logic for Unauthorized and Access Denied exceptions, where we can return a meaningful message to user. The following code can be used for the same in configure() method:
 ```
 http
 .exceptionHandling()
 .accessDeniedHandler(restAccessDeniedErrorHandler)
 .authenticationEntryPoint(restUnAuthorizedErrorHandler);

 public class RestUnAuthorizedErrorHandler extends BasicAuthenticationEntryPoint { ... }

 public class RestAccessDeniedErrorHandler implements AccessDeniedHandler {
 ```
 - Authenticated user details can be fetched in controller by passing another argument Authentication or Principal in a method, which is provided by spring security
 
### Spring Data JPA
To implement JPA based repositories

 - Create new JPA entities with required annotations, validations and mappings
 - Create new classes which implements JpaRepository and provides custom query methods with @Query annotation and placeholder in the queries like 'id = ?1' 
 - Add @Transactional annotation

### OAuth2 Resource Server
Spring boot application as a OAuth2 resource server, which provides the protected resource to user only upon receiving a valid token, which user can obtain from OAuth2 Authorization Server

 - To convert spring boot application into an OAuth2 Resource server add the dependency 'spring-boot-starter-oauth2-resource-server'. This by default includes Spring Security and JWT support as well.
 - Add the below configurations in configure method of WebSecurityConfigurerAdapter. This will automatically expect a user token from a client, sends those token to OAuth2 Authorization server, receives JWT token from Authorization server in return, extract user roles from those JWT token and converts them to list of Spring Security Granted Authorities and set those authorities in SecurityContextHolder so that these roles can be accessed from any part of the application for that logged in user.
 ```
 http
    .oauth2ResourceServer(oauth2ResourceServer ->
        oauth2ResourceServer.jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter()))
    )

 private Converter<Jwt, ? extends AbstractAuthenticationToken> jwtAuthenticationConverter() {
     JwtAuthenticationConverter jwtConverter = new JwtAuthenticationConverter();
     jwtConverter.setJwtGrantedAuthoritiesConverter(new KeycloakRealmRoleConverter());
     return jwtConverter;
 }

 @Bean
 JwtDecoder jwtDecoder() {
     return NimbusJwtDecoder.withJwkSetUri(this.jwkSetUri).build();
 }

 public class KeycloakRealmRoleConverter implements Converter<Jwt, Collection<GrantedAuthority>> {
     @Override
     public Collection<GrantedAuthority> convert(Jwt jwt) {
         final Map<String, Object> realmAccess = (Map<String, Object>) jwt.getClaims().get("realm_access");
         return ((List<String>)realmAccess.get("roles")).stream()
                 .map(roleName -> "ROLE_" + roleName)
                 .map(SimpleGrantedAuthority::new)
                 .collect(Collectors.toList());
     }
 }
 ```
 - Then, we can inject this token into any of the method through '@AuthenticationPrincipal JWt jwt' as a parameter and extract any of the details from access token like below:
 ```
 To get user mail:
    jwt.getClaimAsString("email") (or)
    ((Jwt) SecurityContextHolder.getContext().getAuthentication().getPrincipal()).getClaimAsString("email");
 To get user access token 
    jwt.getTokenValue(); (or)
    ((Jwt) SecurityContextHolder.getContext().getAuthentication().getPrincipal()).getTokenValue;
 ```
 
### Spring Docs OpenAPI
To automate the generation of API documentation
  - Add the dependencies 'springdoc-openapi-ui' and 'springdoc-openapi-webmvc-core'
  - Run the spring boot application
  - Access the yml version of api doc at 'http://host:port/v3/api-docs'
  - Access the html version of api doc at 'http://host:port/swagger-ui.html'
  - Adding ResponseStatus with right status code in each controller's method and each method of @ControllerAdvice will automatically create the right response codes in the doc.
  - Use the annotations @Operation, @Parameter or @ApiResponse to provide additional details in the document or to provide response details manually
  - https://www.baeldung.com/spring-rest-openapi-documentation for reference
  - To show actuator endpoints in the document we can use the below config
    ```
      springdoc:
        show-actuator: true
    ```
  - OpenAPI can be customized by the following configurations:
    ```
      @Bean
      public OpenAPI customOpenAPI() {
          List servers = new ArrayList<Server>();
          servers.add(new Server().url("http://localhost:8080/bookstore-order-service").description("Development server"));
          //In the above code we use the Host and Port of the API Gatway server along with base path a particular microservice
          return new OpenAPI().components(new Components()).info(new Info()
                  .description("<p>Provides list of REST APIs for User Account</p>")
                  .title("API documentation for Account Service").version("1.0.0")).servers(servers);
      }
    ```
  - If spring security is added, by default user needs to enter a username and password to access this swagger ui. To disable this we can use the following configurations in to WebSecurityConfigurerAdapter class. 
    ```
        .antMatchers("/v3/api-docs/**", "/swagger-ui/**", "/swagger-ui.html").permitAll()
    ```
  - Also, If we need to enable 'Authorize' button with Basic Authentication to appear in the swagger UI, we need to use the below configurations:
    ```
        @Configuration
        @SecurityScheme(
                name = "BasicAuth", //We can also setup BearerAuth
                type = SecuritySchemeType.HTTP,
                scheme = "basic"
        )
        public class OpenAPIDocsConfig { ... }
    ```
  - And, If we need to enable 'Authorize' button with Bearer Token (In case of OAuth2) to appear in the swagger UI, we need to use the below configurations:
      ```
          @Configuration
          @SecurityScheme(
                  name = "bearerAuth",
                  type = SecuritySchemeType.HTTP,
                  scheme = "bearer",
                  bearerFormat = "JWT"
          )
          public class OpenAPIDocsConfig { ... }
      ```  
  - And then in each API where we need to restrict the APIs call through Swagger, need to add the below configuration:
    ```
        @Operation(security = @SecurityRequirement(name = "BasicAuth/bearerAuth")
    ```  
  - To generate the json format of swagger document through gradle add the below plugins, gradle configurations and then run the command 'gradle clean generateOpenApiDocs'. Later this json file can be imported to Swagger Online Editor and save as PDF file. This will create a json file under the path build -> docs in the root directory of project.
    ```
      id "com.github.johnrengelman.processes" version "0.5.0"
      id "org.springdoc.openapi-gradle-plugin" version "1.3.0"

      openApi {
        apiDocsUrl.set("http://localhost:8080/<replace by base path of a micro service>/v3/api-docs") //This API call is through API Gateway
        outputDir.set(file("$buildDir/docs"))
        outputFileName.set("account-service.json")
        waitTimeInSeconds.set(10)
      }
    ```  
### Spring Profile
To provide separate configurations for different environments
  - Create different configurations for each profile, either in config-server or in each micro services
  - Create one such profile for Docker, where service's host can be given as each service-name instead of 'localhost', so that services can be discoverable inside docker containers
    ```
      ---
      spring:
        profiles: docker
      eureka:
        client:
          serviceUrl:
            defaultZone: http://server-discovery:8082/eureka/
    ```
  - Profiles can be activated for each services in docker-compose.yml file through environment variable or by passing -Dspring.profile.active field in IDE
    ```
      environment:
        SPRING_PROFILES_ACTIVE: docker  
    ```  
    
### Spring Boot Actuator
To automate providing infrastructure and application specific metrics data
  - Add the dependency 'spring-boot-starter-actuator'
  - By default, this plugin activates only 'health' and 'info' endpoints
  - To add build related information in to 'info' endpoint, add the below to build.gradle file of each micro services
    ```
      springBoot {
        buildInfo()
      }
    ```
    which produces the info endpoint as 
    ```
      {
        "build": {
          "artifact": "service-product",
          "name": "service-product",
          "time": "2020-12-04T05:47:02.805Z",
          "version": "0.0.1-SNAPSHOT",
          "group": "com.learning.cloud"
        }
      }
    ```
  - To activate all other endpoints provided by the actuator plugin, use the below configuration 
    ```
      management:
        endpoints:
          web:
            exposure:
              include: "*"
        enpoint:
          health:
            show-details: always #To show other details in health endpoint 
    ```
  - View the health information at 'http://host:port/actuator/health' and information at 'http://host:port/actuator/info'
  - If spring security is in the classpath, and if the above endpoints are not configured to permitAll() in the WebSecurityConfigurationAdapter file, then browser will show the login page where user needs to enter the username and password of the user to view the actuator endpoints details.
  - If we implement spring security OAuth2 through the plugin 'spring-boot-starter-oauth2-resource-server' and if the above endpoints are not configured to permitAll(), then we must provide the valid access token for the configured user to view the details of each actuator endpoints. 

---

# Distributed Messaging System
By using Kafka

## Zookeeper

 - Zookeeper is used to manage Kafka
 - Electing a controller: The controller is one of the brokers and is responsible for maintaining the leader/follower relationship for all the partitions. When a node shuts down, it is the controller that tells other replicas to become partition leaders to replace the partition leaders on the node that is going away. Zookeeper is used to elect a controller, make sure there is only one and elect a new one it if it crashes.
 - Cluster membership: Which brokers are alive and part of the cluster? this is also managed through ZooKeeper.
 - Topic configuration: Which topics exist, how many partitions each has, where are the replicas, who is the preferred leader, what configuration overrides are set for each topic
 - Quotas: how much data is each client allowed to read and write
 - ACLs: who is allowed to read and write to which topic (old high level consumer) - Which consumer groups exist, who are their members and what is the latest offset each group got from each partition.
 - We can run the Zookeeper in docker through docker-compose.yml file as mentioned below
 
## Kafka

 - Kafka consists of Records/Message(key-value pair), Topics, Consumers, Producers, Brokers, Logs, Partitions, Offsets and Clusters. 
 - Records can have key (optional), value and timestamp. Kafka Records are immutable. 
 - A Kafka Topic is a stream of records. A topic has a Log which is the topic’s storage on disk. A Topic Log is broken up into partitions and segments. 
 - The Kafka Producer API is used to produce streams of data records. 
 - The Kafka Consumer API is used to consume a stream of records from Kafka. 
 - A Broker is a Kafka server that runs in a Kafka Cluster. Kafka Brokers form a cluster. The Kafka Cluster consists of many Kafka Brokers on many servers. 
 - Add the below Kafka related configuration in common application.yml file of Spring Cloud Config Server
 ```
 kafka-config:
   bootstrap-servers: localhost:19092, localhost:29092, localhost:39092
   schema-registry-url-key: schema.registry.url
   schema-registry-url: http://localhost:8081
 ```
 - Above configuration contains all the available Kafka broker urls of a Kafka Cluster, along with Schema Registry Server URL
 - Provide the corresponding Java class through ConfigurationProperties
 ```
 @Data
 @Configuration
 @ConfigurationProperties(prefix = "kafka-config")
 public class KafkaConfigData {
     private String bootstrapServers;
     private String schemaRegistryUrlKey;
     private String schemaRegistryUrl;
 }
 ```
 - We can create a Kafka Cluster with 3 Kafka broker running in docker through docker-compose.yml file as mentioned below
 
## Kafka Admin Client

 - The administrative client for Kafka, which supports managing and inspecting topics, brokers, configurations and ACLs
 - Kafka Admin Client provides set of APIs for creating new topics with topic name, partition and replication factor counts, for fetching list of available topics etc
 - Add the dependency 'spring-kafka' which will give access to AdminClient
 - We can fetch available list of topics as following:
 ```
 Collection<TopicListing> topics = adminClient.listTopics().listings().get();
 ```
 - Add the dependency 'spring-cloud-starter-config', so that all the configuration related to Kafka, Admin Client, Schema Registry, Producer, Consumer, Retry can be configured in Spring Cloud Config Server
 - Also, we can wrap all the adminClient calls with Spring Retry. So if the Kafka server is not ready yet, Spring Retry can call the same API for the mentioned number of times as configured before throwing exception
 - For that, add the dependency 'spring-retry', below configuration in spring cloud config server common application.yml
 ```
 retry-config:
   initial-interval-ms: 1000
   max-interval-ms: 10000
   multiplier: 2.0
   maxAttempts: 3
   sleep-time-ms: 2000
 ```
 - Create Spring RetryTemplate bean, with configured RetryPolicy and BackOffPolicy details
 ```
 @Data
 @Configuration
 @ConfigurationProperties(prefix = "retry-config")
 public class RetryConfigData {
     private Long initialIntervalMs;
     private Long maxIntervalMs;
     private Double multiplier;
     private Integer maxAttempts;
     private Long sleepTimeMs;
 }
 -----
 @Bean
 public RetryTemplate retryTemplate() {
     RetryTemplate retryTemplate = new RetryTemplate();
     ExponentialBackOffPolicy exponentialBackOffPolicy = new ExponentialBackOffPolicy();
     exponentialBackOffPolicy.setInitialInterval(retryConfigData.getInitialIntervalMs());
     exponentialBackOffPolicy.setMaxInterval(retryConfigData.getMaxIntervalMs());
     exponentialBackOffPolicy.setMultiplier(retryConfigData.getMultiplier());
     SimpleRetryPolicy simpleRetryPolicy = new SimpleRetryPolicy();
     simpleRetryPolicy.setMaxAttempts(retryConfigData.getMaxAttempts());
     retryTemplate.setBackOffPolicy(exponentialBackOffPolicy);
     retryTemplate.setRetryPolicy(simpleRetryPolicy);
     return retryTemplate;
 ```
 - Finally, create a AdminClient Bean with Kafka Broker URLs and wrap it with Spring Retry, so all the calls goes through Spring Retry
 ```
 @EnableRetry
 @Configuration
 @RequiredArgsConstructor
 public class KafkaAdminClientConfig {
     private final KafkaConfigData kafkaConfigData;
     @Bean
     public AdminClient adminClient() {
         return AdminClient.create(Map.of(CommonClientConfigs.BOOTSTRAP_SERVERS_CONFIG, kafkaConfigData.getBootstrapServers()));
     }
 }
 ----
 retryTemplate.execute(this::doCreateTopics);
 
 NewTopic kafkaTopic = TopicBuilder.name(kafkaTopicConfigData.getTopicName())
         .partitions(kafkaTopicConfigData.getNumOfPartitions())
         .replicas(kafkaTopicConfigData.getReplicationFactor())
         .build();
 return adminClient.createTopics(List.of(kafkaTopic));
 ```
 - The above api call will create a new topic with the provided details in Kafka broker

## Schema Registry
To provide version control for schema definition

 - Reference link: https://aseigneurin.github.io/2018/08/02/kafka-tutorial-4-avro-and-schema-registry.html
 - Schema Registry is a distributed storage layer for schemas which uses Kafka as its underlying storage mechanism and keeps history of schema as well
 - Schema Registry lives outside of and separately from your Kafka brokers. Kafka producers and consumers still talk to Kafka to publish and read data (messages) to topics. 
 - it is a server that runs in your infrastructure (close to your Kafka brokers) and that stores your schemas (including all their versions). When you send Avro messages to Kafka, the messages contain an identifier of a schema stored in the Schema Registry.
 - Concurrently, they can also talk to Schema Registry to send and retrieve schemas that describe the data models for the messages. And, later they can use Apache Avro to serialize or deserialize such message
 - A Kafka topic contains messages, and each message is a key-value pair. Either the message key, or the message value, or both, can be serialized as Avro, JSON, or Protobuf. 
 - A schema defines the structure of such data format, which can be either send by a producer or consumed by a consumer
 - In this application we are using Apache Avro which is a data serialization or deserialization system
 - We define the Schema Registry Server URL in the application.yml file
 ```
 kafka-config:
   schema-registry-url-key: schema.registry.url
   schema-registry-url: http://localhost:8081
 ```
 - We can check whether Schema Registry Server is Up and Running programmatically as below:
 ```
 @Override
 private HttpStatus getSchemaRegistryStatus() {
     try {
         return webClient
                 .method(HttpMethod.GET)
                 .uri(kafkaConfigData.getSchemaRegistryUrl())
                 .exchange()
                 .map(ClientResponse::statusCode)
                 .block();
     } catch (Exception e) {
         log.error("KafkaClientException in KafkaAdminClient.getSchemaRegistryStatus(): Schema Registry Server is unavailable", kv("exception", e.getLocalizedMessage()));
         return HttpStatus.SERVICE_UNAVAILABLE;
     }
 }
 ```
 - In order to use the WebClient, add the dependency 'spring-boot-starter-webflux'

## Apache Avro
Schema based serialization system in bytes

 - Avro is a cross-language serialization library that require the data structure to be formally defined by schemas. These schemas basically saved in schema registry server.
 - A library allows you to serialize and deserialize Avro messages, and to interact transparently with the Schema Registry:
   - When sending a message, the serializer will make sure the schema is registered, get its ID, or register a new version of the schema for you
   - When reading a message, the deserializer will find the ID of the schema in the message, and fetch the schema from the Schema Registry to deserialize the Avro data.
 - It relies on schemas (defined in JSON format) that define what fields are present and their type. We can have multiple versions of your schema, by adding or removing fields
 - The advantage of having a schema is that it clearly specifies the structure, the type and the meaning (through documentation) of the data. With a schema, data can also be encoded more efficiently. 
 - To use this Avro with Kafka add the dependency 'kafka-avro-serializer'
 - For example, an Avro schema defines the data structure in a JSON format. The following Avro schema specifies a user record with two fields: name and favorite_number of type string and int, respectively.
 ```
 {"namespace": "example.avro",
  "type": "record",
  "name": "user",
  "fields": [
      {"name": "name", "type": "string"},
      {"name": "favorite_number",  "type": "int"}
  ]
 }
 ```
 - We can use this Avro schema, for example, to serialize a Java object (POJO) into bytes, and deserialize these bytes back into the Java object.
 - Add the dependency 'org.apache.avro:avro' and plugin 'com.github.davidmc24.gradle.plugin.avro'. By using this plugin we can write different Avro Models as '.avsc' file with required field and description in a specific source directory path. for example 'src/main/resources/avro'
 - Then above plugin provides an option to read all such Avro Models from a specific path and convert them to Java POJOs automatically and create them in the specified package, just by running 'gradle build' with the below configuration in build.gradle
 ```
 def generateAvro = tasks.register("generateAvro", com.github.davidmc24.gradle.plugin.avro.GenerateAvroJavaTask) {
 	source("src/main/resources/avro")
 	outputDir = file("src/main/java")
 }
 tasks.named("compileJava").configure {
 	source(generateAvro)
 }
 ```
 
## Kafka Producer

 - Used to send a stream of data to a Kafka topic of specific partition, or we can ask Kafka only to choose th partition 
 - Add the below config details in common application.yml file of Spring Cloud Config Server
 ```
 kafka-producer-config:
   key-serializer-class: org.apache.kafka.common.serialization.LongSerializer
   value-serializer-class: io.confluent.kafka.serializers.KafkaAvroSerializer
   compression-type: snappy
   acks: all
   batch-size: 16384
   batch-size-boost-factor: 100
   linger-ms: 5
   request-timeout-ms: 60000
   retry-count: 5
 ```
 ```
 @Data
 @Configuration
 @ConfigurationProperties(prefix = "kafka-producer-config")
 public class KafkaProducerConfigData {
     private String keySerializerClass;
     private String valueSerializerClass;
     private String compressionType;
     private String acks;
     private Integer batchSize;
     private Integer batchSizeBoostFactor;
     private Integer lingerMs;
     private Integer requestTimeoutMs;
     private Integer retryCount;
 }
 ```
 - Create a customized KafkaProducer, which provide send method with topicName, key and value in the Avro model format. 
 - KafkaProducer internally uses send method of KafkaTemplate 
 - Also, add callback handler for success and failure scenarios
 ```
 public class KafkaProducer implements KafkaProducerService<Long, OrderAvroModel> {
     private final KafkaTemplate<Long, OrderAvroModel> kafkaTemplate;
     @Override
     public void send(String topicName, Long key, OrderAvroModel message) {
         ListenableFuture<SendResult<Long, OrderAvroModel>> kafkaResultFuture = kafkaTemplate.send(topicName, key, message);
         addCallback(topicName, message, kafkaResultFuture);
     }
     private void addCallback(String topicName, OrderAvroModel message, ListenableFuture<SendResult<Long, OrderAvroModel>> kafkaResultFuture) {
         kafkaResultFuture.addCallback(new ListenableFutureCallback<>() {
             @Override
             public void onFailure(Throwable throwable) {
                log.error("Error while sending message {} to topic {}", message.toString(), topicName, throwable);
             }
             @Override
             public void onSuccess(SendResult<Long, OrderAvroModel> result) {
                RecordMetadata metadata = result.getRecordMetadata();
             }
         });
     }
 }
 ```
 - Finally, create a custom KafkaTemplate with mentioned Producer configuration
 ```
 @Configuration
 @RequiredArgsConstructor
 public class KafkaProducerConfig<K extends Serializable, V extends SpecificRecordBase> {
     private final KafkaConfigData kafkaConfigData;
     private final KafkaProducerConfigData kafkaProducerConfigData;
     @Bean
     public Map<String, Object> producerConfig() {
         Map<String, Object> props = new HashMap<>();
         props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaConfigData.getBootstrapServers());
         props.put(kafkaConfigData.getSchemaRegistryUrlKey(), kafkaConfigData.getSchemaRegistryUrl());
         ....
         ....
         return props;
     }
     @Bean
     public ProducerFactory<K, V> producerFactory() {
         return new DefaultKafkaProducerFactory<>(producerConfig());
     }
     @Bean
     public KafkaTemplate<K, V> kafkaTemplate() {
         return new KafkaTemplate<>(producerFactory());
     }
 }
 ```
 - Now other micro service can use this KafkaProducer.send() method with their topicName, key and value details 
 - Each microservice can pass their own topic name, partition and replication count through property file:
 ```
 kafka-topic-config:
   topic-name: bookstore-product-topic
   num-of-partitions: 3
   replication-factor: 3
 ```

## Kafka UI

 - Kafka-UI provide a user interface, where we can see all the available kafka brokers along with their corresponding topic, partition, offset and record details
 - Follow the link: https://github.com/provectus/kafka-ui
  
---

### Alert and Monitoring system metrics
By using Prometheus and Grafana
  - Add the dependency 'micrometer-registry-prometheus'
  - Add the below configurations to expose the metrics endpoint by spring boot actuator
    ```
      management:
        endpoints:
          web:
            exposure:
              include: "*"
        enpoint:
          health:
            show-details: always
    ``` 
  - With the above plugin in place, micrometer generates the metrics in the format as required by the Prometheus
  - View the metrics related to Prometheus at 'http://host:port/actuator/prometheus'
 
### Spring developer tools
To help local development
  - Lombok
  - spring boot DevTools - an automatic restart of server on code changes, live reload of resource changes in the browser. By default, auto restart support does not work in IntelliJ. Follow the steps mentioned in here to configure it in IntelliJ: https://medium.com/@bhanuchaddha/spring-boot-devtools-on-intellij-c0ab3f9afa63
  - spring boot configuration processor - helps developers in providing available configuration options in yml/properties files
    
### Cross Cutting Concerns
 - Externalize configurations: Can be achieved by using multiple yml/properties files with Spring Cloud Config  or Consul Config
 - Logging: Can be implemented by using Logback configuration files(By default spring boot supports it) and then send these log details to Elastic Search with the help of Logstash and finally can be visualized each log details by using Kibana
 - Exception Handling: Can be implemented with the help of annotations provided by 'spring-boot-starter-validation' plugin and Global exception handler in Spring Boot (Refer: https://devwithus.com/exception-handling-for-rest-api-with-spring-boot/)
 - Security(Authentication): Can be implemented by the support available in spring-boot-starter-security plugin
 - Security(Authorization): Can be implemented by OAuth2 Authorization server along with spring boot security and JWT
 - Alerts and Monitoring: Spring boot actuator along with MicroMeter provides many infrastructures and application related metrics, which can be sent to Prometheus easily and later can be visualized in Grafana
 - Distributed Tracing: Each API request can be traced across multiple microservices easily with the help of Correlation ID provided by tools like Zipkin and Sleuth
 - API Documentation: By using Swagger or Spring Docs Open API or Spring Rest Docs
 - All the above cross-cutting concerns can also be implemented at API Gateway server(Basically to requests coming from client to server) or by using Service Mesh/sidecar proxy tool(Requests coming from one server to another)

### Microservice Patterns
 - Service Discovery or Service Registry: By using spring cloud Netflix Eureka or Consul Service Discovery
 - Distributed Configuration: Configurations of each microservice can be externalized by using spring cloud config or consul config
 - API Gateway or Gateway server: By using Spring cloud netflix Zuul or Spring Cloud API Gateway or Kong API Gateway
 - Circuit Breaker: By using Ribbon or Resilience4J
 - Client side load balancing: By using Hystrix or Spring cloud load balancer

### Design Pattern
 - Interface driven REST Controllers: https://www.baeldung.com/spring-interface-driven-controllers

### H2 Database
Database for development and testing environment
 - Add 'spring-boot-starter-data-jpa' and 'h2' dependencies
 - Add below configurations in application.yml
   ```
      h2:
        console:
          enabled: true
          settings:
            web-allow-others: false
            trace: false
          path: /h2-console
      datasource:
        url: jdbc:h2:mem:testdb
        driver-class-name: org.h2.Driver
        username: sa
        password: password
      jpa:
        database-platform: org.hibernate.dialect.H2Dialect
   ```
 - Also add below configuration in WebSecurityConfigurerAdapter if we are using Spring Security. This will allow H2 page to display once logged in.
   ```
    http.headers().frameOptions().disable();
   ```
 - Access the H2 database from any browser. URL is http://localhost:8090/h2-console. If spring security is added in the project by default browser login page will be displayed. User need to enter the right username and password.

### Loading initial data
To have pre-required data in the database tables

Spring Boot
 - Create data.sql and schema.sql files in the classpath i.e src/main/resources
 - Spring will automatically load these files to create the required schema and insert data 
 - For production environment, we can make use of tools like Liquibase or Flyway

Flyway - Version controls for your database
 - Add the dependency 'flyway-core'
 - Create a new folder path 'db/migration' under the resources folder
 - Create multiple sql scripts for creating tables or add initial data to tables. These scripts must follow particular naming conventions(with Prefix, version, separator and description) as defined by Flyway.
 - Once we run the spring boot application, all the tables will be created with initial data.
 - If we need to add any new tables/data, create a separate new script file with a new version.
 
### Model Mapper Utility plugin
To convert DTO to Entities and vice versa
 - Add 'modelmapper' dependency
 - Add a configuration class to create ModelMapper bean
   ```
        @Bean
        public ModelMapper modelMapper() {
            return new ModelMapper();
        }
   ``` 
 - Use the method ModelMapper.map() to convert DTO's to Entities and vice versa  
         
---
 
# Docker

---

# Kubernetes

---
 
# Testing
By using JUnit
 - Add the dependency 'spring-boot-starter-test'
 - Add a new folder 'resources' in the path 'src/test' and create a new file 'bootstrap.yml' under that
 - Add the below configuration details in this yml file to disable spring cloud config server and spring cloud consul server while running test cases along with providing required properties.
 ```
 spring:
   cloud:
     config:
       enabled: false
     discovery:
       enabled: false
     bus:
       enabled: false
     consul:
       enabled: false
       discovery:
         enabled: false
       config:
         enabled: false
 ```