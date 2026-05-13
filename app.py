import streamlit as st
import pandas as pd
import time
import os

# --- 讀取資源數據庫 ---
def load_data():
    return pd.read_csv("resources.csv")

df = load_data()

# --- 實質匹配邏輯 ---
st.title("SDG 10 實質資源匹配平台")

# 使用者輸入
u_need = st.selectbox("需求類型", df["category"].unique())
u_pain = st.text_input("描述困難")

if st.button("開始匹配並產生解決辦法"):
    start_time = time.time()
    # 這裡就是「回傳資料」的過濾過程
    results = df[df["category"] == u_need] 
    exec_time = time.time() - start_time
    
    st.write(f"⚡ 後端效能：{exec_time:.4f} 秒")
    
    # 顯示實質解決辦法 [cite: 69]
    for _, row in results.iterrows():
        st.success(f"建議方案：{row['name']}")
        st.write(f"實質內容：{row['description']}")
        st.link_button("點我立即申請", row["url"])

# --- 解決「回饋資料存哪裡」的問題 ---
st.divider()
st.subheader("📝 測試與驗證回饋")
f_score = st.radio("結果是否有用？", ["十分有效", "普通", "無效"])
f_text = st.text_area("建議：")

if st.button("提交並儲存回饋"):
    # 這裡將資料實質存入 GitHub 上的 feedback.csv
    feedback_data = pd.DataFrame([[u_need, f_score, f_text]], columns=["類別", "評分", "建議"])
    
    # 如果檔案不存在就建立，存在就續寫 (Append)
    file_exists = os.path.isfile("feedback.csv")
    feedback_data.to_csv("feedback.csv", mode='a', index=False, header=not file_exists)
    
    st.info("資料已儲存至後端 feedback.csv 檔案中，供團隊分析。")
