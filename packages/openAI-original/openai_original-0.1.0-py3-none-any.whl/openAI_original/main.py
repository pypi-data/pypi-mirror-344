from openai import OpenAI as aai

class OpenAI_Ori:
    """
    # --- USE ---
    conn = OpenAI_Ori()
    conn.connect_API("sk-proj-nNK...")
    res = conn.ask("Hi, what is you ?")
    print(res)
    """
    def __init__(self):
        self.client = None 

    def connect_API(self, api, model='gpt-4o-mini'):
        """API kalit bilan OpenAI clientga ulanadi"""
        self.client = aai(api_key=api)
        self.model = model

    def ask(self, question):
        if self.client is None:
            raise ValueError("Avval connect_API() orqali ulanishingiz kerak.")

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return completion.choices[0].message.content

