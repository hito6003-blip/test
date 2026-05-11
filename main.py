import streamlit as st
from supabase import create_client

# 1. Supabaseへの接続設定
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("履歴が残るチャットボット 🤖")

# 2. 過去のメッセージをSupabaseから取得して表示
response = supabase.table("messages").select("*").order("created_at").execute()
for msg in response.data:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 3. 新しい入力があった時の処理
if prompt := st.chat_input("メッセージを入力..."):
    # ユーザーの入力を表示
    st.chat_message("user").write(prompt)
    
    # データをSupabaseに保存
    supabase.table("messages").insert({"role": "user", "content": prompt}).execute()
    
    # ボットの回答（仮）
    bot_msg = f"{prompt} についてですね。承知しました！"
    st.chat_message("assistant").write(bot_msg)
    
    # ボットの回答も保存
    supabase.table("messages").insert({"role": "assistant", "content": bot_msg}).execute()
