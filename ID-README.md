# ComfyUI-Resolution-Divider

Sebuah node utilitas cerdas untuk [ComfyUI](https://github.com/comfyanonymous/ComfyUI) yang dirancang untuk menghitung resolusi yang diperkecil (*downscaled*) sambil tetap menjaga rasio aspek asli secara ketat.

Node ini sangat penting untuk alur kerja (*workflow*) **Image-to-Video (I2V)** (seperti **Wan 2.2**), di mana penggunaan gambar input beresolusi tinggi sering menyebabkan error **OOM (Out of Memory)**. Node ini membantu kamu menemukan "titik manis" (misalnya, 480p atau 720p) secara instan tanpa perlu menghitung secara manual.

![Simple Resolution Divider Node](Node%20Resolution%20Divider.png)

## 🚀 Fitur Utama

*   **Parsing Cerdas:** Menerima berbagai format input seperti `1920 x 1080`, `1920x1080`, `1920 1080`, atau `1920, 1080`.
*   **Deteksi Resolusi Otomatis:** Pilih gambar dari folder input kamu atau **upload langsung** pada node. Node ini akan membaca dimensi (*resolusi*) secara otomatis.
*   **Perhitungan Real-Time:** Bagian "Live Result" diperbarui secara instan melalui JavaScript saat kamu menggeser slider tidak perlu menjalankan antrean (*queue*) prompt untuk melihat angkanya.
*   **Penghemat VRAM:** Sempurna untuk mengecilkan gambar yang besar seperti 4K/HD ke ukuran yang dapat ditangani oleh model berat (Wan 2.1, Wan 2.2, dll.) tanpa membuat gambar menjadi "gepeng".

## 📦 Instalasi

### Metode 1: Clone Manual
1. Buka direktori `custom_nodes` di dalam folder ComfyUI kamu.
2. Buka terminal/command prompt.
3. Jalankan perintah ini:
   ```bash
   git clone https://github.com/CraftBlack/ComfyUI-Resolution-Divider.git
   ```
4. Mulai ulang (*Restart*) ComfyUI.

## 🛠️ Cara Penggunaan

1.  **Tambahkan Node:**
    *   Klik kanan pada kanvas (area kosong) -> `Resolution Divider`.
2.  **Input:**
    *   **Opsi A:** Ketik resolusi secara manual di `res_string` (contoh: `1024x1024`).
    *   **Opsi B:** Klik "Upload" atau pilih gambar. Node akan mengisi resolusi secara otomatis.
3.  **Atur Pembagi (Divider):**
    *   Sesuaikan nilai float `divider`.
    *   `1.0` = Ukuran Asli.
    *   `1.5` = 1.5x lebih kecil (Rekomendasi).
    *   `2.0` = Setengah ukuran.

## 💡 Mengapa "Divider" (Pembagi)?

Berbeda dengan node "Scale" yang biasanya mengalikan (*upscale*), node ini **membagi** (*downscales*).

$$ \text{Ukuran Baru} = \frac{\text{Ukuran Asli}}{\text{Divider}} $$

Contoh:
*   Input: `1280 x 720`
*   Divider: `1.5`
*   Hasil: `853 x 480` (Zona aman 480p yang sempurna untuk model AI berat)

## 🤝 Kontribusi

Jangan ragu untuk mengirimkan *issue* atau *pull request* jika kamu memiliki ide untuk perbaikan!

## 📄 Lisensi

Lisensi MIT. Gratis untuk digunakan oleh siapa saja.
