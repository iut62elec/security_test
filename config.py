"""Configuration module with intentional security vulnerabilities."""
import pickle
import yaml


# VULNERABILITY: Debug mode enabled in production
DEBUG = True
SECRET_KEY = "my-super-secret-key-do-not-share-2024"


def load_session(data):
    """VULNERABILITY: Unsafe deserialization with pickle."""
    return pickle.loads(data)


def load_config(user_input):
    """VULNERABILITY: Unsafe YAML loading."""
    return yaml.load(user_input, Loader=yaml.FullLoader)


def process_payment(amount, card_number):
    """VULNERABILITY: No input validation, logging sensitive data."""
    print(f"Processing payment: card={card_number}, amount={amount}")
    return {"status": "ok", "card": card_number}


def handle_error(error):
    """VULNERABILITY: Information disclosure in error responses."""
    return {
        "error": str(error),
        "stack": repr(error.__traceback__),
        "db_host": "prod-db.internal.company.com:5432",
        "db_password": DB_PASSWORD,
    }


DB_PASSWORD = "prod_db_p@ssw0rd_2024"
