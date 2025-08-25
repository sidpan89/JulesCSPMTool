#!/bin/bash

# A script to verify that the .env file is set up correctly.

# --- START robust path finding ---
# cd to the project root (the parent directory of this script's location)
cd "$(dirname "$0")/.."
# --- END robust path finding ---

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ENV_EXAMPLE_FILE=".env.example"
ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}ERROR: .env file not found in project root ($(pwd)).${NC}"
    echo -e "Please copy ${YELLOW}${ENV_EXAMPLE_FILE}${NC} to ${YELLOW}${ENV_FILE}${NC} and fill in the values."
    exit 1
fi

# Get all variable names from .env.example (excluding comments and blank lines)
REQUIRED_VARS=$(grep -vE '^\s*#|^\s*$' "$ENV_EXAMPLE_FILE" | cut -d= -f1)

MISSING_VARS=0

echo "Verifying environment variables in $ENV_FILE..."

for VAR in $REQUIRED_VARS; do
    # Check if the variable is present in the .env file
    if ! grep -q "^${VAR}=" "$ENV_FILE"; then
        echo -e "${RED}✖ Missing required variable: ${VAR}${NC}"
        MISSING_VARS=$((MISSING_VARS + 1))
    else
        # Optional: check if the value is empty
        VALUE=$(grep "^${VAR}=" "$ENV_FILE" | cut -d= -f2-)
        if [ -z "$VALUE" ]; then
            echo -e "${YELLOW}⚠ Warning: Variable ${VAR} is present but empty.${NC}"
        else
            echo -e "${GREEN}✔ Found variable: ${VAR}${NC}"
        fi
    fi
done

if [ "$MISSING_VARS" -ne 0 ]; then
    echo -e "\n${RED}Found ${MISSING_VARS} missing environment variables. Please update your .env file.${NC}"
    exit 1
else
    echo -e "\n${GREEN}All required environment variables are present.${NC}"
    exit 0
fi
