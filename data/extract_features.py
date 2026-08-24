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

queries = [
    "SELECT * FROM film WHERE rental_rate > 4.00",
    "SELECT * FROM film WHERE length > 120",
    "SELECT f.title, c.name FROM film f JOIN film_category fc ON f.film_id = fc.film_id JOIN category c ON fc.category_id = c.category_id",
    "SELECT * FROM customer WHERE active = 1",
    "SELECT * FROM rental WHERE return_date IS NULL",
    "SELECT * FROM payment WHERE amount > 5.00",
    "SELECT c.first_name, r.rental_date FROM customer c JOIN rental r ON c.customer_id = r.customer_id",
    "SELECT * FROM film WHERE replacement_cost > 20.00",
    "SELECT * FROM actor WHERE last_name = 'DAVIS'",
    "SELECT * FROM inventory WHERE store_id = 1",
    "SELECT * FROM address WHERE district = 'California'",
    "SELECT * FROM city WHERE country_id = 1",
    "SELECT * FROM staff WHERE active = 1",
    "SELECT * FROM film WHERE rating = 'PG'",
    "SELECT * FROM customer WHERE store_id = 2",
    "SELECT * FROM rental WHERE staff_id = 1",
    "SELECT * FROM payment WHERE staff_id = 2",
    "SELECT a.first_name, f.title FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film f ON fa.film_id = f.film_id",
    "SELECT c.email, a.address FROM customer c JOIN address a ON c.address_id = a.address_id",
    "SELECT s.first_name, st.store_id FROM staff s JOIN store st ON s.store_id = st.store_id",
    "SELECT * FROM film ORDER BY rental_rate DESC",
    "SELECT * FROM customer ORDER BY last_name",
    "SELECT * FROM film WHERE rental_duration > 5",
    "SELECT * FROM film WHERE language_id = 1",
    "SELECT * FROM customer WHERE store_id = 1",
    "SELECT * FROM address WHERE city_id = 300",
    "SELECT * FROM category WHERE name = 'Action'",
    "SELECT * FROM language WHERE name = 'English'",
    "SELECT * FROM store WHERE manager_staff_id = 1",
    "SELECT * FROM inventory WHERE film_id = 1",
    "SELECT * FROM rental WHERE inventory_id = 1",
    "SELECT * FROM payment WHERE customer_id = 1",
    "SELECT * FROM film_actor WHERE actor_id = 1",
    "SELECT * FROM film_category WHERE category_id = 1",
    "SELECT * FROM city WHERE city = 'London'",
    "SELECT * FROM country WHERE country = 'India'",
    "SELECT * FROM staff WHERE store_id = 1",
    "SELECT * FROM film WHERE release_year = 2006",
    "SELECT * FROM customer WHERE last_name LIKE 'A%'",
    "SELECT * FROM rental WHERE rental_date > '2005-07-01'",
    "SELECT f.title, l.name FROM film f JOIN language l ON f.language_id = l.language_id",
    "SELECT c.city, co.country FROM city c JOIN country co ON c.country_id = co.country_id",
    "SELECT i.inventory_id, f.title FROM inventory i JOIN film f ON i.film_id = f.film_id",
    "SELECT p.amount, c.first_name FROM payment p JOIN customer c ON p.customer_id = c.customer_id",
    "SELECT r.rental_date, i.inventory_id FROM rental r JOIN inventory i ON r.inventory_id = i.inventory_id",
    "SELECT s.store_id, a.address FROM store s JOIN address a ON s.address_id = a.address_id",
    "SELECT * FROM film ORDER BY length DESC",
    "SELECT * FROM payment ORDER BY amount DESC",
    "SELECT * FROM customer ORDER BY create_date",
    "SELECT * FROM film WHERE special_features LIKE '%Trailers%'",
    "SELECT * FROM actor WHERE first_name = 'NICK'",
    "SELECT * FROM film WHERE rating = 'R'",
    "SELECT * FROM film WHERE rental_rate < 2.00",
    "SELECT * FROM film WHERE length < 90",
    "SELECT * FROM customer WHERE active = 0",
    "SELECT * FROM rental WHERE return_date IS NOT NULL",
    "SELECT * FROM payment WHERE amount < 2.00",
    "SELECT * FROM actor WHERE first_name = 'PENELOPE'",
    "SELECT * FROM inventory WHERE store_id = 2",
    "SELECT * FROM address WHERE district = 'Texas'",
    "SELECT * FROM city WHERE country_id = 2",
    "SELECT * FROM staff WHERE active = 0",
    "SELECT * FROM film WHERE rating = 'PG-13'",
    "SELECT * FROM film WHERE rating = 'NC-17'",
    "SELECT * FROM customer WHERE store_id = 1",
    "SELECT * FROM rental WHERE staff_id = 2",
    "SELECT * FROM payment WHERE staff_id = 1",
    "SELECT * FROM film_actor WHERE film_id = 1",
    "SELECT * FROM film_category WHERE film_id = 1",
    "SELECT * FROM city WHERE city = 'Paris'",
    "SELECT * FROM country WHERE country = 'China'",
    "SELECT * FROM film WHERE release_year = 2005",
    "SELECT * FROM customer WHERE last_name LIKE 'B%'",
    "SELECT * FROM rental WHERE rental_date < '2005-07-01'",
    "SELECT a.actor_id, f.title FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id JOIN film f ON fa.film_id = f.film_id WHERE f.rating = 'PG'",
    "SELECT c.first_name, p.amount FROM customer c JOIN payment p ON c.customer_id = p.customer_id WHERE p.amount > 3.00",
    "SELECT f.title, i.inventory_id FROM film f JOIN inventory i ON f.film_id = i.film_id WHERE f.rental_rate > 3.00",
    "SELECT * FROM film ORDER BY replacement_cost DESC",
    "SELECT * FROM actor ORDER BY last_name",
    "SELECT * FROM city ORDER BY city",
    "SELECT * FROM film WHERE special_features LIKE '%Commentaries%'",
    "SELECT * FROM film WHERE rental_duration = 7",
]

rows = []
for q in queries:
    cursor.execute("EXPLAIN " + q)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    for r in result:
        row_dict = dict(zip(columns, r))
        is_join = 1 if "JOIN" in q.upper() else 0
        filtered_pct = row_dict.get("filtered", 100) or 100
        selectivity_ratio = round(float(filtered_pct) / 100, 2)
        table_row_count = row_dict.get("rows", 0) or 0
        scan_type = row_dict.get("type", "ALL")
        scan_type_frequency = 1 if scan_type == "ALL" else 0

        base_label = 1 if (scan_type == "ALL" and selectivity_ratio < 0.5) else 0
        # 15% chance label flip ho jaye - real-world noise simulate karne ke liye
        label = base_label if random.random() > 0.15 else 1 - base_label

        rows.append({
            "is_join_column": is_join,
            "selectivity_ratio": selectivity_ratio,
            "table_row_count": table_row_count,
            "scan_type_frequency": scan_type_frequency,
            "label": label
        })

df = pd.DataFrame(rows)
df.to_csv("data/real_query_data.csv", index=False)
print(df)
print(f"\nSaved {len(df)} rows to data/real_query_data.csv")

cursor.close()
conn.close()