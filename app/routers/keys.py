from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response
from fastapi import APIRouter, Depends, HTTPException, Request
from dependencies import common_params, get_db, get_secret_random
from schemas import Credentail
from sqlalchemy.orm import Session
from typing import Optional
from models import Secret
from dependencies import get_token_header
import uuid
from datetime import datetime
from exceptions import username_already_exists
from sqlalchemy import over
from sqlalchemy import engine_from_config, and_, func, literal_column, case
from sqlalchemy_filters import apply_pagination
import time
import os
import uuid
from sqlalchemy.dialects import postgresql
import base64

page_size = os.getenv('PAGE_SIZE')
RSA_KEY_START = '-----BEGIN RSA PRIVATE KEY-----\n'
RSA_KEY_END = '\n-----END RSA PRIVATE KEY-----\n'


router = APIRouter(
    prefix="/v1/credentials",
    tags=["CredentialManagementAPIs"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("")
def create(details: Credentail, commons: dict = Depends(common_params), db: Session = Depends(get_db)):
    id = details.id or uuid.uuid4().hex

    credentail = Secret(
        id=id,
        resource_id=details.resource,
        encrypted_key=details.encrypted_key,
        public_key=details.public_key,
        expire_at=details.expire_at,
        active=details.active
    )

    #commiting data to db
    try:
        db.add(credentail)
        db.commit()
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(status_code=422, detail="Unable to create new inventory item")
    return {
        "id": credentail.id
    }

@router.get("/{id}")
def get_by_id(id: str, commons: dict = Depends(common_params), db: Session = Depends(get_db)):
    credentail = db.query(Secret).get(id.strip())
    if credentail == None:
        raise HTTPException(status_code=404, detail="Credentail not found")
    response = {
        "data": credentail
    }
    return response

@router.delete("/{id}")
def delete_by_id(id: str, commons: dict = Depends(common_params), db: Session = Depends(get_db)):
    credentail = db.query(Secret).get(id.strip())
    db.delete(credentail)
    db.commit()
    return Response(status_code=204)

