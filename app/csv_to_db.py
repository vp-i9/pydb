import csv
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dateutil.parser import parse
from models import Vendor, Product, Purchase

engine = create_engine("sqlite:///db.sqlite")
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# vendor_ids = [n for n in range(1, len(vendors))]


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


file = r"C:\Users\omniv\OneDrive\Documents\pydb2\app\inventory.csv"

vendors = {
    1: "Boston Scientific",
    2: "Abbott",
    3: "ev3",
    4: "Medtronic",
    5: "COOK Medical",
    6: "Terumo",
    7: "COULMED (COVEX)",
    8: "COVIDIEN",
}

vendors_abbrev = {
    "Boston Scientific": "BSCI",
    "Abbott": "ABBT",
    "ev3": "EV3",
    "Medtronic": "MTRNC",
    "COOK Medical": "COOK",
    "Terumo": "TRMO",
    "COULMED (COVEX)": "COULMD",
    "COVIDIEN": "CVDN",
}

with db_session() as session:
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        for index, row in enumerate(reader, start=1):
            row_number = index
            print(f"At this row: {row_number}, for item: {row}")
            company = row["company"].strip()
            product = row["product"]
            reference_id = row["reference_id"]
            ref_id_expiry_date = row["ref_id_expiry_date"]
            size = row["size"]
            expiry_date = row["expiry_date"]
            quantity = int(row["quantity"])
            v_id = 0
            for v, x in vendors.items():
                if company == x:
                    v_id = v
                    # print(v_id)

            product_check = (
                session.query(Product).filter(Product.id == row_number).first()
            )
            if product_check is None:  # create product if not existing already
                product = Product(
                    id=row_number,
                    id_reference=reference_id,
                    id_expiry_date=expiry_date,
                    ref_id_expiry_date=ref_id_expiry_date,
                    name=product,
                    size=size,
                    quantity_on_hand=quantity,
                    vendor_id=v_id,
                )
                session.add(product)
                print(f"Added product {product} to db.")
                vendor_check = session.query(Vendor).filter(Vendor.id == v_id).first()
                if vendor_check is None:  # create vendor if not existing already
                    vendor = Vendor(
                        id=v_id,
                        abbrev=vendors_abbrev[company],
                        name=company,
                    )
                    session.add(vendor)
                    print(f"Added vendor {vendor} to db.")
                    vendor.products.append(product)
                elif vendor_check == v_id:
                    print(f"Vendor {v_id} already present in db, skipping.")
                    product.vendor = v_id
            elif product_check is not None:
                print(f"Product {product} already exists, skipping.")
            session.commit()


# with db_session() as session:
#     # vendor = Vendor(
#     #     id = 1,
#     #     abbrev = 'BSCI',
#     #     name = "Boston Scientific",
#     # )
#     # product = Product(
#     #     id = 1,
#     #     id_reference = 'H749-06/25/2020',
#     #     id_expiry_date = parse('06/25/2020'),
#     #     name = 'eluvia stent system',
#     #     category = 'stent',
#     #     size = '6-10-40',
#     #     quantity_on_hand = 10,
#     #     quantity_on_order = 5,
#     #     vendor_id = 1,
#     # )
#     # purchase = Purchase(
#     #     id = 1,
#     #     product_id = 1,
#     #     vendor_abbrev = 'BSCI',
#     #     quantity = 5,
#     #     date = parse('05/20/2021'),
#     # )

#         vendor = Vendor(
#         id = 2,
#         abbrev = 'MDTRN',
#         name = "Medtronic",
#     )
#         product = Product(
#             id = 2,
#             id_reference = 'M625-09/29/2024',
#             id_expiry_date = parse('09/29/2024'),
#             name = 'balloon catheter',
#             category = 'catheter',
#             size = '9-165-35',
#             quantity_on_hand =4,
#             quantity_on_order = 1,
#             vendor_id = 2,
#         )
#         purchase = Purchase(
#             id = 2,
#             product_id = 2,
#             vendor_abbrev = 'MDTRN',
#             quantity = 2,
#             date = parse('05/20/2029'),
#         )

#         vendor.products.append(product)
#         purchase.vendor = vendor
#         purchase.product = product
#         product.vendor = vendor

#         session.add(vendor)
#         print(f"Added vendor {vendor} to db.")
#         session.add(product)
#         print(f"Added product {product} to db.")
#         session.add(purchase)
#         print(f"Added purchase {purchase} to db.")
#         session.commit()

# def insert_vendors_from_csv(file):
#     with open(
#         f"/home/vector-phi/Documents/pydb/app/{file}", "r", encoding="utf-8"
#     ) as csvfile:
#         csvreader = csv.reader(csvfile)
#         next(csvreader)
#         with db_session() as session:
#             for row in csvreader:
#                 # user_id = int(row[0])
#                 # first_name = row[1]
#                 # last_name = row[2]
#                 # post_id = int(row[3])
#                 # date = parse(row[4])

#                 abbrev = row[0]
#                 name = row[1]

#                 vendor = Vendor(abbrev=abbrev, name=name)
#                 product = Product(post_id=post_id, user_id=user_id, date=date)
#                 purchase = Purchase()
#                 print(user)
#                 print(post)
#                 session.add(user)
#                 session.add(post)
#                 print(f"Added record for User {first_name} successfully!")


# insert_vendors_from_csv("vendors.csv")

# def insert_products_from_csv(file):
#     with open(
#         f"/home/vector-phi/Documents/pydb/app/{file}", "r", encoding="utf-8"
#     ) as csvfile:
#         csvreader = csv.reader(csvfile)
#         next(csvreader)
#         with db_session() as session:
#             for row in csvreader:
#                 # user_id = int(row[0])
#                 # first_name = row[1]
#                 # last_name = row[2]
#                 # post_id = int(row[3])
#                 # date = parse(row[4])

#                 company_abbrev = int(row[0])
#                 product = row[1]
#                 reference_num_expiry_date = row[2]
#                 size = int(row[3])
#                 quantity = int(row[4])
#                 reference_num = row[5]
#                 expiry_date = parse(row[4])

#                 vendor = Vendor(user_id=user_id, first_name=first_name, last_name=last_name)
#                 product = Product(post_id=post_id, user_id=user_id, date=date)
#                 purchase = Purchase()
#                 print(user)
#                 print(post)
#                 session.add(user)
#                 session.add(post)
#                 print(f"Added record for User {first_name} successfully!")

# insert_products_from_csv("products.csv")

# def insert_purchases_from_csv(file):
#     with open(
#         f"/home/vector-phi/Documents/pydb/app/{file}", "r", encoding="utf-8"
#     ) as csvfile:
#         csvreader = csv.reader(csvfile)
#         next(csvreader)
#         with db_session() as session:
#             for row in csvreader:
#                 # user_id = int(row[0])
#                 # first_name = row[1]
#                 # last_name = row[2]
#                 # post_id = int(row[3])
#                 # date = parse(row[4])

#                 company_abbrev = int(row[0])
#                 product = row[1]
#                 reference_num_expiry_date = row[2]
#                 size = int(row[3])
#                 quantity = int(row[4])
#                 reference_num = row[5]
#                 expiry_date = parse(row[4])

#                 vendor = Vendor(user_id=user_id, first_name=first_name, last_name=last_name)
#                 product = Product(post_id=post_id, user_id=user_id, date=date)
#                 purchase = Purchase()
#                 print(user)
#                 print(post)
#                 session.add(user)
#                 session.add(post)
#                 print(f"Added record for User {first_name} successfully!")


# insert_purchases_from_csv("purchases.csv")
