# Developer Store

A full-stack e-commerce web application built with Flask and Python.

The project was created as a practical way to work with user authentication, relational databases, shopping carts, checkout, payments, Stripe webhooks, and order management in a single application.


## Live Demo

[Developer Store](https://e-commerce-65u9.onrender.com)

## Features

* User registration and login
* Password hashing with Werkzeug
* Product catalog
* Product images served locally
* Shopping cart
* Increase, decrease, and remove cart items
* Checkout page
* Stripe Checkout integration
* Stripe webhook for confirming completed payments
* Order creation after successful payment
* Order history
* Automatic cart clearing after a successful order
* Protected routes using Flask-Login

## Technologies

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* SQLite
* Flask-Login
* Werkzeug
* Stripe
* HTML
* CSS
* Bootstrap
* Jinja2
* python-dotenv

## How It Works

### Authentication

Users can create an account and log in to the application.

Passwords are never stored as plain text. They are hashed using Werkzeug before being saved to the database.

Authenticated users can access their cart, checkout, and order history.

### Products

Products are stored in a SQLite database and displayed dynamically on the home page.

Product images are stored locally in:

```text
static/images/
```

Each product contains information such as its name, description, price, and image path.

### Shopping Cart

Logged-in users can add products to their cart.

The cart allows users to:

* Add products
* Increase quantities
* Decrease quantities
* Remove products
* View individual item subtotals
* View the total order amount

Cart items are associated with the currently logged-in user.

### Checkout and Payments

The application uses Stripe Checkout to process payments.

When a user proceeds to payment, the application creates a Stripe Checkout Session based on the products and quantities currently in their cart.

Stripe handles the payment page, while the application receives the result through a webhook.

### Stripe Webhook

The `/webhook` endpoint receives Stripe's `checkout.session.completed` event.

After a successful payment, the application:

1. Identifies the user associated with the Stripe session.
2. Retrieves the user's cart.
3. Calculates the order total.
4. Creates an `Order`.
5. Creates the corresponding `OrderItems`.
6. Removes the purchased items from the cart.
7. Stores the Stripe Checkout Session ID.

The Stripe Session ID is also used to prevent the same payment event from creating duplicate orders.

### Order History

After completing a purchase, users can access their order history.

Each order contains:

* Order date
* Order status
* Total amount
* Products purchased
* Quantity
* Price at the time of purchase

## Database Structure

The application uses SQLAlchemy models to represent the main entities:

```text
User
  │
  ├── CartItem ─── Product
  │
  └── Order
        │
        └── OrderItems ─── Product
```

Main models:

* `User`
* `Product`
* `CartItem`
* `Order`
* `OrderItems`

Relationships between these models allow users to have multiple cart items and orders, while orders can contain multiple products.

## Project Structure

```text
e-commerce/
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── scripts.js
│   └── images/
│       ├── developer-tshirt.jpg
│       ├── gamer-chair.jpg
│       └── gamer_keyboard.jpeg
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── cart.html
│   ├── checkout.html
│   ├── orders.html
│   └── payment_success.html
│
├── main.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/gustavodev6331/e-commerce.git
cd e-commerce
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
STRIPE_SECRET_KEY=your_stripe_test_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

The `.env` file should not be committed to GitHub.

### 5. Run the application

```bash
python main.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

## Testing Stripe Locally

Because Stripe cannot directly access a local Flask server, the Stripe CLI can be used to forward Stripe webhook events to the local application.

Start the Flask application first:

```bash
python main.py
```

Then, in another terminal, run:

```bash
stripe listen --events checkout.session.completed --forward-to localhost:5000/webhook
```

The Stripe CLI will provide a webhook signing secret. Use that value as:

```env
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

You can then complete a test payment through the application and Stripe will forward the `checkout.session.completed` event to the local `/webhook` endpoint.

This setup is only required for local Stripe testing. The deployed application uses a Stripe webhook endpoint configured for the Render deployment.

