from config.database import engine

def test_db_connection():
    try:
        with engine.connect() as connection:
            print("Successfully connected to the database!")
            connection.close()
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    test_db_connection()