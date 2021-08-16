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
 
## Docker Compose
To run all the above servers

 - Refer docker-compose.yml file
 - Here we are running zookeeper, schema-registry, 3 different kafka brokers and kafka-ui
  


