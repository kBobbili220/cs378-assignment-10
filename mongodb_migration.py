from collections import defaultdict
from pymongo import ASCENDING, MongoClient
from data_loader import load_customers_and_orders

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "online_shop"
COLLECTION_NAME = "customers"


def connect_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return client, db[COLLECTION_NAME]


def task_1_1_migrate_to_mongodb(collection):
    """Task 1.1: Read CSVs, embed orders into customer JSON documents, and insert into MongoDB."""
    print("=== Task 1.1: Migrating Customers & Orders to MongoDB ===")
    customers, orders = load_customers_and_orders()

    orders_by_cust = defaultdict(list)
    for order in orders:
        order_doc = {k: v for k, v in order.items() if k != "custkey"}
        orders_by_cust[order["custkey"]].append(order_doc)

    customer_docs = []
    for cust in customers:
        doc = {
            "_id": cust["custkey"],
            **cust,
            "orders": orders_by_cust.get(cust["custkey"], []),
        }
        customer_docs.append(doc)

    # Reset collection for clean, repeatable runs
    collection.drop()
    if customer_docs:
        collection.insert_many(customer_docs)

    collection.create_index([("orders.order_priority", ASCENDING)])

    print(
        f"Inserted {collection.count_documents({})} customer documents "
        f"(total {len(orders)} embedded orders) into '{DB_NAME}.{COLLECTION_NAME}'.\n"
    )


def task_1_2_urgent_priority_customers(collection):
    """Task 1.2: Query customers who have at least one order with priority '1-URGENT'."""
    print("=== Task 1.2: Customers with '1-URGENT' Orders (MongoDB) ===")
    cursor = collection.find(
        {"orders.order_priority": "1-URGENT"},
        {"_id": 0, "custkey": 1, "name": 1, "mktsegment": 1, "phone": 1},
    ).sort("custkey", ASCENDING)

    results = list(cursor)
    print(f"Total customers with '1-URGENT' orders: {len(results)}")
    print(f"{'CUSTKEY':<10} {'NAME':<22} {'MKTSEGMENT':<15} {'PHONE':<18}")
    print("-" * 68)
    for cust in results[:25]:  # Prints preview; remove [:25] if full dump is desired
        print(
            f"{cust['custkey']:<10} {cust['name']:<22} "
            f"{cust['mktsegment']:<15} {cust['phone']:<18}"
        )
    if len(results) > 25:
        print(f"... ({len(results) - 25} more customers omitted for brevity)")
    print()


def task_1_3_top_10_customers_by_totalprice(collection):
    """Task 1.3: Find top-10 customers by sum of order TOTALPRICE."""
    print("=== Task 1.3: Top-10 Customers by Total Order Price (MongoDB) ===")
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "custkey": 1,
                "name": 1,
                "mktsegment": 1,
                "order_count": {"$size": "$orders"},
                "total_spent": {"$sum": "$orders.totalprice"},
            }
        },
        {"$sort": {"total_spent": -1, "custkey": 1}},
        {"$limit": 10},
    ]

    top_10 = list(collection.aggregate(pipeline))
    print(
        f"{'RANK':<6} {'CUSTKEY':<10} {'NAME':<22} "
        f"{'MKTSEGMENT':<15} {'ORDERS':<8} {'TOTALPRICE SUM':>16}"
    )
    print("-" * 82)
    for rank, row in enumerate(top_10, start=1):
        print(
            f"{rank:<6} {row['custkey']:<10} {row['name']:<22} "
            f"{row['mktsegment']:<15} {row['order_count']:<8} "
            f"${row['total_spent']:>15,.2f}"
        )
    print()


def main():
    client, collection = connect_mongodb()
    try:
        task_1_1_migrate_to_mongodb(collection)
        task_1_2_urgent_priority_customers(collection)
        task_1_3_top_10_customers_by_totalprice(collection)
    finally:
        client.close()


if __name__ == "__main__":
    main()