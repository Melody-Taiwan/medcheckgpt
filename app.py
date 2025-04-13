import streamlit as st
import json

# === 模擬資料區 ===
drug_data = {
    "Amoxicillin": {
        "type": "Antibiotic",
        "allergy_risk": ["Penicillin"],
        "interactions": {
            "Allopurinol": "Moderate - Risk of rash and kidney toxicity",
            "Methotrexate": "High - Increased toxicity due to impaired clearance"
        },
        "alternatives": ["Clarithromycin", "Doxycycline"]
    }
}

patient_profile = {
    "Patient 001": {
        "allergies": ["Penicillin"],
        "current_meds": ["Allopurinol"]
    }
}

# === Streamlit UI ===
st.title("🧠 MedCheckGPT | 醫囑風險提示系統")

st.markdown("這是一個模擬型智慧醫療原型系統，用於展示用藥安全提示。")

# 選擇病人
selected_patient = st.selectbox("請選擇病人：", list(patient_profile.keys()))
patient_data = patient_profile[selected_patient]

# 輸入醫囑
med_order = st.text_input("請輸入醫囑（例如：Amoxicillin 500mg tid for 7 days）：")

if med_order:
    found_drug = None
    for drug in drug_data:
        if drug.lower() in med_order.lower():
            found_drug = drug
            break

    if not found_drug:
        st.error("⚠️ 無法識別醫囑中的藥品，請確認拼寫是否正確。")
    else:
        drug_info = drug_data[found_drug]
        allergy_match = any(allergen in patient_data['allergies'] for allergen in drug_info['allergy_risk'])
        interaction_issues = [med for med in patient_data['current_meds'] if med in drug_info['interactions']]

        st.subheader("🔍 分析結果")

        if allergy_match:
            st.error(f"❌ 過敏警示：{selected_patient} 對 {', '.join(drug_info['allergy_risk'])} 過敏。")

        if interaction_issues:
            for med in interaction_issues:
                st.warning(f"⚠️ 交互作用：與 {med} 合併使用 → {drug_info['interactions'][med]}")

        if not allergy_match and not interaction_issues:
            st.success("✅ 醫囑與病患資料比對無安全疑慮。")

        st.markdown("---")
        st.markdown("**💊 建議替代藥物：**")
        for alt in drug_info['alternatives']:
            st.markdown(f"- {alt}")

        st.markdown("---")
        st.markdown("📝 *本系統為原型展示用途，不提供實際醫療建議。*")
