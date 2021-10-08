variable "region" {
  type        = string
  description = "regiao onde serao provisionados os recursos"
  default     = "sa-east-1"
}
variable "profile_account" {
  type = map(any)
  default = {
    prod = "prod"
    qa   = "qa"
    dev  = "dev"
    poc  = "poc"
  }
}