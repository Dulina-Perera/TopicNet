#!/usr/bin/env zsh

# Function to check if a package is already installed.
function is_installed {
    if pacman --query --quiet --search $1 > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

PACKAGE="postgresql"

# Check if PostgreSQL is already installed and install it if not.
if is_installed $PACKAGE; then
    echo "PostgreSQL is already installed."
else
    echo "Installing PostgreSQL..."
    sudo pacman --noconfirm --sync --refresh --sysupgrade
    sudo pacman --noconfirm --sync $PACKAGE

    if is_installed $PACKAGE; then
        echo "PostgreSQL has been installed successfully."
    else
        echo "Failed to install PostgreSQL."
        exit 1
    fi
fi

# Check if the database cluster is already initialized
PGDATA_DIR="/var/lib/postgres/data"

if [ -d "$PGDATA_DIR" ] && [ "$(ls --almost-all $PGDATA_DIR)" ]; then
    echo "Database cluster already initialized."
else
    # Initialize the database cluster.
    echo "Initializing the database cluster..."
    sudo --user postgres initdb --locale en_US.UTF-8 --encoding UTF8 --pgdata $PGDATA_DIR --data-checksums
fi

# Start and enable the PostgreSQL service.
echo "Starting and enabling the PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create a new user named "topicnet" with the password "CS3501_Group20".
echo "Creating a new user..."
sudo --user postgres psql --command "DO \$\$ BEGIN CREATE USER topicnet WITH CREATEDB PASSWORD 'CS3501_Group20'; EXCEPTION WHEN DUPLICATE_OBJECT THEN RAISE NOTICE 'User already exists, skipping.'; END \$\$;"

# Create a new database named "topicnet" owned by the user "topicnet".
echo "Creating a new database..."
sudo --user postgres psql --command "CREATE DATABASE topicnet OWNER topicnet;" 2>/dev/null || echo "Database 'topicnet' already exists, skipping creation."
