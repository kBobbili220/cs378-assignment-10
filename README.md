// 1. Student Name : Karthik Bobbili
// Student UT EID : kkb2333
//
// ## Course Name : CS378
// ## Unique Number : 55500
// ## Date Created : 11/18/2026

# CS378 - Relational to NoSQL Database Migration (MongoDB & Cassandra)

## 1. Environment Setup

### Install Python Dependencies
```bash  
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Results

### Mongo Results
=== Task 1.1: Migrating Customers & Orders to MongoDB ===
Inserted 15000 customer documents (total 150000 embedded orders) into 'online_shop.customers'.

=== Task 1.2: Customers with '1-URGENT' Orders (MongoDB) ===
Total customers with '1-URGENT' orders: 9292
CUSTKEY    NAME                   MKTSEGMENT      PHONE             
--------------------------------------------------------------------
1          Customer#000000001     BUILDING        25-989-741-2988   
2          Customer#000000002     AUTOMOBILE      23-768-687-3665   
4          Customer#000000004     MACHINERY       14-128-190-5944   
5          Customer#000000005     HOUSEHOLD       13-750-942-6364   
7          Customer#000000007     AUTOMOBILE      28-190-982-9759   
8          Customer#000000008     BUILDING        27-147-574-9335   
10         Customer#000000010     HOUSEHOLD       15-741-346-9870   
11         Customer#000000011     BUILDING        33-464-151-3439   
13         Customer#000000013     BUILDING        13-761-547-5974   
14         Customer#000000014     FURNITURE       11-845-129-3851   
16         Customer#000000016     FURNITURE       20-781-609-3107   
17         Customer#000000017     AUTOMOBILE      12-970-682-3487   
19         Customer#000000019     HOUSEHOLD       28-396-526-5053   
20         Customer#000000020     FURNITURE       32-957-234-8742   
22         Customer#000000022     MACHINERY       13-806-545-9701   
25         Customer#000000025     FURNITURE       22-603-468-3533   
28         Customer#000000028     FURNITURE       18-774-241-1462   
29         Customer#000000029     FURNITURE       10-773-203-7342   
31         Customer#000000031     HOUSEHOLD       33-197-837-7094   
32         Customer#000000032     BUILDING        25-430-914-2194   
34         Customer#000000034     HOUSEHOLD       25-344-968-5422   
35         Customer#000000035     HOUSEHOLD       27-566-888-7431   
37         Customer#000000037     FURNITURE       18-385-235-7162   
38         Customer#000000038     HOUSEHOLD       22-306-880-7212   
40         Customer#000000040     BUILDING        13-652-915-8939   
... (9267 more customers omitted for brevity)

=== Task 1.3: Top-10 Customers by Total Order Price (MongoDB) ===
RANK   CUSTKEY    NAME                   MKTSEGMENT      ORDERS     TOTALPRICE SUM
----------------------------------------------------------------------------------
1      8362       Customer#000008362     BUILDING        35       $   5,793,605.05
2      6958       Customer#000006958     AUTOMOBILE      30       $   5,370,682.19
3      9454       Customer#000009454     MACHINERY       35       $   5,354,381.81
4      346        Customer#000000346     FURNITURE       33       $   5,323,350.43
5      10354      Customer#000010354     MACHINERY       34       $   5,227,957.24
6      1075       Customer#000001075     BUILDING        31       $   5,174,472.52
7      14398      Customer#000014398     AUTOMOBILE      31       $   5,103,754.83
8      8761       Customer#000008761     AUTOMOBILE      36       $   5,077,001.26
9      11998      Customer#000011998     FURNITURE       36       $   5,074,872.00
10     8542       Customer#000008542     MACHINERY       32       $   5,072,337.21

### Cassandra Results
=== Task 2.1: Migrating Customers & Orders to Cassandra ===
Inserted 15000 customers and 150000 orders into Cassandra keyspace 'online_shop'.

=== Task 2.2: Customers with '1-URGENT' Orders (Cassandra) ===
Total customers with '1-URGENT' orders: 9292
CUSTKEY    NAME                   MKTSEGMENT      PHONE             
--------------------------------------------------------------------
1          Customer#000000001     BUILDING        25-989-741-2988   
2          Customer#000000002     AUTOMOBILE      23-768-687-3665   
4          Customer#000000004     MACHINERY       14-128-190-5944   
5          Customer#000000005     HOUSEHOLD       13-750-942-6364   
7          Customer#000000007     AUTOMOBILE      28-190-982-9759   
8          Customer#000000008     BUILDING        27-147-574-9335   
10         Customer#000000010     HOUSEHOLD       15-741-346-9870   
11         Customer#000000011     BUILDING        33-464-151-3439   
13         Customer#000000013     BUILDING        13-761-547-5974   
14         Customer#000000014     FURNITURE       11-845-129-3851   
16         Customer#000000016     FURNITURE       20-781-609-3107   
17         Customer#000000017     AUTOMOBILE      12-970-682-3487   
19         Customer#000000019     HOUSEHOLD       28-396-526-5053   
20         Customer#000000020     FURNITURE       32-957-234-8742   
22         Customer#000000022     MACHINERY       13-806-545-9701   
25         Customer#000000025     FURNITURE       22-603-468-3533   
28         Customer#000000028     FURNITURE       18-774-241-1462   
29         Customer#000000029     FURNITURE       10-773-203-7342   
31         Customer#000000031     HOUSEHOLD       33-197-837-7094   
32         Customer#000000032     BUILDING        25-430-914-2194   
34         Customer#000000034     HOUSEHOLD       25-344-968-5422   
35         Customer#000000035     HOUSEHOLD       27-566-888-7431   
37         Customer#000000037     FURNITURE       18-385-235-7162   
38         Customer#000000038     HOUSEHOLD       22-306-880-7212   
40         Customer#000000040     BUILDING        13-652-915-8939   
... (9267 more customers omitted for brevity)

=== Task 2.3: Top-10 Customers by Total Order Price (Cassandra) ===
RANK   CUSTKEY    NAME                   MKTSEGMENT      ORDERS     TOTALPRICE SUM
----------------------------------------------------------------------------------
1      8362       Customer#000008362     BUILDING        35       $   5,793,605.05
2      6958       Customer#000006958     AUTOMOBILE      30       $   5,370,682.19
3      9454       Customer#000009454     MACHINERY       35       $   5,354,381.81
4      346        Customer#000000346     FURNITURE       33       $   5,323,350.43
5      10354      Customer#000010354     MACHINERY       34       $   5,227,957.24
6      1075       Customer#000001075     BUILDING        31       $   5,174,472.52
7      14398      Customer#000014398     AUTOMOBILE      31       $   5,103,754.83
8      8761       Customer#000008761     AUTOMOBILE      36       $   5,077,001.26
9      11998      Customer#000011998     FURNITURE       36       $   5,074,872.00
10     8542       Customer#000008542     MACHINERY       32       $   5,072,337.21