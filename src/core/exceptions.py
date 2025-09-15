class DomainError(Exception):
    """Base exception for domain errors."""
    pass

class DomainValidationError(DomainError):
    """Custom exception for domain validation errors."""
    pass


class DuplicateError(DomainError):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"Duplicate {field}: {value}")


class NotFoundError(DomainError):
    def __init__(self, entity: str, entity_id: int):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"{entity} with id={entity_id} not found")