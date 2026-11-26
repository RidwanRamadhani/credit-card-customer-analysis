import io
from pathlib import Path
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA MODERN DASHBOARD
# ==============================================================================
st.set_page_config(
    page_title="Sistem Analisis Data Kartu Kredit Nasabah",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

REQUIRED_COLUMNS = [
    "Sl_No",
    "Customer Key",
    "Avg_Credit_Limit",
    "Total_Credit_Cards",
    "Total_visits_bank",
    "Total_visits_online",
    "Total_calls_made",
]

NUMERIC_COLUMNS = [
    "Avg_Credit_Limit",
    "Total_Credit_Cards",
    "Total_visits_bank",
    "Total_visits_online",
    "Total_calls_made",
]

# Custom CSS for Modern Professional Navy Dashboard
CUSTOM_CSS = """
<style>
    /* Google Fonts & Body */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Container background */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #0A192F 0%, #1E3A8A 60%, #2563EB 100%);
        padding: 26px 32px;
        border-radius: 16px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .dashboard-header h1 {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        margin: 0 0 8px 0 !important;
        letter-spacing: -0.5px;
    }
    .dashboard-header p {
        font-size: 14px;
        color: #E2E8F0;
        margin: 0;
        max-width: 850px;
        line-height: 1.5;
    }
    .header-badge {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        color: #93C5FD;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Card styling */
    .analytics-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .analytics-card h4 {
        color: #0F172A;
        font-size: 16px;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Sidebar info box */
    .sidebar-author-box {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 14px 16px;
        color: #E2E8F0;
        margin-top: 15px;
        margin-bottom: 15px;
        font-size: 12px;
    }
    .sidebar-author-box strong {
        color: #60A5FA;
    }

    /* Metric cards customization */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 16px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #93C5FD;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #475569 !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #1E3A8A !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }

    /* Footer styling */
    .footer-container {
        text-align: center;
        padding: 24px 0 10px 0;
        margin-top: 40px;
        border-top: 1px solid #E2E8F0;
        color: #64748B;
        font-size: 12px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. FUNGSI PEMBACAAN & PENGOLAHAN DATASET AMAN
# ==============================================================================
@st.cache_data(show_spinner=False)
def load_default_dataset() -> tuple[pd.DataFrame | None, str | None]:
    """
    Membaca dataset default Credit Card Customer Data.csv secara aman
    menggunakan path relatif terhadap file app.py saat ini.
    """
    file_path = Path(__file__).resolve().parent / "Credit Card Customer Data.csv"
    if not file_path.is_file():
        # Fallback pencarian pada direktori kerja saat ini
        alt_path = Path.cwd() / "Credit Card Customer Data.csv"
        if alt_path.is_file():
            file_path = alt_path
        else:
            return None, f"File dataset '{file_path.name}' tidak ditemukan di lokasi: {file_path.parent}"

    try:
        df = pd.read_csv(file_path)
    except Exception as exc:
        return None, f"Gagal membaca file CSV: {exc}"

    # Validasi struktur kolom
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        return None, f"Kolom wajib tidak ditemukan dalam file: {', '.join(missing_cols)}"

    # Konversi kolom numerik secara aman
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sl_No numeric
    df["Sl_No"] = pd.to_numeric(df["Sl_No"], errors="coerce")
    # Customer Key sebagai string / identitas
    df["Customer Key"] = df["Customer Key"].astype(str)

    return df, None


def validate_and_clean_dataframe(raw_df: pd.DataFrame) -> tuple[pd.DataFrame | None, str | None]:
    """
    Memvalidasi dan mengonversi DataFrame baru (misal hasil upload).
    """
    if raw_df is None or raw_df.empty:
        return None, "Dataset yang diunggah kosong atau tidak memiliki data."

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in raw_df.columns]
    if missing_cols:
        return None, f"Dataset tidak memiliki kolom wajib: {', '.join(missing_cols)}"

    clean_df = raw_df.copy()
    for col in NUMERIC_COLUMNS:
        clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")

    clean_df["Sl_No"] = pd.to_numeric(clean_df["Sl_No"], errors="coerce")
    clean_df["Customer Key"] = clean_df["Customer Key"].astype(str)

    return clean_df, None


def mask_key(val: str) -> str:
    """Masking identitas Customer Key untuk keamanan publik (contoh: ***073)."""
    s = str(val).strip()
    if len(s) > 3:
        return f"***{s[-3:]}"
    return "***"


# Inisialisasi Session State
if "initial_df" not in st.session_state:
    with st.spinner("Memuat dataset kartu kredit..."):
        df_loaded, err = load_default_dataset()
        if df_loaded is not None:
            st.session_state["initial_df"] = df_loaded.copy()
            st.session_state["active_df"] = df_loaded.copy()
            st.session_state["dataset_source"] = "Dataset Standar (Credit Card Customer Data.csv)"
            st.session_state["load_error"] = None
        else:
            st.session_state["initial_df"] = None
            st.session_state["active_df"] = None
            st.session_state["dataset_source"] = "Gagal memuat dataset"
            st.session_state["load_error"] = err

if "filters" not in st.session_state:
    st.session_state["filters"] = {
        "credit_cards": [],
        "bank_visits": (0, 10),
        "online_visits": (0, 20),
        "calls_made": (0, 15),
        "credit_limit": (3000, 200000),
        "mask_keys": True,
    }

if "last_simulation" not in st.session_state:
    st.session_state["last_simulation"] = None

if "edited_df" not in st.session_state:
    st.session_state["edited_df"] = None


# ==============================================================================
# 3. SIDEBAR & NAVIGASI UTAMA
# ==============================================================================
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 12px 0 16px 0;">
        <span style="font-size: 38px;">💳</span>
        <h3 style="margin: 6px 0 2px 0; color: #1E3A8A; font-weight: 800; font-size: 18px;">ANALYTICS HUB</h3>
        <p style="margin: 0; font-size: 11px; color: #64748B; font-weight: 600;">Data Kartu Kredit Nasabah</p>
    </div>
    """,
    unsafe_allow_html=True,
)

menu_options = [
    "🏠 Dashboard Utama",
    "🔍 Eksplorasi Data",
    "📊 Visualisasi Data",
    "🔗 Analisis Korelasi",
    "🧪 Simulasi Nasabah",
    "⚙️ Pengelolaan Data",
    "ℹ️ Tentang Aplikasi",
]

selected_page = st.sidebar.radio(
    "Navigasi Modul:",
    menu_options,
    index=0,
    label_visibility="collapsed",
)

# Sidebar Card Info Dataset & Mahasiswa
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style="background-color: #F1F5F9; border-radius: 10px; padding: 12px; margin-bottom: 12px; border: 1px solid #E2E8F0;">
        <p style="margin: 0 0 4px 0; font-size: 11px; color: #64748B; font-weight: 700; text-transform: uppercase;">Sumber Data Aktif</p>
        <p style="margin: 0; font-size: 12px; color: #0F172A; font-weight: 600;">📄 {st.session_state.get('dataset_source', '-')}</p>
        <p style="margin: 4px 0 0 0; font-size: 11px; color: #3B82F6;">Total Baris: <strong>{len(st.session_state['active_df']) if st.session_state.get('active_df') is not None else 0} baris</strong></p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Identitas Kelompok 5 pada sidebar
st.sidebar.markdown(
    """
    <div class="sidebar-author-box">
        <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 700; margin-bottom: 6px;">
            🎓 Kelompok 5 - Praktikum
        </div>
        <div style="font-size: 12px; line-height: 1.5;">
            • <strong>Ridwan Ramadhani</strong> (241011400477)<br>
            • <strong>Sihabudin F.</strong> (241011400486)<br>
            • <strong>Dendi Bayu S.</strong> (241011400468)<br>
        </div>
        <div style="font-size: 11px; color: #94A3B8; margin-top: 6px; border-top: 1px solid #334155; padding-top: 4px;">
            Teknik Informatika - Semester 5<br>
            Universitas Pamulang
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# FUNGSI FILTER DATASET REUSABLE
# ==============================================================================
def get_filtered_data(df: pd.DataFrame) -> pd.DataFrame:
    """Mengembalikan DataFrame setelah menerapkan filter di session_state."""
    if df is None or df.empty:
        return df

    filtered = df.copy()
    f = st.session_state["filters"]

    # Filter credit cards
    if f.get("credit_cards"):
        filtered = filtered[filtered["Total_Credit_Cards"].isin(f["credit_cards"])]

    # Filter bank visits
    b_min, b_max = f.get("bank_visits", (0, 10))
    filtered = filtered[(filtered["Total_visits_bank"] >= b_min) & (filtered["Total_visits_bank"] <= b_max)]

    # Filter online visits
    o_min, o_max = f.get("online_visits", (0, 20))
    filtered = filtered[(filtered["Total_visits_online"] >= o_min) & (filtered["Total_visits_online"] <= o_max)]

    # Filter calls made
    c_min, c_max = f.get("calls_made", (0, 15))
    filtered = filtered[(filtered["Total_calls_made"] >= c_min) & (filtered["Total_calls_made"] <= c_max)]

    # Filter credit limit
    l_min, l_max = f.get("credit_limit", (0, 300000))
    filtered = filtered[(filtered["Avg_Credit_Limit"] >= l_min) & (filtered["Avg_Credit_Limit"] <= l_max)]

    return filtered


# ==============================================================================
# CEK KONDISI DATASET ERROR
# ==============================================================================
if st.session_state.get("load_error"):
    st.error(f"⚠️ {st.session_state['load_error']}")
    st.info(
        "Petunjuk Perbaikan:\n"
        "1. Pastikan file 'Credit Card Customer Data.csv' diletakkan pada folder yang sama dengan 'app.py'.\n"
        "2. Gunakan menu 'Pengelolaan Data' di bilah samping untuk mengunggah file CSV secara manual jika diinginkan."
    )

active_df = st.session_state.get("active_df")
if active_df is None:
    active_df = pd.DataFrame(columns=REQUIRED_COLUMNS)


# ==============================================================================
# MODUL 1: DASHBOARD UTAMA
# ==============================================================================
if selected_page == "🏠 Dashboard Utama":
    st.title("SISTEM ANALISIS & EKSPLORASI DATA KARTU KREDIT NASABAH")
    st.header("Ringkasan Eksekutif Portofolio Nasabah")
    st.markdown(
        """
        <div class="dashboard-header">
            <span class="header-badge">PRAKTIKUM PENGOLAHAN & ANALISIS DATA</span>
            <p style="font-size: 15px; margin: 0; line-height: 1.6;">Dashboard analitik komprehensif untuk menganalisis karakteristik portofolio kartu kredit, pola perilaku interaksi multichannel nasabah (bank, online, panggilan telepon), serta profil limit kredit.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if active_df.empty:
        st.warning("⚠️ Tidak ada data aktif yang tersedia untuk ditampilkan.")
    else:
        # Metrik Utama (4 Kartu Sesuai PRD Bagian 6)
        total_customers = len(active_df)
        avg_limit = active_df["Avg_Credit_Limit"].mean()
        avg_cards = active_df["Total_Credit_Cards"].mean()
        avg_bank = active_df["Total_visits_bank"].mean()
        avg_online = active_df["Total_visits_online"].mean()
        avg_calls = active_df["Total_calls_made"].mean()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label="👥 Total Nasabah Aktif",
                value=f"{total_customers:,}",
                help="Jumlah total baris nasabah yang sedang aktif dianalisis",
            )
        with col2:
            st.metric(
                label="💳 Rata-rata Batas Kredit",
                value=f"{avg_limit:,.0f}",
                help="Rata-rata Avg_Credit_Limit dari seluruh nasabah",
            )
        with col3:
            st.metric(
                label="🗂️ Rata-rata Kartu Dimiliki",
                value=f"{avg_cards:.2f} Kartu",
                help="Rata-rata Total_Credit_Cards yang dimiliki per nasabah",
            )
        with col4:
            st.metric(
                label="📞 Interaksi Multichannel Rata-rata",
                value=f"Online: {avg_online:.1f}",
                delta=f"Bank: {avg_bank:.1f} | Telp: {avg_calls:.1f}",
                delta_color="off",
                help="Rata-rata kunjungan online, kunjungan fisik bank, dan panggilan",
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Baris 2: Ringkasan Kondisi Dataset & Statistik Penting
        col_summary, col_dist = st.columns([1, 1])

        with col_summary:
            st.markdown(
                """
                <div class="analytics-card">
                    <h4>📋 Ringkasan Parameter Dataset</h4>
                """,
                unsafe_allow_html=True,
            )

            null_count = int(active_df.isnull().sum().sum())
            dup_keys = int(active_df["Customer Key"].duplicated().sum())
            min_limit = active_df["Avg_Credit_Limit"].min()
            max_limit = active_df["Avg_Credit_Limit"].max()

            summary_dict = {
                "Parameter": [
                    "Jumlah Baris",
                    "Jumlah Kolom",
                    "Total Nilai Kosong (NaN)",
                    "Duplikat Customer Key",
                    "Batas Kredit Minimum",
                    "Batas Kredit Maksimum",
                    "Median Batas Kredit",
                    "Total Kepemilikan Kartu Terbanyak",
                ],
                "Nilai": [
                    f"{len(active_df)} baris",
                    f"{len(active_df.columns)} kolom",
                    f"{null_count} nilai",
                    f"{dup_keys} identitas",
                    f"{min_limit:,.0f}",
                    f"{max_limit:,.0f}",
                    f"{active_df['Avg_Credit_Limit'].median():,.0f}",
                    f"{int(active_df['Total_Credit_Cards'].max())} kartu",
                ],
            }
            summary_table_df = pd.DataFrame(summary_dict)
            st.table(summary_table_df)

            st.markdown("</div>", unsafe_allow_html=True)

        with col_dist:
            st.markdown(
                """
                <div class="analytics-card">
                    <h4>📊 Ringkasan Distribusi Jumlah Kartu Kredit</h4>
                """,
                unsafe_allow_html=True,
            )
            # Distribusi kepemilikan kartu kredit
            card_dist = active_df["Total_Credit_Cards"].value_counts().reset_index()
            card_dist.columns = ["Jumlah Kartu", "Total Nasabah"]
            card_dist = card_dist.sort_values("Jumlah Kartu")

            fig_dist = px.bar(
                card_dist,
                x="Jumlah Kartu",
                y="Total Nasabah",
                text="Total Nasabah",
                color="Total Nasabah",
                color_continuous_scale="Blues",
                title="Distribusi Nasabah Berdasarkan Jumlah Kartu",
            )
            fig_dist.update_traces(textposition="outside")
            fig_dist.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                height=300,
                xaxis_title="Jumlah Kartu Kredit yang Dimiliki",
                yaxis_title="Banyaknya Nasabah",
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_dist, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Deskripsi Singkat Kondisi Dataset
        st.markdown(
            f"""
            <div class="analytics-card">
                <h4>💡 Analisis Ringkas Kondisi Dataset</h4>
                <p style="color: #334155; font-size: 13.5px; line-height: 1.6; margin: 0;">
                    Dataset saat ini memuat <strong>{len(active_df):,} catatan nasabah</strong> dengan batas kredit berkisar antara 
                    <strong>{min_limit:,.0f}</strong> hingga <strong>{max_limit:,.0f}</strong> (rata-rata: <strong>{avg_limit:,.0f}</strong>).
                    Tercatat mayoritas nasabah memiliki antara 1 hingga 10 kartu kredit. 
                    Dalam hal interaksi, nasabah aktif berinteraksi secara online (rata-rata {avg_online:.1f} kali), 
                    disusul kunjungan fisik ke kantor cabang bank ({avg_bank:.1f} kali), dan panggilan layanan ({avg_calls:.1f} kali).
                    Dataset memiliki <strong>{null_count} nilai hilang</strong> dan <strong>{dup_keys} identitas Customer Key ganda</strong> 
                    yang dapat dieksplorasi lebih mendalam melalui modul Eksplorasi & Visualisasi Data.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# MODUL 2: EKSPLORASI DATA
# ==============================================================================
elif selected_page == "🔍 Eksplorasi Data":
    st.header("🔍 Penjelajahan Data & Struktur Atribut")
    st.markdown(
        """
        <div class="dashboard-header">
            <span class="header-badge">EKSPLORASI DATASET & FILTER INTERAKTIF</span>
            <p style="font-size: 15px; margin: 0; line-height: 1.6;">Eksplorasi struktur data, kamus variabel, ringkasan statistik deskriptif lima angka, serta gunakan filter interaktif terpadu untuk menelaah segmen nasabah tertentu.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if active_df.empty:
        st.warning("⚠️ Tidak ada data aktif yang tersedia untuk dieksplorasi.")
    else:
        # Bagian Filter Interaktif
        st.markdown("### 🎛️ Filter Interaktif")
        with st.expander("Buka Panel Filter Data", expanded=True):
            col_f1, col_f2, col_f3 = st.columns(3)

            all_cards = sorted(active_df["Total_Credit_Cards"].dropna().unique().astype(int).tolist())
            with col_f1:
                selected_cards = st.multiselect(
                    "Pilih Jumlah Kartu Kredit:",
                    options=all_cards,
                    default=st.session_state["filters"].get("credit_cards", []),
                    help="Pilih satu atau beberapa jumlah kartu kredit",
                )

            with col_f2:
                min_limit_val = int(active_df["Avg_Credit_Limit"].min())
                max_limit_val = int(active_df["Avg_Credit_Limit"].max())
                cur_limit_range = st.session_state["filters"].get("credit_limit", (min_limit_val, max_limit_val))
                # Pastikan batas berada dalam rentang
                valid_l_min = max(min_limit_val, cur_limit_range[0])
                valid_l_max = min(max_limit_val, cur_limit_range[1])
                selected_limit = st.slider(
                    "Rentang Batas Kredit (Avg_Credit_Limit):",
                    min_value=min_limit_val,
                    max_value=max_limit_val,
                    value=(valid_l_min, valid_l_max),
                    step=1000,
                )

            with col_f3:
                max_bank = int(active_df["Total_visits_bank"].max())
                cur_bank = st.session_state["filters"].get("bank_visits", (0, max_bank))
                selected_bank = st.slider(
                    "Kunjungan ke Bank (Fisik):",
                    min_value=0,
                    max_value=max(1, max_bank),
                    value=(max(0, cur_bank[0]), min(max_bank, cur_bank[1])),
                )

            col_f4, col_f5, col_f6 = st.columns(3)
            with col_f4:
                max_online = int(active_df["Total_visits_online"].max())
                cur_online = st.session_state["filters"].get("online_visits", (0, max_online))
                selected_online = st.slider(
                    "Kunjungan Layanan Online:",
                    min_value=0,
                    max_value=max(1, max_online),
                    value=(max(0, cur_online[0]), min(max_online, cur_online[1])),
                )

            with col_f5:
                max_calls = int(active_df["Total_calls_made"].max())
                cur_calls = st.session_state["filters"].get("calls_made", (0, max_calls))
                selected_calls = st.slider(
                    "Panggilan ke Call Center:",
                    min_value=0,
                    max_value=max(1, max_calls),
                    value=(max(0, cur_calls[0]), min(max_calls, cur_calls[1])),
                )

            with col_f6:
                st.write("")
                st.write("")
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    apply_filter = st.button("Terapkan Filter", use_container_width=True, type="primary")
                with col_btn2:
                    reset_filter = st.button("Reset Filter", use_container_width=True)

            if apply_filter:
                st.session_state["filters"]["credit_cards"] = selected_cards
                st.session_state["filters"]["credit_limit"] = selected_limit
                st.session_state["filters"]["bank_visits"] = selected_bank
                st.session_state["filters"]["online_visits"] = selected_online
                st.session_state["filters"]["calls_made"] = selected_calls
                st.rerun()

            if reset_filter:
                st.session_state["filters"] = {
                    "credit_cards": [],
                    "bank_visits": (0, int(active_df["Total_visits_bank"].max())),
                    "online_visits": (0, int(active_df["Total_visits_online"].max())),
                    "calls_made": (0, int(active_df["Total_calls_made"].max())),
                    "credit_limit": (int(active_df["Avg_Credit_Limit"].min()), int(active_df["Avg_Credit_Limit"].max())),
                    "mask_keys": True,
                }
                st.rerun()

        # Dapatkan Data Terfilter
        filtered_df = get_filtered_data(active_df)

        st.markdown("---")
        # Sub-bagian A: Tampilan Dataset
        st.subheader("📑 Tampilan Dataset")
        col_meta, col_mask = st.columns([3, 1])
        with col_meta:
            st.markdown(
                f"Menampilkan **{len(filtered_df):,}** baris dari total **{len(active_df):,}** baris data aktif "
                f"({len(filtered_df.columns)} kolom)."
            )
        with col_mask:
            mask_active = st.checkbox("Samarkan Customer Key (Privacy)", value=st.session_state["filters"].get("mask_keys", True))
            st.session_state["filters"]["mask_keys"] = mask_active

        if filtered_df.empty:
            st.info("ℹ️ Tidak ada data nasabah yang sesuai dengan kriteria filter yang diterapkan. Silakan ubah rentang filter atau tekan 'Reset Filter'.")
        else:
            display_df = filtered_df.copy()
            if mask_active:
                display_df["Customer Key"] = display_df["Customer Key"].apply(mask_key)

            st.dataframe(
                display_df,
                use_container_width=True,
                height=320,
            )

        # Sub-bagian B: Informasi Struktur Dataset & st.json
        st.markdown("---")
        st.subheader("🏗️ Struktur Data & Konfigurasi Variabel")

        col_struct1, col_struct2 = st.columns([1, 1])
        with col_struct1:
            st.markdown("##### Ringkasan Kolom & Tipe Data")
            struct_info = []
            for col in active_df.columns:
                struct_info.append({
                    "Nama Kolom": col,
                    "Tipe Data": str(active_df[col].dtype),
                    "Data Terisi": int(active_df[col].count()),
                    "Nilai Kosong": int(active_df[col].isnull().sum()),
                    "Nilai Unik": int(active_df[col].nunique()),
                })
            st.dataframe(pd.DataFrame(struct_info), use_container_width=True)

        with col_struct2:
            st.markdown("##### Konfigurasi Metadata Dataset (Format JSON)")
            dataset_metadata = {
                "dataset_name": "Credit Card Customer Data",
                "active_rows": len(active_df),
                "active_columns": len(active_df.columns),
                "numeric_attributes": NUMERIC_COLUMNS,
                "identifier_attributes": ["Sl_No", "Customer Key"],
                "missing_values_total": int(active_df.isnull().sum().sum()),
                "duplicate_customer_keys": int(active_df["Customer Key"].duplicated().sum()),
                "source": st.session_state.get("dataset_source", "Unknown"),
            }
            st.json(dataset_metadata)

        # Sub-bagian C: Kamus Variabel
        st.markdown("---")
        st.subheader("📖 Kamus Variabel Dataset")
        variable_dict = [
            {"Variabel": "Sl_No", "Tipe": "Numerik (Integer)", "Keterangan": "Nomor urut indeks pencatatan data nasabah dalam dataset."},
            {"Variabel": "Customer Key", "Tipe": "Identitas (String)", "Keterangan": "Kunci unik tanda pengenal nasabah pada sistem perbankan."},
            {"Variabel": "Avg_Credit_Limit", "Tipe": "Numerik Kontinu", "Keterangan": "Rata-rata batas (limit) kredit yang diberikan bank kepada nasabah."},
            {"Variabel": "Total_Credit_Cards", "Tipe": "Numerik Diskrit", "Keterangan": "Jumlah kartu kredit aktif yang dimiliki nasabah di bank."},
            {"Variabel": "Total_visits_bank", "Tipe": "Numerik Diskrit", "Keterangan": "Frekuensi kunjungan fisik nasabah ke kantor cabang bank."},
            {"Variabel": "Total_visits_online", "Tipe": "Numerik Diskrit", "Keterangan": "Frekuensi akses/kunjungan nasabah menggunakan layanan online banking / mobile banking."},
            {"Variabel": "Total_calls_made", "Tipe": "Numerik Diskrit", "Keterangan": "Jumlah panggilan telepon yang dilakukan nasabah ke customer care layanan bank."},
        ]
        st.table(pd.DataFrame(variable_dict))

        # Sub-bagian D: Statistik Deskriptif
        st.markdown("---")
        st.subheader("📐 Statistik Deskriptif (Pandas describe)")
        st.markdown("Tabel ringkasan ukuran pemusatan dan penyebaran data untuk seluruh variabel numerik:")
        desc_df = active_df[NUMERIC_COLUMNS].describe().T
        desc_df = desc_df.rename(columns={
            "count": "Count",
            "mean": "Mean",
            "std": "Std Dev",
            "min": "Min",
            "25%": "Q1 (25%)",
            "50%": "Median (50%)",
            "75%": "Q3 (75%)",
            "max": "Max",
        })
        st.dataframe(desc_df.style.format("{:,.2f}"), use_container_width=True)

        # Sub-bagian E: Analisis Nilai Ekstrem (st.selectbox)
        st.markdown("---")
        st.subheader("🔎 Penelusuran Nilai Ekstrem Atribut Numerik")
        chosen_col = st.selectbox(
            "Pilih Atribut Numerik untuk Melihat 5 Nilai Tertinggi dan Terendah:",
            options=NUMERIC_COLUMNS,
            index=0,
            help="Gunakan selectbox ini untuk meninjau distribusi ekstrem atas variabel terpilih",
        )
        col_top, col_bot = st.columns(2)
        with col_top:
            st.markdown(f"**Top 5 Nilai Tertinggi ({chosen_col}):**")
            top5 = active_df.nlargest(5, chosen_col)[["Customer Key", chosen_col, "Total_Credit_Cards"]]
            if st.session_state["filters"].get("mask_keys", True):
                top5["Customer Key"] = top5["Customer Key"].apply(mask_key)
            st.dataframe(top5, use_container_width=True)
        with col_bot:
            st.markdown(f"**Top 5 Nilai Terendah ({chosen_col}):**")
            bot5 = active_df.nsmallest(5, chosen_col)[["Customer Key", chosen_col, "Total_Credit_Cards"]]
            if st.session_state["filters"].get("mask_keys", True):
                bot5["Customer Key"] = bot5["Customer Key"].apply(mask_key)
            st.dataframe(bot5, use_container_width=True)


# ==============================================================================
# MODUL 3: VISUALISASI DATA
# ==============================================================================
elif selected_page == "📊 Visualisasi Data":
    st.header("📊 Visualisasi Data Nasabah Multi-Framework")
    st.markdown(
        """
        <div class="dashboard-header">
            <span class="header-badge">VISUALISASI MULTI-FRAMEWORK</span>
            <p style="font-size: 15px; margin: 0; line-height: 1.6;">Eksplorasi grafis interaktif memanfaatkan perpaduan Streamlit Charts, Altair, dan Plotly Express untuk menemukan pola, tren, dan anomali pada portofolio nasabah.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df_vis = get_filtered_data(active_df)

    if df_vis.empty:
        st.info("ℹ️ Dataset kosong berdasarkan filter saat ini. Harap reset filter di menu Eksplorasi Data untuk melihat grafik.")
    else:
        # Pilihan Tampilan Berdasarkan Tab
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Line Chart (Tren Limit)",
            "🌊 Area Chart (Pola Interaksi)",
            "📊 Bar Chart (Kunjungan Bank)",
            "✨ Altair Scatter (Interaktif)",
            "📦 Plotly (Distribusi & Box Plot)",
        ])

        # TAB 1: Line Chart
        with tab1:
            st.markdown("#### Tren Rata-rata Batas Kredit Berdasarkan Jumlah Kartu Kredit")
            line_data = df_vis.groupby("Total_Credit_Cards")["Avg_Credit_Limit"].mean().reset_index()
            line_data = line_data.sort_values("Total_Credit_Cards")
            line_chart_input = line_data.set_index("Total_Credit_Cards")

            st.line_chart(line_chart_input, use_container_width=True)
            st.caption(
                "💡 **Interpretasi Grafik:** Grafik garis di atas menunjukkan tren rata-rata batas kredit (Avg_Credit_Limit) "
                "berdasarkan jumlah kepemilikan kartu kredit (Total_Credit_Cards). Terlihat jelas adanya korelasi positif yang sangat kuat: "
                "nasabah dengan kepemilikan kartu kredit tinggi (misal 8-10 kartu) menikmati rata-rata batas kredit yang jauh lebih tinggi secara signifikan."
            )

        # TAB 2: Area Chart
        with tab2:
            st.markdown("#### Pola Aktivitas Interaksi Multichannel Nasabah")
            area_data = df_vis.groupby("Total_Credit_Cards")[["Total_visits_bank", "Total_visits_online", "Total_calls_made"]].mean().reset_index()
            area_data = area_data.sort_values("Total_Credit_Cards")
            area_chart_input = area_data.set_index("Total_Credit_Cards")

            st.area_chart(area_chart_input, use_container_width=True)
            st.caption(
                "💡 **Interpretasi Grafik:** Grafik area memperlihatkan perbandingan intensitas saluran interaksi nasabah. "
                "Nasabah dengan kartu sedikit (1-4 kartu) cenderung mendominasi panggilan telepon (calls made) dan kunjungan fisik ke bank, "
                "sedangkan nasabah dengan kepemilikan kartu tinggi (7-10 kartu) memiliki frekuensi kunjungan online yang sangat dominan."
            )

        # TAB 3: Bar Chart
        with tab3:
            st.markdown("#### Rata-rata Batas Kredit Berdasarkan Frekuensi Kunjungan Fisik ke Bank")
            bar_data = df_vis.groupby("Total_visits_bank")["Avg_Credit_Limit"].mean().reset_index()
            bar_data = bar_data.sort_values("Total_visits_bank")
            bar_chart_input = bar_data.set_index("Total_visits_bank")

            st.bar_chart(bar_chart_input, use_container_width=True)
            st.caption(
                "💡 **Interpretasi Grafik:** Grafik batang menunjukkan bahwa nasabah yang sangat jarang atau tidak pernah berkunjung ke bank fisik "
                "(kunjungan 0-1 kali) justru memiliki rata-rata batas kredit tertinggi. Hal ini mengindikasikan segmen nasabah bernilai tinggi "
                "(affluent / tech-savvy) yang lebih memilih interaksi digital mandiri."
            )

        # TAB 4: Altair Chart
        with tab4:
            st.markdown("#### Hubungan Aktivitas Online dengan Batas Kredit (Altair Scatter)")
            sample_size = min(len(df_vis), 1000)
            chart_df = df_vis.sample(sample_size, random_state=42) if len(df_vis) > 1000 else df_vis.copy()

            chart_altair = (
                alt.Chart(chart_df)
                .mark_circle(size=70, opacity=0.7)
                .encode(
                    x=alt.X("Total_visits_online:Q", title="Jumlah Akses Online (Total_visits_online)"),
                    y=alt.Y("Avg_Credit_Limit:Q", title="Rata-rata Batas Kredit (Avg_Credit_Limit)"),
                    color=alt.Color("Total_Credit_Cards:Q", title="Jml Kartu", scale=alt.Scale(scheme="blues")),
                    tooltip=[
                        alt.Tooltip("Customer Key:N", title="Customer Key"),
                        alt.Tooltip("Avg_Credit_Limit:Q", title="Limit Kredit", format=",.0f"),
                        alt.Tooltip("Total_Credit_Cards:Q", title="Jml Kartu"),
                        alt.Tooltip("Total_visits_online:Q", title="Kunjungan Online"),
                        alt.Tooltip("Total_visits_bank:Q", title="Kunjungan Bank"),
                    ],
                )
                .properties(height=420)
                .interactive()
            )

            st.altair_chart(chart_altair, use_container_width=True)
            st.caption(
                "💡 **Fitur Interaktif:** Arahkan kursor mouse ke setiap lingkaran data untuk melihat rincian spesifik nasabah "
                "(Customer Key, Limit, Jumlah Kartu, dan Frekuensi Kunjungan). Grafik ini memvisualisasikan bagaimana nasabah dengan aktivitas online "
                "tinggi berkelompok di bagian atas rentang batas kredit."
            )

        # TAB 5: Plotly Charts
        with tab5:
            col_px1, col_px2 = st.columns(2)

            with col_px1:
                st.markdown("##### 1. Histogram Distribusi Batas Kredit")
                fig_hist = px.histogram(
                    df_vis,
                    x="Avg_Credit_Limit",
                    nbins=30,
                    marginal="box",
                    color_discrete_sequence=["#2563EB"],
                    title="Distribusi Avg_Credit_Limit",
                )
                fig_hist.update_layout(
                    xaxis_title="Avg_Credit_Limit",
                    yaxis_title="Frekuensi",
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=380,
                )
                st.plotly_chart(fig_hist, use_container_width=True)
                st.caption("Distribusi batas kredit menunjukkan skewness positif (miring ke kanan), dengan konsentrasi terbesar pada limit di bawah 30.000.")

            with col_px2:
                st.markdown("##### 2. Box Plot Sebaran Limit per Jumlah Kartu")
                fig_box = px.box(
                    df_vis,
                    x="Total_Credit_Cards",
                    y="Avg_Credit_Limit",
                    color="Total_Credit_Cards",
                    title="Box Plot Sebaran Limit vs Kartu",
                )
                fig_box.update_layout(
                    xaxis_title="Jumlah Kartu Kredit",
                    yaxis_title="Avg_Credit_Limit",
                    showlegend=False,
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=380,
                )
                st.plotly_chart(fig_box, use_container_width=True)
                st.caption("Box plot memperlihatkan kuartil, median, serta sebaran batas kredit di setiap kategori kepemilikan kartu kredit nasabah.")


# ==============================================================================
# MODUL 4: ANALISIS KORELASI
# ==============================================================================
elif selected_page == "🔗 Analisis Korelasi":
    st.header("🔗 Analisis Korelasi & Heatmap Antarvariabel")
    st.markdown(
        """
        <div class="dashboard-header">
            <span class="header-badge">ANALISIS STATISTIK MULTIVARIAT</span>
            <p style="font-size: 15px; margin: 0; line-height: 1.6;">Pemeriksaan koefisien korelasi Pearson antarvariabel numerik analitik untuk memahami derajat hubungan linier tanpa mengasumsikan hubungan sebab-akibat.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if active_df.empty:
        st.warning("⚠️ Tidak ada data aktif untuk menghitung korelasi.")
    else:
        # Hitung matriks korelasi
        corr_matrix = active_df[NUMERIC_COLUMNS].corr(numeric_only=True)

        col_heat, col_tbl = st.columns([1.2, 1])

        with col_heat:
            st.markdown("### 🌡️ Heatmap Matriks Korelasi (Matplotlib)")

            fig, ax = plt.subplots(figsize=(7, 5.5))
            cax = ax.matshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
            fig.colorbar(cax)

            ticks = range(len(corr_matrix.columns))
            labels = [
                "Credit Limit",
                "Total Cards",
                "Bank Visits",
                "Online Visits",
                "Calls Made",
            ]
            ax.set_xticks(ticks)
            ax.set_yticks(ticks)
            ax.set_xticklabels(labels, rotation=35, ha="left", fontsize=9)
            ax.set_yticklabels(labels, fontsize=9)

            # Tambahkan nilai korelasi pada setiap kotak heatmap
            for i in range(len(corr_matrix.columns)):
                for j in range(len(corr_matrix.columns)):
                    val = corr_matrix.iloc[i, j]
                    text_color = "white" if abs(val) > 0.45 else "black"
                    ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=text_color, fontweight="bold", fontsize=10)

            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        with col_tbl:
            st.markdown("### 📋 Tabel Nilai Korelasi Pearson")
            st.dataframe(corr_matrix.style.background_cmap(cmap="Blues").format("{:.3f}"), use_container_width=True)

            st.markdown("### 💡 Interpretasi Objektif Korelasi")
            st.info(
                "📌 **Pedoman Penafsiran Statistik:**\n\n"
                "1. **Avg_Credit_Limit & Total_Credit_Cards (Korelasi Positif Kuat, ~0.61):** Nasabah yang memiliki kartu kredit lebih banyak cenderung memiliki batas kredit rata-rata yang lebih tinggi.\n"
                "2. **Avg_Credit_Limit & Total_visits_online (Korelasi Positif Sedang, ~0.56):** Aktivitas online memiliki hubungan searah dengan batas kredit nasabah.\n"
                "3. **Avg_Credit_Limit & Total_calls_made (Korelasi Negatif Sedang, ~ -0.41):** Nasabah dengan batas kredit tinggi cenderung lebih jarang melakukan panggilan layanan dibanding nasabah berlimit rendah.\n"
                "4. **Total_Credit_Cards & Total_calls_made (Korelasi Negatif Kuat, ~ -0.65):** Frekuensi panggilan berbanding terbalik dengan kepemilikan kartu.\n\n"
                "⚠️ **Catatan Penting:** Korelasi hanya menggambarkan derajat asosiasi linier secara statistik, **bukan hubungan sebab-akibat (kausalitas)**."
            )

        # Dua Scatter Plot Analisis Korelasi Tambahan Sesuai PRD
        st.markdown("---")
        st.subheader("🔍 Scatter Plot Analisis Hubungan Kunci")
        col_sc1, col_sc2 = st.columns(2)

        with col_sc1:
            fig_sc1 = px.scatter(
                active_df,
                x="Total_Credit_Cards",
                y="Avg_Credit_Limit",
                trendline="ols",
                color_discrete_sequence=["#1E3A8A"],
                title="Batas Kredit vs Jumlah Kartu Kredit",
                labels={"Total_Credit_Cards": "Jumlah Kartu Kredit", "Avg_Credit_Limit": "Rata-rata Batas Kredit"},
            )
            fig_sc1.update_layout(height=360, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_sc1, use_container_width=True)

        with col_sc2:
            fig_sc2 = px.scatter(
                active_df,
                x="Total_visits_online",
                y="Avg_Credit_Limit",
                trendline="ols",
                color_discrete_sequence=["#2563EB"],
                title="Batas Kredit vs Kunjungan Online",
                labels={"Total_visits_online": "Kunjungan Layanan Online", "Avg_Credit_Limit": "Rata-rata Batas Kredit"},
            )
            fig_sc2.update_layout(height=360, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_sc2, use_container_width=True)


# ==============================================================================
# MODUL 5: SIMULASI NASABAH
# ==============================================================================
elif selected_page == "🧪 Simulasi Nasabah":
    st.header("🧪 Simulasi Profil & Pengajuan Nasabah Baru")
    st.markdown(
        """
        <div class="dashboard-header">
            <span class="header-badge">SIMULASI PROFIL EKSPLORATIF</span>
            <p style="font-size: 15px; margin: 0; line-height: 1.6;">Uji skenario profil nasabah dan bandingkan secara langsung terhadap distribusi rata-rata dataset aktif sebagai sarana pembelajaran interaktif.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.warning(
        "⚖️ **Pemberitahuan Kepatuhan & Akademik:**\n"
        "Dataset ini tidak memuat label keputusan persetujuan kredit (approved/rejected). "
        "Formulir ini dirancang semata-mata untuk eksplorasi statistik data akademik, "
        "bukan sebagai rekomendasi resmi perbankan atau alat penilaian kelayakan risiko kredit."
    )

    col_form, col_result = st.columns([1, 1.1])

    with col_form:
        st.markdown("### 📝 Formulir Masukan Profil Nasabah")
        with st.form("customer_simulation_form", clear_on_submit=False):
            # Customer Key string input
            sim_customer_key = st.text_input(
                "Customer Key (Identifier):",
                value="99881",
                help="Identitas unik nasabah (string/teks, bukan variabel kalkulasi).",
            )

            sim_limit = st.number_input(
                "Rata-rata Batas Kredit (Avg_Credit_Limit):",
                min_value=0.0,
                max_value=1000000.0,
                value=35000.0,
                step=1000.0,
                help="Batas kredit rata-rata yang diajukan atau dimiliki",
            )

            sim_cards = st.number_input(
                "Jumlah Kartu Kredit (Total_Credit_Cards):",
                min_value=0,
                max_value=20,
                value=4,
                step=1,
                help="Banyaknya kartu kredit yang dimiliki",
            )

            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                sim_bank = st.number_input(
                    "Kunjungan Bank Fisik:",
                    min_value=0,
                    max_value=50,
                    value=2,
                    step=1,
                    help="Frekuensi ke kantor cabang",
                )
            with col_sub2:
                sim_online = st.number_input(
                    "Kunjungan Layanan Online:",
                    min_value=0,
                    max_value=50,
                    value=4,
                    step=1,
                    help="Frekuensi akses mobile / internet banking",
                )

            sim_calls = st.number_input(
                "Panggilan Call Center:",
                min_value=0,
                max_value=50,
                value=2,
                step=1,
                help="Banyaknya panggilan ke call center bank",
            )

            submit_simulation = st.form_submit_button("Jalankan Simulasi Profil", type="primary", use_container_width=True)

        if submit_simulation:
            if not sim_customer_key.strip():
                st.error("Customer Key tidak boleh kosong.")
            else:
                sim_data = {
                    "Customer Key": sim_customer_key.strip(),
                    "Avg_Credit_Limit": float(sim_limit),
                    "Total_Credit_Cards": int(sim_cards),
                    "Total_visits_bank": int(sim_bank),
                    "Total_visits_online": int(sim_online),
                    "Total_calls_made": int(sim_calls),
                }
                st.session_state["last_simulation"] = sim_data
                st.success("✅ Simulasi profil nasabah berhasil diproses dan disimpan di session state!")

    with col_result:
        st.markdown("### 📊 Hasil Evaluasi & Perbandingan Profil")
        sim_data = st.session_state.get("last_simulation")

        if sim_data is None:
            st.info("👈 Masukkan parameter pada formulir di sebelah kiri dan klik **'Jalankan Simulasi Profil'** untuk melihat perbandingan.")
        else:
            avg_dataset = {
                "Avg_Credit_Limit": active_df["Avg_Credit_Limit"].mean() if not active_df.empty else 34574.0,
                "Total_Credit_Cards": active_df["Total_Credit_Cards"].mean() if not active_df.empty else 4.7,
                "Total_visits_bank": active_df["Total_visits_bank"].mean() if not active_df.empty else 2.4,
                "Total_visits_online": active_df["Total_visits_online"].mean() if not active_df.empty else 2.6,
                "Total_calls_made": active_df["Total_calls_made"].mean() if not active_df.empty else 3.5,
            }

            # Kartu Rangkuman
            st.markdown(
                f"""
                <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 12px; padding: 16px; margin-bottom: 16px;">
                    <div style="font-size: 12px; color: #64748B; font-weight: 700; text-transform: uppercase;">Profil Hasil Simulasi</div>
                    <div style="font-size: 20px; font-weight: 800; color: #1E3A8A; margin: 4px 0;">Customer Key: {sim_data['Customer Key']}</div>
                    <div style="font-size: 13px; color: #334155; line-height: 1.5;">
                        • Batas Kredit: <strong>{sim_data['Avg_Credit_Limit']:,.0f}</strong><br>
                        • Kepemilikan Kartu: <strong>{sim_data['Total_Credit_Cards']} Kartu</strong><br>
                        • Interaksi: Bank ({sim_data['Total_visits_bank']}x), Online ({sim_data['Total_visits_online']}x), Call Center ({sim_data['Total_calls_made']}x)
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Perbandingan Grafik Interaksi
            metrics_compare = ["Total_Credit_Cards", "Total_visits_bank", "Total_visits_online", "Total_calls_made"]
            metric_labels = ["Jumlah Kartu", "Kunjungan Bank", "Kunjungan Online", "Panggilan Telp"]

            comp_df = pd.DataFrame({
                "Parameter": metric_labels * 2,
                "Nilai": [sim_data[m] for m in metrics_compare] + [avg_dataset[m] for m in metrics_compare],
                "Kategori": ["Simulasi Nasabah"] * 4 + ["Rata-rata Dataset"] * 4,
            })

            fig_comp = px.bar(
                comp_df,
                x="Parameter",
                y="Nilai",
                color="Kategori",
                barmode="group",
                color_discrete_map={"Simulasi Nasabah": "#2563EB", "Rata-rata Dataset": "#94A3B8"},
                title="Perbandingan Parameter Interaksi dengan Rata-rata Dataset",
            )
            fig_comp.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_comp, use_container_width=True)

            # Persentase Batas Kredit terhadap Rata-rata
            diff_limit = ((sim_data["Avg_Credit_Limit"] - avg_dataset["Avg_Credit_Limit"]) / avg_dataset["Avg_Credit_Limit"]) * 100
            diff_text = f"{'+' if diff_limit >= 0 else ''}{diff_limit:.1f}%"

            st.caption(
                f"ℹ️ Batas kredit simulasi adalah **{sim_data['Avg_Credit_Limit']:,.0f}** "
                f"({diff_text} dibandingkan rata-rata portofolio yaitu {avg_dataset['Avg_Credit_Limit']:,.0f})."
            )


# ==============================================================================
# MODUL 6: PENGELOLAAN DATA
# ==============================================================================
elif selected_page == "⚙️ Pengelolaan Data":
    st.header("⚙️ Pengelolaan Dataset, Upload, Edit & Download")
    st.markdown(
        """
        <div class="dashboard-header">
            <span class="header-badge">MANAJEMEN DATASET & PENYIMPANAN SESI</span>
            <p style="font-size: 15px; margin: 0; line-height: 1.6;">Kelola dataset aktif melalui fitur unggah CSV alternatif, pengeditan tabel data secara interaktif di session state, unduh data, serta opsi pemulihan dataset awal.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_upload, tab_edit, tab_download, tab_reset = st.tabs([
        "📤 Upload Dataset CSV",
        "✏️ Edit Data Interaktif",
        "📥 Download Dataset",
        "🔄 Reset Data Awal",
    ])

    # A. UPLOAD CSV
    with tab_upload:
        st.markdown("### 📤 Unggah Dataset Alternatif")
        st.markdown(
            "Anda dapat mengunggah file CSV lain untuk dianalisis sementara pada sesi saat ini. "
            "File CSV wajib memiliki 7 kolom standar: `Sl_No`, `Customer Key`, `Avg_Credit_Limit`, "
            "`Total_Credit_Cards`, `Total_visits_bank`, `Total_visits_online`, `Total_calls_made`."
        )

        uploaded_file = st.file_uploader(
            "Pilih file CSV alternatif:",
            type=["csv"],
            help="Hanya menerima file berformat CSV ber-encoding UTF-8",
        )

        if uploaded_file is not None:
            try:
                uploaded_raw_df = pd.read_csv(uploaded_file)
                valid_df, val_err = validate_and_clean_dataframe(uploaded_raw_df)

                if val_err:
                    st.error(f"❌ Validasi Gagal: {val_err}")
                else:
                    st.success(f"✅ File '{uploaded_file.name}' valid! Berisi {len(valid_df):,} baris dan {len(valid_df.columns)} kolom.")
                    col_up1, col_up2 = st.columns([1, 3])
                    with col_up1:
                        if st.button("Gunakan Dataset Ini Sebagai Data Aktif", type="primary"):
                            st.session_state["active_df"] = valid_df.copy()
                            st.session_state["dataset_source"] = f"Upload: {uploaded_file.name}"
                            st.session_state["load_error"] = None
                            st.rerun()
                    with col_up2:
                        st.write("Pratinjau 3 data teratas:")
                        st.dataframe(valid_df.head(3), use_container_width=True)

            except Exception as e:
                st.error(f"Gagal memproses file yang diunggah: {e}")

    # B. EDIT DATA INTERAKTIF
    with tab_edit:
        st.markdown("### ✏️ Edit Data Secara Interaktif (Data Editor)")
        st.markdown(
            "Gunakan tabel interaktif di bawah ini untuk mengedit nilai baris data secara langsung. "
            "Perubahan akan tersimpan di memory session state dan **tidak akan menimpa file CSV asli di disk**."
        )

        if active_df.empty:
            st.warning("Tidak ada data untuk diedit.")
        else:
            edited_result = st.data_editor(
                active_df,
                num_rows="dynamic",
                use_container_width=True,
                height=350,
                key="customer_data_editor",
            )

            col_ed1, col_ed2 = st.columns([1, 4])
            with col_ed1:
                if st.button("Simpan Perubahan ke Sesi Aktif", type="primary"):
                    st.session_state["active_df"] = edited_result.copy()
                    st.session_state["dataset_source"] = f"{st.session_state['dataset_source']} (Hasil Edit Manual)"
                    st.success("✅ Perubahan data berhasil disimpan ke dataset sesi aktif!")
                    st.rerun()

    # C. DOWNLOAD DATASET
    with tab_download:
        st.markdown("### 📥 Unduh Dataset dalam Format CSV")
        st.markdown("Pilih jenis dataset yang ingin diunduh sesuai kebutuhan analisis Anda:")

        col_dl1, col_dl2, col_dl3 = st.columns(3)

        # 1. Dataset Aktif
        with col_dl1:
            st.markdown("##### 1. Dataset Sesi Aktif")
            if not active_df.empty:
                csv_active = active_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Dataset Aktif",
                    data=csv_active,
                    file_name="Credit_Card_Active_Dataset.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
                st.caption(f"Total baris: {len(active_df):,}")

        # 2. Dataset Terfilter
        with col_dl2:
            st.markdown("##### 2. Dataset Hasil Filter")
            filtered_for_dl = get_filtered_data(active_df)
            if not filtered_for_dl.empty:
                csv_filtered = filtered_for_dl.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Dataset Terfilter",
                    data=csv_filtered,
                    file_name="Credit_Card_Filtered_Dataset.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
                st.caption(f"Total baris: {len(filtered_for_dl):,}")

        # 3. Profil Simulasi Terakhir
        with col_dl3:
            st.markdown("##### 3. Data Simulasi Terakhir")
            last_sim = st.session_state.get("last_simulation")
            if last_sim is not None:
                sim_dl_df = pd.DataFrame([last_sim])
                csv_sim = sim_dl_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Hasil Simulasi",
                    data=csv_sim,
                    file_name=f"Simulasi_Nasabah_{last_sim['Customer Key']}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
                st.caption(f"Customer Key: {last_sim['Customer Key']}")
            else:
                st.info("Belum ada simulasi nasabah yang dilakukan.")

    # D. RESET DATA
    with tab_reset:
        st.markdown("### 🔄 Pemulihan Dataset Awal (Reset)")
        st.markdown(
            "Tindakan ini akan mengembalikan data aktif ke file CSV bawaan "
            "(`Credit Card Customer Data.csv`) serta membatalkan seluruh perubahan upload maupun pengeditan manual sesi."
        )

        confirm_reset = st.button("Kembalikan ke Dataset Bawaan Asli", type="secondary")
        if confirm_reset:
            with st.spinner("Memuat ulang dataset bawaan asli..."):
                fresh_df, err = load_default_dataset()
                if fresh_df is not None:
                    st.session_state["initial_df"] = fresh_df.copy()
                    st.session_state["active_df"] = fresh_df.copy()
                    st.session_state["dataset_source"] = "Dataset Standar (Credit Card Customer Data.csv)"
                    st.session_state["load_error"] = None
                    st.session_state["last_simulation"] = None
                    st.success("✅ Dataset berhasil di-reset sepenuhnya ke kondisi awal!")
                    st.rerun()
                else:
                    st.error(f"Gagal memuat ulang: {err}")


# ==============================================================================
# MODUL 7: TENTANG APLIKASI
# ==============================================================================
elif selected_page == "ℹ️ Tentang Aplikasi":
    st.header("ℹ️ Tentang Sistem & Tim Pengembang")
    st.markdown(
        """
        <div class="dashboard-header">
            <span class="header-badge">PROFIL SISTEM & INFORMASI PENGEMBANG</span>
            <p style="font-size: 15px; margin: 0; line-height: 1.6;">Dokumentasi lengkap mengenai tujuan pembuatan, susunan pengembang kelompok, spesifikasi teknologi, serta kepatuhan akademik proyek.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_about1, col_about2 = st.columns([1.1, 1])

    with col_about1:
        st.markdown(
            """
            <div class="analytics-card">
                <h4>🎯 Tujuan & Latar Belakang Aplikasi</h4>
                <p style="color: #334155; font-size: 13.5px; line-height: 1.6;">
                    Aplikasi ini dirancang sebagai tugas proyek praktikum pengolahan dan analisis data 
                    guna mengeksplorasi portofolio nasabah kartu kredit secara komprehensif.
                    Melalui dashboard ini, praktikan dan pemangku kepentingan dapat mempelajari pola segmentasi perilaku, 
                    hubungan antarvariabel interaksi nasabah dengan bank, serta kecenderungan penetapan batas kredit.
                </p>
                <div style="background-color: #EFF6FF; border-left: 4px solid #3B82F6; padding: 12px; border-radius: 6px; margin-top: 12px; font-size: 13px; color: #1E40AF;">
                    <strong>Pernyataan Akademik:</strong> Aplikasi ini merupakan produk penelitian akademik. 
                    Tidak ada model penetapan kelayakan kredit resmi atau keputusan finansial mengikat yang dihasilkan oleh sistem ini.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="analytics-card">
                <h4>👥 Tim Pengembang (Kelompok 5)</h4>
                <p style="color: #64748B; font-size: 13px; margin-bottom: 12px;">
                    Program Studi Teknik Informatika, Semester 5, Universitas Pamulang.
                </p>
                <div style="font-size: 13.5px; color: #1E293B; line-height: 1.8;">
                    1. <strong>Ridwan Ramadhani</strong> — NIM: <code>241011400477</code> (Mahasiswa Pengembang)<br>
                    2. <strong>Sihabudin Firmansyah</strong> — NIM: <code>241011400486</code><br>
                    3. <strong>Dendi Bayu Saputra</strong> — NIM: <code>241011400468</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_about2:
        st.markdown(
            """
            <div class="analytics-card">
                <h4>🛠️ Spesifikasi Teknologi & Pustaka</h4>
                <ul style="color: #334155; font-size: 13.5px; line-height: 1.8; margin-bottom: 0; padding-left: 20px;">
                    <li><strong>Python 3.10+</strong> — Bahasa pemrograman inti</li>
                    <li><strong>Streamlit</strong> — Kerangka kerja web dashboard responsif</li>
                    <li><strong>Pandas & NumPy</strong> — Pengolahan dan agregasi data tabular</li>
                    <li><strong>Matplotlib</strong> — Pembuatan visualisasi matriks korelasi heatmap</li>
                    <li><strong>Altair</strong> — Visualisasi scatter interaktif berbasis Vega-Lite</li>
                    <li><strong>Plotly Express</strong> — Histogram distribusi dan diagram box plot interaktif</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="analytics-card">
                <h4>📁 Ringkasan Dataset Aktual</h4>
                <table style="width: 100%; font-size: 13px; color: #334155; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 6px 0;"><strong>Nama Berkas:</strong></td>
                        <td style="text-align: right;"><code>Credit Card Customer Data.csv</code></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 6px 0;"><strong>Jumlah Rekaman:</strong></td>
                        <td style="text-align: right;">{len(active_df):,} baris</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 6px 0;"><strong>Jumlah Kolom:</strong></td>
                        <td style="text-align: right;">{len(active_df.columns)} atribut</td>
                    </tr>
                    <tr>
                        <td style="padding: 6px 0;"><strong>Status Keamanan:</strong></td>
                        <td style="text-align: right; color: #16A34A; font-weight: 600;">Data Publik / Masking Enabled</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# FOOTER DASHBOARD
# ==============================================================================
st.markdown(
    """
    <div class="footer-container">
        Sistem Analisis & Eksplorasi Data Kartu Kredit Nasabah © 2026 | Kelompok 5 — Teknik Informatika Universitas Pamulang<br>
        Ridwan Ramadhani (241011400477) • Sihabudin Firmansyah (241011400486) • Dendi Bayu Saputra (241011400468)
    </div>
    """,
    unsafe_allow_html=True,
)
