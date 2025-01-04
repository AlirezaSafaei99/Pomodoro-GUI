from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
# Define color constants for the UI
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"

# Define other constants
FONT_NAME = "Courier"
WORK_MIN = 0.1
SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN = 0.1

# Global variables for session tracking and timer management
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    """
    Reset the timer and clear all progress.
    - Cancels any active timer.
    - Resets the repetition count and UI elements.
    """
    global reps
    window.after_cancel(timer)
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")  # Reset timer display
    title_label.config(text="Timer")  # Reset title label
    checkmark_emoji.config(text=" ")  # Clear checkmarks
# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """
    Start the Pomodoro timer and switch between work and break sessions.
    - Alternates between work, short breaks, and long breaks.
    """
    global reps
    # Determine session type based on repetition count
    reps += 1
    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)  # Start long break
        title_label.config(text="Long Break", fg=RED, bg=YELLOW)
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)  # Start short break
        title_label.config(text="Short Break", fg=PINK, bg=YELLOW)
    else:
        count_down(WORK_MIN * 60)  # Start work session
        title_label.config(text="Work", fg=GREEN, bg=YELLOW)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """
    Handle the countdown timer logic.
    - Updates the timer display.
    - Triggers the next session when the countdown reaches zero.
    """
    # Calculate minutes and seconds
    count_min = math.floor(count / 60)
    count_sec = count % 60

    # Format seconds to always display two digits
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # Update the timer text
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    # Continue countdown if time remains
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)  # Schedule the next update
    else:
        start_timer()  # Start the next session
        marks = "✔" * (reps // 2)  # Add checkmarks for completed work sessions
        checkmark_emoji.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
# Create the main window
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Create a title label
title_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, "36", "bold"))
title_label.grid(row=0, column=1)

# Create a canvas for the timer and image
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
image = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=image)
timer_text = canvas.create_text(100, 135, text="00:00", fill="white", font=(FONT_NAME, 22, "bold"))
canvas.grid(row=1, column=1)

# Create Start and Reset buttons
start_button = Button(text="Start", command=start_timer, highlightthickness=0)
start_button.grid(row=2, column=0)
reset_button = Button(text="Reset",command=reset_timer, highlightthickness=0)
reset_button.grid(row=2, column=2)

# Create a label for checkmarks
checkmark_emoji = Label(text="", bg=YELLOW, fg=GREEN)
checkmark_emoji.grid(row=3, column=1)

window.mainloop()