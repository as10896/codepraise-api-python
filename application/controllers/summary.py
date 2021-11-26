from fastapi import APIRouter


router = APIRouter()


@router.get("/summary/")
def summary_index_request():
    pass
