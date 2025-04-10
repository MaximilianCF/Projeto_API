from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.submission import Submission, SubmissionCreate, SubmissionRead

router = APIRouter()


@router.post("/", response_model=SubmissionRead,
             summary="Enviar uma nova submissão")
def create_submission(
    submission: SubmissionCreate, session: Session = Depends(get_session)
):
    new_submission = Submission.from_orm(submission)
    session.add(new_submission)
    session.commit()
    session.refresh(new_submission)
    return new_submission


@router.get("/",
            response_model=List[SubmissionRead],
            summary="Listar todas submissões")
def read_submissions(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    submissions = session.exec(
        select(Submission).offset(offset).limit(limit)).all()
    return submissions


@router.get(
    "/{submission_id}",
    response_model=SubmissionRead,
    summary="Detalhes de uma submissão específica",
)
def read_submission(
        submission_id: int,
        session: Session = Depends(get_session)):
    submission = session.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submissão não encontrada")
    return submission
