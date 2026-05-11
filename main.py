import streamlit as st
from supabase import create_client

# 1. Supabaseへの接続設定
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("履歴が残るチャットボット 🤖")

# 2. 過去のメッセージを安全に取得
try:
    response = supabase.table("messages").select("*").order("created_at").execute()
    # 取得したデータが空でないか確認
    if response.data:
        for msg in response.data:
            # msgの中に"role"というキーがあるか確認して表示
            role = msg.get("role", "assistant")
            content = msg.get("content", "")
            with st.chat_message(role):
                st.write(content)
except Exception as e:
    st.error("データの読み込みに失敗しました。テーブル設定を確認してください。")

# 3. 新しい入力があった時の処理
if prompt := st.chat_input("メッセージを入力..."):
    st.chat_message("user").write(prompt)
    
    # Supabaseに保存
    try:
        supabase.table("messages").insert({"role": "user", "content": prompt}).execute()
        
        bot_msg = f"{prompt} についてですね。承知しました！"
        st.chat_message("assistant").write(bot_msg)
        
        # ボットの回答も保存
        supabase.table("messages").insert({"role": "assistant", "content": bot_msg}).execute()
    except Exception as e:
        st.error(f"保存に失敗しました: {e}")
