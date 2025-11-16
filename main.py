# main.py
import tkinter as tk
from tkinter import PhotoImage, scrolledtext
import threading
from crawler import run_crawler

# Flags
is_running = False
is_paused = False

# Buttons
start_btn = None
pause_btn = None
resume_btn = None
stop_btn = None


def should_run():
    return is_running


def is_paused_flag():
    return is_paused


def reset_button_colors():
    start_btn.config(bg="SystemButtonFace")
    pause_btn.config(bg="SystemButtonFace")
    resume_btn.config(bg="SystemButtonFace")
    stop_btn.config(bg="SystemButtonFace")


def highlight(btn, color):
    reset_button_colors()
    btn.config(bg=color)


def gui_log(text_area, msg):
    text_area.configure(state="normal")
    text_area.insert(tk.END, msg + "\n")
    text_area.configure(state="disabled")
    text_area.see(tk.END)


def start_clicked(text_area, uid_entry, time_entry):
    global is_running, is_paused

    # Nếu đang chạy: tắt task cũ trước
    if is_running:
        gui_log(text_area, ">>> Stopping previous crawler...")
        is_running = False
        time.sleep(0.5)  # chờ thread đóng ChromeDriver

    uid = uid_entry.get().strip()
    if not uid.isdigit():
        gui_log(text_area, "❌ UID must be a number.")
        return

    try:
        time_range = int(time_entry.get())
    except:
        gui_log(text_area, "❌ Invalid time range.")
        return

    is_running = True
    is_paused = False
    highlight(start_btn, "lightgreen")

    gui_log(text_area, f">>> START crawler for UID {uid} ...")

    threading.Thread(
        target=run_crawler,
        args=(uid, time_range, lambda m: gui_log(text_area, m), should_run, is_paused_flag),
        daemon=True
    ).start()


def pause_clicked(text_area):
    global is_paused, is_running

    if not is_running:
        gui_log(text_area, "❌ Not running.")
        return

    is_paused = True
    highlight(pause_btn, "yellow")
    gui_log(text_area, ">>> PAUSED.")


def resume_clicked(text_area):
    global is_paused, is_running

    if not is_running:
        gui_log(text_area, "❌ Not running.")
        return

    is_paused = False
    highlight(resume_btn, "lightblue")
    gui_log(text_area, ">>> RESUMED.")


def stop_clicked(text_area):
    global is_running, is_paused

    if not is_running:
        gui_log(text_area, "❌ Already stopped.")
        return

    gui_log(text_area, ">>> STOPPING...")
    is_running = False
    is_paused = False
    highlight(stop_btn, "tomato")


def main():
    global start_btn, pause_btn, resume_btn, stop_btn

    root = tk.Tk()
    root.title("Templar Log Monitor")
    root.geometry("1050x650")
    try:
    # PNG version
        root.iconphoto(True, PhotoImage(file="templar.png"))
    except:
        try:
            # ICO fallback for Windows
            root.iconbitmap("templar.ico")
        except:
            pass


    # ==================================================================
    # LOGO ASCII TEMPLAR
    # ==================================================================
    logo_text = """
 __|__ _  _ _  _ | _  _  
  †  (/_| | ||_)|(_||   
  |          |       
    """

    logo_label = tk.Label(
        root,
        text=logo_text,
        font=("Consolas", 16, "bold"),
        fg="#d9d9d9",
        bg="#1e1e1e",
        justify="center"
    )
    logo_label.pack(fill="x", pady=10)

    # ==================================================================
    # INPUT AREA
    # ==================================================================
    input_frame = tk.Frame(root)
    input_frame.pack(pady=5)

    tk.Label(input_frame, text="UID:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
    uid_entry = tk.Entry(input_frame, width=10, font=("Arial", 12))
    uid_entry.grid(row=0, column=1, padx=5)

    tk.Label(input_frame, text="Time range (minutes):", font=("Arial", 12)).grid(row=0, column=2, padx=5)
    time_entry = tk.Entry(input_frame, width=10, font=("Arial", 12))
    time_entry.insert(0, "10")
    time_entry.grid(row=0, column=3, padx=5)

    # ==================================================================
    # BUTTON AREA (centered row)
    # ==================================================================
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    start_btn = tk.Button(button_frame, text="START", width=12,
                          font=("Arial", 12, "bold"),
                          command=lambda: start_clicked(text_area, uid_entry, time_entry))
    pause_btn = tk.Button(button_frame, text="PAUSE", width=12,
                          font=("Arial", 12, "bold"),
                          command=lambda: pause_clicked(text_area))
    resume_btn = tk.Button(button_frame, text="RESUME", width=12,
                           font=("Arial", 12, "bold"),
                           command=lambda: resume_clicked(text_area))
    stop_btn = tk.Button(button_frame, text="STOP", width=12,
                         font=("Arial", 12, "bold"),
                         command=lambda: stop_clicked(text_area))

    start_btn.grid(row=0, column=0, padx=10)
    pause_btn.grid(row=0, column=1, padx=10)
    resume_btn.grid(row=0, column=2, padx=10)
    stop_btn.grid(row=0, column=3, padx=10)

    # ==================================================================
    # LOG OUTPUT AREA
    # ==================================================================
    log_frame = tk.Frame(root)
    log_frame.pack(fill="both", expand=True, pady=10)
    text_area = scrolledtext.ScrolledText(
            log_frame,
            state="disabled",
            font=("Consolas", 13)    # tăng nhẹ font log
        )
    text_area.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
