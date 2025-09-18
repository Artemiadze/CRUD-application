from typing import NewType
from uuid import UUID

UserId = NewType("UserId", UUID)
PassportId = NewType("PassportId", UUID)