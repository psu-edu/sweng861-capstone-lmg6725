from flask import Blueprint, jsonify, request
from models.database import SessionLocal
from models.prompt import Prompt
from User import User
from flask import g
from middleware.authMiddleware import require_auth
from flask import logging

# Blueprint for all AI prompt-related API endpoints
# Handle creating, reading, updating, and deleting saved prompt/response pairs

prompt_bp = Blueprint("prompts", __name__)

@prompt_bp.route("/prompts", methods=["POST"])
@require_auth
def create_prompt():
    # Create a database session for this request
    session = SessionLocal()

    try:
        # Read JSON request from client
        data = request.get_json()

        # Reject request if no JSON body
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        # Prompt and response are required fields
        if "prompt" not in data or "response" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        # Get the current user from database
        current_user = (
                session.query(User)
                .filter(User.provider_id == g.user_id)
                .first()
        )

        # New prompt pair is associated with the current user
        prompt = Prompt(
                    prompt = data["prompt"],
                    response= data["response"],
                    user_id = current_user.id
                )
        
        # Save the new prompt pair to the database
        session.add(prompt)
        session.commit()
        session.refresh(prompt)
        logging.info(f"PROMPT_CREATED: user={current_user.id} prompt={prompt.id}")

        return jsonify({
            "id": prompt.id,
            "prompt": prompt.prompt,
            "response": prompt.response
        }), 201
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally: # Close database session
        session.close()

# Get all prompts for the authenticated user
@prompt_bp.route("/prompts", methods=["GET"])
@require_auth
def get_prompts():
    # Create a database session for this request
    session = SessionLocal()

    try:
        # Get prompts from the database
        prompts = session.query(Prompt).all()

        return jsonify([
            {
                "id": p.id,
                "prompt": p.prompt,
                "response": p.response
            }
            for p in prompts
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally: # Close database session
        session.close()

# Get a specific prompt by ID
@prompt_bp.route("/prompts/<int:prompt_id>", methods=["GET"])
def get_prompt(prompt_id):
    session = SessionLocal()

    try: # Get the prompt from the database by filtering by the prompt ID
        prompt = session.query(Prompt).filter(
            Prompt.id == prompt_id
        ).first()

        if not prompt:
            return jsonify({"error": "Not found"}), 404

        return jsonify({
            "id": prompt.id,
            "prompt": prompt.prompt,
            "response": prompt.response
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

# Update a specific prompt by ID
@prompt_bp.route("/prompts/<int:prompt_id>", methods=["PUT"])
@require_auth
def update_prompt(prompt_id):
    session = SessionLocal()

    try:
        prompt = session.query(Prompt).filter(
            Prompt.id == prompt_id
        ).first()

        # If the prompt does not exist, return a 404 error
        if not prompt:
            return jsonify({"error": "Not found"}), 404

        # Get the current user from the database
        current_user = (
            session.query(User)
            .filter(User.provider_id == g.user_id)
            .first()
        )

        # Check if the current user is the owner of the prompt or a doctor
        if (
            prompt.user_id != current_user.id
            and current_user.role != "doctor"
        ):
            return jsonify({
                "error": "Unauthorized"
            }), 403

        # Read the JSON request from the client
        data = request.get_json()

        # Only update fields in request
        if "prompt" in data:
            prompt.prompt = data["prompt"]
        if "response" in data:
            prompt.response = data["response"]

        # Save the updated prompt to the database
        session.commit()

        return jsonify({"message": "Updated"})

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()

# Delete a specific prompt by ID if the user is the owner or a doctor
@prompt_bp.route("/prompts/<int:prompt_id>", methods=["DELETE"])
@require_auth
def delete_prompt(prompt_id):
    session = SessionLocal()

    try:
        prompt = session.query(Prompt).filter(
            Prompt.id == prompt_id
        ).first()

        if not prompt:
            return jsonify({"error": "Not found"}), 404

        current_user = (
            session.query(User)
            .filter(User.provider_id == g.user_id)
            .first()
        )

        if (
            prompt.user_id != current_user.id
            and current_user.role != "doctor"
        ):
            return jsonify({
                "error": "Unauthorized"
            }), 403

        session.delete(prompt)
        session.commit()

        return jsonify({"message": "Deleted"})

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()