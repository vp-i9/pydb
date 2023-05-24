from dateutil.parser import parse
import csv
import pandas as pd


file = r"C:\Users\omniv\OneDrive\Documents\pydb2\app\inventory.csv"
# with open(r"C:\Users\omniv\OneDrive\Documents\pydb2\app\inventory.csv", "r", encoding="utf-8") as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#                 if 'Boston' in row['company']:
#                     print(row)


df = pd.read_csv(file)

print(df["company"].unique())

print(df["quantity"].sum())

# print(df[['reference_number']['expiry_date'].unique()]) #not working

# print(df[['reference_number', 'expiry_date']].drop_duplicates())

df["ref_id_expiry_date"] = (
    df["reference_id"].astype(str) + "***" + df["expiry_date"].astype(str)
)

# print(df['combined_column'])

# df['ref_id_expiry_date'].to_csv('output_column.csv', index=False)

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

for x, y in vendors.items():
    print(y)

with open(file, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for index, row in enumerate(reader, start=1):
        for v, x in vendors.items():
            if x == "Boston Scientific":
                print(f"{index} contains {x} as company.")
    # for row in reader:  # change these to reflect row top
    #     company = row[0]
    #     product = row[1]
    #     ref_id_expiry_date = row[2]
    #     reference_id = row[3]
    #     size = row[4]
    #     expiry_date = row[5]
    #     quantity = int(row[6])
    #     # v_id = 0
    #     for v, x in vendors.items():
    #         if company == x:
    #             print(company)
