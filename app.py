1 import streamlit as st
2 from openai import OpenAI
3 
4 st.title("AC Troubleshooter")
5 st.write("Ask me anything about your AC problem 👇")
6 
7 # Get key from Secrets
8 api_key = st.secrets["OPENAI_API_KEY"]
9 client = OpenAI(api_key=api_key)
10 
11 # Text box for user
12 user_input = st.text_input("Describe your AC issue:")
13 
14 if user_input:
15 with st.spinner("Thinking..."):
16 response = client.chat.completions.create(
17 model="gpt-3.5-turbo",
18 messages=[{"role": "user", "content": f"You are an AC repair expert. User says: {user_input}. Give diagnosis and fix steps in simple English."}]
19 )
20 answer = response.choices[0].message.content
21 st.write(answer)
