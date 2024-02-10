from openai import OpenAI

class OpenAiClient:

    def __init__(self) -> None:
        self.client = OpenAI()
        self.SYSTEM_PROMPT = """You are a helpful assistant."""
        
    def ask(self, question) -> str:
        completions =  self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ]
        )
        
        return completions.choices[0].message.content