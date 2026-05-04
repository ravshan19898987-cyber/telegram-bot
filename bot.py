import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# 🔑 TOKEN environmentdan olinadi
TOKEN = os.getenv("BOT_TOKEN")

# Kim nechta odam qo‘shgan
invites = {}

# Kimni kim qo‘shgan
joined_by = {}


async def new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.new_chat_members:
        inviter = update.message.from_user

        for user in update.message.new_chat_members:

            if user.is_bot:
                continue

            joined_by[user.id] = inviter.id

            if inviter.id != user.id:
                invites[inviter.id] = invites.get(inviter.id, 0) + 1

                await update.message.reply_text(
                    f"👤 {inviter.full_name} → {user.full_name} ni qo‘shdi ✅"
                )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not invites:
        await update.message.reply_text("Hozircha hech kim hech kimni qo‘shmagan.")
        return

    text = "📊 Kim nechta odam qo‘shgan:\n\n"

    for user_id, count in invites.items():
        text += f"👤 ID: {user_id} — {count} ta odam\n"

    await update.message.reply_text(text)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_members))
app.add_handler(CommandHandler("stats", stats))

print("Bot ishga tushdi 🚀")  # log uchun

app.run_polling()
