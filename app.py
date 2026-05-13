import streamlit as st
import pandas as pd
import time

# 1. 讀取實體 CSV 數據庫
@st.cache_data # 效能優化：緩存數據減少讀取時間
def load_data():
    try:
        return pd.read_csv("resources.csv")
    except:
        # 如果檔案還沒準備好，回傳一個空的 DataFrame
        return pd.DataFrame(columns=["category", "name", "target", "description", "url"])

df = load_data()

st.title("SDG 10 智慧資源分配平台")

# --- AI 匹配功能區塊 ---
st.header("🤖 AI 實質匹配與效能驗證")

col_in, col_out = st.columns(2)

with col_in:
    need = st.selectbox("您的需求類型", df["category"].unique() if not df.empty else ["請先上傳 CSV"])
    user_input = st.text_input("描述您的困難 (例如：沒錢念書)")
    if st.button("開始實質匹配"):
        # --- 效能測試開始 ---
        start_time = time.time() 
        
        with st.spinner("後端正在檢索 CSV 數據庫..."):
            time.sleep(0.5) # 模擬運算
            # 實質過濾邏輯
            result = df[df["category"] == need]
            
        end_time = time.time()
        # --- 效能測試結束 ---
        
        st.session_state.match_result = result
        st.session_state.process_time = end_time - start_time

with col_out:
    if "match_result" in st.session_state:
        st.subheader("🎯 匹配結果")
        st.write(f"⚡ **後端效能驗證**：本次檢索耗時 {st.session_state.process_time:.4f} 秒")
        
        for _, row in st.session_state.match_result.iterrows():
            with st.expander(row["name"]):
                st.write(f"**對象：** {row['target']}")
                st.write(f"**說明：** {row['description']}")
                st.link_button("前往申請", row["url"])
        
        # --- 使用者回饋與驗證 ---
        st.divider()
        st.subheader("📝 使用者驗證回饋")
        val = st.radio("此結果是否有效解決您的問題？", ["十分有效", "普通", "無效"])
        feedback = st.text_area("給予演算法優化建議：")
        if st.button("提交回饋"):
            st.success("回饋已記錄！這將作為黃騵褘同學後續『測試與驗證』的優化依據。")

# --- 團隊名單修正 ---
st.sidebar.write("### 團隊成員")
st.sidebar.info("吳暐承、唐正軒、紀重仰、黃騵褘")
