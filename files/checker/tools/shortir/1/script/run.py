import os

def extract_logins(file_path):
    logins = {
        'wordpress': [], 'ftp': [], 'cpanel': [], 'whm': [], 'plesk': [], 'drupal': [], 'cyberpanel': [], 'zpanel': [],
        'joomla': [], 'directadmin': [], 'web-admin': [], 'aapanel': [], 'clientarea': [], 'Cms-Website': [], 'sar': [],
        'smss': [], 'moodle': [], 'zcom': [], 'bigdata': [], 'chiangmaipao': [], 'th': [], 'id': [], 'gov': [], 'edu': [], 
        'br': []
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
                    if 'wp-admin' in line or 'wp-login.php' in line or 'wp-content' in line or 'wp-includes' in line:
                        logins['wordpress'].append(line)
                    if 'ftp://' in line:
                        logins['ftp'].append(line)
                    if ':2082' in line or ':2083' in line or '/cpanel.' in line:
                        logins['cpanel'].append(line)
                    if ':2086' in line or ':2087' in line or '/whm.' in line:
                        logins['whm'].append(line)
                    if '/login_up.php' in line or ':8443' in line:
                        logins['plesk'].append(line)
                    if '/user/login' in line or 'drupal' in line or '/core/' in line:
                        logins['drupal'].append(line)
                    if ':7080' in line:
                        logins['cyberpanel'].append(line)
                    if 'zpanel' in line:
                        logins['zpanel'].append(line)
                    if '/administrator' in line or 'joomla' in line or 'com_content' in line: 
                        logins['joomla'].append(line)
                    if ':2222' in line:
                        logins['directadmin'].append(line)
                    if '/web-admin' in line:
                        logins['web-admin'].append(line)
                    if ':7800/login' in line:
                        logins['aapanel'].append(line)
                    if 'clientarea.php' in line:
                        logins['clientarea'].append(line)
                    if '.id/index.php/auth/signin' in line:
                        logins['Cms-Website'].append(line)
                    if 'sar.' in line:
                        logins['sar'].append(line)
                    if 'smss.' in line:
                        logins['smss'].append(line)
                    if 'moodle.' in line:
                        logins['moodle'].append(line)
                    if '.z.com' in line:
                        logins['zcom'].append(line)
                    if 'bigdata.' in line:
                        logins['bigdata'].append(line)
                    if 'chiangmaipao.go.th/cmtrack/' in line:
                        logins['chiangmaipao'].append(line)
                    if '.th' in line:
                        logins['th'].append(line)
                    if '.id' in line:
                        logins['id'].append(line)
                    if '.gov' in line:
                        logins['gov'].append(line)
                    if '.edu' in line:
                        logins['edu'].append(line)
                    if '.br' in line:
                        logins['br'].append(line)
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
