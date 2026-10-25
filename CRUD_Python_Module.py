"""CRUD operations for the AAC animal shelter MongoDB database."""

from pymongo import MongoClient
from pymongo.errors import PyMongoError


class AnimalShelter:
    """Provides access to animal records stored in MongoDB."""

    def __init__(self, username, password):
        """Connect to the AAC database using the supplied credentials."""

        # Connect to MongoDB using the aacuser login.
        self.client = MongoClient(
            "mongodb://localhost:27017",
            username=username,
            password=password,
            authSource="admin"
        )

        # Select the AAC database and animals collection.
        self.database = self.client["aac"]
        self.collection = self.database["animals"]

    def create(self, data):
        """Insert one animal document into the collection."""

        # Make sure the value being inserted is a nonempty dictionary.
        if not isinstance(data, dict) or not data:
            return False

        try:
            # Insert the new document into the animals collection.
            result = self.collection.insert_one(data)

            # Return whether MongoDB acknowledged the insert.
            return result.acknowledged

        except PyMongoError:
            # Return False if MongoDB cannot complete the insert.
            return False

    def read(self, query):
        """Return animal documents that match the supplied query."""

        # A MongoDB query should be supplied as a dictionary.
        if not isinstance(query, dict):
            return []

        try:
            # find() returns all documents that match the query.
            results = self.collection.find(query)

            # Convert the MongoDB cursor into a Python list.
            return list(results)

        except PyMongoError:
            # Return an empty list if the query cannot be completed.
            return []

    def update(self, query, new_values):
        """Update animal documents that match the supplied query."""

        # Both the search criteria and new values must be dictionaries.
        if not isinstance(query, dict):
            return 0

        if not isinstance(new_values, dict) or not new_values:
            return 0

        try:
            # Change the requested fields in all matching documents.
            result = self.collection.update_many(
                query,
                {"$set": new_values}
            )

            # Return the number of documents MongoDB actually modified.
            return result.modified_count

        except PyMongoError:
            # Return zero if MongoDB cannot complete the update.
            return 0

    def delete(self, query):
        """Delete animal documents that match the supplied query."""

        # The search criteria should be supplied as a dictionary.
        if not isinstance(query, dict):
            return 0

        try:
            # Remove every document that matches the query.
            result = self.collection.delete_many(query)

            # Return the number of documents that were removed.
            return result.deleted_count

        except PyMongoError:
            # Return zero if MongoDB cannot complete the delete.
            return 0