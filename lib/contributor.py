class Contributor:
    def __init__(self, contributor_data: dict):
        self._contributor = contributor_data

    @property
    def username(self) -> str:
        return self._contributor["login"]

    @property
    def email(self) -> str:
        return self._contributor["email"]
