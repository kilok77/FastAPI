from fastapi import Body, FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, utils
from .. database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED,  response_model=schemas.UserOut)
def createUser(user
 : schemas.UserCreate, db: Session = Depends(get_db)):    

    #hast the password
    
    user.password = utils.hash(user.password)

    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser



@router.get('/{id}', response_model=schemas.UserOut)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')

    return user