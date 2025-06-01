import streamlit as st
import pandas as pd
import numpy as np
import io
import tempfile
from fpdf import FPDF

st.set_page_config(layout="wide")
st.title("🏅 Sportinės gimnastikos rezultatų sistema su teisėjų vidurkiu")

# Šrifto įkėlimas
font_file = st.file_uploader("📄 Įkelkite DejaVuSans.ttf šriftą (PDF generavimui su lietuviškomis raidėmis)", type=["ttf"])

# Įkelti du Excel failus su teisėjų vertinimais
uploaded_file_1 = st.file_uploader("📂 Įkelkite 1-o teisėjo Excel failą", type=["xlsx"], key="file1")
uploaded_file_2 = st.file_uploader("📂 Įkelkite 2-o teisėjo Excel failą", type=["xlsx"], key="file2")

if uploaded_file_1 and uploaded_file_2 and font_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_font:
        tmp_font.write(font_file.read())
        font_path = tmp_font.name

    xls1 = pd.ExcelFile(uploaded_file_1)
    xls2 = pd.ExcelFile(uploaded_file_2)
    rungtys = list(set(xls1.sheet_names) & set(xls2.sheet_names))  # bendros rungtys

    st.success(f"Rasta bendrų rungčių: {', '.join(rungtys)}")
    selected_rungtis = st.selectbox("🏋️ Pasirinkite rungtį", rungtys)

    df1 = pd.read_excel(xls1, sheet_name=selected_rungtis)
    df2 = pd.read_excel(xls2, sheet_name=selected_rungtis)

    col1, col2 = st.columns(2)
    with col1:
        selected_program = st.selectbox("🔢 Filtruoti pagal programą", ["Visos"] + sorted(df1["Programa"].dropna().unique()))
    with col2:
        selected_team = st.selectbox("👥 Filtruoti pagal komandą", ["Visos"] + sorted(df1["Komanda"].dropna().unique()))

    if selected_program != "Visos":
        df1 = df1[df1["Programa"] == selected_program]
        df2 = df2[df2["Programa"] == selected_program]
    if selected_team != "Visos":
        df1 = df1[df1["Komanda"] == selected_team]
        df2 = df2[df2["Komanda"] == selected_team]

    # Skaičiuoti vidurkius
    df1 = df1.reset_index(drop=True)
    df2 = df2.reset_index(drop=True)

    df_avg = df1.copy()
    df_avg["D"] = (df1["D"] + df2["D"]) / 2
    df_avg["E"] = (df1["E"] + df2["E"]) / 2
    df_avg["Galutinis"] = np.maximum(0, df_avg["D"] - df_avg["E"])
    df_avg = df_avg.sort_values("Galutinis", ascending=False)
    df_avg.insert(0, "Vieta", range(1, len(df_avg)+1))

    st.dataframe(df_avg, use_container_width=True)

    # Excel atsisiuntimas
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        df_avg.to_excel(writer, index=False, sheet_name="Rezultatai")
    st.download_button(
        label="📥 Atsisiųsti kaip Excel",
        data=excel_buffer.getvalue(),
        file_name=f"rezultatai_{selected_rungtis}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # PDF generavimas
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(200, 10, txt=f"Rezultatai – {selected_rungtis}", ln=True)
    pdf.ln(5)

    for _, row in df_avg.iterrows():
        row_text = ', '.join([f"{col}: {row[col]}" for col in df_avg.columns])
        pdf.multi_cell(0, 10, txt=row_text)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button(
        label="📥 Atsisiųsti kaip PDF",
        data=pdf_bytes,
        file_name=f"rezultatai_{selected_rungtis}.pdf",
        mime="application/pdf"
    )

elif (uploaded_file_1 or uploaded_file_2) and not font_file:
    st.warning("⚠️ Norint generuoti PDF su lietuviškais simboliais, būtina įkelti DejaVuSans.ttf šrifto failą.")
else:
    st.info("Įkelkite 2 Excel failus su identiškomis struktūromis, kuriuose yra skirtingų teisėjų vertinimai.")
