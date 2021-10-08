module "lambda_exposed_alltraffic" {
  source              = "./modules"
  function_name       = "rm_ingress_rule_alltraffic_exposed"
  filename            = "lambda_function.zip"
  source_code_hash    = filebase64sha256("lambda_function.zip")
  handler             = "lambda_function.lambda_handler"
  runtime             = "python3.8"
  timeout             = 59
  memory_size         = 128
  event_name          = "a_cada_hora"
  event_description   = "Dispara a cada 1hr"
  schedule_expression = "rate(59 minutes)"
}