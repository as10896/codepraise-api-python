from .. import entities
from .crud_collaborator import CRUDCollaborator
from .crud_repo import CRUDRepo

For = {
    entities.Repo: CRUDRepo,
    entities.Collaborator: CRUDCollaborator,
}
