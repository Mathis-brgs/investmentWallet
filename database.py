import pymongo
from datetime import datetime

# Connexion à la base de données
client = pymongo.MongoClient("mongodb+srv://alphatrack:alphapassword@cluster0.evvb7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/")
db = client["investments"]


collection_name = "investments"
if collection_name not in db.list_collection_names():
    db.create_collection(
        collection_name,
        timeseries={
            "timeField": "timestamp",
            "metaField": "investment_type",
            "granularity": "hours"
        }
    )

# Création de la table pour stocker les investissements
investments = db[collection_name]

def insert_investment(period, investment_type, data):
    # Convertir la période en datetime
    timestamp = datetime.strptime(period, "%Y_%m")

    # Convertir les dates dans les données en datetime
    if "date" in data:
        data["date"] = datetime.combine(data["date"], datetime.min.time())

    investment = {
        "timestamp": timestamp,
        "investment_type": investment_type,
        "data": data
    }
    investments.insert_one(investment)

def fetch_all_investments():
    return list(investments.find())

def get_investment(period):
    return investments.find_one({"timestamp": datetime.strptime(period, "%Y_%m")})

def fetch_portfolio_data():
    return list(investments.find({}, {"_id": 0, "data": 1, "investment_type": 1}))
