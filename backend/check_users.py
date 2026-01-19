from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:postgres@localhost:5432/careerpilot_ai')
conn = engine.connect()
result = conn.execute(text('SELECT id, email, username, full_name, created_at FROM users ORDER BY created_at DESC LIMIT 5'))
print('Recent users:')
for row in result:
    print(f'  ID={row[0]}, Email={row[1]}, Username={row[2]}, Name={row[3]}, Created={row[4]}')
conn.close()
