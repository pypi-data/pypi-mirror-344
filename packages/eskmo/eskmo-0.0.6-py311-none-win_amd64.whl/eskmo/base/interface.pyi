from _typeshed import Incomplete
from abc import ABC
from eskmo.internal.api import api as api
from eskmo.internal.user import User as User

class UserReferable(ABC):
    user: User
    accountIds: Incomplete
    def __init__(self, user: User) -> None: ...

class APIReferable(ABC):
    api: api
    def __init__(self, api: api) -> None: ...
