from typing import Optional

from sqlalchemy.orm import Session

from ....infrastructure import database
from .. import entities


class CRUDCollaborator:
    @classmethod
    def find_id(cls, db: Session, id: int) -> Optional[entities.Collaborator]:
        db_record = db.query(database.orm.CollaboratorORM).filter_by(id=id).first()
        return cls.rebuild_entity(db_record)

    @classmethod
    def find_username(
        cls, db: Session, username: str
    ) -> Optional[entities.Collaborator]:
        db_record = (
            db.query(database.orm.CollaboratorORM).filter_by(username=username).first()
        )
        return cls.rebuild_entity(db_record)

    @classmethod
    def find_or_create(
        cls, db: Session, entity: entities.Collaborator
    ) -> entities.Collaborator:
        return cls.find_username(db, entity.username) or cls.create(db, entity)

    @classmethod
    def create(
        cls, db: Session, entity: entities.Collaborator
    ) -> entities.Collaborator:
        db_collaborator = database.orm.CollaboratorORM(
            origin_id=entity.origin_id, username=entity.username, email=entity.email
        )
        db.add(db_collaborator)
        db.commit()
        db.refresh(db_collaborator)
        return cls.rebuild_entity(db_collaborator)

    @classmethod
    def rebuild_entity(
        cls, db_record: Optional[database.orm.CollaboratorORM]
    ) -> Optional[entities.Collaborator]:
        return entities.Collaborator.from_orm(db_record) if db_record else None
