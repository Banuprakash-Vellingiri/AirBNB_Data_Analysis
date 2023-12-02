#---------------------------------------------------Airbnb Data Analysis---------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------
#                                          Connecting Mongodb_atlas with Python
#---------------------------------------------------------------------------------------------------------------------------------------
#importing neccessary libraries
import pandas as pd
from pymongo.mongo_client import MongoClient

#Making connection with Mongodb_atlas
url = "mongodb+srv://Banu:BanuMongodbatlas.V2@airbnb.tgna0ww.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

database_names = client.list_database_names()
#Connecting with "sample_airbnb" database
db=client["sample_airbnb"]

collection_names = db.list_collection_names()
#Connecting with "listingsAndReviews" collection
collection=db["listingsAndReviews"]

#Converting collection to DataFrame for only for visualize data 
documents = collection.find()
data = list(documents)
df= pd.DataFrame(data)

#Converting DataFrame into csv file
df.to_csv("airbnb.csv", index=False) 

#---------------------------------------------------------------------------------------------------------------------------------------
#                                                     Data Cleaning process
#---------------------------------------------------------------------------------------------------------------------------------------

#importing neccessary libraries
import pandas as pd
import ast 
df=pd.read_csv("airbnb.csv")
#---------------------------------------------------------------------------------------------------------------------------------------
#Cleaning_basic_details of room

df=df.dropna(subset=["name"])
df["security_deposit"]=df["security_deposit"].fillna(0)
df["beds"]=df["beds"].fillna(0)
df["beds"]=df["beds"].astype(int)
df["extra_people"]=df["extra_people"].fillna(0)
df["extra_people"]=df["extra_people"].astype(int)
df["bathrooms"]=df["bathrooms"].fillna(0)
df["bathrooms"]=df["bathrooms"].apply(lambda x:round(x))
df["bedrooms"]=df["bedrooms"].fillna(0)
#---------------------------------------------------------------------------------------------------------------------------------------
#Extracting and cleaning_address_details of room

df["street"]=df["address"].apply(lambda x : ast.literal_eval(x)["street"])
df["sub_urban"]=df["address"].apply(lambda x : ast.literal_eval(x)["suburb"])
df["government_area"]=df["address"].apply(lambda x : ast.literal_eval(x)["government_area"])
df["country"]=df["address"].apply(lambda x : ast.literal_eval(x)["country"])
df["country_code"]=df["address"].apply(lambda x : ast.literal_eval(x)["country_code"])
df["latitude"] = df["address"].apply(lambda x: ast.literal_eval(x)['location']['coordinates'][1])
df["longitude"] = df["address"].apply(lambda x: ast.literal_eval(x)['location']['coordinates'][0])
#---------------------------------------------------------------------------------------------------------------------------------------
#Host details

df["host_id"]=df["host"].apply(lambda x : ast.literal_eval(x)["host_id"])
df["host_name"]=df["host"].apply(lambda x : ast.literal_eval(x)["host_name"])
df["host_location"]=df["host"].apply(lambda x : ast.literal_eval(x)["host_location"])
df["host_is_superhost"]=df["host"].apply(lambda x : ast.literal_eval(x)["host_is_superhost"])
df["host_is_superhost"]=df["host_is_superhost"].apply(lambda x:"yes"if x==True else "no")
df["host_identity_verified"]=df["host"].apply(lambda x : ast.literal_eval(x)["host_identity_verified"])
df["host_identity_verified"]=df["host_identity_verified"].apply(lambda x:"yes"if x==True else "no")
df["host_total_listings_count"]=df["host"].apply(lambda x : ast.literal_eval(x)["host_total_listings_count"])
df["host_has_profile_pic"]=df["host"].apply(lambda x : ast.literal_eval(x)["host_has_profile_pic"])
df["host_has_profile_pic"]=df["host_has_profile_pic"].apply(lambda x:"yes"if x==True else "no")
#---------------------------------------------------------------------------------------------------------------------------------------
#price details

df["cleaning_fee"]=df["cleaning_fee"].fillna(0)
#---------------------------------------------------------------------------------------------------------------------------------------
#Availability details

df["availability_30"]=df["availability"].apply(lambda x : ast.literal_eval(x)["availability_30"])
df["availability_60"]=df["availability"].apply(lambda x : ast.literal_eval(x)["availability_60"])
df["availability_90"]=df["availability"].apply(lambda x : ast.literal_eval(x)["availability_90"])
df["availability_365"]=df["availability"].apply(lambda x : ast.literal_eval(x)["availability_365"])
#---------------------------------------------------------------------------------------------------------------------------------------
#Review scores

def get_scores(scores,x):
   try:
       return ast.literal_eval(x)[scores]
   except (KeyError, ValueError):
       return "not_available"
   
df["review_scores_accuracy"]=df["review_scores"].apply(lambda x :get_scores("review_scores_accuracy",x))
df["review_scores_cleanliness"]=df["review_scores"].apply(lambda x :get_scores("review_scores_cleanliness",x))
df["review_scores_checkin"]=df["review_scores"].apply(lambda x :get_scores("review_scores_checkin",x))
df["review_scores_communication"]=df["review_scores"].apply(lambda x :get_scores("review_scores_communication",x))
df["review_scores_value"]=df["review_scores"].apply(lambda x :get_scores("review_scores_value",x))
df["review_scores_location"]=df["review_scores"].apply(lambda x :get_scores("review_scores_location",x))
df["review_scores_rating"]=df["review_scores"].apply(lambda x :get_scores("review_scores_rating",x))
#---------------------------------------------------------------------------------------------------------------------------------------
#Creating a new dataframe "data"
data=df[['name', 'space', 'property_type', 'room_type', 'bed_type',
       'minimum_nights', 'maximum_nights', 'cancellation_policy',
       'accommodates', 'bedrooms', 'beds', 'number_of_reviews', 'bathrooms',
       'price', 'security_deposit', 'cleaning_fee','monthly_price',
       'extra_people', 'guests_included','weekly_price',
       'host_id', 'host_name', 'host_location', 'host_neighbourhood',
       'host_is_superhost', 'host_identity_verified',
       'host_total_listings_count', 'host_has_profile_pic', 'availability_30',
       'availability_60', 'availability_90', 'availability_365',
       'street', 'sub_urban','government_area', 'country_code', 'latitude', 'longitude', 'country',
       'availability_30','availability_60', 'availability_90', 'availability_365',
       'review_scores_accuracy', 'review_scores_cleanliness',
       'review_scores_checkin', 'review_scores_communication',
       'review_scores_value', 'review_scores_location', 'review_scores_rating',
       ]]
#Converting DataFrame into csv file
data.to_csv("airbnb_cleaned_dataset.csv",index=False)
#---------------------------------------------------------------------------------------------------------------------------------------
