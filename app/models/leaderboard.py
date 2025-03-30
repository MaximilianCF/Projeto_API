# Sem necessidade de tabela real inicialmente — derivado por consulta.
# Exemplo de consulta que retorna o top 5 por challenge
from sqlmodel import Session, select
from models.submission import Submission

def get_top_submissions_by_challenge(session: Session, challenge_id: int):
    return session.exec(
        select(Submission)
        .where(Submission.challenge_id == challenge_id)
        .order_by(Submission.score.desc())
        .limit(5)
    ).all()
