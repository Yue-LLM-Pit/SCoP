from openai import OpenAI
from tenacity import retry, stop_after_attempt
# LLM implimentions from inner sources have been removed due to regulation policy.

@retry(stop=stop_after_attempt(3))
def openai_chat_gen(input_prompt,
                    model_card = 'gpt-3.5-turbo',
                    temperature = 0.7, 
                    max_tokens = 1000):

    assert (type(input_prompt) == str
            ), "openai api does not support batch inference."
  
    client = OpenAI(api_key='YOUR_API_KEY')
    
    message=[{"role": "user", "content": input_prompt}]
    

    response = client.chat.completions.create(
        model= model_card,
        messages = message,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    return response.choices[0].message.content

    