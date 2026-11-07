# Infraestructura base por entorno. Se aplica con: terraform apply -var-file=envs/<env>.tfvars
terraform {
  required_providers {
    azurerm    = { source = "hashicorp/azurerm", version = "~> 4.0" }
    databricks = { source = "databricks/databricks", version = "~> 1.50" }
  }
  backend "azurerm" {}   # estado remoto en Storage Account con bloqueo
}

provider "azurerm" {
  features {}
}

locals {
  prefix = "riskfraud-${var.env}"
  tags   = { proyecto = "riskfraud", entorno = var.env, dueno = "gerencia-analitica" }
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${local.prefix}"
  location = var.location
  tags     = local.tags
}

resource "azurerm_storage_account" "lake" {
  name                     = replace("st${local.prefix}lake", "-", "")
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = var.env == "prod" ? "ZRS" : "LRS"
  is_hns_enabled           = true   # ADLS Gen2
  public_network_access_enabled = false
  tags                     = local.tags
}

resource "azurerm_key_vault" "kv" {
  name                = "kv-${local.prefix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  tenant_id           = var.tenant_id
  sku_name            = "standard"
  purge_protection_enabled = true
  tags                = local.tags
}

resource "azurerm_databricks_workspace" "dbw" {
  name                = "dbw-${local.prefix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  sku                 = "premium"   # requerido para Unity Catalog
  public_network_access_enabled = false
  tags                = local.tags
}

resource "azurerm_eventhub_namespace" "eh" {
  count               = var.enable_streaming ? 1 : 0
  name                = "evh-${local.prefix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  sku                 = "Standard"
  capacity            = var.eventhub_throughput_units
  tags                = local.tags
}

resource "azurerm_api_management" "apim" {
  count               = var.enable_apim ? 1 : 0
  name                = "apim-${local.prefix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  publisher_name      = "Gerencia Analitica"
  publisher_email     = var.publisher_email
  sku_name            = var.apim_sku
  tags                = local.tags
}
