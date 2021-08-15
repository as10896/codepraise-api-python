from .crud_collaborator import CRUDCollaborator
from .crud_repo import CRUDRepo
from .. import entities


For = {entities.Repo: CRUDRepo, entities.Collaborator: CRUDCollaborator}
