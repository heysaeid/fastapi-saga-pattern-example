# fastapi-saga-pattern-example
![Saga Pattern Image](images/saga-pattern.png)

**Note:** Please note that the emphasis of this project is not on the overall architecture, code quality, or best practices. The code provided serves as a simplified example to illustrate the application of the Saga Choreography pattern and may not follow all the principles of clean code or optimal architectural design.


The Saga design pattern is used for managing distributed transactions. In this pattern, a large transaction is broken down into smaller, independent operations. Each operation can be executed separately, and for every main operation, there’s a compensating action that undoes changes if something goes wrong.

To implement Saga, we have two models: choreography and orchestration.
## Choreography Model
In this model, each service starts and manages its operations in sequence. After a service completes its task, it notifies the next service to begin. If an issue arises in any of the services, compensating actions are triggered in reverse order to undo the previous steps.

### Advantages:
Simplicity in implementation, as services automatically interact with each other without needing a central coordinator.
No single point of failure (SPOF), since the operations are distributed among the services.

### Disadvantages:
There’s a higher risk of cyclic dependencies, as services depend on each other’s instructions.

## Orchestration Model
Unlike choreography, this model has a central coordinator that manages all the steps and services. This Saga Orchestrator controls both the main operations and the compensating actions.

### Advantages:
It’s well-suited for managing complex processes, especially when there are many services involved.
The chance of cyclic dependencies is very low because the orchestrator handles everything.

### Disadvantages:
Implementing the orchestration logic can be complex.
It introduces a single point of failure (SPOF), as the orchestrator manages all processes.
In conclusion, choosing between these models depends on the specific needs of the project. It’s important to consider the complexity of the system, the number of services, and the need for compensating actions when selecting the right approach.


# Choreography Pattern
This project implements an Order Management System using the Saga Choreography Pattern to manage distributed transactions across three services: OrderService, PaymentService, and DeliveryService. The system uses an event-driven architecture to ensure that each service can independently handle its part of the transaction while staying synchronized through events.

### System Overview
The system consists of the following services:<br>
<strong>OrderService:</strong> Manages customer orders.<br>
<strong>PaymentService:</strong> Handles payment transactions.<br>
<strong>DeliveryService:</strong> Manages deliveries for confirmed orders.<br>

The Saga Choreography Pattern is used to coordinate the process across these services. Each service listens for and reacts to specific events, ensuring consistency across the system without a central coordinator.

### Workflow
#### 1. Create an Order:
- A new order is created via the /orders/create_order endpoint. 
- After successfully creating the order, an event create-payment is emitted. 

#### 2. Create a Payment
- The PaymentService receives the create-payment event and creates a payment with the status pending. 
- The user can then confirm or cancel the payment using the following endpoints:
  - payments/confirm to confirm the payment.
  - payments/cancel to cancel the payment.

#### 3. Payment Confirmation or Cancellation
- **Cancellation:**<br>
If the user cancels the payment, the system emits a cancel-order event:<br>
  - OrderService receives the cancel-order event and marks the order as cancelled, ending the process.
- **Confirmation:**<br>
If the user confirms the payment:
  - PaymentService emits an order-confirmed event.
  - OrderService updates the order status to confirmed and emits a create-delivery event.

#### 4. Delivery Creation

- **Success:**<br>
  DeliveryService creates a delivery for the order. If the delivery is successfully assigned to a dealer, the process ends.

- **Failure:**<br>
If the delivery cannot be assigned, DeliveryService emits a cancel-payment event:
  - PaymentService cancels the payment and emits a cancel-order event.
  - OrderService marks the order as cancelled.

```mermaid
graph TD
    A[Create Order] --> B{Payment Created}
    B -->|Payment Confirmed| C[Update Order Status to Confirmed]
    C --> D{Delivery Created}
    D -->|Delivery Assigned| E[End] 
    D -->|Delivery Not Assigned| F[Cancel Payment] 
    F --> G[Cancel Order]
    B -->|Payment Cancelled| G[Cancel Order]
    G --> E[End]
```