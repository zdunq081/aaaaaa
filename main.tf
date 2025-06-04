terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=4.1.0"
    }
  }
}
provider "azurerm" {
  resource_provider_registrations = "none"
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "rg-AdrianZ"
    storage_account_name = "saadrianz"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

resource "azurerm_service_plan" "example" {
  name                = "aspAdrianZ"
  location            = "polandcentral"
  resource_group_name = "rg-AdrianZ"
  os_type             = "Linux"
  sku_name            = "P0v3"
}


resource "azurerm_linux_web_app" "example" {
  name                = "webappAdrianZ"
  location            = "polandcentral"
  resource_group_name = "rg-AdrianZ"
  service_plan_id     = azurerm_service_plan.example.id
  site_config {}
}