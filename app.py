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
    # 團隊名單換行顯示
    st.success("👤 吳暐承\n\n👤 唐正軒\n\n👤 紀重仰\n\n👤 黃騵褘")
    
    # 管理員入口
    st.divider()
    admin_mode = st.checkbox("開啟管理員模式")
    is_authenticated = False
    if admin_mode:
        pwd = st.text_input("輸入管理員密碼", type="password")
        if pwd == "1234": # 密碼設定為 1234
            is_authenticated = True
            st.toast("管理員認證成功！")
        else:
            if pwd: st.error("密碼錯誤")

# --- 3. 實質匹配頁面 ---
st.header("🤖 AI 實質資源匹配與效能驗證")

if not df.empty:
    col_in, col_out = st.columns([1, 1.2])
    
    with col_in:
        with st.container(border=True):
            st.subheader("📝 填寫需求")
            u_need = st.selectbox("您的需求類型", df["category"].unique())
            u_pain = st.text_input("描述您的困難 (例如：低收、學費)", placeholder="請輸入關鍵字")
            
            if st.button("立即進行實質匹配", type="primary"):
                start_time = time.time()
                with st.spinner("AI 正在分析最合適的管道..."):
                    time.sleep(0.5) 
                    
                    # A. 取得該類別資料
                    category_matches = df[df["category"] == u_need]
                    
                    # B. 關鍵字意圖擴展 (優化搜尋廣度)
                    search_pattern = u_pain if u_pain else "補助|支援"
                    if "低收" in u_pain:
                        search_pattern = "低收|低收入|弱勢|助學|救助"
                    
                    # C. 執行匹配
                    refined_matches = category_matches[
                        category_matches['name'].str.contains(search_pattern, na=False, regex=True) |
                        category_matches['description'].str.contains(search_pattern, na=False, regex=True) |
                        category_matches['target'].str.contains(search_pattern, na=False, regex=True)
                    ]
                    
                    # --- 【核心優化】：只取第一個最有幫助的結果 ---
                    if not refined_matches.empty:
                        # 優先取精準匹配的第一筆
                        st.session_state.best_match = refined_matches.iloc[0]
                        st.session_state.is_precise = True
                    elif not category_matches.empty:
                        # 若無關鍵字匹配，則取該類別第一筆作為推薦
                        st.session_state.best_match = category_matches.iloc[0]
                        st.session_state.is_precise = False
                    else:
                        st.session_state.best_match = None
                
                st.session_state.exec_time = time.time() - start_time

    with col_out:
        if "best_match" in st.session_state and st.session_state.best_match is not None:
            st.subheader("🎯 為您推薦最有幫助的解決方案")
            st.caption(f"⚡ 後端效能驗證：檢索耗時 {st.session_state.get('exec_time', 0):.4f} 秒")
            
            row = st.session_state.best_match
            
            # 優化後的語句邏輯
            if st.session_state.get("is_precise"):
                st.success(f"✅ 根據「{u_pain}」，AI 為您篩選出最合適的支援管道：")
            else:
                st.info(f"💡 為您提供「{u_need}」相關的主要支援管道：")
            
            # 只顯示一個最精確的推薦卡片
            with st.container(border=True):
                st.subheader(f"📌 {row['name']}")
                st.write(f"**實質內容：** {row['description']}")
                st.write(f"**適合對象：** {row['target']}")
                
                if "低收" in str(row['target']) or "低收" in str(row['description']):
                    st.caption("🆘 此管道包含低收入戶專屬補助，建議備妥證明文件。")
                    
                st.link_button(f"👉 立即前往官方網站申請", row["url"], type="primary")
            
            # 回饋與存檔邏輯
            st.divider()
            st.subheader("📊 測試回饋與存檔")
            feedback_score = st.slider("此單一方案對您的解決力度 (1-10)：", 1, 10, 10)
            feedback_msg = st.text_area("是否有其他更具體的幫助需求？")
            
            if st.button("提交回饋並儲存至後端"):
                fb_df = pd.DataFrame([[u_need, feedback_score, feedback_msg]], columns=["類別", "評分", "建議"])
                fb_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
                st.success("回饋已安全存入 feedback.csv。")
        elif "best_match" in st.session_state:
            st.warning("目前資料庫中尚無相關資料。")
