FROM openjdk:17

COPY build/libs/service-0.0.1-SNAPSHOT.war /app/app.war

CMD ["java", "-jar", "-Dspring.profiles.active=dev", "/app/app.war"]