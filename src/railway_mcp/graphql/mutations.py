"""GraphQL mutations for Railway API."""

# Project mutations
CREATE_PROJECT_MUTATION = """
mutation CreateProject($name: String!, $description: String, $defaultEnvironmentName: String) {
    projectCreate(
        input: {
            name: $name
            description: $description
            defaultEnvironmentName: $defaultEnvironmentName
        }
    ) {
        id
        name
        description
        createdAt
        environments {
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

DELETE_PROJECT_MUTATION = """
mutation DeleteProject($projectId: String!) {
    projectDelete(id: $projectId)
}
"""

# Service mutations
CREATE_SERVICE_MUTATION = """
mutation CreateService($projectId: String!, $name: String!) {
    serviceCreate(
        input: {
            projectId: $projectId
            name: $name
        }
    ) {
        id
        name
        createdAt
    }
}
"""

DELETE_SERVICE_MUTATION = """
mutation DeleteService($serviceId: String!) {
    serviceDelete(id: $serviceId)
}
"""

# Environment mutations
CREATE_ENVIRONMENT_MUTATION = """
mutation CreateEnvironment($projectId: String!, $name: String!) {
    environmentCreate(
        input: {
            projectId: $projectId
            name: $name
        }
    ) {
        id
        name
        createdAt
    }
}
"""

DELETE_ENVIRONMENT_MUTATION = """
mutation DeleteEnvironment($environmentId: String!) {
    environmentDelete(id: $environmentId)
}
"""

# Deployment mutations
DEPLOY_SERVICE_MUTATION = """
mutation DeployService($serviceId: String!, $environmentId: String!) {
    serviceInstanceDeploy(
        serviceId: $serviceId
        environmentId: $environmentId
    )
}
"""

REDEPLOY_MUTATION = """
mutation Redeploy($deploymentId: String!) {
    deploymentRedeploy(id: $deploymentId) {
        id
        status
        createdAt
    }
}
"""

CANCEL_DEPLOYMENT_MUTATION = """
mutation CancelDeployment($deploymentId: String!) {
    deploymentCancel(id: $deploymentId)
}
"""

RESTART_DEPLOYMENT_MUTATION = """
mutation RestartDeployment($deploymentId: String!) {
    deploymentRestart(id: $deploymentId)
}
"""

# Variable mutations
SET_VARIABLES_MUTATION = """
mutation SetVariables($projectId: String!, $environmentId: String!, $serviceId: String, $variables: EnvironmentVariables!) {
    variableCollectionUpsert(
        input: {
            projectId: $projectId
            environmentId: $environmentId
            serviceId: $serviceId
            variables: $variables
        }
    )
}
"""

DELETE_VARIABLE_MUTATION = """
mutation DeleteVariable($projectId: String!, $environmentId: String!, $serviceId: String, $name: String!) {
    variableDelete(
        input: {
            projectId: $projectId
            environmentId: $environmentId
            serviceId: $serviceId
            name: $name
        }
    )
}
"""

# Domain mutations
CREATE_SERVICE_DOMAIN_MUTATION = """
mutation CreateServiceDomain($serviceId: String!, $environmentId: String!) {
    serviceDomainCreate(
        input: {
            serviceId: $serviceId
            environmentId: $environmentId
        }
    ) {
        id
        domain
        suffix
    }
}
"""

DELETE_SERVICE_DOMAIN_MUTATION = """
mutation DeleteServiceDomain($id: String!) {
    serviceDomainDelete(id: $id)
}
"""

CREATE_CUSTOM_DOMAIN_MUTATION = """
mutation CreateCustomDomain($serviceId: String!, $environmentId: String!, $domain: String!) {
    customDomainCreate(
        input: {
            serviceId: $serviceId
            environmentId: $environmentId
            domain: $domain
        }
    ) {
        id
        domain
    }
}
"""

# Template mutations
DEPLOY_TEMPLATE_MUTATION = """
mutation DeployTemplate($projectId: String!, $environmentId: String!, $templateCode: String!, $services: [TemplateServiceInput!]) {
    templateDeploy(
        input: {
            projectId: $projectId
            environmentId: $environmentId
            templateCode: $templateCode
            services: $services
        }
    ) {
        projectId
        workflowId
    }
}
"""
