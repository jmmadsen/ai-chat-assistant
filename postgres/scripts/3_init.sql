CREATE TABLE chatgpt_logs (
  prompt text,
  response text,
  inbound timestamp,
  outbound timestamp,
  error boolean,
  generated_sql text,
  total_tokens decimal,
  total_cost decimal
);