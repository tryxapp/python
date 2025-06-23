import os

def extract_logins(file_path):
    logins = {
        'chiangmaipao': []
    }

    print(f"\nMemproses file: {file_path}")

    encodings = ['utf-8', 'utf-8-sig', 'latin-1']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc, errors='ignore') as file:
                for line in file:
                    line = line.strip().lower()
                    if not line:
                        continue
                    if 'chiangmaipao.go.th' in line:
                        logins['chiangmaipao'].append(line)
            break
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    else:
        print(f"❌ Gagal membaca file: {file_path} (encoding tidak cocok)")

    return logins

def save_logins_to_file(logins):
    result_folder = "result"
    os.makedirs(result_folder, exist_ok=True)

    for category, data in logins.items():
        if not data:
            continue

        file_path = os.path.join(result_folder, f"{category}.txt")

        existing = set()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip().lower()
                    if line:
                        existing.add(line)

        with open(file_path, 'a', encoding='utf-8') as file:
            for line in data:
                if line not in existing:
                    file.write(line + '\n')
                    existing.add(line)

def main():
    folder_path = 'ulp'

    if not os.path.exists(folder_path):
        print(f"❌ Folder '{folder_path}' tidak ditemukan.")
        return

    txt_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.txt')]

    if not txt_files:
        print("❌ Tidak ada file .txt di dalam folder 'ulp'.")
        return

    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        logins = extract_logins(file_path)
        save_logins_to_file(logins)

    print("\n✅ Proses selesai! Hasil disimpan dalam folder 'result' sesuai kategori.")

if __name__ == "__main__":
    main()
