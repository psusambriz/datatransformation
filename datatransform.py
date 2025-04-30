import pandas as pd

csv_file = "bc_trip259172515_230215.csv"
df = pd.read_csv(csv_file)
print("Number of breadcrumb records: ", len(df))

# Only include these columns
columns_to_use = [
    "ACT_TIME",       
    "VEHICLE_ID",
    "GPS_LATITUDE",
    "GPS_LONGITUDE"
]

df = pd.read_csv("bc_trip259172515_230215.csv", usecols=columns_to_use)

print(df.head())

df = pd.read_csv("bc_trip259172515_230215.csv", usecols=[
    "OPD_DATE", "ACT_TIME", "VEHICLE_ID", "GPS_LATITUDE", "GPS_LONGITUDE", "METERS"
])

df["OPD_DATE"] = pd.to_datetime(df["OPD_DATE"], format="%d%b%Y:%H:%M:%S")

df["TIMESTAMP"] = df["OPD_DATE"] + pd.to_timedelta(df["ACT_TIME"],unit="s")

# calculate speed in meters per second
df["dMETERS"] = df["METERS"].diff()
df["dTIMESTAMP"] = df["TIMESTAMP"].diff().dt.total_seconds()

# avoid divide by zero issues
df["SPEED"] = df.apply(lambda row: row["dMETERS"] / row["dTIMESTAMP"]
                       if pd.notnull(row["dMETERS"]) and row["dTIMESTAMP"] > 0 else 0,
                       axis=1)

# drop intermediate delta columns
df.drop(columns=["OPD_DATE", "ACT_TIME", "METERS", "dMETERS", "dTIMESTAMP"], inplace=True)

# print min, max and average speed
print("Min. speed: ", df["SPEED"].min())
print("Max. speed: ", df["SPEED"].max())
print("Avg. speed: ", df["SPEED"].mean())