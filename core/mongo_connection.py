# core/mongo_connection.py
from pymongo import MongoClient

def get_db():
    """
    Returns a handle to the study_buddy_db MongoDB database.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["study_buddy_db"]   
    return db

# Optional shortcuts for collections
db = get_db()
users_col = db["users"]
courses_col = db["courses"]
groups_col = db["study_groups"]
join_requests_col = db["join_requests"]
join_form_requests_col = db["join_form_requests"]
group_suggestions_col = db["group_suggestions"]
help_requests_col = db["help_requests"]
group_feedback_col = db["group_feedback"]
tutor_applications_col = db["tutor_applications"]
