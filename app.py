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
        # 讀取資源庫
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
            u_need = st.selectbox("需求類型", df["category"].unique())
            u_pain = st.text_input("描述您的困難 (例如：低收、學費)", placeholder="請輸入關鍵字")
            
            if st.button("立即進行實質匹配", type="primary"):
                start_time = time.time()
                with st.spinner("後端正在檢索精準管道..."):
                    time.sleep(0.5) 
                    
                    # A. 取得該類別基礎資料
                    category_matches = df[df["category"] == u_need]
                    
                    # B. 關鍵字意圖自動擴展 (解決低收疑慮)
                    search_pattern = u_pain
                    if "低收" in u_pain:
                        search_pattern = "低收|低收入|弱勢|助學|救助"
                    
                    if search_pattern:
                        # 模糊比對
                        refined_matches = category_matches[
                            category_matches['name'].str.contains(search_pattern, na=False, regex=True) |
                            category_matches['description'].str.contains(search_pattern, na=False, regex=True) |
                            category_matches['target'].str.contains(search_pattern, na=False, regex=True)
                        ]
                    else:
                        refined_matches = category_matches
                    
                    # 存入 Session State 確保狀態持久化
                    st.session_state.results = refined_matches
                    st.session_state.is_precise = not refined_matches.empty
                    st.session_state.original_category = category_matches
                    st.session_state.exec_time = time.time() - start_time

    with col_out:
        # 使用 get() 避免 AttributeError
        if "results" in st.session_state:
            st.subheader("🎯 匹配結果")
            st.caption(f"⚡ 後端效能驗證：本次檢索耗時 {st.session_state.get('exec_time', 0):.4f} 秒")
            
            # 優化語句邏輯，消除找不到資料的疑慮
            if st.session_state.get("is_precise", False):
                st.success(f"✅ 已為您匹配到與「{u_pain}」相關的支援管道：")
                display_df = st.session_state.results
            else:
                st.info(f"💡 已為您提供「{u_need}」相關的支援管道如下：")
                display_df = st.session_state.get("original_category", pd.DataFrame())
            
            if not display_df.empty:
                for _, row in display_df.iterrows():
                    with st.expander(f"📌 {row['name']}", expanded=True):
                        st.write(f"**實質內容：** {row['description']}")
                        st.write(f"**適合對象：** {row['target']}")
                        
                        # 針對低收顯示特別標籤
                        if "低收" in str(row['target']) or "低收" in str(row['description']):
                            st.caption("🆘 此管道包含低收入戶專屬補助，建議備妥證明文件。")
                            
                        st.link_button(f"👉 立即前往官方網站", row["url"], type="primary")
                
                # 回饋存檔
                st.divider()
                st.subheader("📊 測試回饋與存檔")
                feedback_score = st.slider("此結果的解決力度評分 (1-10)：", 1, 10, 10)
                feedback_msg = st.text_area("給技術團隊的優化建議：")
                
                if st.button("提交回饋並儲存至後端"):
                    fb_df = pd.DataFrame([[u_need, feedback_score, feedback_msg]], columns=["類別", "評分", "建議"])
                    fb_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
                    st.success("回饋已安全存入後端系統。")
            else:
                st.warning("資料庫檢索中，請點擊左側按鈕開始。")
else:
    st.error("請確認 resources.csv 檔案已正確上傳。")

# --- 4. 管理員後端數據中心 ---
if admin_mode and is_authenticated:
    st.divider()
    st.header("📊 管理員後端數據中心")
    if os.path.exists("feedback.csv"):
        try:
            display_df = pd.read_csv("feedback.csv")
            st.dataframe(display_df.iloc[::-1], use_container_width=True) 
            csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 下載完整測試報告", data=csv_data, file_name="admin_report.csv")
        except:
            st.info("暫無紀錄。")
