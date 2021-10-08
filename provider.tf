provider "aws" {
  region  = var.region
  profile = lookup(var.profile_account, terraform.workspace)
}

provider "aws" {
  alias   = "poc"
  region  = var.region
  profile = "poc"
}

terraform {
  backend "s3" {
    bucket = "terraform-seginfo-seg"
    key    = "lambda/lambdaf_exposedalltraffic.tfstate"
    region = "sa-east-1"
  }
}