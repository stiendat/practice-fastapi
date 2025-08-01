#!/bin/bash
set -e

# This script runs when the PostgreSQL container starts for the first time
# It creates any additional databases or users if needed

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create extensions if needed
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Grant necessary permissions
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
    
    -- You can add more initialization SQL here
    -- For example, creating additional schemas, tables, or users
    
    -- Log successful initialization
    SELECT 'Database initialization completed successfully' as status;
EOSQL

echo "Database initialization script completed"
