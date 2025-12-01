import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

# --- កំណត់រចនាសម្ព័ន្ធ (Configuration) ---
BOT_TOKEN = '8322086006:AAFF2-CuOWMNRcG3AYuhatKWSb5yVCOaFso'  # <--- ដាក់ Token របស់អ្នកនៅទីនេះ

# កំណត់ការបង្ហាញ Log ដើម្បីងាយស្រួលមើលកំហុស
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- មុខងារ Download វីដេអូ (Core Logic) ---
def download_tiktok(url):
    """
    Download វីដេអូពី TikTok ដោយប្រើ yt-dlp
    """
    output_filename = "video.mp4"
    
    # ជម្រើសសម្រាប់ការ Download
    ydl_opts = {
        'outtmpl': output_filename,    # ឈ្មោះឯកសារ
        'format': 'bestvideo+bestaudio/best', # យកគុណភាពល្អបំផុត
        'noplaylist': True,            # មិន Download មួយ Playlist
        'overwrites': True,            # សរសេរជាន់លើឯកសារចាស់
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_filename
    except Exception as e:
        print(f"Error downloading: {e}")
        return None

# --- មុខងារឆ្លើយតបរបស់ Bot (Handlers) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "សួស្តី! ផ្ញើ Link វីដេអូ TikTok មកខ្ញុំ ខ្ញុំនឹង Download ជូនអ្នកភ្លាមៗ។"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # ពិនិត្យមើលថាជា Link TikTok ដែរឬទេ
    if "tiktok.com" in url:
        status_msg = await update.message.reply_text("កំពុង Download... សូមរង់ចាំបន្តិច ⏳")
        
        # ចាប់ផ្តើម Download
        file_path = download_tiktok(url)
        
        if file_path and os.path.exists(file_path):
            try:
                await status_msg.edit_text("កំពុង Upload ចូល Telegram... 🚀")
                # ផ្ញើវីដេអូទៅកាន់ User
                await update.message.reply_video(video=open(file_path, 'rb'))
                await status_msg.delete() # លុបសារ "កំពុង Download" ចោល
                
                # លុបឯកសារចេញពីកុំព្យូទ័រវិញ ដើម្បីកុំឱ្យពេញ Space
                os.remove(file_path)
            except Exception as e:
                await status_msg.edit_text(f"មានបញ្ហាក្នុងការផ្ញើវីដេអូ: {e}")
        else:
            await status_msg.edit_text("បរាជ័យក្នុងការ Download។ សូមពិនិត្យ Link របស់អ្នកម្តងទៀត។")
    else:
        await update.message.reply_text("សួស្តី! ផ្ញើ Link វីដេអូ TikTok មកខ្ញុំ ខ្ញុំនឹង Download ជូនអ្នកភ្លាមៗ! សូមផ្ញើតែ Link មកប៉ុណ្ណោះ!")

# --- ផ្នែកដំណើរការ Bot (Main) ---
if __name__ == '__main__':
    # បង្កើត Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # បន្ថែម Handlers
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("Bot កំពុងដំណើរការ...")
    # រត់ Bot
    application.run_polling()
