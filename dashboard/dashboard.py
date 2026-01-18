import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import streamlit as st

# KONFIGURASI HALAMAN 
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# STYLE CSS 
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# HELPER FUNCTIONS 
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='date').agg({
        "total_count": "sum",
        "casual_hourly": "sum",
        "registered_hourly": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    return daily_orders_df

def create_hourly_trend_df(df):
    return df.groupby("hour").total_count.mean().reset_index()

def create_by_weather_df(df):
    return df.groupby("weather_condition").total_count.mean().sort_values(ascending=False).reset_index()

def create_by_season_df(df):
    return df.groupby("season").total_count.mean().sort_values(ascending=False).reset_index()

def create_rfm_df(df):
    return df.groupby('workingday_hourly')[['casual_hourly', 'registered_hourly']].mean().reset_index()

# LOAD DATA 
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by="date", inplace=True)
    return df

all_df = load_data()

# SIDEBAR DESIGN
with st.sidebar:
    st.header("🚲 Bike Sharing Dashboard")
    st.markdown("")
    
    st.subheader("Filter Data")
    
    # Filter Rentang Waktu
    with st.expander("📅 Rentang Waktu", expanded=True):
        min_date = all_df["date"].min()
        max_date = all_df["date"].max()
        
        start_date, end_date = st.date_input(
            label='Pilih Tanggal',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    # Filter Musim
    with st.expander("🍂 Filter Musim", expanded=True):
        # Ambil daftar musim unik
        season_list = all_df['season'].unique().tolist()
        
        # Checkbox untuk pilih semua
        is_check_all = st.checkbox("Pilih Semua Musim", value=True)
        
        if is_check_all:
            selected_season = season_list # Jika dicentang, pakai semua musim
        else:
            selected_season = st.multiselect(
                'Pilih Musim:',
                season_list,
                default=season_list
            )

# LOGIKA FILTER DATA 
main_df = all_df[
    (all_df["date"] >= str(start_date)) & 
    (all_df["date"] <= str(end_date)) &
    (all_df['season'].isin(selected_season))
]

# MAIN DASHBOARD CONTENT 

st.title("📊 Bike Sharing Analytics")
st.markdown("Analisis interaktif performa penyewaan sepeda.")

#  PENANGANAN DATA KOSONG
if main_df.empty:
    st.warning("⚠️ Data kosong! Silakan pilih filter musim atau rentang tanggal yang lain.")
    # Set nilai default 0 agar tidak error nan
    total_orders = 0
    avg_daily = 0
    total_registered = 0
    total_casual = 0
else:
    # Siapkan Dataframe Agregat jika data ada
    daily_orders_df = create_daily_orders_df(main_df)
    hourly_trend_df = create_hourly_trend_df(main_df)
    weather_df = create_by_weather_df(main_df)
    season_df = create_by_season_df(main_df)
    user_segment_df = create_rfm_df(main_df)

    # Hitung Metrik
    total_orders = daily_orders_df.total_count.sum()
    avg_daily = round(daily_orders_df.total_count.mean(), 0)
    total_registered = daily_orders_df.registered_hourly.sum()
    total_casual = daily_orders_df.casual_hourly.sum()

# KPI / METRICS
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sewa", value=f"{total_orders:,}")

with col2:
    # Handle NaN display specifically for float
    value_display = f"{avg_daily:,.0f}" if pd.notna(avg_daily) else "0"
    st.metric("Rata-rata Harian", value=value_display)

with col3:
    st.metric("Member Terdaftar", value=f"{total_registered:,}")

with col4:
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

st.markdown("")

# Jika data kosong, hentikan eksekusi visualisasi di bawah ini
if main_df.empty:
    st.stop()

#  VISUALISASI 
tab_tren, tab_cuaca, tab_user = st.tabs(["📈 Tren & Jam Sibuk", "🌤️ Cuaca & Musim", "👥 Profil Pengguna"])

# TAB 1: TREN
with tab_tren:
    st.subheader("Tren Penyewaan & Jam Sibuk")
    
    # Chart 1: Daily Trend
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(
        daily_orders_df["date"],
        daily_orders_df["total_count"],
        linewidth=2,
        color="#4A90E2"
    )
    ax.set_title("Pergerakan Jumlah Penyewa Harian")
    ax.set_ylabel("Total Penyewa")
    ax.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig)
    
    # Chart 2: Hourly Trend (Rush Hour)
    st.markdown("#### Analisis Jam Sibuk (Rush Hour)")
    fig, ax = plt.subplots(figsize=(16, 5))
    sns.lineplot(
        x="hour",
        y="total_count",
        data=hourly_trend_df,
        marker='o',
        linewidth=3,
        color="#FF6B6B",
        ax=ax
    )
    ax.set_xticks(range(0, 24))
    ax.set_ylabel("Rata-rata Penyewa")
    ax.set_xlabel("Jam (00:00 - 23:00)")
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Highlight Peak Hours
    ax.axvline(x=8, color='black', linestyle='--', alpha=0.3)
    ax.axvline(x=17, color='black', linestyle='--', alpha=0.3)
    st.pyplot(fig)

# TAB 2: CUACA
with tab_cuaca:
    st.subheader("Pengaruh Faktor Lingkungan")
    
    # Menggunakan container agar manajemen layout lebih stabil
    with st.container():
        col1, col2 = st.columns(2)
        
        #  Grafik (Cuaca) 
        with col1:
            st.markdown("**Statistik Berdasarkan Cuaca**")
            fig, ax = plt.subplots(figsize=(6, 5))
            colors_weather = ["#90CAF9", "#CFD8DC", "#FFAB91", "#FFCCBC"]
            
            if not weather_df.empty:
                sns.barplot(
                    x="total_count", 
                    y="weather_condition",
                    data=weather_df,
                    palette=colors_weather,
                    ax=ax
                )
            ax.set_xlabel("Rata-rata Penyewa", fontsize=10)
            ax.set_ylabel(None)
            ax.tick_params(axis='y', labelsize=10)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            
        #  Grafik (Musim) 
        with col2:
            st.markdown("**Statistik Berdasarkan Musim**")
            fig, ax = plt.subplots(figsize=(6, 5))
            
            if not season_df.empty:
                sns.barplot(
                    x="season", 
                    y="total_count", 
                    data=season_df,
                    palette="viridis",
                    ax=ax
                )
            ax.set_xlabel(None)
            ax.set_ylabel("Rata-rata Penyewa", fontsize=10)
            sns.despine()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

# TAB 3: USER PROFILE
with tab_user:
    st.subheader("Perbandingan Tipe Pengguna")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Melt Dataframe
    user_segment_melted = user_segment_df.melt(
        id_vars='workingday_hourly', 
        var_name='User Type', 
        value_name='Average Rentals'
    )
    
    sns.barplot(
        data=user_segment_melted,
        x='workingday_hourly',
        y='Average Rentals',
        hue='User Type',
        palette=['#64B5F6', '#FFB74D']
    )
    
    ax.set_title("Hari Kerja vs Hari Libur")
    ax.set_ylabel("Rata-rata Penyewa")
    ax.set_xlabel(None)
    ax.legend(title="Tipe Pengguna")
    st.pyplot(fig)
    
    with st.expander("💡 Lihat Penjelasan Insight"):
        st.write(
            """
            - **Registered Users (Member)**: Mendominasi penggunaan pada **Hari Kerja**. Ini menunjukkan sepeda digunakan sebagai sarana transportasi utama untuk bekerja/sekolah.
            - **Casual Users (Umum)**: Mengalami lonjakan signifikan pada **Hari Libur**, yang mengindikasikan penggunaan untuk rekreasi.
            """
        )

#  7. FOOTER
st.caption("Copyright © 2026 Naufal Daffa Erlangga")