import sqlite3

# Connect to the light log database
conn = sqlite3.connect("light_log.db")
cursor = conn.cursor()

# Count how many times the light was turned ON
cursor.execute("SELECT COUNT(*) FROM log WHERE status='ON'")
on_count = cursor.fetchone()[0]

# Count how many times the light was turned OFF
cursor.execute("SELECT COUNT(*) FROM log WHERE status='OFF'")
off_count = cursor.fetchone()[0]

# Optional: show today's ON actions
cursor.execute("SELECT COUNT(*) FROM log WHERE status='ON' AND DATE(timestamp) = DATE('now')")
today_on = cursor.fetchone()[0]

print("----- Light Usage Report -----")
print(f"Total times light turned ON:  {on_count}")
print(f"Total times light turned OFF: {off_count}")
print(f"Today's ON actions:           {today_on}")

conn.close()
