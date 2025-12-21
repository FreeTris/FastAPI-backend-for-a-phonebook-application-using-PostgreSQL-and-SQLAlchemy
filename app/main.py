from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, get_db
from app import models, schemas

app = FastAPI()


# -------- Startup --------

@app.on_event("startup")
def startup():
    # NOTE: For production, Alembic migrations are preferred.
    # This is acceptable for an MVP/demo project.
    models.Base.metadata.create_all(bind=engine)


# -------- Health --------

@app.get("/health")
def health():
    return {"status": "ok"}


# -------- Users --------

@app.post("/users", response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    new_user = models.User(
        email=user.email,
        hashed_password=user.password  # hashing intentionally stubbed
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    db.refresh(new_user)
    return new_user


# -------- Contacts --------
# NOTE: Authentication not implemented yet.
# user_id is intentionally stubbed for MVP purposes.

STUB_USER_ID = 1


@app.post(
    "/contacts",
    response_model=schemas.ContactOut,
    status_code=status.HTTP_201_CREATED
)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == STUB_USER_ID).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )

    new_contact = models.Contact(
        name=contact.name,
        phone_number=contact.phone_number,
        address=contact.address,
        user_id=user.id
    )

    db.add(new_contact)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Contact already exists"
        )

    db.refresh(new_contact)
    return new_contact


@app.get("/contacts", response_model=list[schemas.ContactOut])
def list_contacts(
    db: Session = Depends(get_db)
):
    return (
        db.query(models.Contact)
        .filter(models.Contact.user_id == STUB_USER_ID)
        .all()
    )


@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    contact = (
        db.query(models.Contact)
        .filter(
            models.Contact.id == contact_id,
            models.Contact.user_id == STUB_USER_ID
        )
        .first()
    )

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )

    return contact
