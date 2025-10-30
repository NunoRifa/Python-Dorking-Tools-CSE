## Google CSE Dorking Tool
Alat dorking Google yang powerful dan efisien yang menggunakan Google Custom Search Engine (CSE) API untuk pemindaian permukaan web dan rekonesans yang komprehensif.

### Gambaran Umum
Google CSE Dorking Tool adalah alat rekonesans profesional yang dirancang untuk penetration tester dan peneliti keamanan. Alat ini melakukan Google dorking nyata menggunakan Google Custom Search Engine API resmi untuk menemukan sumber daya web yang terbuka, endpoint rentan, dan informasi sensitif di seluruh domain target.

### Fitur
- 🔍 Integrasi Google CSE: Pencarian Google nyata menggunakan API resmi
- 🎯 Dorking Tertarget: Pencocokan domain dan pola URL yang presisi
- ⚡ Multi-threading: Validasi URL bersamaan yang cepat
- 📊 Filter Status Code: Filter hasil berdasarkan kode status HTTP
- 📝 Laporan Komprehensif: Hasil detail dengan judul dan metadata
- 💾 Multi Format Export: Dukungan ekspor teks dan JSON
- 🛡️ Penanganan SSL: Penanganan error dan mekanisme retry yang robust
- 🎨 Output Berwarna: Tampilan terminal yang bersih dan terorganisir
- 🔧 Konfigurasi Mudah: Setup dan penggunaan yang sederhana

### Instalasi
**Instalasi Otomatis**
```bash
chmod +x install_dork_tool.sh
./install_dork_tool.sh
```

**Instalasi Manual**
```bash
# Clone repository
git clone https://github.com/yourusername/dork-tools.git
cd dork-tools

# Install dependencies
pip3 install requests beautifulsoup4 urllib3

# Buat executable
chmod +x dork_tools.py
```

**Dependensi Sistem (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install -y python3-requests python3-bs4 python3-urllib3
```

### Konfigurasi
**Setup Google API**
- Kunjungi [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/introduction)
- Buat project baru dan aktifkan Custom Search API
- Generate API key
- Buat Custom Search Engine di [Google CSE](https://cse.google.com/)
- Set environment variables:
```bash
GOOGLE_CSE_CX = "YOUR_GOOGLE_CSE_CX"
GOOGLE_PSE_API_KEY = "YOUR_GOOGLE_PSE_API_KEY"
```

### Penggunaan
**Contoh Dasar**
```bash
# Cari pola URL di semua domain
dorktool -u "?id=" -n 20

# Target domain spesifik dengan filter status
dorktool -d "example.com" -u "?page=" -s 200 301 302

# Pencarian domain wildcard dengan ekspor JSON
dorktool -d "*.co.id" -u "?view=" -n 15 -o results.txt --json

# Pemindaian high-throughput dengan multiple threads
dorktool -u "index.php?q=" -n 30 -s 200 --threads 20
```

**Argument Command Line**
| Argument | Deskripsi | Contoh |
| :------- | :------: | -------: |
| `-d, --domain` | Domain target (mendukung wildcard: `*.co.id`) | `-d "example.com"` |
| `-u, --url-pattern` | Pola URL yang dicari (wajib) | `-u "?id="` |
| `-s, --status-codes` | Kode status HTTP untuk filter | `-s 200 301 302` |
| `-n, --number` | Jumlah hasil yang dikumpulkan | `-n 50` |
| `-o, --output` | File output untuk menyimpan hasil | `-o scan_results.txt` |
| `--json` | Ekspor hasil sebagai JSON | `--json` |
| `--threads` | Jumlah thread bersamaan | `--threads 15` |

### Penggunaan Legal & Etis
**⚠️ Peringatan Penting**
- Alat ini ditujukan hanya untuk **penelitian keamanan legal** dan **penetration testing yang diizinkan**
- Dapatkan otorisasi yang tepat sebelum memindai domain apa pun
- Hormati robots.txt dan terms of service
- Pengembang tidak bertanggung jawab atas penyalahgunaan
- Patuhi semua hukum dan peraturan yang berlaku

---

**Dibuat oleh Nuno - Penetration Tester**
*Gunakan dengan bertanggung jawab dan etis 🔐*