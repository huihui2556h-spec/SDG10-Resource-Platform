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

# --- 2. 側邊欄與分頁導覽 ---
with st.sidebar:
    st.title("SDG 10 智慧平台")
    st.info("目標：減少資源分配不均")
    st.divider()
    
    page = st.radio("功能選單", ["🤖 AI 實質資源匹配", "📊 管理員數據中心"])
    
    st.divider()
    st.write("**核心團隊：**")
    # 名單分行顯示
    st.success("👤 吳暐承\n\n👤 唐正軒\n\n👤 紀重仰\n\n👤 黃騵褘")

# --- 3. 頁面 A：AI 實質資源匹配 ---
if page == "🤖 AI 實質資源匹配":
    st.header("🤖 AI 實質資源匹配與效能驗證")

    if not df.empty:
        col_in, col_out = st.columns([1, 1.2])
        
        with col_in:
            with st.container(border=True):
                st.subheader("📝 填寫需求")
                u_need = st.selectbox("1. 選擇您的需求類型", df["category"].unique())
                
                # --- 【新增】：困難點選項與手動輸入結合 ---
                pain_options = ["低收入戶", "學費負擔", "身心障礙", "偏鄉交通", "法律諮詢", "找工作", "租屋補貼", "緊急救助"]
                u_pains = st.multiselect("2. 勾選您的具體困難 (可多選)", pain_options)
                u_custom = st.text_input("3. 其他補充描述 (選填)", placeholder="例如：新住民身分")
                
                if st.button("立即進行實質匹配", type="primary"):
                    start_time = time.time()
                    with st.spinner("AI 正在分析最合適的管道..."):
                        time.sleep(0.5) 
                        
                        category_matches = df[df["category"] == u_need]
                        
                        # 整合勾選與手動輸入的關鍵字
                        combined_pains = "|".join(u_pains) if u_pains else ""
                        if u_custom:
                            combined_pains = f"{combined_pains}|{u_custom}" if combined_pains else u_custom
                        
                        # 關鍵字意圖自動擴展 (解決低收等用語差異)
                        search_pattern = combined_pains if combined_pains else "補助|支援"
                        if "低收" in search_pattern:
                            search_pattern = f"{search_pattern}|低收入|弱勢|助學|救助"
                        
                        # 執行匹配
                        refined_matches = category_matches[
                            category_matches['name'].str.contains(search_pattern, na=False, regex=True) |
                            category_matches['description'].str.contains(search_pattern, na=False, regex=True) |
                            category_matches['target'].str.contains(search_pattern, na=False, regex=True)
                        ]
                        
                        # 只取第一筆最有幫助的
                        if not refined_matches.empty:
                            st.session_state.best_match = refined_matches.iloc[0]
                            st.session_state.is_precise = True
                        elif not category_matches.empty:
                            st.session_state.best_match = category_matches.iloc[0]
                            st.session_state.is_precise = False
                        else:
                            st.session_state.best_match = None
                    
                    st.session_state.exec_time = time.time() - start_time

        with col_out:
            if "best_match" in st.session_state and st.session_state.best_match is not None:
                st.subheader("🎯 為您推薦最有幫助的解決方案")
                st.caption(f"⚡ 後端效能驗證：本次檢索耗時 {st.session_state.get('exec_time', 0):.4f} 秒")
                
                row = st.session_state.best_match
                
                if st.session_state.get("is_precise"):
                    st.success(f"✅ 根據您的具體情況，AI 推薦以下最合適的支援管道：")
                else:
                    st.info(f"💡 根據「{u_need}」類別，為您推薦主要的支援管道：")
                
                with st.container(border=True):
                    st.subheader(f"📌 {row['name']}")
                    st.write(f"**實質內容：** {row['description']}")
                    st.write(f"**適合對象：** {row['target']}")
                    
                    if "低收" in str(row['target']) or "低收" in str(row['description']):
                        st.caption("🆘 此管道包含低收入戶專屬補助，建議備妥證明文件。")
                        
                    st.link_button(f"👉 立即前往官方網站申請", row["url"], type="primary")
                
                st.divider()
                st.subheader("📊 測試回饋與存檔")
                feedback_score = st.slider("此方案對您的解決力度 (1-10)：", 1, 10, 10)
                feedback_msg = st.text_area("是否有其他具體的幫助需求？")
                
                if st.button("提交回饋並儲存至後端"):
                    fb_df = pd.DataFrame([[u_need, feedback_score, feedback_msg]], columns=["類別", "評分", "建議"])
                    fb_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
                    st.success("回饋已安全存入後端系統。")
            else:
                st.warning("請先於左側輸入需求並點擊「立即進行實質匹配」。")
    else:
        st.error("請確認 resources.csv 檔案已正確上傳至 GitHub。")

# --- 4. 頁面 B：管理員數據中心 ---
elif page == "📊 管理員數據中心":
    st.header("📊 管理員後端驗證中心")
    
    # 進入式密碼驗證
    pwd = st.text_input("請輸入管理員授權碼以查看數據", type="password")
    
    if pwd == "1234": # 密碼設定為 1234
        st.success("身分驗證成功，正在讀取後端資料庫...")
        st.divider()
        
        if os.path.exists("feedback.csv"):
            try:
                display_df = pd.read_csv("feedback.csv")
                st.write("### 📥 使用者測試回饋紀錄")
                st.dataframe(display_df.iloc[::-1], use_container_width=True)
                
                csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(label="📥 下載完整測試報告 (.csv)", data=csv_data, file_name="admin_report.csv")
            except:
                st.info("目前後端資料庫暫無可讀取的紀錄。")
        else:
            st.info("目前尚未產生任何使用者回饋紀錄。")
    elif pwd:
        st.error("授權碼錯誤，請重新輸入。")
