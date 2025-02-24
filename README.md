# ECSE3038_lab4

API Endpoints and Expected Behavior

Profile Endpoints

GET /profile:

Retrieves the stored profile from the database.

If a profile exists, it is returned with its _id converted to a string.

If no profile exists, an empty object {} is returned.

POST /profile:

Creates a new profile.

If a profile already exists, it returns a 400 Bad Request error.

The profile includes username, role, and color fields.

The last_updated field is set to the current timestamp upon creation.

Tank Endpoints

GET /tank:

Retrieves all stored tanks from the database.

Returns an array of tank objects, each including _id as a string.

POST /tank:

Creates a new tank entry.

Each tank has a location, lat (latitude), and long (longitude).

A unique ID is generated using uuid.

The profile’s last_updated field is updated upon tank creation.

PATCH /tank/{id}:

Updates an existing tank’s details based on the provided id.

If the tank does not exist, returns a 404 Not Found error.

Updates only the fields that are provided in the request.

The profile’s last_updated field is updated after a successful modification.

DELETE /tank/{id}:

Deletes a tank by id.

If no tank is found, returns a 404 Not Found error.

The profile’s last_updated field is updated upon successful deletion.

Project Purpose

This code was developed as part of an assignment to build a RESTful API for managing IoT-enabled water tanks. It focuses on using FastAPI for efficient asynchronous handling and MongoDB as the database.

Favourite Low Effort Food: Cinnamonrolls, its the nest thing ever created, if you want to taste perfection eat a honey bun cinnamonroll.


