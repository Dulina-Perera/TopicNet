# %%
# Import the required libraries, modules, classes, and functions
import os

from openai import AsyncOpenAI

from .....core_ import is_valid_openai_model
from .....exceptions_ import InvalidOpenAIModelError

# %%
async def refine_topic_and_content_using_openai(
  topic: str,
  content: str,
  model: str = "gpt-4o"
) -> str:
  """
  Refines the given topic and content using OpenAI models.

	:param topic: The topic to refine
	:type topic: str

	:param content: The content to refine
	:type content: str

	:param model: The OpenAI model to use, defaults to "gpt-4o"
	:type model: str, optional
  """
  # Check if the specified OpenAI model is valid.
  if not await is_valid_openai_model(model):
    raise InvalidOpenAIModelError(model)

  # Initialize the OpenAI client.
  client: AsyncOpenAI = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  # Define the prompt.
  system_prompt: str = (
		f"You are a helpful assistant."
		f"You will be provided with an extractive summary of a document."
		f"Please generate a detailed and refined topic, and then enhance the summary to make it more concise and coherent."
		f"It is of utmost importance that you generate content in markdown format. But, don't use code blocks."
	)
  user_prompt: str = (
		f"{topic}\n\n"
		f"{content}"
	)

  # Generate the refined content.
  response: str = await client.chat.completions.create(
		model=model,
		messages=[
			{"role": "system", "content": system_prompt},
			{"role": "user", "content": user_prompt}
		],
		max_tokens=1000,
		temperature=0.3
	)

  # Return the refined content.
  return response.choices[0].message.content
