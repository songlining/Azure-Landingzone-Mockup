terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.28.0"
    }
  }
  cloud {
    organization = "larryslab"
    workspaces {
      name = "WORKSPACE_NAME"
    }
  }
}

variable "rg_name" {
  type = string
  default = "lsong"
}

variable "project_id" {
  type = string
  default = ""
}

variable "costcenter_id" {
  type = string
  default = ""
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

#Create Resource Group
resource "azurerm_resource_group" "terraform_test" {
  name     = var.rg_name
  location = "eastus2"
  tags = {
    project_id = var.project_id,
    costcenter_id = var.costcenter_id
  }
}
