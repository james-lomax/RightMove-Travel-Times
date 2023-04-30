import json
import csv
from collections import defaultdict

# Read JSON data from file
with open("output.json", "r") as f:
    data = json.load(f)

# Prepare the data structure to store the results
results = defaultdict(lambda: {"URL": "", "Price History": {}})

# Process the JSON data
for scan in data:
    timestamp = scan["data"]["createdAt"].split("T")[0]  # Extract the date
    properties = scan["data"]["capturedLists"]["Properties"]

    for prop in properties:
        url = prop["ListingUrl"]
        price = prop["Price"]
        results[url]["URL"] = url
        results[url]["Price History"][timestamp] = price

# Write the results to a CSV file
with open("output.csv", "w", newline="") as csvfile:
    fieldnames = ["URL"] + sorted(list(set([date for result in results.values() for date in result["Price History"].keys()])))
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for result in results.values():
        row = {"URL": result["URL"]}
        for date, price in result["Price History"].items():
            row[date] = price
        writer.writerow(row)
