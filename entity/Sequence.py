from sqlalchemy import Sequence, func
from sqlalchemy.orm import Session

sequence = Sequence("seq", start=1, increment=1)

def get_next_sequence_value(db: Session):
    result = db.execute(func.next_value(sequence))
    return result.scalar()