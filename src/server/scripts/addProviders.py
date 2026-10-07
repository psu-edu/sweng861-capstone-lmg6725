from models.database import SessionLocal
from models.provider import Provider


PROVIDERS = [
    {
        "name": "Dr. Alex",
        "specialty": "Primary Care",
        "service_category": "General Visit"
    },
    {
        "name": "Dr. Lauren",
        "specialty": "Primary Care",
        "service_category": "General Visit"
    },
    {
        "name": "Dr. Harrison",
        "specialty": "Sports Medicine",
        "service_category": "Sports Injury"
    },
    {
        "name": "Nurse Sharon",
        "specialty": "Nursing",
        "service_category": "Vaccination"
    },
    {
        "name": "Nurse Brandon",
        "specialty": "Nursing",
        "service_category": "Wellness Visit"
    },
    {
        "name": "Nurse Braxton",
        "specialty": "Nursing",
        "service_category": "General Visit"
    },
    {
        "name": "Campus Health Center",
        "specialty": "General Health",
        "service_category": "General Visit"
    }
]


def main():
    db = SessionLocal()

    try:
        for provider_data in PROVIDERS:

            existing = (
                db.query(Provider)
                .filter(
                    Provider.name
                    == provider_data["name"]
                )
                .first()
            )

            if existing:
                print(
                    f"{provider_data['name']} "
                    "already exists. Skipping."
                )
                continue

            provider = Provider(
                name=provider_data["name"],
                specialty=provider_data["specialty"],
                service_category=(
                    provider_data["service_category"]
                ),
                active=True
            )

            db.add(provider)

            print(
                f"Adding {provider_data['name']}"
            )

        db.commit()

        print(
            "Provider added completed successfully."
        )

    except Exception as e:
        db.rollback()
        print(f"Provider addition failed: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    main()