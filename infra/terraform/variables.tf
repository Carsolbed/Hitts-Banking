variable "env" {
  type = string
  validation {
    condition     = contains(["dev", "stg", "prod"], var.env)
    error_message = "env debe ser dev, stg o prod."
  }
}

variable "location" {
  type    = string
  default = "eastus2"
}

variable "tenant_id" {
  type = string
}

variable "publisher_email" {
  type = string
}

variable "enable_streaming" {
  type    = bool
  default = false
}

variable "eventhub_throughput_units" {
  type    = number
  default = 1
}

variable "enable_apim" {
  type    = bool
  default = false
}

variable "apim_sku" {
  type    = string
  default = "Developer_1"
}
