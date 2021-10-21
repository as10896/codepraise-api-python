from typing import Optional, List
from sqlalchemy.orm import Session

from .crud_collaborator import CRUDCollaborator

from .. import entities
from infrastructure import database


class CRUDRepo:
    @classmethod
    def all(cls, db: Session) -> List[entities.Repo]:
        db_record = db.query(database.orm.RepoORM).all()
        return list(map(lambda db_repo: cls.rebuild_entity(db_repo), db_record))

    @classmethod
    def find_full_name(
        cls, db: Session, ownername: str, reponame: str
    ) -> Optional[entities.Repo]:
        # SELECT * FROM `repos` LEFT JOIN `collaborators`
        # ON (`collaborators`.`id` = `repos`.`owner_id`)
        # WHERE ((`username` = 'owername') AND (`name` = 'reponame'))
        db_repo = (
            db.query(database.orm.RepoORM)
            .join(
                database.orm.CollaboratorORM,
                database.orm.RepoORM.owner_id == database.orm.CollaboratorORM.id,
            )
            .filter(database.orm.CollaboratorORM.username == ownername)
            .filter(database.orm.RepoORM.name == reponame)
            .first()
        )
        return cls.rebuild_entity(db_repo)

    @classmethod
    def find(cls, db: Session, entity: entities.Repo) -> Optional[entities.Repo]:
        return cls.find_origin_id(db, entity.origin_id)

    @classmethod
    def find_id(cls, db: Session, id: int) -> Optional[entities.Repo]:
        db_record = db.query(database.orm.RepoORM).filter_by(id=id).first()
        return cls.rebuild_entity(db_record)

    @classmethod
    def find_origin_id(cls, db: Session, origin_id: int) -> Optional[entities.Repo]:
        db_record = (
            db.query(database.orm.RepoORM).filter_by(origin_id=origin_id).first()
        )
        return cls.rebuild_entity(db_record)

    @classmethod
    def create(cls, db: Session, entity: entities.Repo) -> entities.Repo:
        if cls.find(db, entity):
            raise Exception("Repo already exists")

        new_owner = CRUDCollaborator.find_or_create(db, entity.owner)
        db_owner = (
            db.query(database.orm.CollaboratorORM).filter_by(id=new_owner.id).first()
        )

        db_repo = database.orm.RepoORM(
            origin_id=entity.origin_id,
            name=entity.name,
            size=entity.size,
            git_url=entity.git_url,
            owner=db_owner,
        )

        for contrib in entity.contributors:
            stored_contrib = CRUDCollaborator.find_or_create(db, contrib)
            contrib = (
                db.query(database.orm.CollaboratorORM)
                .filter_by(id=stored_contrib.id)
                .first()
            )
            db_repo.contributors.append(contrib)

        db.add(db_repo)
        db.commit()
        db.refresh(db_repo)

        return cls.rebuild_entity(db_repo)

    @classmethod
    def rebuild_entity(
        cls, db_record: Optional[database.orm.RepoORM]
    ) -> Optional[entities.Repo]:
        return entities.Repo.from_orm(db_record) if db_record else None
