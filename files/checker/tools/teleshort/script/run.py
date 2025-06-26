import os
from aiogram import Bot, Dispatcher, executor, types
import asyncio

API_TOKEN = '7571503928:AAEg6cRznuQ2c3s5hFHTUjX2eSJpL8at6gY'  # Ganti dengan token Bot Telegram kamu
SEARCH_FOLDER = 'ulp'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Handler untuk command /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Halo! Kirimkan kata kunci yang ingin kamu cari di seluruh file .txt di folder 'ulp'.")

# Handler untuk pencarian kata kunci
@dp.message_handler()
async def handle_search(message: types.Message):
    keyword = message.text.strip().lower()
    if not keyword:
        await message.reply("⚠️ Kata kunci tidak boleh kosong.")
        return

    await message.reply(f"🔍 Mencari kata kunci: `{keyword}` di semua file .txt dalam folder 'ulp'...", parse_mode="Markdown")

    results = []
    for filename in os.listdir(SEARCH_FOLDER):
        if filename.endswith('.txt'):
            filepath = os.path.join(SEARCH_FOLDER, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if keyword in line.lower():
                            results.append(line.strip())
            except Exception as e:
                print(f"Gagal membaca {filename}: {e}")

    if not results:
        await message.reply(f"❌ Tidak ditemukan hasil untuk kata kunci: `{keyword}`", parse_mode="Markdown")
    else:
        result_file = f"hasil_{keyword.replace(' ', '_')}.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))

        await message.reply_document(open(result_file, 'rb'))
        os.remove(result_file)

if __name__ == '__main__':
    if not os.path.exists(SEARCH_FOLDER):
        print(f"❌ Folder '{SEARCH_FOLDER}' tidak ditemukan.")
    else:
        print("✅ Bot Telegram sedang berjalan...")
        executor.start_polling(dp, skip_updates=True)
