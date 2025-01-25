from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import pandas as pd
import random
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

# --- Original Functions ---
def create_initial_dataset():
    check_frequency = [
        "Whenever I have a message", "Every two weeks", "Once a year", "Every six months", 
        "Whenever I have a message", "Whenever I have a message", "Every six months", 
        "Every three days", "Never", "Whenever I have a message", "Never", 
        "Whenever I have a message", "Whenever I have a message", "Rarely", 
        "Every three days", "Rarely", "Whenever I have a message", 
        "Every six months", "Whenever I have a message", "Every month", "Every week"
    ]
    response_probability = [
        "I don't reply", "30%", "I don't reply", "2%", 
        "I don't reply", "10%", "I don't reply", "I don't reply", 
        "I don't reply", "10%", "I don't reply", "10%", 
        "I reply to all", "I don't reply", "I don't reply", "I reply", 
        "I don't reply", "I reply to all", "I reply to all", 
        "20%", "10%"
    ]
    data = pd.DataFrame({
        "Check Frequency": check_frequency,
        "Response Probability": response_probability
    })
    return data

def map_scores(data):
    check_frequency_scores = {
        "Whenever I have a message": 100,
        "Every three days": 80,
        "Every week": 60,
        "Every two weeks": 50,
        "Every month": 40,
        "Every six months": 20,
        "Once a year": 10,
        "Rarely": 5,
        "Never": 0
    }
    response_probability_scores = {
        "I reply to all": 100,
        "I reply": 75,
        "30%": 30,
        "20%": 20,
        "10%": 10,
        "2%": 2,
        "I don't reply": 0
    }
    data["Check Frequency Score"] = data["Check Frequency"].map(check_frequency_scores)
    data["Response Probability Score"] = data["Response Probability"].map(response_probability_scores)
    return data

def calculate_read_probability(data):
    data["Read Probability"] = 0.7 * data["Check Frequency Score"] + 0.3 * data["Response Probability Score"]
    return data

def calculate_day_probabilities(data):
    days = {
        "Day 1": 1,
        "Day 3": 3,
        "Day 7": 7,
        "Day 14": 14,
        "Day 30": 30,
        "Day 90": 90,
        "Day 180": 180
    }
    results = {}
    for day_name, day_value in days.items():
        decay_factor = max(0, 1 - (day_value / 365))
        data[f"{day_name} Probability"] = data["Read Probability"] * decay_factor
        results[day_name] = data[f"{day_name} Probability"].mean()
    return results

# --- Create Plots ---
def create_probability_plot(data, title):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the data
    ax.plot(data.keys(), data.values(), color='royalblue', marker='o', linestyle='-', linewidth=2, markersize=8, label="Probability")

    # Adding grid for better readability
    ax.grid(True, linestyle='--', color='gray', alpha=0.7)

    # Adding title and labels
    ax.set_xlabel('Days', fontsize=12, fontweight='bold', color='darkblue')
    ax.set_ylabel('Probability (%)', fontsize=12, fontweight='bold', color='darkblue')
    ax.set_title(title, fontsize=14, fontweight='bold', color='darkblue')

    # Display legend
    ax.legend()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', dpi=300)
    image_stream.seek(0)
    plt.close()

    return image_stream

# --- Telegram Bot Handlers ---
async def start(update: Update, context: CallbackContext) -> None:
    # Create initial dataset
    data = create_initial_dataset()
    data = map_scores(data)
    data = calculate_read_probability(data)

    # Calculate initial statistics
    initial_avg_read_probability = data["Read Probability"].mean()
    initial_day_probabilities = calculate_day_probabilities(data)

    # Send initial explanation message
    initial_message = (
        "تو پیام اول، شانس اینکه دایرکت منو بخونی و جواب بدی رو می‌بینی. بعدش احتمال اینکه بعد از چند روز پیامم رو ببینی گفته شده. "
        "این احتمالات رو از داده‌هایی که خودم از چندین نفر مختلف جمع‌آوری کردم بدست اومده. تو پیام بعدش، یه شبیه‌سازی انجام شده "
        "که داده‌های منطقی و تصادفی رو به داده‌های قبلی اضافه می‌کنه و دوباره احتمالات رو محاسبه می‌کنه."
    )
    await update.message.reply_text(initial_message)

    # Prepare initial statistics response
    response = "📊 Initial Dataset Statistics:\n"
    response += f"🔢 Average Check Frequency Score: {data['Check Frequency Score'].mean():.2f}\n"
    response += f"💬 Average Response Probability Score: {data['Response Probability Score'].mean():.2f}\n"
    response += f"📈 Average Read Probability: {initial_avg_read_probability:.2f}\n\n"
    response += "🔹 Day-Specific Probabilities for Initial Dataset:\n"
    for day, prob in initial_day_probabilities.items():
        response += f"{day}: {prob:.2f}%\n"

    # Send the initial statistics
    await update.message.reply_text(response)

    # Create and send the probability plot for initial dataset
    plot_image_stream = create_probability_plot(initial_day_probabilities, "Initial Day-Specific Probabilities")

    # Reset the stream position before sending it
    plot_image_stream.seek(0)

    # Send the photo
    await update.message.reply_photo(plot_image_stream)

    # --- Add random and logical data to create a combined dataset ---
    combined_data = data.copy()

    # Adding random data and logical adjustments
    combined_data['Check Frequency'] = combined_data['Check Frequency'].apply(lambda x: random.choice(["Every month", "Every week", "Never", "Whenever I have a message"]))

    combined_data = map_scores(combined_data)
    combined_data = calculate_read_probability(combined_data)

    # Calculate combined statistics
    combined_avg_read_probability = combined_data["Read Probability"].mean()
    combined_day_probabilities = calculate_day_probabilities(combined_data)

    # Prepare combined dataset statistics response
    combined_response = " Combined Dataset Statistics (with random and logical data added):\n"
    combined_response += f"🔢 Average Check Frequency Score: {combined_data['Check Frequency Score'].mean():.2f}\n"
    combined_response += f"💬 Average Response Probability Score: {combined_data['Response Probability Score'].mean():.2f}\n"
    combined_response += f"📈 Average Read Probability: {combined_avg_read_probability:.2f}\n\n"
    combined_response += "🔹 Day-Specific Probabilities for Combined Dataset:\n"
    for day, prob in combined_day_probabilities.items():
        combined_response += f"{day}: {prob:.2f}%\n"

    # Send the combined dataset statistics
    await update.message.reply_text(combined_response)

    # Create and send the probability plot for combined dataset
    plot_image_stream_combined = create_probability_plot(combined_day_probabilities, "Combined Day-Specific Probabilities")

    # Reset the stream position before sending it
    plot_image_stream_combined.seek(0)

    # Send the photo
    await update.message.reply_photo(plot_image_stream_combined)

    # --- Send Final Message with Options ---
    final_message = "شانس اینو دارم تا باهات آشنا بشم؟"
    keyboard = [
        [InlineKeyboardButton("حرف بزنیم", callback_data='chat')],
        [InlineKeyboardButton("علاقه‌ای ندارم", callback_data='no_interest')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(final_message, reply_markup=reply_markup)

async def handle_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Handle the callback data
    if query.data == 'chat':
        await query.edit_message_text(text="هرکدوم یکی از این راه ها که برات راحت میتونی باهام ارتباط برقرار کنی")
        
        # Create new options for contact methods
        contact_keyboard = [
            [InlineKeyboardButton("آیدی تلگرام", callback_data='telegram_id')],
            [InlineKeyboardButton("آیدی اینستاگرام", callback_data='instagram_id')],
            [InlineKeyboardButton("لینک ناشناس", callback_data='anonymous_link')]
        ]
        contact_reply_markup = InlineKeyboardMarkup(contact_keyboard)
        await query.message.reply_text("دوست داری چطوری باهم در ارتباط باشیم؟", reply_markup=contact_reply_markup)
        
    elif query.data == 'no_interest':
        await query.edit_message_text(text="ممنونم برای وقتی که گذاشتی و ممنونم برای اینکه تا اینجا جلو اومدی، امیدوارم خوشحال و موفق باشی")
    elif query.data == 'telegram_id':
        await query.edit_message_text(text="آیدی تلگرام من:\n@Arshia_Madadi")
    elif query.data == 'instagram_id':
        await query.edit_message_text(text="آیدی اینستاگرام من :\n@arsh1amadadi\nhttps://www.instagram.com/arsh1amadadi?igsh=MXNqZmxjN25pbnUwaA==")
    elif query.data == 'anonymous_link':
        await query.edit_message_text(text="لینک ناشناس:\nhttp://t.me/HidenChat_Bot?start=419908264")

# --- Main Function to Start the Bot ---
def main():
    application = Application.builder().token('token').build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
