## Cross Cutting Concerns
 - Externalize configurations: Can be achieved by using multiple yml/properties files with Spring Cloud Config  or Consul Config
 - Logging: Can be implemented by using Logback configuration files(By default spring boot supports it) and then send these log details to Elastic Search with the help of Logstash and finally can be visualized each log details by using Kibana
 - Exception Handling: Can be implemented with the help of annotations provided by 'spring-boot-starter-validation' plugin and Global exception handler in Spring Boot (Refer: https://devwithus.com/exception-handling-for-rest-api-with-spring-boot/)
 - Security(Authentication): Can be implemented by the support available in spring-boot-starter-security plugin
 - Security(Authorization): Can be implemented by OAuth2 Authorization server along with spring boot security and JWT
 - Alerts and Monitoring: Spring boot actuator along with MicroMeter provides many infrastructures and application related metrics, which can be sent to Prometheus easily and later can be visualized in Grafana
 - Distributed Tracing: Each API request can be traced across multiple microservices easily with the help of Correlation ID provided by tools like Zipkin and Sleuth
 - API Documentation: By using Swagger or Spring Docs Open API or Spring Rest Docs
 - All the above cross-cutting concerns can also be implemented at API Gateway server(Basically to requests coming from client to server) or by using Service Mesh/sidecar proxy tool(Requests coming from one server to another)

## Microservice Patterns
 - Service Discovery or Service Registry: By using spring cloud Netflix Eureka or Consul Service Discovery
 - Distributed Configuration: Configurations of each microservice can be externalized by using spring cloud config or consul config
 - API Gateway or Gateway server: By using Spring cloud netflix Zuul or Spring Cloud API Gateway or Kong API Gateway
 - Circuit Breaker: By using Ribbon or Resilience4J
 - Client side load balancing: By using Hystrix or Spring cloud load balancer

## Design Pattern
 - Interface driven REST Controllers: https://www.baeldung.com/spring-interface-driven-controllers
