"""GraphQL queries for Railway API."""

# User queries
ME_QUERY = """
query Me {
    me {
        id
        name
        email
    }
}
"""

# Project queries
LIST_PROJECTS_QUERY = """
query ListProjects {
    me {
        projects {
            edges {
                node {
                    id
                    name
                    description
                    createdAt
                    updatedAt
                    environments {
                        edges {
                            node {
                                id
                                name
                            }
                        }
                    }
                    services {
                        edges {
                            node {
                                id
                                name
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

GET_PROJECT_QUERY = """
query GetProject($projectId: String!) {
    project(id: $projectId) {
        id
        name
        description
        createdAt
        updatedAt
        environments {
            edges {
                node {
                    id
                    name
                }
            }
        }
        services {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
}
"""

# Service queries
LIST_SERVICES_QUERY = """
query ListServices($projectId: String!) {
    project(id: $projectId) {
        services {
            edges {
                node {
                    id
                    name
                    icon
                    createdAt
                    updatedAt
                }
            }
        }
    }
}
"""

GET_SERVICE_QUERY = """
query GetService($serviceId: String!) {
    service(id: $serviceId) {
        id
        name
        icon
        createdAt
        updatedAt
        projectId
    }
}
"""

# Environment queries
LIST_ENVIRONMENTS_QUERY = """
query ListEnvironments($projectId: String!) {
    project(id: $projectId) {
        environments {
            edges {
                node {
                    id
                    name
                    createdAt
                    updatedAt
                }
            }
        }
    }
}
"""

# Deployment queries
LIST_DEPLOYMENTS_QUERY = """
query ListDeployments($serviceId: String!, $environmentId: String!, $first: Int) {
    deployments(
        input: {
            serviceId: $serviceId
            environmentId: $environmentId
        }
        first: $first
    ) {
        edges {
            node {
                id
                status
                createdAt
                updatedAt
                staticUrl
                meta
            }
        }
    }
}
"""

GET_DEPLOYMENT_QUERY = """
query GetDeployment($deploymentId: String!) {
    deployment(id: $deploymentId) {
        id
        status
        createdAt
        updatedAt
        staticUrl
        meta
    }
}
"""

# Variable queries
LIST_VARIABLES_QUERY = """
query ListVariables($projectId: String!, $environmentId: String!, $serviceId: String) {
    variables(
        projectId: $projectId
        environmentId: $environmentId
        serviceId: $serviceId
    )
}
"""

# Logs queries
GET_BUILD_LOGS_QUERY = """
query GetBuildLogs($deploymentId: String!, $limit: Int) {
    buildLogs(deploymentId: $deploymentId, limit: $limit) {
        message
        timestamp
        severity
    }
}
"""

GET_DEPLOYMENT_LOGS_QUERY = """
query GetDeploymentLogs($deploymentId: String!, $limit: Int) {
    deploymentLogs(deploymentId: $deploymentId, limit: $limit) {
        message
        timestamp
        severity
    }
}
"""

# Domain queries
LIST_DOMAINS_QUERY = """
query ListDomains($projectId: String!, $environmentId: String!, $serviceId: String!) {
    domains(
        projectId: $projectId
        environmentId: $environmentId
        serviceId: $serviceId
    ) {
        serviceDomains {
            id
            domain
            suffix
            createdAt
        }
        customDomains {
            id
            domain
            status {
                dnsRecords {
                    hostlabel
                    requiredValue
                    currentValue
                    status
                }
            }
            createdAt
        }
    }
}
"""

# Template queries
LIST_TEMPLATES_QUERY = """
query ListTemplates($first: Int) {
    templates(first: $first) {
        edges {
            node {
                id
                code
                name
                description
                category
                health
                activeProjects
            }
        }
    }
}
"""

GET_TEMPLATE_QUERY = """
query GetTemplate($code: String!) {
    template(code: $code) {
        id
        code
        name
        description
        category
        health
        activeProjects
        services {
            name
            icon
        }
    }
}
"""
