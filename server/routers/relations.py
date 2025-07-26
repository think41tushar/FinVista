from fastapi import APIRouter, HTTPException
from models.relation import RelationIn
from services.relation_service import (
    create_new_relation, 
    update_existing_relation,
    get_relation_by_id,
    get_user_relations,
    list_all_relations,
    remove_relation,
    add_transaction_to_relation
)

router = APIRouter(prefix="/relations")

@router.post("/")
def create(rel: RelationIn):
    try:
        return create_new_relation(rel)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{rel_id}")
def update(rel_id: str, updates: dict):
    try:
        return update_existing_relation(rel_id, updates)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{rel_id}")
def get_by_id(rel_id: str):
    try:
        relation = get_relation_by_id(rel_id)
        if not relation:
            raise HTTPException(status_code=404, detail="Relation not found")
        return relation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}")
def get_by_user_id(user_id: str):
    try:
        return get_user_relations(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_all():
    try:
        return list_all_relations()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{rel_id}")
def delete(rel_id: str):
    try:
        remove_relation(rel_id)
        return {"message": "Relation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{rel_id}/add-transaction/{transaction_id}")
def add_transaction(rel_id: str, transaction_id: str):
    try:
        return add_transaction_to_relation(rel_id, transaction_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))