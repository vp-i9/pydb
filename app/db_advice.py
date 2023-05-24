from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Product, Vendor

# Create SQLAlchemy engine and session
engine = create_engine("sqlite:///db.sqlite")
Session = sessionmaker(bind=engine)
session = Session()

# Define the join condition
join_condition = Product.vendor_id == Vendor.id

# Apply the join condition in a query
query = session.query(Product, Vendor).join(Vendor, join_condition)

# Execute the query
results = query.all()

# Print the results
for product, vendor in results:
    print(f"Product: {product.name}, Vendor: {vendor.name}")



# ----------------------------------------

from sqlalchemy import func

# Assuming you have created a session object named 'session'
unique_pairs_count = session.query(func.count(func.distinct(Product.id_reference, Product.id_expiry_date))).scalar()

print(f"Number of unique pairs: {unique_pairs_count}")

# SELECT COUNT(DISTINCT id_reference, id_expiry_date) FROM products;

# ----------------------------------------


from sqlalchemy import func

# Assuming you have created a session object named 'session'
query = session.query(Product.id_reference, Product.id_expiry_date, func.count().label('count'))
query = query.group_by(Product.id_reference, Product.id_expiry_date)

unique_pairs = query.all()

for pair in unique_pairs:
    id_reference, id_expiry_date, count = pair
    print(f"Pair: {id_reference}, {id_expiry_date} | Count: {count}")

# ----------------------------------------

from sqlalchemy import func

# Assuming you have created a session object named 'session'
product_name = 'eluvia stent system'
query = session.query(Product.id_reference, Product.id_expiry_date, func.count().label('count'))
query = query.filter(Product.name == product_name)
query = query.group_by(Product.id_reference, Product.id_expiry_date)

unique_pairs = query.all()

for pair in unique_pairs:
    id_reference, id_expiry_date, count = pair
    print(f"Pair: {id_reference}, {id_expiry_date} | Count: {count}")
