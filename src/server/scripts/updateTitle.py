from models.database import SessionLocal
from User import User

db = SessionLocal()

test_doctor = db.query(User).filter(
    User.email.ilike("testdoctort@doc@pennmedicine@pennmedicine.edu")
).all()

for user in test_doctor:
    db.delete(user)

users = db.query(User).filter(
    User.email.ilike("%@doc@pennmedicine@pennmedicine.edu")
).all()

if users:
    for user in users:
        malformed_suffix = "@doc@pennmedicine@pennmedicine.edu"
        user.email = user.email[:-len(malformed_suffix)] + "@pennmedicine.edu"

db.commit()

print(
    f"Deleted {len(test_doctor)} testdoctort profile(s) and updated "
    f"{len(users)} user email(s) to @pennmedicine.edu"
)

db.close()