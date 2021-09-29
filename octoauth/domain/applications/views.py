from typing import List

from fastapi import APIRouter

from octoauth.architecture.database import Session
from octoauth.domain.applications.dao import ApplicationDAO
from octoauth.domain.applications.schemas import ApplicationReadDTO, ApplicationWriteDTO

router = APIRouter()


@router.get("/applications/{application_uid}", response_model=ApplicationReadDTO)
def get_application(application_uid: str):
    with Session as session:
        application_dao = ApplicationDAO(session)
        application = application_dao.get_or_404(uid=application_uid)
        response_data = ApplicationReadDTO.from_model(application)
    return response_data


@router.get("/applications", response_model=List[ApplicationReadDTO])
def search_applications():
    with Session as session:
        application_dao = ApplicationDAO(session)
        applications = application_dao.search()
        response_data = [ApplicationReadDTO.from_model(application) for application in applications]
    return response_data


@router.post("/applications", response_model=ApplicationReadDTO)
def create_application(input_data: ApplicationWriteDTO):
    with Session as session:
        application_dao = ApplicationDAO(session)
        application = application_dao.create(input_data)
        response_data = ApplicationReadDTO.from_model(application)
    return response_data


@router.put("/applications/{application_uid}", response_model=ApplicationReadDTO)
def update_application(application_uid: str, input_data: ApplicationWriteDTO):
    with Session as session:
        application_dao = ApplicationDAO(session)
        application = application_dao.update(application_uid, input_data)
        response_data = ApplicationReadDTO.from_model(application)
    return response_data


@router.delete("/applications/{application_uid}")
def delete_application(application_uid: str):
    with Session as session:
        application_dao = ApplicationDAO(session)
        application = application_dao.get_or_404(application_uid)
        response_data = ApplicationReadDTO.from_model(application)
        application_dao.delete(application_uid)
    return response_data
