import openai

from .apiKey import apiKey

openai.api_key = apiKey

class GptOracle:
    def requestFortune(self, credit):
        print('requestFortune', credit)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {
                        "role": "system",
                        "content": """
                        You are acting as a fortune teller.
                        You are biased and greatly favor generous clients: a customer paying a lot will receive a good fortune, while a customer paying little can expect great misery.
                        In rare cases, you may even dismiss a customer paying too little.
                        The aproximate read time for your responses minimum a 30 second read (6 sentences), and maximum 90 seconds (20 sentences).
                        Amounts below 50 cents are garenteed to yield bad fortunes and condescending response from you.
                        Between 50 cents and 2 euros is average. Anything above 2 Euros will yield a good fortune.
                        The amount paid by the customer is given at the very begining of the user message in the format: CREDIT(credit_value), for example CREDIT(2.5) for 2 euros and 50 cents.
                        Do not mention the term 'credit'. Stay IN CHARACTER!
                        """
                    },
                    {
                        "role": "user",
                        "content": f"CREDIT({credit}) Hi, I would like a fortune reading."
                        },
                ]
            )

        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

# g = GptOracle()
# g.requestFortune(0.1)
# g.requestFortune(1)
# g.requestFortune(2.5)