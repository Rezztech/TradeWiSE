# Financial Report Crawling and Scheduling System

## Requirements
* Historical Data Retrieval:
The system needs to fetch historical financial reports until a 'No Data Found' situation is encountered. This implies the system must be capable of going back in time, retrieving available reports, and stopping the process when it hits a period with no available data.
* Retrieval of New Reports Over Time:
As time progresses, the system should periodically attempt to retrieve new financial reports. This ensures that the most up-to-date financial data is always collected.
* Inclusion of New Companies:
The system should automatically add new companies to the queue as they get listed on the stock market. This requires the system to be dynamic and responsive to changes in the market.
* Resuming Tasks After Service Restart:
In case of a service interruption or restart, the system should be able to continue its tasks from where it left off. This feature is crucial for maintaining data integrity and ensuring that no data collection is missed due to system downtime.
* Adaptation to Database Schema Changes:
If there are changes to how data is stored in the database (schema updates), the system should be capable of re-crawling the financial reports of all companies and storing them according to the new format. Additionally, it would be beneficial to have a table in the database that records the version of each company's report, to track changes and updates over time.


## Approaches
### API-Based Task Scheduling
In this approach, the scheduling service sends tasks to the crawler service via API calls. The crawler service receives these calls and performs the tasks asynchronously.
#### Pros:
* Decoupling: Services are loosely coupled, allowing for independent updates and maintenance.
* Flexibility: Easily add more consumers or providers as long as they adhere to the same API protocol.
* Scalability: Services can be distributed across different servers or containers for easier horizontal scaling.

#### Cons:
* Network Latency: API calls involve network communication, which may introduce delays.
* Error Handling: Network issues or service downtime require additional error-handling mechanisms.
* Increased Complexity: Maintaining APIs and handling asynchronous calls adds complexity to the system.

#### Suitability for Your Requirements:
* Good for handling dynamic addition of new companies and tasks (Requirements 3).
* Can be designed to resume tasks after service restarts (Requirement 4).
* Suitable for adapting to database schema changes, as API endpoints can be adjusted to accommodate new data formats (Requirement 5).

### Shared Task Queue
This method involves a scheduling service placing tasks in a shared queue (like RabbitMQ, Kafka, or Redis), from which the crawler service periodically fetches and executes tasks.

#### Pros:
* Efficiency: Reduces network calls, typically faster to retrieve tasks from a queue.
* Reliability: Many queue systems offer persistence and message acknowledgment features to ensure no task loss.
* Scalability: Easy to add more producers or consumers.

#### Cons:
* Additional Component: Requires maintaining an additional queue system.
* Complexity: Introducing a new system component adds to the overall architecture complexity.

#### Suitability for Your Requirements:
* Efficient for retrying tasks for new financial reports over time (Requirement 2).
* Ideal for scaling up with new companies joining the market (Requirement 3).
* Can be designed for resiliency, allowing continuation of tasks post service restart (Requirement 4).
* Potentially integrate with a version tracking system in the database for format changes (Requirement 5).

### Periodic Database Polling
In this model, the scheduling service writes tasks to a database, and the crawler service regularly queries the database for new tasks.

#### Pros:
* Simplicity: If you're already using a database, this method doesn't require introducing new technology.
* Persistence: The database ensures data persistence and consistency.

#### Cons:
* Latency: There might be a delay from task entry to discovery by the crawler service.
* Database Load: Frequent polling can impact database performance.
* Scalability Limits: The pressure on the database increases with the volume of tasks.

#### Suitability for Your Requirements:
* Can handle historical data retrieval until 'No Data Found' scenarios (Requirement 1).
* Suitable for retrying tasks for new reports as time progresses (Requirement 2).
* Can accommodate new companies but might require additional logic for dynamic task generation (Requirement 3).
* Database persistence supports task continuation after service restarts (Requirement 4).
* Adaptable to schema changes with database version tracking (Requirement 5).
