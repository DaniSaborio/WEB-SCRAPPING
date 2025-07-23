import os
from openai import AzureOpenAI
endpoint = "https://voiceflip-openai.openai.azure.com/"
model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"
subscription_key = "<your-api-key>"
api_version = "2024-12-01-preview"
client = AzureOpenAI(
api_version=api_version,
azure_endpoint=endpoint,
api_key=subscription_key,
)