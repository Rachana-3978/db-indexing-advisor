import mysql.connector
import pandas as pd
import random

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="student",
    database="sakila"
)
cursor = conn.cursor()

numeric_columns = {
    "film": ["rental_rate", "length", "replacement_cost", "rental_duration"],
    "payment": ["amount"],
    "rental": ["staff_id"],
    "customer": ["store_id"],
    "inventory": ["store_id", "film_id"],
}

thresholds = [0.5, 1, 2, 5, 10, 20, 50, 100]

queries = []
for table, columns in numeric_columns.items():
    for col in columns:
        for t in thresholds:
            queries.append(f"SELECT * FROM {table} WHERE {col} > {t}")
            queries.append(f"SELECT * FROM {table} WHERE {col} < {t}")

categorical_conditions = [
    "SELECT * FROM customer WHERE active = 1",
    "SELECT * FROM customer WHERE active = 0",
    "SELECT * FROM staff WHERE active = 1",
    "SELECT * FROM film WHERE rating = 'PG'",
    "SELECT * FROM film WHERE rating = 'PG-13'",
    "SELECT * FROM film WHERE rating = 'R'",
    "SELECT * FROM film WHERE rating = 'NC-17'",
    "SELECT * FROM film WHERE rating = 'G'",
    "SELECT * FROM rental WHERE return_date IS NULL",
    "SELECT * FROM rental WHERE return_date IS NOT NULL",
    "SELECT * FROM actor WHERE last_name LIKE 'A%'",
    "SELECT * FROM actor WHERE last_name LIKE 'B%'",
    "SELECT * FROM customer WHERE last_name LIKE 'C%'",
    "SELECT * FROM customer WHERE last_name LIKE 'D%'",
    "SELECT * FROM address WHERE district = 'California'",
    "SELECT * FROM address WHERE district = 'Texas'",
    "SELECT * FROM city WHERE country_id = 1",
    "SELECT * FROM city WHERE country_id = 2",
]
queries += categorical_conditions

order_columns = ["rental_rate", "length", "replacement_cost", "title", "release_year"]
for col in order_columns:
    queries.append(f"SELECT * FROM film ORDER BY {col}")
    queries.append(f"SELECT * FROM film ORDER BY {col} DESC")

join_queries = [
    "SELECT f.title, c.name FROM film f JOIN film_category fc ON f.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id",
    "SELECT c.first_name, r.rental_date FROM customer c JOIN rental r ON c.customer_id = r.customer_id",
    "SELECT a.first_name, f.title FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film f ON fa.film_id = f.film_id",
    "SELECT c.email, a.address FROM customer c JOIN address a ON c.address_id = a.address_id",
    "SELECT f.title, l.name FROM film f JOIN language l ON f.language_id = l.language_id",
    "SELECT c.city, co.country FROM city c JOIN country co ON c.country_id = co.country_id",
    "SELECT i.inventory_id, f.title FROM inventory i JOIN film f ON i.film_id = f.film_id",
    "SELECT p.amount, c.first_name FROM payment p JOIN customer c ON p.customer_id = c.customer_id",
    "SELECT r.rental_date, i.inventory_id FROM rental r JOIN inventory i ON r.inventory_id = i.inventory_id",
    "SELECT f.title, i.inventory_id FROM film f JOIN inventory i ON f.film_id = i.film_id WHERE f.rental_rate > 3",
    "SELECT c.first_name, p.amount FROM customer c JOIN payment p ON c.customer_id = p.customer_id WHERE p.amount > 5",
]
queries += join_queries

print(f"Total queries generated: {len(queries)}")

rows = []
for q in queries:
    try:
        cursor.execute("EXPLAIN " + q)
        result = cursor.fetchall()
        columns_names = [desc[0] for desc in cursor.description]
        for r in result:
            row_dict = dict(zip(columns_names, r))
            is_join = 1 if "JOIN" in q.upper() else 0
            filtered_pct = row_dict.get("filtered", 100) or 100
            selectivity_ratio = round(float(filtered_pct) / 100, 2)
            table_row_count = row_dict.get("rows", 0) or 0
            scan_type = row_dict.get("type", "ALL")
            scan_type_frequency = 1 if scan_type == "ALL" else 0

            base_label = 1 if (scan_type == "ALL" and selectivity_ratio < 0.5) else 0
            label = base_label if random.random() > 0.15 else 1 - base_label

            rows.append({
                "is_join_column": is_join,
                "selectivity_ratio": selectivity_ratio,
                "table_row_count": table_row_count,
                "scan_type_frequency": scan_type_frequency,
                "label": label
            })
    except Exception as e:
        print(f"Skipped: {q[:50]}... -> {e}")

df = pd.DataFrame(rows)
df.to_csv("data/real_query_data.csv", index=False)
print(df)
print(f"\nSaved {len(df)} rows to data/real_query_data.csv")

cursor.close()
conn.close()