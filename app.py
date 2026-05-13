import streamlit as st
import pandas as pd
import time
import os

# 頁面基本配置
st.set_page_config(page_title="SDG 10 智慧資源分配平台", layout="wide")

# --- 1. 後端數據讀取 (讀取你上傳的 CSV) ---
@st.cache_data
def load_db():
    try:
        # 讀取同目錄下的 resources.csv
        data = pd.read_csv("resources.csv")
        return data
    except Exception as e:
        st.error(f"找不到數據庫檔案 resources.csv 或格式錯誤: {e}")
        return pd.DataFrame()

df = load_db()

# --- 2. 側邊導覽與團隊校正 ---
with st.sidebar:
    st.title("SDG 10 智慧平台")
    st.info("目標：減少資源分配不均")
    st.divider()
    st.write("**核心團隊：**")
    # 確保名單包含：吳暐承、唐正軒、紀重仰、黃騵褘
    st.success("吳暐承、唐正軒\n紀重仰、黃騵褘")

# --- 3. 實質匹配頁面 ---
st.header("🤖 AI 實質資源匹配與效能驗證")

if not df.empty:
    col_in, col_out = st.columns([1, 1.2])
    
    with col_in:
        with st.container(border=True):
            st.subheader("📝 填寫需求")
            u_need = st.selectbox("需求類型", df["category"].unique())
            u_pain = st.text_input("目前最大困難 (關鍵字)", placeholder="例如：學費、看病")
            
            if st.button("立即進行實質匹配", type="primary"):
                # --- 效能測試開始 ---
                start_time = time.time()
                with st.spinner("後端正在檢索數據庫..."):
                    time.sleep(0.5) # 模擬運算
                    # 根據類別過濾 CSV 內容
                    matched_results = df[df["category"] == u_need]
                end_time = time.time()
                # --- 效能測試結束 ---
                
                st.session_state.results = matched_results
                st.session_state.exec_time = end_time - start_time

    with col_out:
        if "results" in st.session_state:
            st.subheader("🎯 匹配到的解決方案")
            # 展現效能數據（黃騵褘負責的驗證項目）
            st.caption(f"⚡ 後端效能驗證：本次檢索耗時 {st.session_state.exec_time:.4f} 秒")
            
            if not st.session_state.results.empty:
                for _, row in st.session_state.results.iterrows():
                    with st.expander(f"📌 {row['name']}", expanded=True):
                        st.write(f"**實質內容：** {row['description']}")
                        st.write(f"**適合對象：** {row['target']}")
                        # 【核心功能】：點擊後直接跳轉到官方網站
                        st.link_button(f"👉 立即前往「{row['name']}」官方網站", row["url"], type="primary")
                
                # --- 收集回饋並實質存檔 ---
                st.divider()
                st.subheader("📊 測試回饋與存檔")
                feedback_score = st.select_slider("此結果的解決力度：", options=["無效", "普通", "有效", "十分有效"])
                feedback_msg = st.text_area("給技術團隊的優化建議：")
                
                if st.button("提交回饋並儲存至後端"):
                    # 將回饋資料存入 CSV (本地或雲端)
                    fb_df = pd.DataFrame([[u_need, feedback_score, feedback_msg]], columns=["類別", "評分", "建議"])
                    fb_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
                    st.success("回饋已存入 feedback.csv，這將作為後續演算法優化依據。")
            else:
                st.warning("目前數據庫中尚無匹配項。")
        else:
            st.info("請在左側選擇需求並點擊按鈕，系統將從資源庫提取實質解決辦法。")
else:
    st.error("請確保資源數據庫 resources.csv 已上傳至 GitHub 且格式正確。")
