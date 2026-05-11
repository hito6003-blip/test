import streamlit as st

st.title("社内用テストボット 🤖")

name = st.text_input("あなたの名前を教えてください")

if name:
    st.write(f"こんにちは、{name}さん！今日も仕事頑張りましょう！")
