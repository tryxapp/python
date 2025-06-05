import base64
import os

def obfuscate_script(input_path):
    if not os.path.isfile(input_path):
        print("File tidak ditemukan!")
        return

    file_name = os.path.basename(input_path)
    name_part, ext = os.path.splitext(file_name)
    ext = ext.lstrip('.')  # hapus titik dari ekstensi

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            original_code = f.read()
    except UnicodeDecodeError:
        print("File tidak bisa dibaca sebagai teks. Pastikan file bukan binary.")
        return

    # Encode isi file ke Base64
    encoded_code = base64.b64encode(original_code.encode()).decode()

    # Template hasil obfuscate
    obfuscated = f"""import base64 as b64;exec((lambda z:b64.b64decode(z).decode())(
    b'{encoded_code}'
))"""

    # Nama file output
    output_path = f"obf{name_part}.{ext}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(obfuscated)

    print(f"✅ Script berhasil diobfuscate ke: {output_path}")

# Menjalankan program
if __name__ == "__main__":
    file_input = input("Masukkan nama file script yang ingin di-obfuscate (dengan ekstensi): ").strip()
    obfuscate_script(file_input)
