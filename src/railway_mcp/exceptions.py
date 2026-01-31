"""Custom exceptions for Railway MCP server."""


class RailwayError(Exception):
    """Base exception for Railway API errors."""

    pass


class AuthenticationError(RailwayError):
    """Raised when authentication fails."""

    pass


class GraphQLError(RailwayError):
    """Raised when a GraphQL query fails."""

    def __init__(self, message: str, errors: list | None = None):
        super().__init__(message)
        self.errors = errors or []


class ProjectNotFoundError(RailwayError):
    """Raised when a project is not found."""

    pass


class ServiceNotFoundError(RailwayError):
    """Raised when a service is not found."""

    pass


class EnvironmentNotFoundError(RailwayError):
    """Raised when an environment is not found."""

    pass


class ConfigurationError(RailwayError):
    """Raised when configuration is invalid."""

    pass
