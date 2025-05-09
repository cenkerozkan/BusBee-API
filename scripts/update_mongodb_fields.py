from pymongo import MongoClient


def update_collection():
    # MongoDB connection
    mongo_uri = "mongodb://root:BusOps_3298%40@localhost:27017/"
    client = MongoClient(mongo_uri)
    db = client["bus_ops"]  # Replace with your database name

    # User input
    field_name = input("Enter the field name: ")
    field_operation = input("Enter the operation (add/remove): ").strip().lower()
    field_type = input("Enter the field type (str, int, float, list, dict, bool): ").strip().lower()
    collection_name = input("Enter the collection name: ")

    # Display entered values
    print("\nYou have entered the following details:")
    print(f"Field Name: {field_name}")
    print(f"Operation: {field_operation}")
    print(f"Field Type: {field_type}")
    print(f"Collection Name: {collection_name}")

    # Ask for confirmation
    confirmation = input("Are you sure you want to proceed? (yes/no): ").strip().lower()
    if confirmation != "yes":
        print("Operation canceled.")
        return

    collection = db[collection_name]

    # Default values for field types
    default_values = {
        "str": "",
        "int": 0,
        "float": 0.0,
        "list": [],
        "dict": {},
        "bool": False,
    }
    default_value = default_values.get(field_type, None)

    if field_operation == "add":
        if default_value is None:
            print(f"Unsupported field type: {field_type}")
            return
        # Add the field to all documents
        result = collection.update_many(
            {field_name: {"$exists": False}},  # Only add if the field does not exist
            {"$set": {field_name: default_value}}
        )
        print(f"Added field '{field_name}' to {result.modified_count} documents.")
    elif field_operation == "remove":
        # Remove the field from all documents
        result = collection.update_many(
            {field_name: {"$exists": True}},  # Only remove if the field exists
            {"$unset": {field_name: ""}}
        )
        print(f"Removed field '{field_name}' from {result.modified_count} documents.")
    else:
        print("Invalid operation. Use 'add' or 'remove'.")

    # Close the MongoDB connection
    client.close()


if __name__ == "__main__":
    update_collection()