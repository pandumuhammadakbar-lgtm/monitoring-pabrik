import streamlit as st
import pandas as pd
import time
import os

# Konfigurasi Halaman Web
st.set_page_config(page_title="Sistem Pabrik Digital", layout="wide")

# Lokasi File Excel
FILE_EXCEL = 'data_pabrik.xlsx'

# --- FUNGSI UNTUK MEMBACA/MENULIS EXCEL ---
def load_data(sheet_name):
    try:
        return pd.read_excel(FILE_EXCEL, sheet_name=sheet_name)
    except:
        return pd.DataFrame()

def save_data(df, sheet_name):
    # Trik agar tidak menimpa sheet lain saat save
    with pd.ExcelWriter(FILE_EXCEL, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# --- JUDUL APLIKASI ---
st.title("🏭 Dashboard Monitoring & Inventory")
st.markdown("---")

# Membuat Tab (Menu Atas)
tab1, tab2 = st.tabs(["📊 Monitoring Mesin", "📦 Inventory Gudang"])

# ================= TAB 1: MONITORING MESIN =================
with tab1:
    st.header("Real-time Machine Status")
    
    # Tombol Refresh
    if st.button("🔄 Refresh Data Mesin"):
        st.rerun()

    # Load Data dari Excel Sheet 'Monitoring'
    df_mesin = load_data('Monitoring')

    # Tampilan Dashboard Kartu (Metric)
    col1, col2, col3 = st.columns(3)
    total_mesin = len(df_mesin)
    mesin_running = len(df_mesin[df_mesin['Status'] == 'RUNNING'])
    mesin_down = len(df_mesin[df_mesin['Status'] == 'STOP'])

    col1.metric("Total Mesin", f"{total_mesin} Unit")
    col2.metric("Mesin Running", f"{mesin_running} Unit", "On Track")
    col3.metric("Mesin Stop", f"{mesin_down} Unit", "-Alert", delta_color="inverse")

    # Tampilkan Tabel Warna-Warni
    st.subheader("Detail Parameter Mesin")
    
    # Fitur Edit Data Langsung di Tabel (Data Editor)
    edited_df = st.data_editor(
        df_mesin,
        num_rows="dynamic",
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status Operasi",
                options=["RUNNING", "STOP", "MAINTENANCE"],
                required=True,
            ),
            "Suhu": st.column_config.ProgressColumn(
                "Suhu Mesin (°C)",
                format="%d°C",
                min_value=0,
                max_value=100,
            ),
        },
        use_container_width=True
    )

    # Tombol Simpan Perubahan ke Excel
    if st.button("Simpan Perubahan Status Mesin"):
        save_data(edited_df, 'Monitoring')
        st.success("✅ Data Mesin berhasil disimpan ke Excel!")

# ================= TAB 2: INVENTORY GUDANG =================
with tab2:
    st.header("Manajemen Stok Sparepart")
    
    # Load Data Inventory
    df_inv = load_data('Inventory')

    # Layout 2 Kolom (Kiri: Form Input, Kanan: Tabel Data)
    col_kiri, col_kanan = st.columns([1, 2])

    with col_kiri:
        st.info("Input Barang Baru")
        with st.form("form_tambah_barang"):
            kode_input = st.text_input("Kode Barang")
            nama_input = st.text_input("Nama Barang")
            stok_input = st.number_input("Jumlah Stok", min_value=0, step=1)
            kategori_input = st.selectbox("Kategori", ["Consumable", "Sparepart", "Safety"])
            
            submit = st.form_submit_button("Simpan ke Database")

            if submit:
                # Logika Tambah Data
                new_data = pd.DataFrame([{
                    "Kode Barang": kode_input,
                    "Nama Barang": nama_input,
                    "Stok": stok_input,
                    "Kategori": kategori_input
                }])
                # Gabungkan data lama dan baru
                df_combined = pd.concat([df_inv, new_data], ignore_index=True)
                save_data(df_combined, 'Inventory')
                st.success("Barang ditambahkan!")
                time.sleep(1)
                st.rerun()

    with col_kanan:
        st.write("### Daftar Stok Saat Ini")
        
        # Fitur Pencarian
        search = st.text_input("🔍 Cari nama barang...")
        if search:
            df_inv = df_inv[df_inv['Nama Barang'].str.contains(search, case=False)]

        # Tampilkan Tabel Inventory
        st.dataframe(df_inv, use_container_width=True)
        
        # Alert Stok Menipis
        stok_tipis = df_inv[df_inv['Stok'] < 10]
        if not stok_tipis.empty:
            st.warning(f"⚠️ Peringatan: Ada {len(stok_tipis)} barang dengan stok menipis (<10)!")
            st.dataframe(stok_tipis)