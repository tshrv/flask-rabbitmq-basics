# flask-rabbitmq-basics
Two microservices, where data processing relies on message passing / event-driven architecture


Involved entities -
1. Primary backend
   - Flask app
   - Exposes a POST api to receive data, store in database in "pending" state, puts an event on message queue.
   - Exposes a GET api to show record details.
2. Data processing service
   - Python service, listening to events on message queue, picks data from database, processes it and updates in the database in "complete" state.
3. Message queue
   - RabbitMQ
4. Database
   - MongoDB