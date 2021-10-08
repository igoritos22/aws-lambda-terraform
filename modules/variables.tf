variable filename {
  type        = string
  description = "caminho do arquivo/codigo da função lambda"
}

variable function_name {
  type        = string
  description = "nome da função lambda"
}

variable handler {
  type        = string
  description = "handler da função lambda"
}

variable runtime {
  type        = string
  description = "engine/linguagem que a função lambda é escrita/roda"
}

variable timeout {
  type        = string
  description = "tempo maximo de execução da função lambda em segundos"
}

variable memory_size {
  type        = string
  description = "memoria alocada para execução da função lambda"
}

variable event_name {
  type        = string
  description = "Nome do cloudwatch event que servirá de gatilho para a função lambda"
}

variable event_description {
  type        = string
  description = "descrição do evento de trigger"
}

variable schedule_expression {
  type        = string
  default     = ""
  description = "Intervalo de execução da função lambda"
}

variable source_code_hash {
  type        = string
  description = "arquivo da função lambda compatada hasbase"
}



