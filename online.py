from pyngrok import ngrok
import os
import time

# ==========================================================
# PERHATIKAN: Token harus diapit tanda kutip dua ("...")
# Saya sudah masukkan token dari screenshot Anda di bawah ini:
NGROK_TOKEN = "38CnqZj37c6Vm1F2bdsqroGdchX_2Kis5uppXeXhWDTiYhMrS"
# ==========================================================

print("⏳ Sedang mencoba menghubungkan ke Internet (Ngrok)...")

try:
    # 1. Setting Token
    ngrok.set_auth_token(NGROK_TOKEN)

    # 2. Buka Tunnel
    public_url = ngrok.connect(8501).public_url
    
    print("="*50)
    print(f"🌍 BERHASIL ONLINE! Klik link ini: {public_url}")
    print("="*50)
    print("JANGAN TUTUP TERMINAL INI AGAR WEBSITE TETAP JALAN.")
    
    # 3. Jalankan Aplikasi Streamlit
    os.system("python -m streamlit run app.py")
    
except Exception as e:
    print("❌ Terjadi Error:")
    print(e)