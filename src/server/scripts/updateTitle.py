from models.database import SessionLocal
from User import User

# Open the database session used for the cleanup/update operation.
db = SessionLocal()

# Remove the current email addresses.
test_doctor = db.query(User).filter(
    User.email.ilike("testdoctort@doc@pennmedicine@pennmedicine.edu")
).all()

for user in test_doctor:
    db.delete(user)

# Find all user records whose email still contains the duplicated doc domain suffix.
users = db.query(User).filter(
    User.email.ilike("%@doc@pennmedicine@pennmedicine.edu")
).all()

if users:
    for user in users:
        # Strip the current email and replace it with the correct Penn Medicine domain.
        malformed_suffix = "@doc@pennmedicine@pennmedicine.edu"
        user.email = user.email[:-len(malformed_suffix)] + "@pennmedicine.edu"

# Save the database changes once all removals and email repairs are complete.
db.commit()

# Report how many records were removed and corrected for quick verification.
print(
    f"Deleted {len(test_doctor)} testdoctort profile(s) and updated "
    f"{len(users)} user email(s) to @pennmedicine.edu"
)

# Close the database connection after finishing the update.
db.close()