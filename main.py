import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patches as path_effects

# Sayfa başlığı ve stil ayarları
st.set_page_config(page_title="Oda Sicakliği Dashboard", layout="wide") 

# Veri seti oluşturma
@st.cache_data
def create_initial_data():
    saatler = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(60)]
    gunler = ["Pazartesi", "Sali", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    num_entries = len(saatler) * len(gunler)

    veri = {
        "Gün": np.repeat(gunler, 1440),
        "Saat": saatler * 7,
        "Sicaklik": np.random.uniform(20, 30, num_entries),
        "Metrekare": np.repeat(50, num_entries),
        "Isik Sensörü": np.random.randint(0, 2, num_entries),
        "Hareket Sensörü": np.random.randint(0, 2, num_entries),
        "CO2 Sensörü": np.random.uniform(0, 1000, num_entries),
        "Nem Sensörü": np.random.uniform(30, 90, num_entries),
    }
    return pd.DataFrame(veri)

# Önce veri setini oluştur
df_original = create_initial_data()

# Session state başlangıcı (Sensör durumlarını tanımlıyoruz)
if "show_light_column" not in st.session_state:
    st.session_state["show_light_column"] = False
if "show_co2_column" not in st.session_state:
    st.session_state["show_co2_column"] = False
if "show_motion_column" not in st.session_state:
    st.session_state["show_motion_column"] = False
if "show_humidity_column" not in st.session_state:
    st.session_state["show_humidity_column"] = False
if "show_temperature_column" not in st.session_state:
    st.session_state["show_temperature_column"] = False
if "show_multi_sensor" not in st.session_state:
    st.session_state["show_multi_sensor"] = False
if "selected_day" not in st.session_state:
    st.session_state["selected_day"] = df_original['Gün'].unique().tolist()
if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = df_original[df_original['Gün'].isin(st.session_state["selected_day"])].copy()
if "selected_sensor" not in st.session_state:
    st.session_state["selected_sensor"] = None
if "selected_chart_type" not in st.session_state:
    st.session_state["selected_chart_type"] = None
if "show_table" not in st.session_state:
    st.session_state["show_table"] = True

# Modern ve göze hitap eden arka plan ve stil ayarları
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #1F2A44, #3B4A69);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        div.stButton > button:first-child {
            background-color: #8E44AD;
            color: white;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease-in-out;
            transform: scale(1);
            width: 100%;
            margin-bottom: 10px;
        }
        div.stButton > button:first-child:hover {
            background-color: #9B59B6;
            transform: scale(1.05);
        }
        div.block-container {
            padding-top: 2rem;
        }
        .stSidebar {
            background: linear-gradient(135deg, #16A085, #1ABC9C);
            padding: 20px;
            border-radius: 12px;
            color: white;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        }
        .stMarkdown, .stText, .stJson {
            color: white;
        }
        .stDataFrame {
            border-radius: 10px;
            padding: 10px;
            background-color: #1B2A34;
            color: #333333;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
        }
        .stTable th {
            background-color: #34495E;
            color: #FFFFFF;
        }
        .stTable td {
            background-color: #FFFFFF;
            color: #333333;
        }
        .stSlider div {
            color: white;
        }
        .stRadio div {
            color: white;
        }
        .stTextInput input {
            background-color: #34495E;
            color: white;
            border-radius: 5px;
        }
        .stSelectbox, .stMultiselect {
            background-color: #34495E;
            color: white;
            border-radius: 5px;
            text-align: center;
        }
        .stSelectbox > div > div {
            text-align: center;
        }
        .stSelectbox > div > div > div {
            text-align: center;
        }
        .stTextInput input:focus {
            border-color: #3498DB;
        }
        .section-title {
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.2em;
            font-weight: bold;
        }
        .stSelectbox > div {
            margin: 0 auto;
            width: 80%;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌡 Oda Sicakliği Dashboard")
st.markdown("<br>", unsafe_allow_html=True)

# Veri filtreleme fonksiyonu
@st.cache_data
def filter_data(df, selected_days):
    return df[df['Gün'].isin(selected_days)].copy()

# Grafik oluşturma fonksiyonları
@st.cache_data
def create_pie_chart(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    bins = [20, 22, 24, 26, 28, 30]
    labels = ["20-22°C", "22-24°C", "24-26°C", "26-28°C", "28-30°C"]
    df['Sicaklik Araliği'] = pd.cut(df['Sicaklik'], bins=bins, labels=labels)
    df['Sicaklik Araliği'].value_counts().plot(kind='pie', autopct='%1.1f%%', 
                                              colors=['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845'], ax=ax)
    ax.set_ylabel("")
    return fig

@st.cache_data
def create_line_chart(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.lineplot(x=df['Saat'], y=df['Sicaklik'], ax=ax, color='#3498DB', marker='o')
    ax.set_ylabel("Sicaklik (°C)")
    ax.set_title("Saatlik Ortalama Sicaklik", fontsize=14)
    plt.xticks(rotation=90, fontsize=10)
    return fig

@st.cache_data
def create_column_chart(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=df['Saat'], y=df['Sicaklik'], ax=ax, color='#8E44AD')
    ax.set_ylabel("Sicaklik (°C)")
    plt.xticks(rotation=90, fontsize=10)
    return fig

@st.cache_data
def create_light_sensor_chart(df):
    df_grouped = df.groupby("Saat")["Isik Sensörü"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Arka plan rengini ayarla
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('#F8F9FA')
    
    # Grid çizgilerini ayarla
    ax.grid(True, linestyle='--', alpha=0.3, color='#808080')
    
    # Sütunları çiz
    bars = sns.barplot(data=df_grouped, x="Saat", y="Isik Sensörü", ax=ax, 
                      color='#FFD700',  # Altın sarısı
                      edgecolor='#FFA500',  # Turuncu kenar
                      linewidth=1.5)
    
    # Sütunların üzerine değerleri yaz
    for i, v in enumerate(df_grouped["Isik Sensörü"]):
        ax.text(i, v + 0.01, f'{v:.2f}', ha='center', va='bottom', fontsize=8)
    
    # Eksen etiketlerini ve başlığı ayarla
    ax.set_title("Saatlik Işık Sensörü Durumu\n(0: Kapalı, 1: Açık)", 
                fontsize=14, pad=20, color='#333333', fontweight='bold')
    ax.set_xlabel("Saat", fontsize=12, color='#333333', labelpad=10)
    ax.set_ylabel("Işık Durumu", fontsize=12, color='#333333', labelpad=10)
    
    # Y ekseni aralığını 0-1 olarak ayarla ve grid çizgilerini ekle
    ax.set_ylim(-0.05, 1.05)
    ax.yaxis.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.yaxis.set_ticklabels(['Kapalı (0)', '0.25', '0.5', '0.75', 'Açık (1)'])
    
    # X ekseni etiketlerini düzenle
    plt.xticks(rotation=45, ha='right')
    
    # Grafik kenarlarını ayarla
    for spine in ax.spines.values():
        spine.set_color('#666666')
        spine.set_linewidth(1)
    
    # Grafik boyutlarını otomatik ayarla
    plt.tight_layout()
    
    return fig

@st.cache_data
def create_co2_sensor_chart(df):
    df_grouped = df.groupby("Saat")["CO2 Sensörü"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df_grouped, x="Saat", y="CO2 Sensörü", ax=ax, color='#27AE60')
    ax.set_ylabel("CO2 Seviyesi (ppm)")
    ax.set_title("Saatlik CO2 Sensörü Seviyesi", fontsize=14)
    plt.xticks(rotation=90)
    return fig

@st.cache_data
def create_motion_sensor_chart(df):
    df_grouped = df.groupby("Saat")["Hareket Sensörü"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df_grouped, x="Saat", y="Hareket Sensörü", ax=ax, color='#F39C12')
    ax.set_ylabel("Aktiflik Oranı (0-1)")
    ax.set_title("Saatlik Hareket Sensörü Aktiflik Oranı", fontsize=14)
    plt.xticks(rotation=90)
    return fig

@st.cache_data
def create_humidity_sensor_chart(df):
    df_grouped = df.groupby("Saat")["Nem Sensörü"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df_grouped, x="Saat", y="Nem Sensörü", ax=ax, color='#5DADE2')
    ax.set_ylabel("Nem Oranı (%)")
    ax.set_title("Saatlik Ortalama Nem Oranı", fontsize=14)
    plt.xticks(rotation=90)
    return fig

# Haftanın günlerine göre filtreleme
days = df_original['Gün'].unique()
if "selected_day" not in st.session_state:
    st.session_state["selected_day"] = days.tolist()
selected_day = st.multiselect("Gün Seçiniz:", days, default=st.session_state["selected_day"])

# Gün seçimi değiştiğinde filtrelenmiş veriyi güncelle
if selected_day != st.session_state["selected_day"]:
    st.session_state["df_filtered"] = df_original[df_original['Gün'].isin(selected_day)].copy()

# Eğer filtrelenmiş veri yoksa başlangıçta tanımla
if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = df_original[df_original['Gün'].isin(st.session_state["selected_day"])].copy()

df_filtered = st.session_state["df_filtered"].copy()

# Sensör ve grafik tipi seçimi
st.sidebar.markdown('<div class="section-title">📊 Sensör ve Grafik Seçimi</div>', unsafe_allow_html=True)

sensor_options = ["Sıcaklık", "Işık Sensörü", "CO2 Sensörü", "Hareket Sensörü", "Nem Sensörü"]
chart_options = ["Sütun Grafiği", "Çizgi Grafiği", "Pasta Grafiği"]

selected_sensor = st.sidebar.selectbox(
    "Görüntülemek istediğiniz sensörü seçin:",
    options=[""] + sensor_options,
    index=0,
    key="sensor_select"
)

# Boş satırlar ekle
st.sidebar.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

if selected_sensor:
    selected_chart_type = st.sidebar.selectbox(
        "Grafik tipini seçin:",
        options=[""] + chart_options,
        index=0,
        key="chart_select"
    )
    
    if selected_chart_type:
        st.session_state["selected_sensor"] = selected_sensor
        st.session_state["selected_chart_type"] = selected_chart_type
        st.session_state["show_table"] = False
    else:
        st.session_state["show_table"] = True
else:
    st.session_state["show_table"] = True

# Boş satırlar ekle
st.sidebar.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Ana tabloya dön butonu
if st.sidebar.button("🏠 Ana Tabloya Dön", key="back_to_table_button",
                    help="Ana veri tablosuna dön"):
    st.session_state["selected_sensor"] = None
    st.session_state["selected_chart_type"] = None
    st.session_state["show_table"] = True
    st.session_state["show_multiselect"] = False  # Çoklu sensör seçimini kapat
    
# Boş satırlar ekle
st.sidebar.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Çoklu sensör seçimi butonu
if st.sidebar.button("📊 Çoklu Sensör Seçimi", key="multiselect_button",
                    help="Birden fazla sensörü aynı grafikte göster"):
    st.session_state["show_multiselect"] = not st.session_state.get("show_multiselect", False)
    if st.session_state["show_multiselect"]:
        st.session_state["selected_sensor"] = None
        st.session_state["selected_chart_type"] = None
        st.session_state["show_table"] = False
    else:
        st.session_state["show_table"] = True

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Çoklu sensör seçimi için filtre
if st.session_state.get("show_multiselect", False):
    st.markdown("### 📊 Çoklu Sensör Grafiği")
    
    # Sensör seçim alanını ortala
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_sensors = st.multiselect(
            "Görüntülemek istediğiniz sensörleri seçin (en az 2 sensör seçmelisiniz):",
            options=sensor_options,
            default=[],
            key="multi_sensor_select"
        )
    
    if len(selected_sensors) >= 2:
        # Sensör adlarını veri setindeki karşılıklarına çevir
        sensor_mapping = {
            "Sıcaklık": "Sicaklik",
            "Işık Sensörü": "Isik Sensörü",
            "CO2 Sensörü": "CO2 Sensörü",
            "Hareket Sensörü": "Hareket Sensörü",
            "Nem Sensörü": "Nem Sensörü"
        }
        
        selected_sensors_mapped = [sensor_mapping[sensor] for sensor in selected_sensors]
        
        # Her sensör için değerleri normalize et
        normalized_data = {}
        for sensor in selected_sensors_mapped:
            values = df_filtered.groupby("Saat")[sensor].mean().values
            min_val = values.min()
            max_val = values.max()
            if max_val != min_val:
                normalized_data[sensor] = (values - min_val) / (max_val - min_val) * 100
            else:
                normalized_data[sensor] = values
        
        # Grafik oluştur
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Arka plan rengini ayarla
        ax.set_facecolor('#F0F8FF')
        fig.patch.set_facecolor('#F0F8FF')
        
        # Grid çizgilerini ayarla
        ax.grid(True, linestyle='--', alpha=0.3, color='#808080')
        
        # Saatleri indeks olarak kullan
        hours = df_filtered['Saat'].unique()
        x = np.arange(len(hours))
        width = 0.8 / len(selected_sensors_mapped)  # Her sensör için genişlik
        
        # Her sensör için renk tanımlamaları
        sensor_colors = {
            "Sicaklik": "#FF3333",    # Parlak Kırmızı
            "Isik Sensörü": "#FFD700", # Altın Sarısı
            "CO2 Sensörü": "#33CC33",  # Parlak Yeşil
            "Hareket Sensörü": "#FF8000", # Turuncu
            "Nem Sensörü": "#3399FF"   # Parlak Mavi
        }
        
        # Seçilen sensörleri çiz
        for i, sensor in enumerate(selected_sensors_mapped):
            sensor_color = sensor_colors[sensor]
            bars = ax.bar(x + i*width, normalized_data[sensor], width, 
                         label=sensor, 
                         color=sensor_color,
                         edgecolor=sensor_color,  # Sensörün kendi rengi ile kenar
                         linewidth=1.5,      # Kenar kalınlığı
                         alpha=0.9,          # Hafif şeffaflık
                         zorder=3)           # Sütunları grid çizgilerinin üzerine çiz
        
        # Eksen etiketlerini ve başlığı ayarla
        ax.set_ylabel("Normalize Edilmiş Değer (%)", fontsize=12, color='#333333', fontweight='bold')
        ax.set_title("Çoklu Sensör Grafiği (Normalize Edilmiş)", fontsize=16, color='#333333', fontweight='bold', pad=20)
        
        # X ekseni etiketlerini ayarla
        ax.set_xticks(x + width*(len(selected_sensors_mapped)-1)/2)
        ax.set_xticklabels(hours, rotation=90, fontsize=10, color='#333333')
        
        # Y ekseni etiketlerini ayarla
        ax.tick_params(axis='y', colors='#333333', labelsize=10)
        
        # Açıklama kutusunu ayarla
        legend = ax.legend(fontsize=10, 
                          loc='upper right', 
                          framealpha=0.95, 
                          facecolor='white', 
                          edgecolor='#CCCCCC')
        
        # Kenar çizgilerini ayarla
        for spine in ax.spines.values():
            spine.set_color('#666666')
            spine.set_linewidth(1.5)
        
        plt.tight_layout()
        st.pyplot(fig)
    elif len(selected_sensors) > 0:
        st.warning("Lütfen en az 2 sensör seçin.")
    else:
        st.info("Lütfen en az 2 sensör seçin.")

# Grafik gösterimi
if st.session_state["selected_sensor"] and st.session_state["selected_chart_type"]:
    sensor = st.session_state["selected_sensor"]
    chart_type = st.session_state["selected_chart_type"]
    
    st.markdown(f"### {sensor} - {chart_type}")
    
    # Sensör adını veri setindeki karşılığına çevir
    sensor_mapping = {
        "Sıcaklık": "Sicaklik",
        "Işık Sensörü": "Isik Sensörü",
        "CO2 Sensörü": "CO2 Sensörü",
        "Hareket Sensörü": "Hareket Sensörü",
        "Nem Sensörü": "Nem Sensörü"
    }
    
    sensor_data = sensor_mapping[sensor]
    
    if chart_type == "Sütun Grafiği":
        # Sütun grafiği için
        fig, ax = plt.subplots(figsize=(15, 8))
        sns.barplot(data=df_filtered, x="Saat", y=sensor_data, ax=ax, color="#3498DB")
        ax.set_title(f"{sensor} - Sütun Grafiği", fontsize=14)
        ax.set_xlabel("Saat", fontsize=12)
        ax.set_ylabel("Değer", fontsize=12)
        plt.xticks(rotation=90)
        plt.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)
        
    elif chart_type == "Çizgi Grafiği":
        # Çizgi grafiği için
        fig, ax = plt.subplots(figsize=(15, 8))
        sns.lineplot(data=df_filtered, x="Saat", y=sensor_data, ax=ax, color="#2ECC71", linewidth=2, marker='o')
        ax.set_title(f"{sensor} - Çizgi Grafiği", fontsize=14)
        ax.set_xlabel("Saat", fontsize=12)
        ax.set_ylabel("Değer", fontsize=12)
        plt.xticks(rotation=90)
        plt.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)
        
    else:  # Pasta Grafiği
        fig, ax = plt.subplots(figsize=(10, 10))
        # Veriyi kategorilere ayır
        if sensor_data == "Sicaklik":
            bins = [20, 22, 24, 26, 28, 30]
            labels = ["20-22°C", "22-24°C", "24-26°C", "26-28°C", "28-30°C"]
        else:
            # Diğer sensörler için değer aralıklarını otomatik belirle
            values = df_filtered[sensor_data]
            min_val = values.min()
            max_val = values.max()
            bins = np.linspace(min_val, max_val, 6)  # 5 dilim için 6 sınır
            labels = [f"{bins[i]:.1f}-{bins[i+1]:.1f}" for i in range(len(bins)-1)]
        
        df_filtered['Değer Aralığı'] = pd.cut(df_filtered[sensor_data], bins=bins, labels=labels)
        value_counts = df_filtered['Değer Aralığı'].value_counts()
        
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
        plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', colors=colors)
        plt.title(f"{sensor} - Değer Dağılımı", pad=20, fontsize=14)
        st.pyplot(fig)

# Tablo Görselleştirme
if st.session_state["show_table"]:
    st.markdown("### 📊 Sicaklik Verisi Tablosu")
    st.dataframe(
        df_filtered[["Gün", "Saat", "Sicaklik", "Metrekare", "Isik Sensörü", "Hareket Sensörü", "CO2 Sensörü", "Nem Sensörü"]],
        hide_index=True,
        use_container_width=True
    )

@st.cache_data
def detect_anomalies(df, column='Sicaklik', threshold=2.5):
    """
    Z-score tabanlı anomali tespiti
    """
    # Z-score hesaplama
    mean = df[column].mean()
    std = df[column].std()
    df['Z-score'] = (df[column] - mean) / std
    
    # Anomalileri tespit et
    df['Anomali'] = abs(df['Z-score']) > threshold
    df['Anomali_Degeri'] = np.where(df['Anomali'], df[column], np.nan)
    
    return df

@st.cache_data
def analyze_trends(df, column='Sicaklik', window=5):
    """
    Hareketli ortalama tabanlı trend analizi
    """
    # Hareketli ortalama hesaplama
    df['Hareketli_Ortalama'] = df[column].rolling(window=window).mean()
    
    # Trend yönü hesaplama
    df['Trend'] = np.where(df['Hareketli_Ortalama'] > df[column].shift(1), 'Yükseliş',
                          np.where(df['Hareketli_Ortalama'] < df[column].shift(1), 'Düşüş', 'Stabil'))
    
    return df

@st.cache_data
def create_anomaly_chart(df):
    """
    Anomali tespiti sonuçlarını görselleştiren grafik
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Normal veri noktaları
    ax.plot(df['Saat'], df['Sicaklik'], 'b-', label='Normal Değerler')
    
    # Anomali noktaları
    anomalies = df[df['Anomali']]
    ax.scatter(anomalies['Saat'], anomalies['Sicaklik'], 
              color='red', s=100, label='Anomaliler', zorder=5)
    
    # Z-score eşik çizgileri
    mean = df['Sicaklik'].mean()
    std = df['Sicaklik'].std()
    ax.axhline(y=mean + 2.5*std, color='r', linestyle='--', alpha=0.3, label='Üst Eşik')
    ax.axhline(y=mean - 2.5*std, color='r', linestyle='--', alpha=0.3, label='Alt Eşik')
    
    ax.set_title('Sıcaklık Anomalileri', fontsize=14)
    ax.set_xlabel('Saat')
    ax.set_ylabel('Sıcaklık (°C)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

@st.cache_data
def create_trend_chart(df):
    """
    Trend analizi sonuçlarını görselleştiren grafik
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Orijinal veri
    ax.plot(df['Saat'], df['Sicaklik'], 'b-', label='Sıcaklık')
    
    # Hareketli ortalama
    ax.plot(df['Saat'], df['Hareketli_Ortalama'], 'r--', label='Hareketli Ortalama')
    
    # Trend noktaları
    trend_colors = {'Yükseliş': 'g', 'Düşüş': 'r', 'Stabil': 'y'}
    for trend, color in trend_colors.items():
        mask = df['Trend'] == trend
        ax.scatter(df.loc[mask, 'Saat'], df.loc[mask, 'Sicaklik'], 
                  color=color, s=50, label=trend)
    
    ax.set_title('Sıcaklık Trend Analizi', fontsize=14)
    ax.set_xlabel('Saat')
    ax.set_ylabel('Sıcaklık (°C)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

# Ana dashboard arayüzü
st.sidebar.title("Analiz Seçenekleri")

# Anomali ve trend analizi için parametreler
st.sidebar.subheader("Anomali ve Trend Analizi")
anomaly_threshold = st.sidebar.slider("Anomali Tespiti Eşik Değeri (Z-score)", 1.5, 3.5, 2.5, 0.1)
trend_window = st.sidebar.slider("Trend Analizi Pencere Boyutu", 3, 15, 5, 1)

# Veriyi analiz et
df_analyzed = detect_anomalies(st.session_state["df_filtered"], threshold=anomaly_threshold)
df_analyzed = analyze_trends(df_analyzed, window=trend_window)

# Anomali ve trend analizi grafikleri
st.markdown("### 🔍 Anomali ve Trend Analizi")
col1, col2 = st.columns(2)

with col1:
    st.pyplot(create_anomaly_chart(df_analyzed))
    st.markdown("""
    **Anomali Tespiti:**
    - Kırmızı noktalar anormal sıcaklık değerlerini gösterir
    - Kesikli çizgiler Z-score eşik değerlerini gösterir
    - Eşik değeri yan panelden ayarlanabilir
    """)

with col2:
    st.pyplot(create_trend_chart(df_analyzed))
    st.markdown("""
    **Trend Analizi:**
    - Mavi çizgi gerçek sıcaklık değerlerini gösterir
    - Kırmızı kesikli çizgi hareketli ortalamayı gösterir
    - Renkli noktalar trend yönünü gösterir (Yeşil: Yükseliş, Kırmızı: Düşüş, Sarı: Stabil)
    """)

# Anomali istatistikleri
st.markdown("### 📊 Anomali İstatistikleri")
anomaly_stats = df_analyzed['Anomali'].value_counts()
st.write(f"Toplam veri noktası sayısı: {len(df_analyzed)}")
st.write(f"Anomali sayısı: {anomaly_stats.get(True, 0)}")
st.write(f"Anomali oranı: {anomaly_stats.get(True, 0)/len(df_analyzed)*100:.2f}%")

# Trend istatistikleri
st.markdown("### 📈 Trend İstatistikleri")
trend_stats = df_analyzed['Trend'].value_counts()
st.write("Trend dağılımı:")
st.bar_chart(trend_stats)