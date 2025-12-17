#!/bin/bash
cd backend/data
# Create sample catalog if missing
if [ ! -f shl_catalog.json ]; then
  echo '[{"name":"Python Programming","url":"https://shl.com/python","description":"Python coding assessment","test_type":["Technical"],"duration":"45","adaptive_support":"Yes","remote_support":"Yes"},{"name":"Java Development","url":"https://shl.com/java","description":"Java programming test","test_type":["Technical"],"duration":"50","adaptive_support":"Yes","remote_support":"Yes"},{"name":"SQL Database","url":"https://shl.com/sql","description":"SQL skills test","test_type":["Technical"],"duration":"40","adaptive_support":"Yes","remote_support":"Yes"}]' > shl_catalog.json
fi
# Create .env if missing
touch .env
# Start server
python -m app.main
