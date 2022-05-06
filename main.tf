provider "aws" {
  region = "us-west-2"
}

resource "aws_dynamodb_table" "clients" {
  name           = "clients"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}


