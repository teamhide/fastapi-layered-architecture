from core.db import session
from core.exception import CustomException


class Transaction:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise CustomException(error='transaction error', code=500)
