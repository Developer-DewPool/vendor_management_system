# Vendor Management System with Performance Metrics

This Django project provides an API for managing vendors, purchase orders, and calculating vendor performance metrics. The API supports token-based authentication and can be tested using tools like Curl, Postman, or the Swagger documentation.

## Setup Instructions

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Developer-DewPool/vendor_management_system.git
    ```

2. **Navigate to Project Directory**
    ```bash
    cd vendor_management_system
    ```

3. **Create Virtual Environment**
    ```bash
    python3 -m venv venv
    ```

4. **Activate Virtual Environment**
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

5. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

6. **Apply Database Migrations**
    ```bash
    python manage.py migrate
    ```

7. **Create Superuser**
    ```bash
    python manage.py createsuperuser
    ```

8. **Run Development Server**
    ```bash
    python manage.py runserver
    ```

9. **Access the Admin Interface**
    - Admin Interface: [http://localhost:8000/admin/](http://localhost:8000/admin/)
    - Log in using the superuser credentials created earlier.

## Additional Technical Considerations

- **Efficient Calculation**: Ensure that the logic for calculating metrics is optimized to handle large datasets without significant performance issues.
- **Data Integrity**: Include checks to handle scenarios like missing data points or division by zero in calculations to maintain data integrity.
- **Real-time Updates**: Consider using Django signals to trigger metric updates in real-time when related PO data is modified. This ensures that performance metrics are always up-to-date.

## Additional Notes

- Ensure that the Django development server is running while testing the API endpoints.
- Make sure to obtain authentication tokens before accessing secured endpoints.
- Follow RESTful principles when making requests to the API.
- Ensure proper data validation to maintain data integrity.

## Python Version

This project is developed using Python 3.x.

## API Endpoints

- **purchase_orders**
  - `GET /purchase_orders/` (purchase_orders_list)
  - `POST /purchase_orders/` (purchase_orders_create)
  - `GET /purchase_orders/{id}/` (purchase_orders_read)
  - `PUT /purchase_orders/{id}/` (purchase_orders_update)
  - `DELETE /purchase_orders/{id}/` (purchase_orders_delete)
  - `POST /purchase_orders/{id}/acknowledge/` (purchase_orders_acknowledge_create)

- **token**
  - `POST /token/` (token_create)

- **vendors**
  - `GET /vendors/` (vendors_list)
  - `POST /vendors/` (vendors_create)
  - `GET /vendors/{id}/` (vendors_read)
  - `PUT /vendors/{id}/` (vendors_update)
  - `DELETE /vendors/{id}/` (vendors_delete)
  - `GET /vendors/{id}/performance/` (vendors_performance_read)

## Using the API Endpoints

### Authentication

- Token-based authentication is required for accessing the API endpoints. Obtain a token by sending a POST request to `/token/` with valid credentials (username and password).

### Testing API Endpoints

- You can test the API endpoints using tools like cURL, Postman, or Swagger documentation:
  - For cURL or Postman: Use token-based authentication by including the token in the request headers (`Authorization: Token <your-token>`).
  - For Swagger documentation: Visit [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) and use basic authorization.

## Running the Test Suite

1. **Run the Tests:**
   ```bash
   python manage.py test
   ```

2. **View Test Coverage:**
   ```bash
   coverage run --source='.' manage.py test
   coverage report
   ```

## Here are detailed instructions on how to use each API endpoint along with examples:

### 1. Token Creation Endpoint

- **Endpoint:** `POST /token/`
- **Purpose:** Generate an authentication token for accessing protected endpoints.
- **Example:**
  ```bash
  curl -X POST http://127.0.0.1:8000/token/ -d "username=<your-username>&password=<your-password>"
  ```
  Response:
  ```json
  {
      "token": "<generated-token>"
  }
  ```

### 2. Purchase Orders Endpoint

#### a. List Purchase Orders

- **Endpoint:** `GET /purchase_orders/`
- **Purpose:** Retrieve a list of all purchase orders.
- **Example:**
  ```bash
  curl -H "Authorization: Token <your-token>" http://127.0.0.1:8000/purchase_orders/
  ```

#### b. Create a Purchase Order

- **Endpoint:** `POST /purchase_orders/`
- **Purpose:** Create a new purchase order.
- **Example:**
  ```bash
  curl -X POST -H "Authorization: Token <your-token>" http://127.0.0.1:8000/purchase_orders/ -d "{
            'po_number': 'PO-002',
            'vendor': str(self.vendor.pk),
            'order_date': '2024-04-30T12:00:00Z',
            'delivery_date': '2024-05-05T12:00:00Z',
            'items': [{'name': 'Item 2', 'quantity': 5}],
            'quantity': 5,
            'quality_rating': 5,
            'issue_date': '2024-04-30T09:07:51.312Z',
            'acknowledgment_date': '2024-04-30T09:07:51.312Z',
            'status': 'pending'
        }"
  ```

#### c. Retrieve a Purchase Order

- **Endpoint:** `GET /purchase_orders/{id}/`
- **Purpose:** Retrieve details of a specific purchase order by ID.
- **Example:**
  ```bash
  curl -H "Authorization: Token <your-token>" http://127.0.0.1:8000/purchase_orders/<purchase-order-id>/
  ```

#### d. Update a Purchase Order

- **Endpoint:** `PUT /purchase_orders/{id}/`
- **Purpose:** Update details of a specific purchase order by ID.
- **Example:**
  ```bash
  curl -X PUT -H "Authorization: Token <your-token>" http://127.0.0.1:8000/purchase_orders/<purchase-order-id>/ -d "{
            'po_number': 'PO-003',
            'vendor': self.vendor.pk,
            'order_date': '2024-04-30T12:00:00Z',
            'delivery_date': '2024-05-05T12:00:00Z',
            'items': [{'name': 'Item 3', 'quantity': 8}],
            'quantity': 8,
            'quality_rating': 5,
            'issue_date': '2024-04-30T09:07:51.312Z',
            'acknowledgment_date': '2024-04-30T09:07:51.312Z',
            'status': 'completed'
        }"
  ```

#### e. Delete a Purchase Order

- **Endpoint:** `DELETE /purchase_orders/{id}/`
- **Purpose:** Delete a specific purchase order by ID.
- **Example:**
  ```bash
  curl -X DELETE -H "Authorization: Token <your-token>" http://127.0.0.1:8000/purchase_orders/<purchase-order-id>/
  ```

#### f. Acknowledge a Purchase Order

- **Endpoint:** `POST /purchase_orders/{id}/acknowledge/`
- **Purpose:** Acknowledge receipt of a specific purchase order by ID.
- **Example:**
  ```bash
  curl -X POST -H "Authorization: Token <your-token>" http://127.0.0.1:8000/purchase_orders/<purchase-order-id>/acknowledge/
  ```

### 3. Vendors Endpoint

#### a. List Vendors

- **Endpoint:** `GET /vendors/`
- **Purpose:** Retrieve a list of all vendors.
- **Example:**
  ```bash
  curl -H "Authorization: Token <your-token>" http://127.0.0.1:8000/vendors/
  ```

#### b. Create a Vendor

- **Endpoint:** `POST /vendors/`
- **Purpose:** Create a new vendor.
- **Example:**
  ```bash
  curl -X POST -H "Authorization: Token <your-token>" http://127.0.0.1:8000/vendors/ -d "{
            'name': 'New Vendor',
            'contact_details': 'new_vendor@example.com',
            'address': 'New Address',
            'vendor_code': 'NEW001',
            'on_time_delivery_rate': 90.0,
            'quality_rating_avg': 4.0,
            'average_response_time': 30.0,
            'fulfillment_rate': 95.0
        }"
  ```

#### c. Retrieve a Vendor

- **Endpoint:** `GET /vendors/{id}/`
- **Purpose:** Retrieve details of a specific vendor by ID.
- **Example:**
  ```bash
  curl -H "Authorization: Token <your-token>" http://127.0.0.1:8000/vendors/<vendor-id>/
  ```

#### d. Update a Vendor

- **Endpoint:** `PUT /vendors/{id}/`
- **Purpose:** Update details of a specific vendor by ID.
- **Example:**
  ```bash
  curl -X PUT -H "Authorization: Token <your-token>" http://127.0.0.1:8000/vendors/<vendor-id>/ -d "{
            'name': 'Updated Vendor',
            'contact_details': 'updated_vendor@example.com',
            'address': 'Updated Address',
            'vendor_code': 'UPDATED001',
        }"
  ```

#### e. Delete a Vendor

- **Endpoint:** `DELETE /vendors/{id}/`
- **Purpose:** Delete a specific vendor by ID.
- **Example:**
  ```bash
  curl -X DELETE -H "Authorization: Token <your-token>" http://127.0.0.1:8000/vendors/<vendor-id>/
  ```

#### f. Retrieve Vendor Performance Metrics

- **Endpoint:** `GET /vendors/{id}/performance/`
- **Purpose:** Retrieve performance metrics of a specific vendor by ID.
- **Example:**
  ```bash
  curl -H "Authorization: Token <your-token>" http://127.0.0.1:8000/vendors/<vendor-id>/performance/
  ```

---

This README file provides clear setup instructions, details on using the API endpoints, and instructions for running the test suite. Users can choose to authenticate using token-based authentication with Curl or Postman or access the Swagger documentation for testing with basic authorization. The test suite ensures the functionality and reliability of the endpoints.