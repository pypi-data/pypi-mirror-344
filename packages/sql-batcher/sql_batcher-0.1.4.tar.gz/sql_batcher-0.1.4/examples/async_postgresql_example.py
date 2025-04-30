"""
Async PostgreSQL adapter example for SQL Batcher.

This example demonstrates how to use SQL Batcher with PostgreSQL asynchronously,
taking advantage of PostgreSQL-specific features like JSONB, COPY commands,
and transaction management.

Requirements:
- PostgreSQL database
- asyncpg package: pip install asyncpg
- sql-batcher[postgresql]: pip install "sql-batcher[postgresql]"
"""

import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import asyncio

from sql_batcher import AsyncSQLBatcher
from sql_batcher.adapters.async_postgresql import AsyncPostgreSQLAdapter


def get_connection_params() -> Dict[str, str]:
    """
    Get PostgreSQL connection parameters from environment or defaults.

    Returns:
        Dictionary of connection parameters
    """
    return {
        "host": os.environ.get("PGHOST", "localhost"),
        "port": os.environ.get("PGPORT", "5432"),
        "user": os.environ.get("PGUSER", "postgres"),
        "password": os.environ.get("PGPASSWORD", "postgres"),
        "dbname": os.environ.get("PGDATABASE", "postgres"),
    }


async def setup_database(adapter: AsyncPostgreSQLAdapter) -> None:
    """
    Set up the example database structure asynchronously.

    Args:
        adapter: Async PostgreSQL adapter instance
    """
    print("Setting up database schema...")

    # Create products table
    await adapter.execute(
        """
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        sku VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        attributes JSONB DEFAULT '{}'::jsonb,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    # Create orders table
    await adapter.execute(
        """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        order_number VARCHAR(50) UNIQUE NOT NULL,
        customer_name VARCHAR(255) NOT NULL,
        customer_email VARCHAR(255) NOT NULL,
        status VARCHAR(50) NOT NULL DEFAULT 'pending',
        total_amount DECIMAL(12, 2) NOT NULL,
        order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        metadata JSONB DEFAULT '{}'::jsonb
    )
    """
    )

    # Create order_items table
    await adapter.execute(
        """
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id),
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER NOT NULL,
        unit_price DECIMAL(10, 2) NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        UNIQUE(order_id, product_id)
    )
    """
    )

    print("Database schema created successfully")


def generate_product_data(num_products: int) -> List[Tuple]:
    """
    Generate sample product data.

    Args:
        num_products: Number of products to generate

    Returns:
        List of product data tuples
    """
    print(f"Generating {num_products} sample products...")

    categories = ["Electronics", "Books", "Clothing", "Home", "Food", "Toys"]
    attributes = [
        {"color": "Red", "weight": "1.5kg", "dimensions": "10x15x5cm"},
        {"color": "Blue", "material": "Cotton", "size": "M"},
        {"color": "Black", "connectivity": "Bluetooth", "battery": "10h"},
        {"material": "Wood", "finish": "Matte", "assembly_required": True},
        {"pages": 350, "language": "English", "format": "Hardcover"},
        {"ingredients": ["Sugar", "Flour", "Butter"], "allergens": ["Gluten", "Dairy"]},
    ]

    products = []
    for i in range(1, num_products + 1):
        category = random.choice(categories)
        sku = f"{category[0:3].upper()}{i:06d}"
        name = f"{category} Product {i}"
        price = round(random.uniform(9.99, 999.99), 2)
        stock = random.randint(0, 1000)

        # Select attributes relevant to the category
        category_index = categories.index(category) % len(attributes)
        product_attributes = attributes[category_index].copy()

        # Add some random attributes
        if random.random() > 0.5:
            product_attributes["featured"] = random.random() > 0.8
        if random.random() > 0.7:
            product_attributes["rating"] = round(random.uniform(1, 5), 1)

        # Convert to JSON string
        json_attributes = json.dumps(product_attributes)

        products.append((sku, name, category, price, stock, json_attributes))

    return products


async def generate_order_data(num_orders: int, max_product_id: int) -> List[str]:
    """
    Generate sample order SQL statements asynchronously.

    Args:
        num_orders: Number of orders to generate
        max_product_id: Maximum product ID (to reference existing products)

    Returns:
        List of SQL INSERT statements for orders
    """
    print(f"Generating {num_orders} sample orders...")

    order_statements = []
    now = datetime.now()

    for i in range(1, num_orders + 1):
        # Order details
        order_number = f"ORD-{i:06d}"
        customer_name = f"Customer {i}"
        customer_email = f"customer{i}@example.com"
        status = random.choice(["pending", "processing", "shipped", "delivered", "cancelled"])

        # Create order date within the last 30 days
        days_ago = random.randint(0, 30)
        order_date = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")

        # Generate 1-5 items per order
        num_items = random.randint(1, 5)
        order_items = []
        total_amount = 0

        # Create order items
        for _ in range(num_items):
            product_id = random.randint(1, max_product_id)
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(9.99, 99.99), 2)
            total_price = round(quantity * unit_price, 2)
            total_amount += total_price

            order_items.append(
                {
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                }
            )

        # Order metadata
        metadata = {
            "items_count": num_items,
            "source": random.choice(["web", "mobile", "store", "phone"]),
            "shipping_method": random.choice(["standard", "express", "pickup"]),
            "notes": f"Test order {i}" if random.random() > 0.8 else "",
        }

        # Create order INSERT statement
        order_stmt = f"""
        INSERT INTO orders (
            order_number, customer_name, customer_email, 
            status, total_amount, order_date, metadata
        ) VALUES (
            '{order_number}', '{customer_name}', '{customer_email}',
            '{status}', {total_amount:.2f}, '{order_date}',
            '{json.dumps(metadata)}'::jsonb
        ) RETURNING id;
        """

        order_statements.append(order_stmt)

    return order_statements


async def run_async_postgresql_example(products: int, orders: int) -> None:
    """
    Run the async PostgreSQL example with SQL Batcher.

    Args:
        products: Number of products to generate
        orders: Number of orders to generate
    """
    print("SQL Batcher - Async PostgreSQL Example")
    print("======================================")

    # Get connection parameters
    connection_params = get_connection_params()
    dsn = f"postgresql://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['dbname']}"
    print(f"Connecting to PostgreSQL at {connection_params['host']}:{connection_params['port']}...")

    # Create async PostgreSQL adapter
    adapter = AsyncPostgreSQLAdapter(
        dsn=dsn,
        min_size=5,
        max_size=10,
    )

    # Connect to database
    await adapter.connect()

    try:
        # Set up database
        await setup_database(adapter)

        # Create SQL batcher with appropriate settings
        batcher = AsyncSQLBatcher(
            adapter=adapter,
            max_bytes=500_000,  # 500KB per batch
            auto_adjust_for_columns=True,  # Adjust batch size based on column count
            merge_inserts=True,  # Enable insert merging
        )

        # Insert products using PostgreSQL COPY command for efficiency
        if products > 0:
            print(f"\nInserting {products} products using COPY command...")
            start_time = time.time()

            # Generate product data
            product_data = generate_product_data(products)

            # Use the specialized COPY method for bulk insertion
            copied_count = await adapter.use_copy_for_bulk_insert(
                table_name="products",
                column_names=["sku", "name", "category", "price", "stock", "attributes"],
                data=product_data,
            )

            elapsed = time.time() - start_time
            print(f"Inserted {copied_count} products in {elapsed:.2f} seconds")

            # Create indices for better query performance
            print("\nCreating indices on products table...")
            await adapter.create_indices(
                table_name="products",
                indices=[
                    {"columns": ["category"], "name": "idx_products_category"},
                    {"columns": ["price"], "name": "idx_products_price"},
                ],
            )

        # Insert orders using batched statements
        if orders > 0:
            print(f"\nInserting {orders} orders using batched statements...")
            start_time = time.time()

            # Begin a transaction
            await adapter.begin_transaction()

            try:
                # Generate order INSERT statements
                order_statements = await generate_order_data(orders, products)

                # Process all statements in batches
                # Use async context manager for clean resource management
                async with batcher as b:
                    # Process statements in batches
                    await b.process_statements(order_statements, adapter.execute)

                # Commit the transaction
                await adapter.commit_transaction()

                elapsed = time.time() - start_time
                print(f"Inserted {orders} orders in {elapsed:.2f} seconds")

            except Exception as e:
                # Rollback on error
                await adapter.rollback_transaction()
                print(f"Error: {e}")
                raise

        # Run some example queries to demonstrate PostgreSQL-specific features
        print("\nRunning example queries...")

        # Query using JSONB operations
        print("\n1. Find products with specific attributes using JSONB operators:")
        results = await adapter.execute(
            """
        SELECT id, name, category, attributes->>'color' as color 
        FROM products 
        WHERE attributes @> '{"color": "Red"}'::jsonb 
        LIMIT 5
        """
        )

        for row in results:
            print(f"  Product {row[0]}: {row[1]} ({row[2]}) - Color: {row[3]}")

        # Query with aggregation and filtering
        print("\n2. Order statistics by status:")
        results = await adapter.execute(
            """
        SELECT 
            status, 
            COUNT(*) as order_count, 
            SUM(total_amount) as total_sales,
            AVG(total_amount) as avg_order_value
        FROM orders
        GROUP BY status
        ORDER BY total_sales DESC
        """
        )

        for row in results:
            status, count, total, avg = row
            print(f"  {status}: {count} orders, ${total:.2f} total, ${avg:.2f} average")

        # Query with JOIN and JSON extraction
        print("\n3. Top selling products by order source:")
        results = await adapter.execute(
            """
        SELECT 
            p.category,
            o.metadata->>'source' as order_source,
            COUNT(*) as order_count
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN products p ON oi.product_id = p.id
        GROUP BY p.category, o.metadata->>'source'
        ORDER BY order_count DESC
        LIMIT 10
        """
        )

        for row in results:
            category, source, count = row
            print(f"  {category} via {source}: {count} orders")

    finally:
        # Close the connection
        await adapter.close()
        print("\nExample completed successfully!")


async def main():
    """Run the async PostgreSQL example."""
    import argparse

    parser = argparse.ArgumentParser(description="SQL Batcher Async PostgreSQL Example")
    parser.add_argument(
        "--products",
        type=int,
        default=100,
        help="Number of products to generate (default: 100)",
    )
    parser.add_argument(
        "--orders",
        type=int,
        default=50,
        help="Number of orders to generate (default: 50)",
    )

    args = parser.parse_args()
    await run_async_postgresql_example(args.products, args.orders)


if __name__ == "__main__":
    asyncio.run(main())
