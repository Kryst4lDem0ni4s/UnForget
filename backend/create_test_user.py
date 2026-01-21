import sqlite3
import uuid

# Connect to database
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Insert test user with specific UUID
test_user_id = "00000000-0000-0000-0000-000000000001"
cursor.execute("""
    INSERT OR REPLACE INTO users (id, email, auth_provider_id, subscription_tier, subscription_status)
    VALUES (?, ?, ?, ?, ?)
""", (test_user_id, "testuser@example.com", test_user_id, "free", "active"))

conn.commit()
conn.close()

print(f"Created test user with ID: {test_user_id}")
