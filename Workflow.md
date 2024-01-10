Project: Online shop selling books

Use Github as a lifecycle management software

Use python as the programming language


Implement an architecture based on microservices and serverless functions

1. **Product Catalog Service** :

* **Purpose** : Manages book listings, details, prices, and categories.
* **APIs** : RESTful APIs to add, update, delete, and retrieve product information.

2. **User Handling Service** :

* **Purpose** : Manages user accounts, authentication, and profiles.
* **APIs** : Integrations with Cognito for authentication and custom APIs for profile management.

3. **Shopping Cart Service** :

* **Purpose** : Manages items that users intend to purchase.
* **APIs** : APIs to add, remove items from the cart, and view the current cart.

4. **Order Service** :

* **Purpose** : Handles order processing, order history, and order status.
* **APIs** : APIs to place orders, view order history, and track order status.

5. **Payment Service** :

* **Purpose** : Simulates payment processing.
* **APIs** : A mock API to simulate payment success or failure.
