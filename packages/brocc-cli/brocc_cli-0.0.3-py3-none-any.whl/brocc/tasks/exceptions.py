class ModelNotReadyError(Exception):
    """Raised when an embedding task is called before the model is loaded."""

    pass
