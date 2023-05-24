import csv
from contextlib import contextmanager
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from models import Vendor, Product, Purchase

engine = create_engine("sqlite:///db.sqlite")
Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)


@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_products_by_vendor(vendor):
    return vendor.products


with db_session() as session:
    # vendor = session.query(Vendor).get(1) #where vendor_id is 1

    # ---finds all products by vendor
    # products = get_products_by_vendor(vendor)
    # for product in products:
    #     print(f"{vendor.name} has this product: {product}")
    # product = session.query(Product).filter(Product.name == 'eluvia stent system').first()

    # ////////////////////////////

    # ---finds partial matches to product search string
    # search = 'stent'
    # product = session.query(Product).filter(Product.name.like(f'%{search}%')).first()
    # print(product)
    # print('almost somewhere')

    # # ////////////////////////////

    # start_date = datetime(2019, 1, 1)
    # end_date = datetime(2023, 12, 31)

    # #---finds between two specific dates
    # # Query products within the date range
    # products = session.query(Product).filter(Product.id_expiry_date >= start_date, Product.id_expiry_date <= end_date).all()

    # # Iterate over the retrieved products
    # for product in products:
    #     print(f"{product}, with expiry of {product.id_expiry_date}")
    #     print('found this')

    # # ////////////////////////////

    # ---finds between current date and precisely 3 months in future, results filtered

    # # Set the start date as the current time
    # start_date = datetime.now()

    # # Add a relativedelta of 3 months to the start date
    # end_date = start_date + relativedelta(months=3)

    # # Query products within the date range
    # products = session.query(Product).filter(Product.id_expiry_date >= start_date, Product.id_expiry_date <= end_date).all()

    # # ////////////////////////////

    # ---finds precise or similar string match, with unique pairs of reference id-expiry date

    product_name = "eluvia stent system"
    # product = session.query(Product).filter(Product.name.like(f'%{product_name}%')).first()

    query = session.query(
        Product.id_reference, Product.id_expiry_date, func.count().label("count")
    )
    query = query.filter(Product.name == product_name)
    query = query.group_by(Product.id_reference, Product.id_expiry_date)

    unique_pairs = query.all()

    for pair in unique_pairs:
        id_reference, id_expiry_date, count = pair
        print(f"Pair: {id_reference}, {id_expiry_date} | Count: {count}")

    test = 2
    check = session.query(Vendor).filter(Vendor.id == 90).first()
    print(check)
    if check == test:
        print("present")
    else:
        print("not here")

    start_date = datetime.now()
    print(start_date.strftime("%m/%d/%Y"))

    # Add a relativedelta of 3 months to the start date
    end_date = start_date + relativedelta(months=3)

    # Query products within the date range
    products = (
        session.query(Product)
        .filter(
            Product.id_expiry_date >= start_date, Product.id_expiry_date <= end_date
        )
        .all()
    )

    print(f"These items expiring within next 3 months: {products}")

    products = session.query(Product).filter(Product.id_expiry_date >= end_date).all()

    for p in products:
        print(f"These items expiring within next 3 months: {p.name}")

    print(len(products))


# Usage example
# Assuming you have a vendor object named 'vendor'
# products = get_products_by_vendor(vendor) # this vendor object needs to derive from db retrieval or created current session
#
# for product in products: #iterating over a list, can do anything needed
#     print(product)


"""
for creating a vendor object, find an existing by vendor id:
# Retrieve the Vendor with id 1
    vendor = session.query(Vendor).get(1)




"""
