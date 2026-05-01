#!/usr/bin/env python3
"""
Advanced Telegram Background Removal Bot
Removes backgrounds from images and resizes to 100x100 PNG
Built with Pyrogram, rembg, and Pillow
"""

import os
import io
import logging
import threading

from pyrogram import Client, filters
from pyrogram.types import Message
from rembg import remove, new_session
from PIL import Image
from flask import Flask

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENVIRONMENT VARIABLES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API_ID = int(os.getenv("36811424", "0"))
API_HASH = os.getenv("f28edfab583936ea62d6b458f754a4bd", "")
BOT_TOKEN = os.getenv("8683358561:AAHe8V3EQwx0JkTaue_41kM3Zkpc7FfYRrU", "")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    logger.error("Missing required environment variables: API_ID, API_HASH, BOT_TOKEN")
    raise ValueError("Please set API_ID, API_HASH, and BOT_TOKEN environment variables")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FLASK KEEP-ALIVE SERVER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080, debug=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
logger.info("Flask keep-alive server started on port 8080")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PYROGRAM BOT CLIENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
bot = Client(
    "background_remover_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=4,
    max_bots=1
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PREMIUM WELCOME MESSAGE - /start
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name or "𝐔𝐬𝐞𝐫"
    
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    
    status = "𝐔𝐬𝐞𝐫"
    if user_id == 123456789:
        status = "𝐀𝐝𝐦𝐢𝐧"
    
    welcome_text = f"""
╔═══《 🎉 𝐖𝐞𝐥𝐜𝐨𝐦𝐞! 》═══╗

👤 𝐔𝐬𝐞𝐫: {first_name}
🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}
🌟 𝐒𝐭𝐚𝐭𝐮𝐬: {status}

╰═══════《 🤖 》═══════╝

𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 {bot_name}

📌 𝐀𝐛𝐨𝐮𝐭 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭:
• 🎨 𝐁𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐑𝐞𝐦𝐨𝐯𝐞𝐫
• 📐 𝐀𝐮𝐭𝐨 𝐑𝐞𝐬𝐢𝐳𝐞 (𝟏𝟎𝟎𝐱𝟏𝟎𝟎)
• ⚡ 𝐅𝐚𝐬𝐭 & 𝐇𝐢𝐠𝐡 𝐐𝐮𝐚𝐥𝐢𝐭𝐲
• 📂 𝐒𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝐉𝐏𝐆 / 𝐏𝐍𝐆

━━━━━━━━━━━━━━━━━━━━━━

✅ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐫𝐚𝐧𝐭𝐞𝐝!
𝐘𝐨𝐮𝐫 𝐛𝐨𝐭 𝐢𝐬 𝐫𝐞𝐚𝐝𝐲 𝐭𝐨 𝐮𝐬𝐞.

📌 𝐐𝐮𝐢𝐜𝐤 𝐆𝐮𝐢𝐝𝐞:
• 📤 𝐒𝐞𝐧𝐝 𝐚𝐧 𝐢𝐦𝐚𝐠𝐞
• 🤖 𝐁𝐨𝐭 𝐰𝐢𝐥𝐥 𝐫𝐞𝐦𝐨𝐯𝐞 𝐛𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝
• 📐 𝐈𝐭 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐫𝐞𝐬𝐢𝐳𝐞𝐝 𝐭𝐨 𝟏𝟎𝟎𝐱𝟏𝟎𝟎
• 📥 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐲𝐨𝐮𝐫 𝐫𝐞𝐬𝐮𝐥𝐭

⚠️ 𝐍𝐨𝐭𝐞:
𝐎𝐧𝐥𝐲 𝐢𝐦𝐚𝐠𝐞 𝐟𝐢𝐥𝐞𝐬 𝐚𝐫𝐞 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐞𝐝.
"""
    await message.reply_text(welcome_text)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELP COMMAND - /help
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@bot.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    help_text = """
📚 𝐇𝐞𝐥𝐩 - 𝐁𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐑𝐞𝐦𝐨𝐯𝐞𝐫 𝐁𝐨𝐭

┏━━━━━━━━━━━━━━━━━━┓
┃  𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄  ┃
┗━━━━━━━━━━━━━━━━━━┛

📤 𝐒𝐞𝐧𝐝 𝐚𝐧 𝐢𝐦𝐚𝐠𝐞:
• 𝐏𝐡𝐨𝐭𝐨 𝐨𝐫 𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭
• 𝐉𝐏𝐆, 𝐏𝐍𝐆, 𝐨𝐫 𝐉𝐏𝐄𝐆
• 𝐁𝐨𝐭 𝐚𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜𝐚𝐥𝐥𝐲 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐞𝐬

🤖 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠:
• 𝐑𝐞𝐦𝐨𝐯𝐞𝐬 𝐛𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝
• 𝐑𝐞𝐬𝐢𝐳𝐞𝐬 𝐭𝐨 𝟏𝟎𝟎𝐱𝟏𝟎𝟎
• 𝐎𝐮𝐭𝐩𝐮𝐭 𝐢𝐧 𝐏𝐍𝐆 𝐟𝐨𝐫𝐦𝐚𝐭

━━━━━━━━━━━━━━━━━━━━

📌 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
/𝐬𝐭𝐚𝐫𝐭 - 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞
/𝐡𝐞𝐥𝐩 - 𝐒𝐡𝐨𝐰 𝐭𝐡𝐢𝐬 𝐠𝐮𝐢𝐝𝐞

━━━━━━━━━━━━━━━━━━━━

⚠️ 𝐍𝐨𝐭𝐞:
𝐎𝐧𝐥𝐲 𝐢𝐦𝐚𝐠𝐞 𝐟𝐢𝐥𝐞𝐬 𝐚𝐫𝐞 𝐚𝐜𝐜𝐞𝐩𝐭𝐞𝐝.
"""
    await message.reply_text(help_text)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IMAGE PROCESSING FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
async def process_image(input_path: str, output_path: str):
    """Process image: remove background and resize to 100x100 with center crop"""
    
    # Read input image
    with open(input_path, 'rb') as f:
        input_data = f.read()
    
    # Remove background using rembg
    output_data = remove(input_data)
    
    # Open processed image
    img = Image.open(io.BytesIO(output_data)).convert("RGBA")
    
    # Calculate resize maintaining aspect ratio
    target_size = (100, 100)
    
    # Create a new 100x100 transparent canvas
    new_img = Image.new("RGBA", target_size, (0, 0, 0, 0))
    
    # Resize image maintaining aspect ratio to fit within 100x100
    img.thumbnail(target_size, Image.Resampling.LANCZOS)
    
    # Calculate position to center the image
    paste_x = (target_size[0] - img.width) // 2
    paste_y = (target_size[1] - img.height) // 2
    
    # Paste resized image onto transparent canvas
    new_img.paste(img, (paste_x, paste_y), img if img.mode == 'RGBA' else None)
    
    # Save as PNG
    new_img.save(output_path, "PNG")
    
    logger.info(f"Image processed: {output_path}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PHOTO HANDLER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@bot.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    """Handle photos sent by users"""
    
    processing_msg = await message.reply_text("🔄 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐢𝐦𝐚𝐠𝐞...")
    
    try:
        # Download photo
        input_path = f"input_{message.id}.jpg"
        output_path = f"output_{message.id}.png"
        
        await message.download(file_name=input_path)
        
        # Process image
        await process_image(input_path, output_path)
        
        # Send processed image
        await message.reply_document(
            document=output_path,
            caption="✅ 𝐁𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐑𝐞𝐦𝐨𝐯𝐞𝐝 + 𝐑𝐞𝐬𝐢𝐳𝐞𝐝 𝐭𝐨 𝟏𝟎𝟎𝐱𝟏𝟎𝟎"
        )
        
        # Clean up
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
            
    except Exception as e:
        logger.error(f"Error processing photo: {e}")
        await message.reply_text("❌ 𝐄𝐫𝐫𝐨𝐫 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐢𝐦𝐚𝐠𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧.")
        
    finally:
        await processing_msg.delete()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DOCUMENT HANDLER (Image Documents)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@bot.on_message(filters.document)
async def handle_document(client: Client, message: Message):
    """Handle image documents sent by users"""
    
    # Check if file is an image
    mime_type = message.document.mime_type or ""
    file_name = message.document.file_name or ""
    
    if not (mime_type.startswith("image/") or file_name.lower().endswith(('.jpg', '.jpeg', '.png'))):
        await message.reply_text(
            "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐭𝐲𝐩𝐞!\n\n"
            "📌 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝:\n"
            "• 𝐉𝐏𝐆 𝐢𝐦𝐚𝐠𝐞𝐬\n"
            "• 𝐏𝐍𝐆 𝐢𝐦𝐚𝐠𝐞𝐬\n"
            "• 𝐉𝐏𝐄𝐆 𝐢𝐦𝐚𝐠𝐞𝐬"
        )
        return
    
    processing_msg = await message.reply_text("🔄 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐲𝐨𝐮𝐫 𝐢𝐦𝐚𝐠𝐞...")
    
    try:
        # Download document
        input_path = f"input_doc_{message.id}"
        output_path = f"output_doc_{message.id}.png"
        
        await message.download(file_name=input_path)
        
        # Process image
        await process_image(input_path, output_path)
        
        # Send processed image
        await message.reply_document(
            document=output_path,
            caption="✅ 𝐁𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐑𝐞𝐦𝐨𝐯𝐞𝐝 + 𝐑𝐞𝐬𝐢𝐳𝐞𝐝 𝐭𝐨 𝟏𝟎𝟎𝐱𝟏𝟎𝟎"
        )
        
        # Clean up temp files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
            
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        await message.reply_text("❌ 𝐄𝐫𝐫𝐨𝐫 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐢𝐦𝐚𝐠𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧.")
        
    finally:
        await processing_msg.delete()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ERROR HANDLER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@bot.on_message(filters.text & ~filters.command(["start", "help"]))
async def handle_text(client: Client, message: Message):
    """Handle non-command text messages"""
    await message.reply_text(
        "📌 𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐚𝐧 𝐢𝐦𝐚𝐠𝐞 𝐟𝐢𝐥𝐞!\n\n"
        "🤖 𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐨𝐧𝐥𝐲 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐞𝐬:\n"
        "• 📸 𝐏𝐡𝐨𝐭𝐨𝐬\n"
        "• 📄 𝐈𝐦𝐚𝐠𝐞 𝐃𝐨𝐜𝐮𝐦𝐞𝐧𝐭𝐬 (𝐉𝐏𝐆, 𝐏𝐍𝐆)\n\n"
        "💡 𝐔𝐬𝐞 /𝐡𝐞𝐥𝐩 𝐟𝐨𝐫 𝐦𝐨𝐫𝐞 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧."
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# START BOT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    logger.info("Starting Background Remover Bot...")
    print("""
╔═══════════════════════════════╗
║   🤖 𝐁𝐎𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃   ║
║   𝐁𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐑𝐞𝐦𝐨𝐯𝐞𝐫   ║
╚═══════════════════════════════╝
    """)
    bot.run()
