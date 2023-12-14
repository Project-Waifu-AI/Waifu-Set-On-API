from configs import config
from openai import OpenAI

client = OpenAI(api_key=config.api_key_openai)

response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
  n=1,
)

print(response.data[0].url)
