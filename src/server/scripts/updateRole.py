from models.database import SessionLocal
from User import User

db = SessionLocal()


users = db.query(User).filter(
    User.role.ilike("user")
).all()

if users:
    for user in users:
        user.role = "patient"

db.commit()

print(
    f"{len(users)} user role to patient"
)

db.close()