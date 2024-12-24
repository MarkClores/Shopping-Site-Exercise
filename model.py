"""Model for Ubermelon shopping site."""

import sqlite3
import hashlib

class Melon(object):
    """An Ubermelon Melon type.

    A wrapper object that corresponds to rows in the melons table.
    """

    def __init__(self,
                 id,
                 melon_type,
                 common_name,
                 price, imgurl,
                 flesh_color,
                 rind_color,
                 seedless):
        self.id = id
        self.melon_type = melon_type
        self.common_name = common_name
        self.price = price
        self.imgurl = imgurl
        self.flesh_color = flesh_color
        self.rind_color = rind_color
        self.seedless = bool(seedless)

    def price_str(self):
        """Return price formatted as string $x.xx"""

        return "$%.2f" % self.price

    def __repr__(self):
        """Convenience method to show information about melon in console."""

        return "<Melon: %s, %s, %s>" % (
            self.id, self.common_name, self.price_str())

    @classmethod
    def get_all(cls, max=30):
        """Return list of melons.

        Query the database for the first [max] melons, returning each as a
        Melon object
        """

        cursor = db_connect()
        QUERY = """
                  SELECT id,
                         melon_type,
                         common_name,
                         price,
                         imgurl,
                         flesh_color,
                         rind_color,
                         seedless
                   FROM Melons
                   WHERE imgurl <> ''
                   LIMIT ?;
               """

        cursor.execute(QUERY, (max,))
        melon_rows = cursor.fetchall()

        # list comprehension to build a list of Melon objects by going through
        # the database records and making a melon for each row. This is done
        # by unpacking in the for-loop.

        melons = [Melon(*row) for row in melon_rows]

        print(melons)

        return melons

    @classmethod
    def get_by_id(cls, id):
        """Query for a specific melon in the database by the primary key"""

        cursor = db_connect()
        QUERY = """
                  SELECT id,
                         melon_type,
                         common_name,
                         price,
                         imgurl,
                         flesh_color,
                         rind_color,
                         seedless
                   FROM Melons
                   WHERE id = ?;
               """

        cursor.execute(QUERY, (id,))

        row = cursor.fetchone()

        if not row:
            return None

        melon = Melon(*row)

        return melon


class Customer(object):
    """Ubermelon customer.

    A wrapper object that corresponds to rows in the customers table.
    """

    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def __repr__(self):
        """Convenience method to show information about customer in console."""
        return "<Customer: %s, %s>" % (self.email, self.first_name + ' ' + self.last_name)

    @classmethod
    def get_by_email(cls, email):
        """Query for a specific customer in the database by the primary key"""

        cursor = db_connect()
        QUERY = """
            SELECT email, first_name, last_name, password FROM Customers 
            WHERE email = ? """

        cursor.execute(QUERY, (email,))
        row = cursor.fetchone()

        if not row:
            return None

        customer = Customer(*row)
        return customer

    @classmethod
    def create(cls, email, first_name, last_name, password):
        """Create a new customer and insert them into the database."""
        
        cursor = db_connect()
        QUERY = """
            INSERT INTO Customers (email, first_name, last_name, password)
            VALUES (?, ?, ?, ?)
        """

        cursor.execute(QUERY, (email, first_name, last_name, password))

        # Commit the changes and close the connection
        cursor.connection.commit()

        # Return the new customer instance
        return cls(email, first_name, last_name, password)
    
class Cart(object):
    """Ubermelon shopping cart for a specific customer."""

    @classmethod
    def get_cart_for_customer(cls, customer_email):
        """Get the cart for a specific customer."""
        cursor = db_connect()
        QUERY = """
            SELECT melon_id, quantity
            FROM Cart
            WHERE customer_email = ?;
        """
        cursor.execute(QUERY, (customer_email,))
        cart_items = cursor.fetchall()
        return cart_items

    @classmethod
    def add_to_cart(cls, customer_email, melon_id):
        """Add a melon to the cart of a specific customer."""
        cursor = db_connect()
        QUERY = """
            INSERT OR REPLACE INTO Cart (customer_email, melon_id, quantity)
            VALUES (?, ?, COALESCE((SELECT quantity FROM Cart WHERE customer_email = ? AND melon_id = ?), 0) + 1);
        """
        cursor.execute(QUERY, (customer_email, melon_id, customer_email, melon_id))
        cursor.connection.commit()

    @classmethod
    def remove_from_cart(cls, customer_email, melon_id):
        """Remove a melon from the cart of a specific customer."""
        cursor = db_connect()
        QUERY = """
            DELETE FROM Cart
            WHERE customer_email = ? AND melon_id = ?;
        """
        cursor.execute(QUERY, (customer_email, melon_id))
        cursor.connection.commit()





def db_connect():
    """Return a database cursor."""
    conn = sqlite3.connect("melons.db")
    conn.execute('PRAGMA journal_mode=WAL;')  # Enable WAL mode
    cursor = conn.cursor()
    return cursor

