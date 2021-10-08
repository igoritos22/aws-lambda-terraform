resource "aws_lambda_function" "traffic_exposed" {
    filename = var.filename
    function_name = "${var.function_name}_${terraform.workspace}"
    source_code_hash = var.source_code_hash
    role = aws_iam_role.iam_for_lambda.arn
    handler = var.handler
    runtime = var.runtime
    timeout     = var.timeout
    memory_size = var.memory_size
}
resource "aws_cloudwatch_event_rule" "rate_minutes" {
    name = var.event_name
    description = var.event_description
    schedule_expression = var.schedule_expression
}
resource "aws_cloudwatch_event_target" "check_foo_every_five_minutes" {
    rule = aws_cloudwatch_event_rule.rate_minutes.name
    target_id = "lambda_check"
    arn = aws_lambda_function.traffic_exposed.arn
}
resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda_check" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.traffic_exposed.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.rate_minutes.arn
}