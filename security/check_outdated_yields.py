import psycopg2
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import os

load_dotenv()

# SQL query to find the latest yield_id and created_date
query = """
WITH LatestYield AS (
    SELECT 
        yield_id, 
        MAX(created_date) AS latest_date
    FROM 
        defi_yield
    GROUP BY 
        yield_id
)
SELECT 
       dyp.yield_id,
    ly.latest_date
FROM 
    defi_yield_products dyp
JOIN 
    LatestYield ly ON dyp.yield_id = ly.yield_id;
"""


def get_latest_yields():
    # Connect to the PostgreSQL database
    conn = None
    try:
        conn = psycopg2.connect(
                dbname=os.getenv('DATABASE_NAME'),
                user=os.getenv('DATABASE_USER'),
                password=os.getenv('DATABASE_PASSWORD'),
                host=os.getenv('DATABASE_HOST'),
                port=os.getenv('DATABASE_PORT')
        )
        cur = conn.cursor()

        # Execute the SQL query
        cur.execute(query)

        # Fetch all results
        results = cur.fetchall()

        # Get the current time
        timezone = pytz.timezone('GMT')
        current_time = datetime.now(timezone)

        # Print the results
        for row in results:
            latest_date = timezone.localize(row[1])
            if latest_date < current_time - timedelta(hours=1):
                print(f"Yield ID: {row[0]}, Latest Date: {row[1]}")

        # Close the cursor and connection
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    get_latest_yields()