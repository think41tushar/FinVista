from fastapi import APIRouter, HTTPException
from models.relation import RelationIn
from services.relation_service import create_new_relation, update_existing_relation

router = APIRouter(prefix="/relations")

@router.post("/")
def create(rel: RelationIn):
    return create_new_relation(rel)

@router.put("/{rel_id}")
def update(rel_id: str, updates: dict):
    try:
        return update_existing_relation(rel_id, updates)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))