import csv
import os
from typing import Dict, List, Tuple

CUSTOMER_FIELDS = [
    "CUSTKEY",
    "NAME",
    "ADDRESS",
    "PHONE",
    "ACCTBAL",
    "MKTSEGMENT",
    "COMMENT",
]

ORDER_FIELDS = [
    "ORDERKEY",
    "CUSTKEY",
    "ORDERSTATUS",
    "TOTALPRICE",
    "ORDERDATE",
    "ORDER-PRIORITY",
    "CLERK",
    "SHIP-PRIORITY",
    "COMMENT",
]


def resolve_csv_path(candidates: List[str]) -> str:
    """Locate the first matching CSV file in the current directory."""
    existing = {f.lower(): f for f in os.listdir(".")}
    for name in candidates:
        if name.lower() in existing:
            return existing[name.lower()]
    raise FileNotFoundError(
        f"Could not find any of {candidates} in {os.getcwd()}"
    )


def _detect_delimiter(sample_line: str) -> str:
    return "|" if sample_line.count("|") >= sample_line.count(",") else ","


def _parse_rows(filepath: str, default_headers: List[str]) -> List[Dict[str, str]]:
    with open(filepath, mode="r", encoding="utf-8", newline="") as f:
        first_line = f.readline()
        if not first_line:
            return []

        delimiter = _detect_delimiter(first_line)
        f.seek(0)
        reader = csv.reader(f, delimiter=delimiter)

        first_row = [col.strip() for col in next(reader)]
        # Drop empty trailing element caused by trailing '|'
        if first_row and first_row[-1] == "":
            first_row.pop()

        # Check if first row is a header row or data row
        has_header = not first_row[0].isdigit()
        if has_header:
            headers = [
                "ACCTBAL" if h.upper() == "ACCBATL" else h.upper()
                for h in first_row
            ]
        else:
            headers = default_headers
            f.seek(0)
            reader = csv.reader(f, delimiter=delimiter)

        records = []
        for raw_row in reader:
            if not raw_row:
                continue
            cleaned = [col.strip() for col in raw_row]
            if cleaned and cleaned[-1] == "":
                cleaned.pop()
            if len(cleaned) < len(headers):
                continue
            records.append(dict(zip(headers, cleaned[: len(headers)])))
        return records


def load_customers_and_orders() -> Tuple[List[Dict], List[Dict]]:
    """Read and type-cast customers and orders from CSV files."""
    cust_path = resolve_csv_path(["customers.csv", "Customer.csv", "customer.csv"])
    order_path = resolve_csv_path(["orders.csv", "Order.csv", "order.csv", "Orders.csv"])

    raw_customers = _parse_rows(cust_path, CUSTOMER_FIELDS)
    raw_orders = _parse_rows(order_path, ORDER_FIELDS)

    customers = []
    for c in raw_customers:
        customers.append(
            {
                "custkey": int(c["CUSTKEY"]),
                "name": c["NAME"],
                "address": c["ADDRESS"],
                "phone": c["PHONE"],
                "acctbal": float(c.get("ACCTBAL", 0.0)),
                "mktsegment": c["MKTSEGMENT"],
                "comment": c["COMMENT"],
            }
        )

    orders = []
    for o in raw_orders:
        orders.append(
            {
                "orderkey": int(o["ORDERKEY"]),
                "custkey": int(o["CUSTKEY"]),
                "orderstatus": o["ORDERSTATUS"],
                "totalprice": float(o["TOTALPRICE"]),
                "orderdate": o["ORDERDATE"],
                "order_priority": o["ORDER-PRIORITY"],
                "clerk": o["CLERK"],
                "ship_priority": int(o["SHIP-PRIORITY"]),
                "comment": o["COMMENT"],
            }
        )

    return customers, orders