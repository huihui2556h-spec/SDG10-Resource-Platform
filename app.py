import streamlit as st
import pandas as pd
import time
import os

# 頁面基本配置
st.set_page_config(page_title="SDG 10 智慧資源分配平台", layout="wide")

# 自定義可愛風格 CSS (保持介面溫馨可愛)
st.markdown("""
    <style>
    .main { background-color: #fdfbfb; }
    .stButton>button { border-radius: 20px; background-color: #ff823a; color: white; }
    .hero-box { 
        background: linear-gradient(135deg, #fdd5bd 0%, #bc84ee 100%); 
        padding: 40px; border-radius: 30px; color: white; text-align: center; margin-bottom: 30px;
    }
    .card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }
    h1, h2, h3 { color: #4b4b4b; }
    </style>
""", unsafe_allow_html=True)

# --- 1. 後端數據讀取邏輯 ---
@st.cache_data
def load_db():
    try:
        return pd.read_csv("resources.csv")
    except Exception:
        return pd.DataFrame(columns=["category", "name", "target", "description", "url"])

df = load_db()

# --- 2. 側邊欄與分頁導覽 ---
with st.sidebar:
    st.title("🌈 導覽選單")
    # 這裡多了一個首頁選項，其餘重點功能都在
    page = st.radio("功能選單", ["🏠 專案首頁", "🤖 AI 實質資源匹配", "📊 管理員數據中心"])
    st.divider()
    st.info("目標：減少資源分配不均")
    st.write("**核心團隊：**")
    st.success("👤 吳暐承\n\n👤 唐正軒\n\n👤 紀重仰\n\n👤 黃騵褘")

# --- 3. 頁面 A：專案首頁 (新增的可愛門面) ---
if page == "🏠 專案首頁":
    st.markdown("""
        <div class="hero-box">
            <h1 style="color: white; font-size: 3rem;">SDG 10 智慧資源分配平台</h1>
            <h3 style="color: white;">🌟 隊名：資源守護隊</h3>
            <p style="font-size: 1.2rem;">組員：吳暐承、唐正軒、紀重仰、黃騵褘</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 專案目標與理想")
        st.info("""
        **我們的目標：** 減少國內資源分配不均，確保弱勢族群（低收、身障、偏鄉）能跨越資訊鴻溝，迅速對接實質資源。
        
        **我們的理想：** 建立一個透明、無障礙的社會互助網絡，讓政策資源不再只是看得到吃不到的公文，而是真正能幫助到人的溫暖。
        """)
        
        st.markdown("### 🛠️ 使用工具")
        st.write("✨ **開發架構：** Python, Streamlit")
        st.write("📊 **數據處理：** Pandas, CSV 資料庫")
        st.write("🚀 **部署環境：** GitHub, Streamlit Cloud")

    with col2:
        st.markdown("### 🚀 未來展望")
        st.success("""
        1. **AI 智慧進化：** 加入自然語言處理，讓對話與匹配更人性化。
        2. **平台整合：** 串接政府 Open Data API 達成全台數據共享。
        3. **普及推廣：** 開發 LINE Bot 或 App，讓長者與偏鄉族群更易操作。
        """)
        
        st.markdown("### 📚 參考資料")
        with st.expander("查看參考來源"):
            st.write("- 行政院永續發展委員會：SDG 10 目標說明")
            st.write("- 衛福部社會司：弱勢族群社會福利資源手冊")
            st.write("- 天下雜誌《未來城市》：SDGs 永續發展專欄")

# --- 4. 頁面 B：AI 實質資源匹配 (原本的核心代碼) ---
elif page == "🤖 AI 實質資源匹配":
    st.header("🤖 AI 實質資源匹配與效能驗證")

    if not df.empty:
        col_in, col_out = st.columns([1, 1.2])
        
        with col_in:
            with st.container(border=True):
                st.subheader("📝 填寫需求")
                u_need = st.selectbox("1. 選擇您的需求類型", df["category"].unique())
                
                # 保留你要求的選項與手動輸入
                pain_options = ["低收入戶", "學費負擔", "身心障礙", "偏鄉交通", "法律諮詢", "找工作", "租屋補貼", "緊急救助"]
                u_pains = st.multiselect("2. 勾選您的具體困難 (可多選)", pain_options)
                u_custom = st.text_input("3. 其他補充描述 (選填)", placeholder="例如：新住民身分")
                
                if st.button("立即進行實質匹配", type="primary"):
                    start_time = time.time()
                    with st.spinner("AI 正在分析最合適的管道..."):
                        time.sleep(0.5) 
                        category_matches = df[df["category"] == u_need]
                        
                        # 整合關鍵字邏輯
                        combined_pains = "|".join(u_pains) if u_pains else ""
                        if u_custom:
                            combined_pains = f"{combined_pains}|{u_custom}" if combined_pains else u_custom
                        
                        # 關鍵字自動擴展 (解決低收疑慮)
                        search_pattern = combined_pains if combined_pains else "補助|支援"
                        if "低收" in search_pattern:
                            search_pattern = f"{search_pattern}|低收入|弱勢|助學|救助"
                        
                        refined_matches = category_matches[
                            category_matches['name'].str.contains(search_pattern, na=False, regex=True) |
                            category_matches['description'].str.contains(search_pattern, na=False, regex=True) |
                            category_matches['target'].str.contains(search_pattern, na=False, regex=True)
                        ]
                        
                        # 保留多重建議機制 (最多給3筆)
                        if not refined_matches.empty:
                            st.session_state.matched_list = refined_matches.head(3)
                            st.session_state.is_precise = True
                        elif not category_matches.empty:
                            st.session_state.matched_list = category_matches.head(2)
                            st.session_state.is_precise = False
                        else:
                            st.session_state.matched_list = None
                    
                    st.session_state.exec_time = time.time() - start_time

        with col_out:
            if "matched_list" in st.session_state and st.session_state.matched_list is not None:
                st.subheader("🎯 為您推薦最合適的解決方案")
                st.caption(f"⚡ 後端效能驗證：耗時 {st.session_state.get('exec_time', 0):.4f} 秒")
                
                if st.session_state.get("is_precise"):
                    st.success(f"✅ 根據您的情況，AI 推薦以下支援管道：")
                else:
                    st.info(f"💡 根據「{u_need}」類別，為您推薦主要的支援管道：")
                
                # 循環顯示匹配到的結果
                for _, row in st.session_state.matched_list.iterrows():
                    with st.container(border=True):
                        st.subheader(f"📌 {row['name']}")
                        st.write(f"**實質內容：** {row['description']}")
                        st.write(f"**適合對象：** {row['target']}")
                        if "低收" in str(row['target']) or "低收" in str(row['description']):
                            st.caption("🆘 此管道包含低收入戶專屬補助，建議備妥證明文件。")
                        st.link_button(f"👉 立即前往官方網站", row["url"], type="primary")
                
                st.divider()
                st.subheader("📊 測試回饋與存檔")
                feedback_score = st.slider("解決力度評分 (1-10)：", 1, 10, 10)
                feedback_msg = st.text_area("優化建議：")
                
                if st.button("提交回饋"):
                    fb_df = pd.DataFrame([[u_need, feedback_score, feedback_msg]], columns=["類別", "評分", "建議"])
                    fb_df.to_csv("feedback.csv", mode='a', index=False, header=not os.path.exists("feedback.csv"))
                    st.success("回饋已成功儲存至後端系統。")
            else:
                st.warning("請先於左側輸入需求並點擊「立即進行實質匹配」。")
    else:
        st.error("請確認 resources.csv 檔案已上傳至 GitHub。")

# --- 5. 頁面 C：管理員數據中心 (原本的後台驗證) ---
elif page == "📊 管理員數據中心":
    st.header("📊 管理員後端驗證中心")
    pwd = st.text_input("請輸入管理員授權碼以查看數據", type="password")
    
    if pwd == "1234": # 密碼 1234
        st.success("驗證成功")
        st.divider()
        if os.path.exists("feedback.csv"):
            try:
                display_df = pd.read_csv("feedback.csv")
                st.write("### 📥 使用者測試回饋紀錄")
                st.dataframe(display_df.iloc[::-1], use_container_width=True)
                csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(label="📥 下載完整報告 (.csv)", data=csv_data, file_name="admin_report.csv")
            except:
                st.info("暫無紀錄。")
        else:
            st.info("目前尚未產生任何紀錄。")
    elif pwd:
        st.error("授權碼錯誤。")
