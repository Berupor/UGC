# User-Generated Service
This is a high-load user-generated service built using FastAPI and utilizing a microservices architecture with Apache Kafka for event streaming, ClickHouse for movie watching history storage, and MongoDB for storing user reviews, likes, and movie bookmarks. The service offers a RESTful API and is designed for high-performance and scalability to handle large amounts of data and traffic. It features an easy-to-use RESTful API and is designed to handle large amounts of data and traffic, making it suitable for high-performance and scalable applications. Additionally, it offers advanced monitoring and logging capabilities, using ELK (Elasticsearch, Logstash, Kibana) stack for centralized logging and data analysis, and easy integration with other systems and services to ensure smooth performance under high loads.

## Features:
- High-performance and scalability using FastAPI
- Microservices architecture using Apache Kafka, ClickHouse, and MongoDB
- User data ingestion using Kafka topics
- Advanced monitoring and logging using ELK stack for centralized logging and data analysis
- Easy integration with other systems
- Asynchronous processing using async/await
- Advanced error handling and exception management
- Easy scalability with the ability to handle large amounts of data and high-load traffic
- ELK stack for data analysis and visualization
- User-friendly API documentation with Swagger UI/ReDoc

## Project initialization
1. Create an .env file and fill it with values from `env.example`
2. Run Docker `docker-compose up -d --build`

## API
Main API:
- $HOST/api/v1/reviews
- $HOST/api/v1/likes
- $HOST/api/v1/bookmarks

For more detailed usage and API documentation, please refer to
- $HOST/api/openapi

## Team

The User-Generated Service is a result of the hard work and dedication of a talented team of developers. Each member brings unique skills and expertise to the project, ensuring its success.


<details>
<summary>Berupor</summary>

---
Berupor is a true expert in distributed systems and high-performance architectures. With a deep understanding of Kafka and MongoDB, he drives the core business logic of the User-Generated Service, ensuring its reliability and scalability. Additionally, his expertise in testing and CI processes ensures that the service is of the highest quality.
</details>
<details>
<summary>Mburdonos</summary>

---
Maxim is a talented API designer and developer, with a passion for creating user-friendly and intuitive interfaces. He is responsible for the development of the RESTful API, as well as the documentation, which makes it easy for developers to integrate the service into their own applications. With his experience in MongoDB and Kafka, Maxim ensures that the service runs smoothly and can handle high loads.

</details><details>
<summary>Nikita</summary>

---
Nikita is a data specialist, with a deep understanding of how to store and analyze large amounts of data. He is responsible for integrating the service with ClickHouse, which allows for efficient storage and analysis of movie watching history. Additionally, his work with ELK ensures that the service has robust monitoring and logging capabilities, making it easy to diagnose and resolve issues as they arise.
</details>
