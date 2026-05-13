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
    st.success("👤 吳暐承\n\n👤 唐正軒\n\n👤 紀重仰\n\n👤 黃騵褘")
    
    # --- 管理員入口 ---
    st.divider()
    admin_mode = st.checkbox("開啟管理員模式")
    is_authenticated = False
    if admin_mode:
        pwd = st.text_input("輸入管理員密碼", type="password")
        if pwd == "1234": 
            is_authenticated = True
            st.toast("管理員認證成功！")
        else:
            if pwd:
                st.error("密碼錯誤，請重新輸入")

# --- 3. 實質匹配頁面 ---
st.header("🤖 AI 實質資源匹配與效能驗證")

if not df.empty:
    col_in, col_out = st.columns([1, 1.2])
    
    with col_in:
        with st.container(border=True):
            st.subheader("📝 填寫需求")
            u_need = st.selectbox("需求類型", df["category"].unique())
            u_pain = st.text_input("描述您的困難 (關鍵字搜尋)", placeholder="例如：新住民、學費、身障")
            
            if st.button("立即進行實質匹配", type="primary"):
                start_time = time.time()
                with st.spinner("後端正在進行多重關鍵字檢索..."):
                    time.sleep(0.5) 
                    # --- 優化後的精準匹配邏輯 ---
                    category_matches = df[df["category"] == u_need]
                    if u_pain:
                        # 同時搜尋名稱與描述中的關鍵字
                        refined_matches = category_matches[
                            category_matches['description'].str.contains(u_pain, na=False) | 
                            category_matches['name'].str.contains(u_pain, na=False)
                        ]
                    else:
                        refined_matches = category_matches
                    
                    # 若精準搜尋無果，則回歸顯示該類別一般資源
                    if refined_matches.empty:
                        st.session_state.results = category_matches
                        st.session_state.search_status = "general"
                    else:
                        st.session_state.results = refined_matches
                        st.session_state.search_status = "precise"
                        
                end_time = time.time()
                st.session_state.exec_time = end_time - start_time

    with col_out:
        if "results" in st.session_state:
            st.subheader("🎯 匹配到的解決方案")
            st.caption(f"⚡ 後端效能驗證：本次檢索耗時 {st.session_state.exec_time:.4f} 秒")
            
            if st.session_state.get("search_status") == "general" and u_pain:
                st.info(f"💡 找不到與「{u_pain}」直接相關的特定管道，為您推薦「{u_need}」的一般性資源：")
            
            if not st.session_state.results.empty:
                for _, row in st.session_state.results.iterrows():
                    with st.expander(f"📌 {row['name']}", expanded=True):
                        st.write(f"**實質內容：** {row['description']}")
                        st.write(f"**適合對象：** {row['target']}")
                        
                        # --- 根據類型提供額外協助管道標籤 ---
                        if row['category'] == "醫療協助":
                            st.caption("🆘 緊急醫療諮詢：請撥打 119 或 1922 (防疫專線)")
                        elif row['category'] == "法律支援":
                            st.caption("🆘 法律扶助專線：(02)412-8518 (市話請直撥)")
                        elif row['category'] == "生活補助":
                            st.caption("🆘 社會福利諮詢專線：1957 (免付費專線)")
                        
                        st.link_button(f"👉 立即前往官方網站", row["url"], type="primary")
                
                # --- 收集回饋並實質存檔 ---
                st.divider()
                st.subheader("📊 測試回饋與存檔")
                feedback_score = st.slider("此結果的解決力度評分 (1-10)：", 1, 10, 10)
                feedback_msg = st.text_area("給技術團隊的優化建議：")
                
                if st.button("提交回饋並儲存至後端"):
                    fb_df = pd.DataFrame([[u_need, feedback_score, feedback_msg]], columns=["類別", "評分", "建議"])
                    fb_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
                    st.success("回饋已安全存入後端系統。")
            else:
                st.warning("目前數據庫中尚無匹配項。")
else:
    st.error("請確認 resources.csv 檔案正確。")

# --- 4. 管理員後端數據中心 ---
if admin_mode and is_authenticated:
    st.divider()
    st.header("📊 管理員後端數據中心")
    if os.path.exists("feedback.csv"):
        try:
            display_df = pd.read_csv("feedback.csv")
            st.write("這是目前儲存在後端的完整紀錄（一般使用者看不到）：")
            st.dataframe(display_df.iloc[::-1], use_container_width=True) 
            
            csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 下載完整測試報告", data=csv_data, file_name="admin_report.csv")
        except:
            st.info("後端暫無可讀取的紀錄。")
    else:
        st.info("目前後端尚未產生任何回饋紀錄。")
