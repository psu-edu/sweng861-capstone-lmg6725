from flask import Blueprint, jsonify

from models.database import SessionLocal
from models.provider import Provider
from middleware.authMiddleware import require_auth


provider_bp = Blueprint("provider_bp", __name__)


@provider_bp.route("/providers", methods=["GET"])
@require_auth
def get_providers():
    db = SessionLocal()

    try:
        providers = (
            db.query(Provider)
            .filter(
                Provider.active.is_(True)
            )
            .order_by(
                Provider.name.asc()
            )
            .all()
        )

        result = []

        for provider in providers:
            result.append({
                "id": provider.id,
                "name": provider.name,
                "specialty": provider.specialty,
                "service_category":
                    provider.service_category
            })

        return jsonify({
            "providers": result
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

    finally:
        db.close()