"""
Inventory System Module
Provides functions for adding, removing, loading, and saving
stock items with proper logging and validation.
"""

import json
import logging
from datetime import datetime

# Configure logging (only console output)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add an item to the stock data."""
    if logs is None:
        logs = []

    if not isinstance(item, str):
        logging.warning("Invalid item name. Must be a string.")
        return

    if not isinstance(qty, (int, float)) or qty <= 0:
        logging.warning("Quantity must be positive for %s. Ignored.", item)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s. Total: %d", qty, item, stock_data[item])


def remove_item(item, qty):
    """Remove an item from stock data safely."""
    try:
        if item not in stock_data:
            raise KeyError(item)
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("%s removed completely (quantity <= 0).", item)
        else:
            logging.info(
                "Removed %d of %s. Remaining: %d", qty, item, stock_data[item]
            )
    except KeyError:
        logging.error("Item not found: '%s'", item)
    except ValueError as e:
        logging.error("Invalid quantity for %s: %s", item, e)


def get_qty(item):
    """Get quantity of a specific item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data.clear()
            stock_data.update(json.load(f))
        logging.info("Data loaded successfully from %s", file)
    except FileNotFoundError:
        logging.warning(
            "File %s not found. Starting with empty inventory.", file
        )
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in %s", file)


def save_data(file="inventory.json"):
    """Save inventory data to file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        logging.info("Data saved successfully to %s", file)
    except OSError as e:
        logging.error("Error saving data to %s: %s", file, e)


def print_data():
    """Print all items in stock."""
    logging.info("Items Report:")
    for i, qty in stock_data.items():
        logging.info("%s -> %d", i, qty)


def check_low_items(threshold=5):
    """Return a list of items below the threshold."""
    return [i for i, qty in stock_data.items() if qty < threshold]


def main():
    """Main execution for inventory operations."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")
    remove_item("apple", 3)
    remove_item("orange", 1)

    apple_qty = get_qty("apple")
    logging.info("Apple stock: %d", apple_qty)

    low_items = check_low_items()
    logging.info("Low items: %s", low_items)

    save_data()
    load_data()
    print_data()

    print("\n Inventory operations completed successfully.\n")


if __name__ == "__main__":
    main()
