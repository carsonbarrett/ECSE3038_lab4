from fastapi import FastAPI
import motor.motor_asyncio 
from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import uuid

app = FastAPI()

connection = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Lab5:Lab5@cluster0.7stqq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

profiles_db = connection.get_database("profiles")
tanks_db = connection.get_database("tanks")

PyObjectId = Annotated[str, BeforeValidator(str)]

class Profile(BaseModel):
    username: str
    role: str
    color: str

class Tank(BaseModel):
    location: str
    lat: float
    long: float

origins = ["https://ecse3038-lab3-tester.netlify.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/profile")
async def get_profile():
    profile = await profiles_db.find_one({})
    if profile:
        profile["_id"] = str(profile["_id"])
        return profile
    return {}

@app.post("/profile")
async def create_profile(profile: Profile):
    existing_profile = await profiles_db.find_one({})
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    new_profile = profile.dict()
    new_profile["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = await profiles_db.insert_one(new_profile)
    new_profile["id"] = str(result.inserted_id)
    return new_profile


@app.get("/tank")
async def get_tanks():
    tanks = []
    async for tank in tanks_db.find():
        tank["_id"] = str(tank["_id"])
        tanks.append(tank)
    return tanks

@app.post("/tank")
async def create_tank(tank: Tank):
    tank_data = tank.dict()
    tank_data["id"] = str(uuid.uuid4())  # Generate unique ID
    await tanks_db.insert_one(tank_data)

    # Update profile's last_updated field
    await profiles_db.update_one({}, {"$set": {"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})

    return tank_data

@app.patch("/tank/{id}")
async def update_tank(id: str, tank: Tank):
    update_data = {k: v for k, v in tank.dict().items() if v is not None}
    result = await tanks_db.update_one({"id": id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Tank not found")

    # Update profile's last_updated field
    await profiles_db.update_one({}, {"$set": {"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})

    return await tanks_db.find_one({"id": id})

@app.delete("/tank/{id}")
async def delete_tank(id: str):
    result = await tanks_db.delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tank not found")

    # Update profile's last_updated field
    await profiles_db.update_one({}, {"$set": {"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})

    return {}
