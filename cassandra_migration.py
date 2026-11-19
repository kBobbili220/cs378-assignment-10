from collections import defaultdict
from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent_with_args
from data_loader import load_customers_and_orders

CASSANDRA_HOSTS = ["127.0.0.1"]
KEYSPACE = "online_shop"


def connect_cassandra():
    cluster = Cluster(CASSANDRA_HOSTS)
    session = cluster.connect()
    return cluster, session


def setup_schema(session):
    """Create keyspace and query-driven Cassandra tables."""
    session.execute(f"DROP KEYSPACE IF EXISTS {KEYSPACE};")
    session.execute(
        f"""
        CREATE KEYSPACE {KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}};
        """
    )
    session.set_keyspace(KEYSPACE)

    # 1. Base customer table
    session.execute(
        """
        CREATE TABLE customers (
            custkey int PRIMARY KEY,
            name text,
            address text,
            phone text,
            acctbal double,
            mktsegment text,
            comment text
        );
        """
    )

    # 2. Orders partitioned by customer
    session.execute(
        """
        CREATE TABLE orders_by_customer (
            custkey int,
            orderkey int,
            orderstatus text,
            totalprice double,
            orderdate text,
            order_priority text,
            clerk text,
            ship_priority int,
            comment text,
            PRIMARY KEY (custkey, orderkey)
        );
        """
    )

    # 3. Query-driven table for Task 2.2 (deduplicated by clustering key custkey)
    session.execute(
        """
        CREATE TABLE customers_by_order_priority (
            order_priority text,
            custkey int,
            name text,
            address text,
            phone text,
            acctbal double,
            mktsegment text,
            comment text,
            PRIMARY KEY (order_priority, custkey)
        ) WITH CLUSTERING ORDER BY (custkey ASC);
        """
    )

    # 4. Query-driven table for Task 2.3 (pre-sorted descending by total_spent)
    session.execute(
        """
        CREATE TABLE customer_order_totals (
            bucket text,
            total_spent double,
            custkey int,
            name text,
            mktsegment text,
            order_count int,
            PRIMARY KEY (bucket, total_spent, custkey)
        ) WITH CLUSTERING ORDER BY (total_spent DESC, custkey ASC);
        """
    )


def task_2_1_migrate_to_cassandra(session):
    """Task 2.1: Read CSVs and populate Cassandra tables concurrently."""
    print("=== Task 2.1: Migrating Customers & Orders to Cassandra ===")
    setup_schema(session)
    customers, orders = load_customers_and_orders()

    cust_map = {c["custkey"]: c for c in customers}

    # Insert into customers
    insert_cust = session.prepare(
        """
        INSERT INTO customers (custkey, name, address, phone, acctbal, mktsegment, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
    )
    cust_params = [
        (
            c["custkey"],
            c["name"],
            c["address"],
            c["phone"],
            c["acctbal"],
            c["mktsegment"],
            c["comment"],
        )
        for c in customers
    ]
    execute_concurrent_with_args(session, insert_cust, cust_params, concurrency=100)

    # Insert into orders_by_customer
    insert_order = session.prepare(
        """
        INSERT INTO orders_by_customer (
            custkey, orderkey, orderstatus, totalprice, orderdate,
            order_priority, clerk, ship_priority, comment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    )
    order_params = [
        (
            o["custkey"],
            o["orderkey"],
            o["orderstatus"],
            o["totalprice"],
            o["orderdate"],
            o["order_priority"],
            o["clerk"],
            o["ship_priority"],
            o["comment"],
        )
        for o in orders
    ]
    execute_concurrent_with_args(session, insert_order, order_params, concurrency=100)

    # Populate query-driven tables: customers_by_order_priority & customer_order_totals
    priority_pairs = set()
    spend_by_cust = defaultdict(float)
    count_by_cust = defaultdict(int)

    for o in orders:
        ck = o["custkey"]
        priority_pairs.add((o["order_priority"], ck))
        spend_by_cust[ck] += o["totalprice"]
        count_by_cust[ck] += 1

    insert_priority = session.prepare(
        """
        INSERT INTO customers_by_order_priority (
            order_priority, custkey, name, address, phone, acctbal, mktsegment, comment
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
    )
    priority_params = []
    for priority, ck in priority_pairs:
        c = cust_map.get(ck)
        if c:
            priority_params.append(
                (
                    priority,
                    c["custkey"],
                    c["name"],
                    c["address"],
                    c["phone"],
                    c["acctbal"],
                    c["mktsegment"],
                    c["comment"],
                )
            )
    execute_concurrent_with_args(session, insert_priority, priority_params, concurrency=100)

    insert_totals = session.prepare(
        """
        INSERT INTO customer_order_totals (
            bucket, total_spent, custkey, name, mktsegment, order_count
        ) VALUES (?, ?, ?, ?, ?, ?)
        """
    )
    totals_params = [
        (
            "ALL",
            round(spend_by_cust[c["custkey"]], 2),
            c["custkey"],
            c["name"],
            c["mktsegment"],
            count_by_cust[c["custkey"]],
        )
        for c in customers
    ]
    execute_concurrent_with_args(session, insert_totals, totals_params, concurrency=100)

    print(
        f"Inserted {len(customers)} customers and {len(orders)} orders "
        f"into Cassandra keyspace '{KEYSPACE}'.\n"
    )


def task_2_2_urgent_priority_customers(session):
    """Task 2.2: Query Cassandra for customers with '1-URGENT' orders."""
    print("=== Task 2.2: Customers with '1-URGENT' Orders (Cassandra) ===")
    rows = list(
        session.execute(
            """
            SELECT custkey, name, mktsegment, phone
            FROM customers_by_order_priority
            WHERE order_priority = '1-URGENT';
            """
        )
    )

    print(f"Total customers with '1-URGENT' orders: {len(rows)}")
    print(f"{'CUSTKEY':<10} {'NAME':<22} {'MKTSEGMENT':<15} {'PHONE':<18}")
    print("-" * 68)
    for r in rows[:25]:
        print(f"{r.custkey:<10} {r.name:<22} {r.mktsegment:<15} {r.phone:<18}")
    if len(rows) > 25:
        print(f"... ({len(rows) - 25} more customers omitted for brevity)")
    print()


def task_2_3_top_10_customers_by_totalprice(session):
    """Task 2.3: Query Cassandra for top-10 customers by total order price."""
    print("=== Task 2.3: Top-10 Customers by Total Order Price (Cassandra) ===")
    rows = list(
        session.execute(
            """
            SELECT custkey, name, mktsegment, order_count, total_spent
            FROM customer_order_totals
            WHERE bucket = 'ALL'
            LIMIT 10;
            """
        )
    )

    print(
        f"{'RANK':<6} {'CUSTKEY':<10} {'NAME':<22} "
        f"{'MKTSEGMENT':<15} {'ORDERS':<8} {'TOTALPRICE SUM':>16}"
    )
    print("-" * 82)
    for rank, r in enumerate(rows, start=1):
        print(
            f"{rank:<6} {r.custkey:<10} {r.name:<22} "
            f"{r.mktsegment:<15} {r.order_count:<8} "
            f"${r.total_spent:>15,.2f}"
        )
    print()


def main():
    cluster, session = connect_cassandra()
    try:
        task_2_1_migrate_to_cassandra(session)
        task_2_2_urgent_priority_customers(session)
        task_2_3_top_10_customers_by_totalprice(session)
    finally:
        cluster.shutdown()


if __name__ == "__main__":
    main()