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
        # 讀取 resources.csv 資料庫
        return pd.read_csv("resources.csv")
    except Exception:
        return pd.DataFrame(columns=["category", "name", "target", "description", "url"])

df = load_db()

# --- 2. 側邊導覽 ---
with st.sidebar:
    st.title("SDG 10 智慧平台")
    st.info("目標：減少資源分配不均")
    st.divider()
    st.write("**核心團隊：**")
    # 名單校正：吳暐承、唐正軒、紀重仰、黃騵褘
    st.success("吳暐承、唐正軒\n紀重仰、黃騵褘")
    
    # --- 管理員入口 (隱藏功能) ---
    st.divider()
    admin_mode = st.checkbox("開啟管理員模式")
    is_authenticated = False
    if admin_mode:
        pwd = st.text_input("輸入管理員密碼", type="1234")
        if pwd == "sdg10admin": 
            is_authenticated = True
        else:
            if pwd:
                st.error("密碼錯誤")

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
                start_time = time.time()
                with st.spinner("後端正在檢索數據庫..."):
                    time.sleep(0.5) 
                    matched_results = df[df["category"] == u_need]
                end_time = time.time()
                
                st.session_state.results = matched_results
                st.session_state.exec_time = end_time - start_time

    with col_out:
        if "results" in st.session_state:
            st.subheader("🎯 匹配到的解決方案")
            st.caption(f"⚡ 後端效能驗證：{st.session_state.exec_time:.4f} 秒")
            
            if not st.session_state.results.empty:
                for _, row in st.session_state.results.iterrows():
                    with st.expander(f"📌 {row['name']}", expanded=True):
                        st.write(f"**實質內容：** {row['description']}")
                        # 【實質跳轉核心】：確保點選前往申請時可以真的到官方網站
                        st.link_button(f"👉 立即前往官方網站", row["url"], type="primary")
                
                # --- 收集回饋並實質存檔 ---
                st.divider()
                st.subheader("📊 測試回饋與存檔")
                # 滿意分數 1-10 分
                feedback_score = st.slider("此結果的解決力度評分 (1-10)：", 1, 10, 10)
                feedback_msg = st.text_area("給技術團隊的優化建議：")
                
                if st.button("提交回饋並儲存至後端"):
                    fb_df = pd.DataFrame([[u_need, feedback_score, feedback_msg]], columns=["類別", "評分", "建議"])
                    # 資料存入 feedback.csv
                    fb_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
                    st.success("回饋已安全存入後端系統。")
            else:
                st.warning("目前數據庫中尚無匹配項。")
else:
    st.error("請確認 resources.csv 是否已正確上傳至 GitHub")

# --- 4. 隱藏的數據驗證中心 (只有管理員看得到) ---
if admin_mode and is_authenticated:
    st.divider()
    st.header("📊 管理員後端數據中心")
    if os.path.exists("feedback.csv"):
        try:
            display_df = pd.read_csv("feedback.csv")
            st.write("這是目前儲存在後端的完整紀錄（一般使用者看不到此區塊）：")
            st.dataframe(display_df, use_container_width=True)
            
            csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 下載完整測試報告", data=csv_data, file_name="admin_report.csv")
        except:
            st.info("後端暫無可讀取的紀錄。")
    else:
        st.info("目前後端尚無紀錄。")
