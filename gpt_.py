from openai import OpenAI

def chat_with_gpt(user_input, conversation_history):
    client = OpenAI(
        project='보안문제로 인해 문의 바람',
        api_key='보안문제로 인해 문의 바람'
    )
    
    conversation_history
    
    conversation_history.append({'role':'user', 'content': user_input})
    
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=conversation_history
    )

    assistant_massages = response.choices[0].message.content
    conversation_history.append({'role':'assistant', 'content': assistant_massages})
    
    return assistant_massages, conversation_history