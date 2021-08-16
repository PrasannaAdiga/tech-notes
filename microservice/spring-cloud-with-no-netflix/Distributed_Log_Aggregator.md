##Distributed Log Aggregator
To aggregate the logger data from different micro services into one place for analyzing purpose

 - Use the tools like Logstash-logback-encoder, logback-access-spring-boot-starter, Logstash, Elastic Search and Kibana
 
### Logstash-logback-encoder 
To store the logback log information which are defined in the application logic, into a physical log file, in a structured format lke JSON or to append the log data into Console in a specific pattern
 - If 'logstash-logback-encoder' plugin is in the classpath, it will read the appender details to Logstash which are defined in the 'logback-spring.xml' file and generates a local physical file which contains all the logs data of the application, in a specific format which is required by Logstash
 - Further, details of the 'logback-spring.xml' file provided in the below logback section

### logback-access-spring-boot-starter
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

### Logstash
To Collect, Filter and Transform data through configuration file (logstash.conf)

#### To read application logs and send to Elastic Search
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
 - Filter: If we use logstash-logback-encoder plugin we automatically send JSOn format of log details to logsatsh. so no need to define any formatting logic in filter section. else, we can use Grok filter to split, aggregate and transform unstructured log data to structured JSON format. 
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

#### To read events from Kafka and send to Elastic Search

 - Use the Kafka input plugin provided by Elastic Stack, which can read data from Kafka topic(s) and send those read data to specific Elastic index. 
 - If Kafka topic contains data in the byte format, where Kafka Producer sent the data by using Avro and Schema Registry, then Logstash also needs Avro and Schema Registry to deserialize these data into a specific Avro schema model
 - For that, use the plugin 'logstash-codec-avro_schema_registry', which can be installed through 'logstash-plugin' script provided in bin directory of Logstash
 ```
 logstash-plugin install logstash-codec-avro_schema_registry
 ---
 input {
   kafka {
     ...
     codec => avro_schema_registry {
       endpoint => "http://localhost:8081" #Schema Registry URL from where it can fetch Registered Schema definitions
     }
     value_deserializer_class => "org.apache.kafka.common.serialization.ByteArrayDeserializer"
   }
 }
 - The above configuration, will read the data in byte format from Kafka topic and uses registred schema definition which are in Avro data format from 'Schema Registry' and desirialize the data into those schema format and send them to ES, so that we can visualize such events in Kibana later
 ```
 - Complete such Logstash input and output configuration is as below:
 ```
 input {
   kafka {
     type => "product-event-data"
     group_id => "bookstore-product-group"
     bootstrap_servers => "localhost:19092,localhost:29092,localhost:39092"
     topics => ["bookstore-product-topic"]
     auto_offset_reset => "earliest"
     enable_auto_commit => "false"
     session_timeout_ms => 10000
     heartbeat_interval_ms => 3000
     max_poll_interval_ms => 300000
     max_poll_records => 500
     poll_timeout_ms => 150
     decorate_events => true
     codec => avro_schema_registry {
       endpoint => "http://localhost:8081"
     }
     key_deserializer_class => "org.apache.kafka.common.serialization.StringDeserializer"
     value_deserializer_class => "org.apache.kafka.common.serialization.ByteArrayDeserializer"
   }
 } 
 output {
   elasticsearch {
      hosts => ["https://bc4315f93c074ac995953bb0696639a9.eastus2.azure.elastic-cloud.com:9243"]
      index => "bookstore-product-message"
      user => "<elastic_host_username>"
      password => "<elastic_host_password>"
   }
 }
 ```

### Elastic Search
Search Engine to store and search all the application related log data or application related events for analysis purpose

### Kibana
A visual interface to search and visualize log file records, which are read from Elastic Search
