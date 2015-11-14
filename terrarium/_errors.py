class TerrariumError(Exception):
    pass


class ResourceNotFoundError(TerrariumError):
    pass


class ResourceAlreadyExistsError(TerrariumError):
    pass


class ResourceCreationError(TerrariumError):
    pass


class ResourceAttributeNotFoundError(TerrariumError):
    pass


class ResourceUpdateError(TerrariumError):
    pass
