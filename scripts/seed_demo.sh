#!/bin/bash

# A script to seed the database with demo data.

# cd to the project root (the parent directory of this script's location)
cd "$(dirname "$0")/.."

echo "Seeding the database with demo data..."
echo "This may take a moment..."

# Run the python seeding script inside the 'backend' container
# This ensures it has access to the installed packages and the correct environment
docker-compose exec backend python3 /app/seed_db.py

if [ $? -eq 0 ]; then
    echo "✅ Seeding complete."
else
    echo "❌ Seeding failed. Please check the output above."
    exit 1
fi
