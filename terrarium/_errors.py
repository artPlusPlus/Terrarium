class TerrariumError(Exception):
    """Base class for Terrarium errors."""
    pass


class ResourceNotFoundError(TerrariumError):
    """Raised when a resource was requested, but not found."""
    pass


class ResourceCreationError(TerrariumError):
    """Raised when the creation of a resource fails."""
    pass


class ResourceAlreadyExistsError(ResourceCreationError):
    """Raised when trying to create a resource that matches the name of an existing resource."""
    pass


class ResourceUpdateError(TerrariumError):
    """Raised when an attempt to update a resource fails."""
    pass


class ResourceAttributeNotFoundError(ResourceUpdateError):
    """Raised when attempting to update a resource that does not have the target attribute"""
    pass
