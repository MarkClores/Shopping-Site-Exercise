# Ubermelon Shopping Site

## **Project Overview**

The Ubermelon shopping site is an e-commerce platform built with Flask, SQLite, Jinja, and Python. It allows users to browse melons, add them to their shopping carts, and manage their cart either as a guest or logged-in user. The application also offers user authentication, account management, and secure password storage using SHA256 hashing.

## **Setup Instructions**

### **Step 1. Install Python and Flask**

-   Ensure Python (version 3.8 or higher) is installed on your system.
-   Install Flask using pip: `pip install flask` 

### **Step 2. Install Additional Dependencies**

-   Open a terminal in the project’s main directory, where the `requirements.txt` file is located.
-   Install the required dependencies: `pip install -r requirements.txt` 

### **Step 3. Set up the Database**

-   The project uses SQLite as its database system. Ensure the `melons.db` file is located in the root directory of the project.
-   If you want to inspect the database or modify it, use SQLite commands: `sqlite3 melons.db` 

### **Step 4. Run the Application**

-   After setting up the environment, run the Flask application by executing: `python shoppingsite.py` 

-   Open your browser and navigate to `http://127.0.0.1:5000` to access the site.

### **Project Structure**

-   `static/`: Contains static files like CSS and images.
-   `templates/`: Contains HTML templates.
-   `shoppingsite.py`: Main Flask application.
-   `model.py`: Contains database interaction and model classes.
-   `melons.db`: SQLite database file.
-   `requirements.txt`: List of dependencies.

----------

## **User Manual**

### **1. Accessing the Application**

-   Once the application is running, navigate to `http://127.0.0.1:5000` in your browser to access the home page.

### **2. Navigating the Application**

#### **Homepage**

-   The homepage showcases top-selling melons and allows users to navigate to the full melon list or the cart.

#### **Melon List**

-   Click the "Melons" link in the navbar to view the full list of available melons.
    -   **Details**: View details of a specific melon, including price, type, and color.
    -   **Add to Cart**: Add a melon to your cart directly from the melon list or details page.

#### **Shopping Cart**

-   Click "My Melon Cart" in the navbar to view the items you have added to your cart.
    -   **Remove Items**: Remove a melon by clicking "Remove" next to the item.
    -   **Checkout**: Proceed to checkout (feature under development).
    -   **Back to Shop**: Return to the melon list.

#### **Signing Up**

-   Click "Login" in the navbar, then select "Sign Up" if you don’t have an account.
    -   Fill in your details, including email, first name, last name, and password (minimum 8 characters).
    -   Passwords are securely hashed using SHA256.

#### **Logging In**

-   Once you have created an account, log in using your email and password.
    -   After logging in, you can manage your cart, which will persist across sessions.

#### **Logging Out**

-   Click "Log Out" in the navbar to end your session and clear the cart from the session.

### **3. New Features and Functionalities**

#### **Password Hashing**

-   Passwords are now securely hashed using SHA256 to ensure security and prevent password exposure.

#### **Cart Persistence**

-   Logged-in users have their cart saved across sessions, meaning you can log out and return without losing items in your cart.

----------

## **Troubleshooting**

### **Common Issues**

#### 1. **Database Not Found**

-   Ensure that the `melons.db` file is in the root folder of your project. If missing, create the database using the provided schema.

#### 2. **Dependencies Not Installed**

-   Double-check that all dependencies are installed by running `pip install -r requirements.txt`.

#### 3. **Password Errors**

-   Ensure the password entered during signup is at least 8 characters long and matches the confirmation field.
