from data.spending_dao import (
    create_spending,
    get_spending_by_id,
    get_all_spendings,
    update_spending,
    delete_spending,
    bulk_create_spendings
)
import logging

logger = logging.getLogger(__name__)

def create_new_spending(spending_data: dict):
    logger.info("Creating new spending")
    return create_spending(spending_data)

def get_spending(spending_id: str):
    logger.info("Getting spending %s", spending_id)
    return get_spending_by_id(spending_id)

def list_all_spendings():
    logger.info("Getting all spendings")
    return get_all_spendings()

def update_spending_data(spending_id: str, updates: dict):
    logger.info("Updating spending %s", spending_id)
    return update_spending(spending_id, updates)

def remove_spending(spending_id: str):
    logger.info("Deleting spending %s", spending_id)
    return delete_spending(spending_id)

def create_multiple_spendings(spendings: list):
    logger.info("Creating multiple spendings")
    return bulk_create_spendings(spendings)