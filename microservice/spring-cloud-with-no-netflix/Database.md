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