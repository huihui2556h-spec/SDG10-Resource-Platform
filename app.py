import streamlit as st
import pandas as pd
import time

# 設定頁面資訊 [cite: 45]
st.set_page_config(
    page_title="減少不平等｜智慧資源分配平台",
    page_icon="⚖️",
    layout="wide"
)

# --- 側邊欄導覽 ---
with st.sidebar:
    st.title("SDG 10 智慧平台")
    page = st.radio("選單", ["🏠 首頁與目標", "📊 數據分析與技術", "🤖 AI 資源匹配 Demo", "👥 團隊成員"])
    st.divider()
    st.info("對應目標 10：減少國家內與國家間的不平等 [cite: 26]")

# --- 1. 首頁與目標 ---
if page == "🏠 首頁與目標":
    st.title("用數據與 AI，讓資源分配更公平")
    st.subheader("針對教育、醫療、就業等資源分配不均問題，建立智慧化需求分析平台 [cite: 14, 42]。")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 現有困境 [cite: 15]")
        st.write("❌ 社會資源分配不均，弱勢族群難獲公平機會 [cite: 16]")
        st.write("❌ 資訊落差與數位鴻溝加劇不平等 [cite: 17]")
        st.write("❌ 缺乏智慧化分析，效率低、透明度不足 [cite: 18]")
    with col2:
        st.markdown("### 改善課題 [cite: 22]")
        st.write("✅ 自動化分析需求、精準匹配資源 [cite: 23, 32]")
        st.write("✅ 提升資源效率、透明度與公平性 [cite: 24, 35]")

# --- 2. 數據分析與技術 ---
elif page == "📊 數據分析與技術":
    st.header("技術架構與數據分析 [cite: 43]")
    
    tab1, tab2 = st.tabs(["工具清單", "核心指標"])
    with tab1:
        st.markdown("### 軟體工具 [cite: 44]")
        st.write("- **主框架**：Streamlit [cite: 45]")
        st.write("- **數據處理**：Python (Pandas, NumPy) [cite: 47]")
        st.write("- **視覺化**：Plotly 或 Pydeck [cite: 48]")
        st.write("- **部署**：Streamlit Community Cloud [cite: 56]")
    
    with tab2:
        st.markdown("### 關鍵指標分析 [cite: 50]")
        st.write("📈 **所得不平等指標**：吉尼係數 (Gini Coefficient) 計算 [cite: 51]")
        st.write("📍 **城鄉差距分析**：醫療或教育資源分布密度 [cite: 53]")

# --- 3. AI 資源匹配 Demo ---
elif page == "🤖 AI 資源匹配 Demo":
    st.header("互動 Demo：需求 → AI 資源匹配 [cite: 68]")
    st.write("填入需求，系統會立即給予匹配建議與透明說明 [cite: 42, 69]。")
    
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("📝 填寫需求")
            need_type = st.selectbox("需求類型", ["教育資源", "醫療協助", "就業/職訓", "生活補助"])
            situation = st.multiselect("身分/情境", ["低收入/中低收入", "身心障礙", "學生", "失業/待業"])
            pain = st.text_input("目前最大困難")
            submit = st.button("立即進行 AI 匹配")

    with c2:
        st.subheader("🎯 匹配結果")
        if submit:
            with st.spinner('AI 正在分析需求中...'):
                time.sleep(1)
            st.success("匹配完成！")
            st.metric("匹配分數", "92%", "+2%")
            st.write(f"**建議方案：** 針對您的「{need_type}」需求，系統已優選合適資源 [cite: 32, 42]。")
        else:
            st.info("完成左側表單後，這裡會出現匹配建議。")

# --- 4. 團隊成員 ---
elif page == "👥 團隊成員":
    st.header("團隊：(請填入新隊名)")
    team_data = {
        "職稱": ["隊長", "組員1", "組員2", "組員3"],
        "姓名": ["吳暐承", "唐正軒", "紀重仰", "黃騵褘"],
        "學號": ["1411335016", "1411335020", "1411335018", "1411335029"]
    }
    st.table(pd.DataFrame(team_data)) [cite: 7]
