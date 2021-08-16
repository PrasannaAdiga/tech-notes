## Testing
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