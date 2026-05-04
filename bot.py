from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "8551468127:AAG48CRg8fJecQ_uMhM0S13aqsCTA1Pqbrw"

# Kim nechta odam qo‘shgan
invites = {}

# Kimni kim qo‘shgan
joined_by = {}


async def new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔍 DEBUG (terminalda chiqadi)
    print(update.message)

    if update.message.new_chat_members:
        inviter = update.message.from_user

        for user in update.message.new_chat_members:

            # Botlarni hisoblamaymiz
            if user.is_bot:
                continue

            # Kim qo‘shganini yozamiz
            joined_by[user.id] = inviter.id

            # Agar boshqa odam qo‘shgan bo‘lsa
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

app.run_polling()
