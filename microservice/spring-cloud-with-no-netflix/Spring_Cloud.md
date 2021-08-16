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