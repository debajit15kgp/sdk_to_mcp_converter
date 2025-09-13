# Azure SDK Functions Coverage

## 🔍 **Azure SDK to MCP Converter - Function Coverage**

Your SDK to MCP converter now supports comprehensive Azure SDK functionality. Here's what types of functions will be automatically discovered and converted to MCP tools:

## 📊 **Azure Resource Management SDK (`azure.mgmt.resource`)**

### **Resource Groups**
- `create_or_update_resource_group` - Create or update resource groups
- `delete_resource_group` - Delete resource groups
- `get_resource_group` - Get resource group details
- `list_resource_groups` - List all resource groups
- `check_existence` - Check if resource group exists
- `update_resource_group` - Update resource group properties

### **Resources**
- `create_or_update_by_id` - Create or update resources by ID
- `delete_by_id` - Delete resources by ID
- `get_by_id` - Get resource details by ID
- `list_by_resource_group` - List resources in a resource group
- `move_resources` - Move resources between resource groups
- `validate_move_resources` - Validate resource moves

### **Tags**
- `tags_operations.create_or_update` - Create or update tags
- `tags_operations.delete` - Delete tags
- `tags_operations.get` - Get tag details
- `tags_operations.list` - List all tags
- `tags_operations.update` - Update tag properties

### **Locks**
- `management_locks.create_or_update_at_resource_group_level` - Create resource locks
- `management_locks.delete_at_resource_group_level` - Delete resource locks
- `management_locks.get_at_resource_group_level` - Get lock details
- `management_locks.list_at_resource_group_level` - List locks

## 🔐 **Azure Identity SDK (`azure.identity`)**

### **Authentication Methods**
- `DefaultAzureCredential` - Default authentication chain
- `ClientSecretCredential` - Service principal authentication
- `ManagedIdentityCredential` - Managed identity authentication
- `AzureCliCredential` - Azure CLI authentication
- `EnvironmentCredential` - Environment variable authentication
- `InteractiveBrowserCredential` - Interactive browser authentication
- `DeviceCodeCredential` - Device code authentication

### **Token Management**
- `get_token` - Get access tokens
- `close` - Close credential sessions
- `__enter__` and `__exit__` - Context manager support

## 🖥️ **Azure Compute SDK (`azure.mgmt.compute`)**

### **Virtual Machines**
- `virtual_machines.create_or_update` - Create or update VMs
- `virtual_machines.delete` - Delete VMs
- `virtual_machines.get` - Get VM details
- `virtual_machines.list` - List VMs
- `virtual_machines.start` - Start VMs
- `virtual_machines.stop` - Stop VMs
- `virtual_machines.restart` - Restart VMs
- `virtual_machines.deallocate` - Deallocate VMs

### **Virtual Machine Scale Sets**
- `virtual_machine_scale_sets.create_or_update` - Create or update scale sets
- `virtual_machine_scale_sets.delete` - Delete scale sets
- `virtual_machine_scale_sets.get` - Get scale set details
- `virtual_machine_scale_sets.list` - List scale sets
- `virtual_machine_scale_sets.update` - Update scale sets

### **Disks**
- `disks.create_or_update` - Create or update disks
- `disks.delete` - Delete disks
- `disks.get` - Get disk details
- `disks.list` - List disks
- `disks.grant_access` - Grant disk access
- `disks.revoke_access` - Revoke disk access

## 💾 **Azure Storage SDK (`azure.mgmt.storage`)**

### **Storage Accounts**
- `storage_accounts.create` - Create storage accounts
- `storage_accounts.delete` - Delete storage accounts
- `storage_accounts.get_properties` - Get storage account properties
- `storage_accounts.list` - List storage accounts
- `storage_accounts.update` - Update storage accounts
- `storage_accounts.regenerate_key` - Regenerate access keys

### **Blob Services**
- `blob_services.set_service_properties` - Set blob service properties
- `blob_services.get_service_properties` - Get blob service properties
- `blob_services.list` - List blob services

## 🌐 **Azure Network SDK (`azure.mgmt.network`)**

### **Virtual Networks**
- `virtual_networks.create_or_update` - Create or update VNets
- `virtual_networks.delete` - Delete VNets
- `virtual_networks.get` - Get VNet details
- `virtual_networks.list` - List VNets
- `virtual_networks.list_all` - List all VNets

### **Subnets**
- `subnets.create_or_update` - Create or update subnets
- `subnets.delete` - Delete subnets
- `subnets.get` - Get subnet details
- `subnets.list` - List subnets

### **Network Security Groups**
- `network_security_groups.create_or_update` - Create or update NSGs
- `network_security_groups.delete` - Delete NSGs
- `network_security_groups.get` - Get NSG details
- `network_security_groups.list` - List NSGs

### **Load Balancers**
- `load_balancers.create_or_update` - Create or update load balancers
- `load_balancers.delete` - Delete load balancers
- `load_balancers.get` - Get load balancer details
- `load_balancers.list` - List load balancers

## 🗄️ **Azure Database SDK (`azure.mgmt.sql`)**

### **SQL Servers**
- `servers.create_or_update` - Create or update SQL servers
- `servers.delete` - Delete SQL servers
- `servers.get` - Get SQL server details
- `servers.list` - List SQL servers
- `servers.list_by_resource_group` - List servers in resource group

### **SQL Databases**
- `databases.create_or_update` - Create or update databases
- `databases.delete` - Delete databases
- `databases.get` - Get database details
- `databases.list_by_server` - List databases on server
- `databases.pause` - Pause databases
- `databases.resume` - Resume databases

## 🔧 **Usage Examples**

### **Convert Azure Resource Management SDK**
```bash
sdk-to-mcp azure azure.mgmt.resource --output-dir ./azure-resource-mcp-server
```

### **Convert Azure Identity SDK**
```bash
sdk-to-mcp azure azure.identity --output-dir ./azure-identity-mcp-server
```

### **Convert Azure Compute SDK**
```bash
sdk-to-mcp azure azure.mgmt.compute --output-dir ./azure-compute-mcp-server
```

### **Convert Azure Storage SDK**
```bash
sdk-to-mcp azure azure.mgmt.storage --output-dir ./azure-storage-mcp-server
```

### **Convert Azure Network SDK**
```bash
sdk-to-mcp azure azure.mgmt.network --output-dir ./azure-network-mcp-server
```

## 🔐 **Authentication Configuration**

Set these environment variables for Azure authentication:

```bash
# Service Principal Authentication
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_RESOURCE_GROUP="your-resource-group"
```

## 📊 **Expected Results**

Based on the Azure SDK structure, you can expect:

- **Azure Resource Management**: ~100-200 tools
- **Azure Identity**: ~20-30 tools  
- **Azure Compute**: ~300-500 tools
- **Azure Storage**: ~150-250 tools
- **Azure Network**: ~400-600 tools

**Total Azure SDK Coverage**: 1,000+ tools across all Azure services!

## 🚀 **Benefits**

1. **Complete Azure Coverage**: Access to all Azure management operations
2. **Production Ready**: Proper authentication and error handling
3. **AI Assistant Integration**: Natural language access to Azure resources
4. **Automated Discovery**: No manual tool creation required
5. **Scalable**: Works with any Azure SDK module

Your converter now provides comprehensive Azure cloud management capabilities through the Model Context Protocol!
