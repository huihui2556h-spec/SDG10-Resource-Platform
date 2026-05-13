import streamlit as st
import pandas as pd
import time
import os

# 頁面基本配置
st.set_page_config(page_title="SDG 10 智慧資源分配平台", layout="wide")

# --- 1. 後端數據讀取邏輯 ---
@st.cache_data
def load_db():
    try:
        # 讀取同目錄下的 resources.csv
        return pd.read_csv("resources.csv")
    except Exception as e:
        return pd.DataFrame(columns=["category", "name", "target", "description", "url"])

df = load_db()

# --- 2. 側邊導覽 ---
with st.sidebar:
    st.title("SDG 10 智慧平台")
    st.info("目標：減少資源分配不均")
    st.divider()
    st.write("**核心團隊：**")
    # 確保名單包含：吳暐承、唐正軒、紀重仰、黃騵褘
    st.success("吳暐承、唐正軒\n紀重仰、黃騵褘")

# --- 3. 實質匹配與效能驗證頁面 ---
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
                    time.sleep(0.5) 
                    # 根據類別過濾 CSV 內容
                    matched_results = df[df["category"] == u_need]
                end_time = time.time()
                
                st.session_state.results = matched_results
                st.session_state.exec_time = end_time - start_time

    with col_out:
        if "results" in st.session_state:
            st.subheader("🎯 匹配到的解決方案")
            st.caption(f"⚡ 後端效能驗證：本次檢索耗時 {st.session_state.exec_time:.4f} 秒")
            
            if not st.session_state.results.empty:
                for _, row in st.session_state.results.iterrows():
                    with st.expander(f"📌 {row['name']}", expanded=True):
                        st.write(f"**實質內容：** {row['description']}")
                        st.write(f"**適合對象：** {row['target']}")
                        # 【實質跳轉核心】：確保點選前往申請時可以真的到官方網站
                        st.link_button(f"👉 立即前往官方網站", row["url"], type="primary")
                
                # --- 收集回饋並實質存檔 ---
                st.divider()
                st.subheader("📊 測試回饋與存檔")
                # 修改滿意分數為 1-10 分
                feedback_score = st.slider("此結果的解決力度評分 (1-10)：", 1, 10, 10)
                feedback_msg = st.text_area("給技術團隊的優化建議：")
                
                if st.button("提交回饋並儲存至後端"):
                    fb_df = pd.DataFrame([[u_need, feedback_score, feedback_msg]], columns=["類別", "評分", "建議"])
                    # 實質存入 feedback.csv
                    fb_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
                    st.success("回饋已存入 feedback.csv！下方的數據中心將同步更新。")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("目前數據庫中尚無匹配項。")
        else:
            st.info("請在左側選擇需求並點擊按鈕。")
else:
    st.error("請檢查 resources.csv 是否已正確上傳。")

# --- 4. 後端數據驗證中心 (證明存檔成功) ---
st.divider()
st.header("📊 後端數據驗證中心")
st.write("此區塊用於展示 `feedback.csv` 中的實時回傳資料。")

if os.path.exists("feedback.csv"):
    try:
        display_df = pd.read_csv("feedback.csv")
        st.dataframe(display_df.tail(10), use_container_width=True) # 顯示最後 10 筆
        
        # 提供下載按鈕給黃騵褘同學下載報告
        csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(label="📥 下載實質測試報告 (CSV)", data=csv_data, file_name="feedback_report.csv")
    except:
        st.write("暫時無法讀取回饋資料。")
else:
    st.info("等待第一筆回饋資料中...")
