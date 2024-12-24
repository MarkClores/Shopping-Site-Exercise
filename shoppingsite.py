from flask import Flask, render_template, redirect, flash, session, request, url_for
import jinja2
import hashlib
import model

app = Flask(__name__)
app.secret_key = 'this-should-be-something-unguessable'
app.jinja_env.undefined = jinja2.StrictUndefined

# Helper functions

def initialize_cart():
    """Ensure the cart is initialized in the session and/or database."""
    if 'logged_in_customer_email' in session:
        customer_email = session['logged_in_customer_email']
        # Fetch cart from the database for the logged-in user
        cart_items = model.Cart.get_cart_for_customer(customer_email)
        session['cart'] = {item[0]: item[1] for item in cart_items}  # melon_id: quantity
    else:
        if 'cart' not in session or not isinstance(session['cart'], dict):
            session['cart'] = {}



def calculate_cart_summary():
    """Calculate total price and quantity in the cart."""
    total_price = 0
    total_quantity = 0
    cart_dict = {}

    for melon_id in session['cart']:
        cart_dict[melon_id] = cart_dict.get(melon_id, 0) + 1

    for melon_id, quantity in cart_dict.items():
        melon = model.Melon.get_by_id(melon_id)
        total_price += melon.price * quantity
        total_quantity += quantity

    return total_price, total_quantity


@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    print(melon) 
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def cart():
    """Display the content of the shopping cart."""
    initialize_cart()  # Ensure the cart is initialized correctly
    
    cart_dict = session.get('cart', {})
    melon_info_tuples = []
    total_price, total_quantity = 0, 0

    for melon_id, quantity in cart_dict.items():
        melon = model.Melon.get_by_id(melon_id)
        melon_info_tuples.append((melon.common_name, quantity, melon.price, melon_id))
        total_price += melon.price * quantity
        total_quantity += quantity

    return render_template("cart.html", 
                           melon_info_tuples=melon_info_tuples, 
                           total_price=total_price, 
                           total_quantity=total_quantity)




@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to the cart and redirect to the shopping cart page."""
    if 'logged_in_customer_email' in session:
        # Logged-in user
        customer_email = session['logged_in_customer_email']
        
        # Add melon to the database cart
        model.Cart.add_to_cart(customer_email, id)
        
        flash("Melon was successfully added to the cart.")
    else:
        # Logged-out user: store in session temporarily
        if 'cart' not in session or not isinstance(session['cart'], dict):
            session['cart'] = {}
        
        session['cart'][str(id)] = session['cart'].get(str(id), 0) + 1  # Add melon to the session cart
        
        flash("Melon was successfully added to the temporary cart.")
    
    return redirect(url_for('cart'))  # Redirect to the shopping cart page





@app.route("/remove_from_cart/<int:id>")
def remove_from_cart(id):
    """Remove a melon from the cart and redirect to the shopping cart page."""
    if 'logged_in_customer_email' in session:
        customer_email = session['logged_in_customer_email']
        # Remove from the database cart
        model.Cart.remove_from_cart(customer_email, id)
        flash("Melon was successfully removed from the cart.")
    else:
        melon_id_str = str(id)
        if melon_id_str in session['cart']:
            del session['cart'][melon_id_str]  # Remove from the session cart
            flash("Melon was successfully removed from the cart.")
        else:
            flash("Melon not found in cart.")
    
    return redirect("/cart")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle the creation of a new user account."""
    if 'logged_in_customer_email' in session:
        flash("You are already logged in.")
        return redirect("/melons")  # or any other page you prefer

    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")  # Add first name field
        last_name = request.form.get("last_name")    # Add last name field
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Password length validation
        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return redirect("/signup")

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect("/signup")

        # Check if user already exists
        existing_user = model.Customer.get_by_email(email)
        if existing_user:
            flash("Email already in use. Please log in or use a different email.")
            return redirect("/signup")

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Create the new user and add to the database
        new_user = model.Customer.create(email=email, first_name=first_name, last_name=last_name, password=hashed_password)

        flash("Account created successfully. Please log in.")
        return redirect("/login")

    return render_template("signup.html")


@app.route("/login", methods=["GET"])
def login():
    """Show login form."""
    return render_template("login.html")

@app.route('/logout')
def logout():
    """Logs the user out and clears the cart."""
    # Clear the cart from the session
    session.pop('cart', None)
    
    # Clear the logged-in user's email
    session.pop('logged_in_customer_email', None)
    
    flash('You have been logged out, and your cart has been cleared.')
    
    return redirect(url_for('login'))  # Redirect to login page



@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site."""
    email = request.form.get('email')
    password = request.form.get('password')

    customer = model.Customer.get_by_email(email)

    if not customer:
        flash('No such email')
        return redirect('/login')

    # Hash the entered password and compare with stored hash
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if hashed_password == customer.password:
        session['logged_in_customer_email'] = email  # Store the email in session, not id
        # session['customer_id'] = customer.id  # Remove this line

        # If there is a cart in the session, transfer it to the database
        if 'cart' in session:
            for melon_id, quantity in session['cart'].items():
                model.Cart.add_to_cart(customer.email, melon_id)  # Use email instead of customer.id

        flash('Login successful')
        return redirect('/melons')
    else:
        flash('Incorrect password')
        return redirect('/login')



@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
