#!/bin/bash

# A script to seed the database with demo data.

# cd to the project root (the parent directory of this script's location)
cd "$(dirname "$0")/.."

echo "Seeding the database with demo data..."
echo "This may take a moment..."

# Set the SECRET_KEY environment variable required by the seeding script
# and run the python script.
SECRET_KEY='your_super_secret_key_for_jwt' \
python3 backend/seed_db.py

if [ $? -eq 0 ]; then
    echo "✅ Seeding complete."
else
    echo "❌ Seeding failed. Please check the output above."
    exit 1
fi
