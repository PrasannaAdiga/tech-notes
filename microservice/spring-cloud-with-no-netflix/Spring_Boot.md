## Spring Boot
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
 - Events: To trigger application specific events from one component and fetching them in another component by listening to same event 
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
 
### Spring Event
To communicate between application components

 - By using Spring Boot Events, we can publish and listen for a specific events which contains usufull data across componets
 - One use case where spring events are helpful is, to raise an event when a new Product created, which contains created Product data, and later we can listen the same Product event and send it to specific topic of Kafka
 - To do that, create an Event Published logic as:
 ```
 @Component
 @RequiredArgsConstructor
 public class ProductEventPublisher implements IProductEventPublisher {
     private final ApplicationEventPublisher publisher;
     public void publish(Product product) {
         publisher.publishEvent(product); #To publish an Event
     }
 
 }
 ```
 - Then, create an Event Listener class as:
 ```
 @Component
 @RequiredArgsConstructor
 public class ProductEventListener {
     private final KafkaProductProducer kafkaProductProducer;
     private final KafkaTopicConfigData kafkaTopicConfigData;
     private final PrincipalResolver principalResolver;

     @EventListener #To listen an event
     public void onEvent(Product product) {
         ProductEvent productEvent = convert(product);
         kafkaProductProducer.send(kafkaTopicConfigData.getTopicName(), principalResolver.getCurrentLoggedInUserMail(), productEvent);
     }
 }
 ```
 - In the above code, we use the customized Kafka Producer which has the customized KafkaTemplate with Producer Configuration to send the data to specific topic of Kafka
 - And finally, use the above publisher in the application logic wherever it is needed:
 ```
 public String createProduct(CreateProductRequest createProductRequest) {
      Product createdProduct = productPersistenceAdapter.createProduct(product);
      productEventPublisher.publish(createdProduct);
      return createdProduct.getId();
 }
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
   
### Spring developer tools
To help local development
  - Lombok
  - spring boot DevTools - an automatic restart of server on code changes, live reload of resource changes in the browser. By default, auto restart support does not work in IntelliJ. Follow the steps mentioned in here to configure it in IntelliJ: https://medium.com/@bhanuchaddha/spring-boot-devtools-on-intellij-c0ab3f9afa63
  - spring boot configuration processor - helps developers in providing available configuration options in yml/properties files

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
