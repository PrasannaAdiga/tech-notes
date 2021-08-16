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
