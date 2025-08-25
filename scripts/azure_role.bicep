@description('The name of the custom role for the AI Security Suite scanner.')
param roleName string = 'AI Security Suite Auditor'

@description('A description for the custom role.')
param roleDescription string = 'Provides read-only access to audit security configurations across various Azure resources.'

targetScope = 'subscription'

resource customRoleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: guid(subscription().id, roleName) // Creates a unique, deterministic GUID for the role definition
  properties: {
    roleName: roleName
    description: roleDescription
    type: 'CustomRole'
    permissions: [
      {
        actions: [
          // General Read Permissions
          '*/read',

          // Specific actions that might be needed for deeper inspection, beyond just read properties
          'Microsoft.Storage/storageAccounts/listKeys/action',
          'Microsoft.KeyVault/vaults/secrets/get/action'
          // Note: Granting list/get access to keys and secrets is powerful.
          // This should be applied with caution and only to trusted principals.
        ]
        notActions: [
          // Exclude write, delete, and other sensitive operations explicitly
          '*/write',
          '*/delete',
          '*/action'
        ]
        dataActions: [
            // Allow reading blob data for secret scanning
            'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read'
        ]
        notDataActions: [
            'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write',
            'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/delete'
        ]
      }
    ]
    assignableScopes: [
      subscription().id
    ]
  }
}

output roleDefinitionId string = customRoleDefinition.id
