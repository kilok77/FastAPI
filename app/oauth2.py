from hashlib import algorithms_available

from jose import JWTError, jwt
from datetime import date, datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2Scheme = OAuth2PasswordBearer(tokenUrl = 'login')

#SECRET_KEY
#Algorithm
#Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.acces_token_expire_minutes

def createAccessToken(data: dict):
    toEncode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp": expire})

    encodedJWT = jwt.encode(toEncode,SECRET_KEY,algorithm=ALGORITHM)

    return encodedJWT

def verifyAccessToken(token: str, credentialsException):

    try:

        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("userId")

        if id is None:
            raise credentialsException
        
        tokenData = schemas.TokenData(id=id)

    except JWTError:
        raise credentialsException

    return tokenData

    
def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(database.get_db)):
    credentialException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate your credentials", headers={"WWW-Authenticate": "Bearer"})


    token = verifyAccessToken(token,credentialException)

    user = db.query(models.User).filter(models.User.id == token.id).first() 
    return user
