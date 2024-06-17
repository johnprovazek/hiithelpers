""" H.I.I.T Helpers Tkinter Application. """

import tkinter as tk  # Main application tkinter library.
from tkinter import ttk  # Used to create themed scales.
from tkinter import messagebox  # Used to display error messages.
import os  # Used to override the GUI exit button functionality and interact with directories.
import time  # Used to keep track of exercise time and scale usage.
import random  # Used to randomize memes, trainers, and trainer sounds
import threading  # Used to run the canvas image loading thread.
import pygame  # Used for game sounds.

# pylint: disable=C0103
# pylint: disable=W0603


def splash_page(action):
    """Handles loading and tearing down splash page. After teardown runs main application."""
    global game_state
    if action == "load":
        loading_title.place(x=360, y=340, anchor="s")
        loading_label.config(image=loading_images[0])
        loading_label.place(x=360, y=420, anchor="s")
    elif action == "remove":
        loading_title.place_forget()
        loading_label.place_forget()
        # Running main application.
        game_state = "trainer_select_state"
        menu_title.place(x=540, y=120, anchor="s")
        t_canvas.place(x=180, y=480, anchor="s")
        trainer_title.place(x=180, y=120, anchor="s")
        canvas_loop(t_canvas_loop_id, 0)
        trainer_select("load")


def load_canvas_images():
    """Handles loading canvas images and updating progress bar. Ran in separate thread."""
    # t_canvas_frames is an array of frames used in the trainer canvas_loop().
    # t_canvas_frames is ordered in sequential groups separated by each trainer.
    # The first loop of each trainer is the waiting frames loop.
    # The rest of the loops for each trainer are ordered by exercise number.
    # This t_canvas_frames structure is not an ideal design pattern.
    # This design pattern was used during testing multi threading.
    # This design pattern should be altered in the future if sticking with loading the images first.
    frames_count = len(t_canvas_frames)
    for frame_index in range(frames_count):
        if (frame_index + 1) % (frames_count / 10) == 0:
            loading_label.config(image=loading_images[int((frame_index + 1) / (frames_count / 10))])
            w.update()
        trainer_frames_count = num_frames * total_loops
        trainer_index = frame_index // trainer_frames_count
        adjusted_frame_index = frame_index - (trainer_index * trainer_frames_count)
        t_name = t_names[trainer_index]
        l_i = str(int(adjusted_frame_index / num_frames))  # Loop index in file path.
        f_i = str(int(adjusted_frame_index % num_frames))  # Frame index in file path.
        t_canvas_frames[frame_index] = tk.PhotoImage(
            file=path("\\images\\trainer\\" + t_name + "\\canvas\\" + l_i + "_" + f_i + ".png")
        )
    w.after(300, splash_page, "remove")  # After a delay remove splash page and start application.


def navigate_back():
    """Handles navigating back game states."""
    global game_state
    if game_state == "exercise_select_state":
        exercise_select("remove")
        trainer_select("load")
        game_state = "trainer_select_state"
        play("click")
    elif game_state == "time_select_state":
        time_select("remove")
        exercise_select("load")
        game_state = "exercise_select_state"
        play("click")
    elif game_state == "workout_state":
        workout("remove")
        time_select("load")
        game_state = "time_select_state"
        play("click")
    else:
        messagebox.showerror(
            "hiithelpers application error",
            "navigate_back called with an invalid state. Closing application.",
            command=w.destroy(),
        )


def navigate_next():
    """Handles navigating forwards game states."""
    global game_state
    if game_state == "trainer_select_state":
        trainer_select("remove")
        exercise_select("load")
        game_state = "exercise_select_state"
        play("click")
    elif game_state == "exercise_select_state":
        if len(exercises_selected) < 1:  # At least one exercise needs to be selected.
            no_exercise_button_flash(7)
        else:
            exercise_select("remove")
            time_select("load")
            game_state = "time_select_state"
            play("click")
    elif game_state == "time_select_state":
        time_select("remove")
        workout("load")
        game_state = "workout_state"
        play("click")
    else:
        messagebox.showerror(
            "hiithelpers application error",
            "navigate_next called with an invalid state. Closing application.",
            command=w.destroy(),
        )


def trainer_select(action):
    """Handles loading and removing tkinter elements in trainer_select_state."""
    if action == "load":
        menu_title.config(text="Select Trainer")
        next_button.place(x=630, y=480, height=60, width=180, anchor="s")
        t_button_y = 180
        for t_name_i in range(len(t_names)):
            t_buttons[t_name_i].place(x=540, y=t_button_y, height=60, width=360, anchor="s")
            t_button_y = t_button_y + 60
        sound_index = t_sounds_i[t_selected] % t_sounds_count + 1
        t_sounds_i[t_selected] = sound_index
        play(t_selected + str(sound_index))
    elif action == "remove":
        next_button.place_forget()
    else:
        messagebox.showerror(
            "hiithelpers application error",
            "trainer_select called with an invalid action. Closing application.",
            command=w.destroy(),
        )


def exercise_select(action):
    """Handles loading and removing tkinter elements in exercise_select_state."""
    if action == "load":
        menu_title.config(text="Select Exercises")
        back_button.place(x=450, y=480, height=60, width=180, anchor="s")
        next_button.place(x=630, y=480, height=60, width=180, anchor="s")
        exercise_button_canvas.place(x=540, y=420, anchor="s")
    elif action == "remove":
        next_button.place_forget()
        back_button.place_forget()
        exercise_button_canvas.place_forget()
    else:
        messagebox.showerror(
            "hiithelpers application error",
            "exercise_select called with an invalid action. Closing application.",
            command=w.destroy(),
        )


def time_select(action):
    """Handles loading and removing tkinter elements in time_select_state."""
    if action == "load":
        back_button.place(x=450, y=480, height=60, width=180, anchor="s")
        next_button.place(x=630, y=480, height=60, width=180, anchor="s")
        menu_title.config(text="Select Intervals")
        menu_outline_label.config(image=menu_outline_image)
        menu_outline_label.place(x=540, y=420, anchor="s")
        exercise_time_title.place(x=540, y=200, height=30, width=300, anchor="s")
        exercise_time_scale.place(x=540, y=280, height=60, width=300, anchor="s")
        rest_time_title.place(x=540, y=320, height=30, width=300, anchor="s")
        rest_time_scale.place(x=540, y=390, height=60, width=300, anchor="s")
    elif action == "remove":
        next_button.place_forget()
        back_button.place_forget()
        exercise_time_title.place_forget()
        exercise_time_scale.place_forget()
        rest_time_title.place_forget()
        rest_time_scale.place_forget()
        menu_outline_label.place_forget()
    else:
        messagebox.showerror(
            "hiithelpers application error",
            "time_select called with an invalid action. Closing application.",
            command=w.destroy(),
        )


def workout(action):
    """Handles loading and removing tkinter elements in workout_state."""
    global t_canvas_loop_id
    if action == "load":
        back_button.place(x=450, y=480, height=60, width=180, anchor="s")
        menu_title.config(text="Workout Time")
        workout_button.config(image=start_button_image)
        workout_button.place(x=630, y=480, height=60, width=180, anchor="s")
        menu_outline_label.place(x=540, y=420, anchor="s")
        menu_outline_label.config(image=meme_images[random.randint(0, num_memes - 1)])
        reset_countdown_vars()
    elif action == "remove":
        trainer_title.config(text="")
        workout_button.place_forget()
        menu_outline_label.place_forget()
        workout_interval_title.place_forget()
        timer_title.place_forget()
        workout_progress_title.place_forget()
        t_canvas_loop_id = t_canvas_loop_id + 1
        canvas_loop(t_canvas_loop_id, 0)
        reset_countdown_vars()
    else:
        messagebox.showerror(
            "hiithelpers application error",
            "workout called with an invalid action. Closing application.",
            command=w.destroy(),
        )


def no_exercise_button_flash(count):
    """Flashes exercise button colors indicating an exercise needs to be selected."""
    if count > 0:
        if count % 2 == 0:
            for button_i, button in enumerate(exercise_buttons):
                button.config(image=exercise_button_images[t_selected][button_i])
                play("error")
        else:
            for button_i, button in enumerate(exercise_buttons):
                button.config(image=exercise_button_images["default"][button_i])
        count = count - 1
        w.after(125, no_exercise_button_flash, count)
    else:
        # Reset colors for scenario where a button was selected during the flashing.
        for exercise_num in exercises_selected:
            exercise_buttons[exercise_num].config(image=exercise_button_images[t_selected][exercise_num])


def exercise_button_mouse(action, exercise_num=None):
    """Handles mouse movement over exercise button canvas."""
    global t_canvas_loop_id
    t_canvas_loop_id = t_canvas_loop_id + 1
    if action == "enter":
        if exercise_num is None:
            messagebox.showerror(
                "hiithelpers application error",
                "exercise_button_mouse called without an exercise_num. Closing application.",
                command=w.destroy(),
            )
        canvas_loop(t_canvas_loop_id, exercise_num + 1)
        trainer_title.config(text=exercises[exercise_num])
    elif action == "leave":
        canvas_loop(t_canvas_loop_id, 0)
        trainer_title.config(text="")


def toggle_exercise_button(exercise_num):
    """Handles selecting and unselecting exercises."""
    global sound_easter_egg
    if exercise_num in exercises_selected:
        exercises_selected.remove(exercise_num)
        exercise_buttons[exercise_num].config(image=exercise_button_images["default"][exercise_num])
        play("unpop")
    else:
        exercises_selected.append(exercise_num)
        exercise_buttons[exercise_num].config(image=exercise_button_images[t_selected][exercise_num])
        if sound_easter_egg and len(exercises_selected) == len(exercises):
            sound_easter_egg = False
            play("wow")
        else:
            play("pop")


def canvas_loop(cid, loop_index):
    """Trainer canvas loop."""
    global t_canvas_index
    global t_canvas_direction
    if cid == t_canvas_loop_id:
        base_index = t_names.index(t_selected) * num_frames * total_loops
        frame_image = t_canvas_frames[base_index + (num_frames * loop_index) + t_canvas_index]
        t_canvas.itemconfigure(t_canvas_frame, image=frame_image)
        if t_canvas_index == 20:
            t_canvas_direction = -1
        elif t_canvas_index == 0:
            t_canvas_direction = 1
        t_canvas_index = t_canvas_index + t_canvas_direction
        w.after(frame_time, canvas_loop, cid, loop_index)


def reset_countdown_vars():
    """Resets countdown variables."""
    global countdown_status
    global countdown_stage
    global countdown_timer
    global countdown_exercises
    global countdown_exercise
    global countdown_exercises_len
    global countdown_pause
    countdown_status = "stop"
    countdown_stage = "Get Ready"
    countdown_timer = countdown_init_time
    countdown_exercises = exercises_selected.copy()
    countdown_exercises_len = len(countdown_exercises)
    countdown_exercise = ""
    countdown_pause = 0
    workout_interval_title.config(text=countdown_stage)
    timer_title.config(text=countdown_timer)
    workout_progress_title.config(text="")


def toggle_exercise_start_stop():
    """Handles workout buttons presses."""
    global countdown_status
    global countdown_pause
    global countdown_after
    if countdown_status == "stop":
        workout_button.config(image=pause_button_image)
        countdown_status = "start"
        menu_outline_label.config(image=menu_outline_image)
        workout_interval_title.place(x=540, y=220, anchor="s")
        timer_title.place(x=540, y=310, anchor="s")
        workout_progress_title.place(x=540, y=355, anchor="s")
        countdown_after = w.after(countdown_pause, countdown_loop)
    elif countdown_status == "start":
        workout_button.config(image=resume_button_image)
        countdown_status = "stop"
        countdown_pause = int(1000 * (1.0 - float(time.time() - countdown_epoch)))
    play("click")


def countdown_loop():
    """Handles the workout countdown loop."""
    global countdown_status
    global countdown_stage
    global countdown_timer
    global countdown_exercise
    global countdown_after
    global countdown_epoch
    global t_canvas_loop_id
    if countdown_status == "start":
        # Killing all countdown_loop calls after functions to handling scenario where
        # pause and resume buttons are clicked within a second of each other.
        w.after_cancel(countdown_after)
        timer_title.config(text=countdown_timer)
        workout_interval_title.config(text=countdown_stage)
        # Exercise stage just started.
        if countdown_stage == "Exercise" and countdown_timer == exercise_time_int:
            exercises_complete = str(countdown_exercises_len - len(countdown_exercises))
            progress_string = "(" + exercises_complete + "/" + str(countdown_exercises_len) + ")"
            workout_progress_title.config(text=progress_string)
            play("start")
        # Rest stage just started.
        elif countdown_stage == "Rest" and countdown_timer == rest_time_int:
            if len(countdown_exercises) != 0:
                countdown_exercise = countdown_exercises[-1]
            trainer_title.config(text=exercises[countdown_exercise])
            t_canvas_loop_id = t_canvas_loop_id + 1
            canvas_loop(t_canvas_loop_id, countdown_exercise + 1)
            play("rest")
        # Get Ready stage just started.
        elif countdown_stage == "Get Ready" and countdown_timer == countdown_init_time:
            if len(countdown_exercises) != 0:
                countdown_exercise = countdown_exercises[-1]
            trainer_title.config(text=exercises[countdown_exercise])
            t_canvas_loop_id = t_canvas_loop_id + 1
            canvas_loop(t_canvas_loop_id, countdown_exercise + 1)
        if countdown_timer <= 5 and countdown_timer > 0:
            play("countdown")
        if countdown_timer > 1:
            countdown_timer = countdown_timer - 1
            countdown_epoch = time.time()
            countdown_after = w.after(1000, countdown_loop)
        elif countdown_timer == 1:
            if countdown_stage == "Get Ready" or countdown_stage == "Rest":
                countdown_stage = "Exercise"
                countdown_exercise = countdown_exercises.pop()
                countdown_timer = exercise_time_int
            elif countdown_stage == "Exercise":
                if len(countdown_exercises) == 0:
                    countdown_timer = 0
                else:
                    countdown_stage = "Rest"
                    countdown_timer = rest_time_int
            countdown_epoch = time.time()
            countdown_after = w.after(1000, countdown_loop)
        elif countdown_timer == 0:
            reset_countdown_vars()
            workout_interval_title.place(x=540, y=280, anchor="s")
            workout_interval_title.config(text="Workout Complete!")
            trainer_title.config(text="")
            t_canvas_loop_id = t_canvas_loop_id + 1
            canvas_loop(t_canvas_loop_id, 0)
            timer_title.place_forget()
            workout_progress_title.place_forget()
            countdown_status = "stop"
            workout_button.config(image=start_button_image)


def toggle_mute_volume():
    """Handles toggling the mute/volume button."""
    global sound_on
    if sound_on:
        sound_on = False
        play("mute")
        mute_volume_button.config(image=mute_image)
    else:
        sound_on = True
        play("unmute")
        mute_volume_button.config(image=volume_image)


def play(sound_name):
    """Handles playing game sounds."""
    if sound_name not in sounds:
        messagebox.showerror(
            "hiithelpers application error",
            "play called with an invalid sound file. Closing application.",
            command=w.destroy(),
        )
    elif sound_on or sound_name == "mute":
        pygame.mixer.Sound.play(sounds[sound_name])


def toggle_trainer(trainer_name):
    """Handles changing the trainer."""
    global t_selected
    if trainer_name in t_names:
        if t_selected != trainer_name:
            t_selected = trainer_name
            # Updating scale colors to correspond with selected trainer.
            exercise_time_scale.configure(style=t_selected + ".exercise.Horizontal.TScale")
            rest_time_scale.configure(style=t_selected + ".rest.Horizontal.TScale")
            # Updating selected exercise buttons color to correspond with selected trainer.
            for exercise_num in exercises_selected:
                exercise_buttons[exercise_num].config(image=exercise_button_images[t_selected][exercise_num])
            # Updating trainer button colors to correspond with selected trainer.
            for t_i, t_name in enumerate(t_names):
                if trainer_name == t_name:
                    t_buttons[t_i].config(image=t_selected_button_images[t_i])
                else:
                    t_buttons[t_i].config(image=t_default_button_images[t_i])
        sound_index = t_sounds_i[t_selected] % t_sounds_count + 1
        t_sounds_i[t_selected] = sound_index
        play(t_selected + str(sound_index))
    else:
        messagebox.showerror(
            "hiithelpers application error",
            "toggle_trainer called with an invalid trainer. Closing application.",
            command=w.destroy(),
        )


def handle_scale_slide(value, scale):
    """Handles interaction the exercise/rest interval scales."""
    global exercise_time_int, rest_time_int, scale_time
    formatted_value = 5 * round(int(float(value)) / 5)
    cur_time = time.time()
    if scale == "exercise":
        if formatted_value != exercise_time_int and cur_time - scale_time > 0.05:
            play("tick")
            scale_time = cur_time
        exercise_time_int = formatted_value
        exercise_time_title.config(text="Exercise Length: " + str(formatted_value) + " seconds")
    elif scale == "rest":
        if formatted_value != rest_time_int and cur_time - scale_time > 0.05:
            play("tick")
            scale_time = cur_time
        rest_time_int = formatted_value
        rest_time_title.config(text="Rest Length: " + str(formatted_value) + " seconds")


def kill_app():
    """Overrides the logic of the GUI exit button allowing for the terminal to exit cleanly."""
    os._exit(1)


def path(relative_path):
    """Returns absolute path for files. Necessary for when building application with pyinstaller"""
    return root_dir + relative_path


# File Setup.
root_dir = os.path.dirname(__file__)  # Absolute path of the directory containing this file.

# Window Setup.
w = tk.Tk()  # Initializing tkinter window.
w.geometry("720x480")  # Setting window height and width.
w.resizable(False, False)  # Disabling resizing the window.
w.configure(bg="#FFFFFF")  # Configuring the window background color.
w.protocol("WM_DELETE_WINDOW", kill_app)  # Overriding the GUI exit button function.
w.title("hiithelpers")  # Overriding the app title.
w.iconbitmap(path("\\images\\hh.ico"))  # Overriding the app icon.

# Tkinter Widget Defaults.
w.option_add("*background", w["bg"])  # Setting background for all widgets.
w.option_add("*activeBackground", w["bg"])  # Setting activeBackground for all widgets.
w.option_add("*Button*BorderWidth", 0)  # Setting borderwidth for all button widgets.
w.option_add("*Button*cursor", "hand2")  # Setting cursor for all button widgets.
w.option_add("*Label*BorderWidth", 0)  # Setting borderwidth for all label widgets.

# Game Fonts.
lg = ("Comic Sans MS", 40, "bold")  # Large font used in main heading.
md = ("Comic Sans MS", 25, "bold")  # Medium font used in sub heading.
sm = ("Comic Sans MS", 15, "bold")  # Small font used in any other text.

# Sounds.
pygame.mixer.init()  # Initializing pygame mixer.
pygame.mixer.set_num_channels(3)  # Setting three sound channels.
sound_on = False  # Flag for application sound on/off.
sounds = {}  # Game sounds.
for filename in os.listdir(path("\\sounds\\")):
    name, file_extension = os.path.splitext(filename)
    if ".wav" in file_extension:
        sounds[name] = pygame.mixer.Sound(path("\\sounds\\" + filename))
sound_easter_egg = True  # Used to only play the easter egg sound once.

# Game State (trainer_select_state, exercise_select_state, time_select_state, workout_state).
game_state = ""  # Keeps track of current game state.

# Trainer Setup.
t_names = ["arnold", "rex", "shaq", "shrek", "spiderman"]  # List of all trainers.
t_selected = ""  # Keeps track of the trainer selected.
t_sounds_count = 5  # Number of trainer selection sounds per trainer.
t_sounds_i = {}  # Index for trainer selection sounds so trainer sounds won't repeat.
t_default_button_images = []  # Trainer selection buttons default images.
t_selected_button_images = []  # Trainer selection buttons selected images.
t_buttons = []  # Trainer selection buttons.
for name in t_names:
    t_sounds_i[name] = random.randint(1, t_sounds_count)
    default_image = tk.PhotoImage(file=path("\\images\\trainer\\" + name + "\\default.png"))
    t_default_button_images.append(default_image)
    selected_image = tk.PhotoImage(file=path("\\images\\trainer\\" + name + "\\selected.png"))
    t_selected_button_images.append(selected_image)
    t_button = tk.Button(w, image=default_image, command=lambda name=name: toggle_trainer(name))
    t_buttons.append(t_button)

# Titles.
game_title = tk.Label(w, text="H.I.I.T. Helpers!", font=lg)  # Main heading.
menu_title = tk.Label(w, text="", font=md)  # Sub heading on the right.
trainer_title = tk.Label(w, text="", font=sm)  # Trainer heading on the left.

# Navigation Buttons.
back_button_image = tk.PhotoImage(file=path("\\images\\back.png"))
back_button = tk.Button(w, image=back_button_image, command=navigate_back)
next_button_image = tk.PhotoImage(file=path("\\images\\next.png"))
next_button = tk.Button(w, image=next_button_image, command=navigate_next)

# Mute/Volume Sound Button.
mute_image = tk.PhotoImage(file=path("\\images\\mute.png"))
volume_image = tk.PhotoImage(file=path("\\images\\volume.png"))
mute_volume_button = tk.Button(w, command=toggle_mute_volume)

# Countdown Loop Setup.
countdown_status = ""  # Status of countdown loop ("stop","start").
countdown_stage = ""  # Stage of countdown loop ("Get Ready", "Exercise", "Rest").
countdown_timer = 0  # Timer counting down seconds in stages of countdown loop.
countdown_exercises = []  # Queue of exercises in countdown loop.
countdown_exercises_len = 0  # Total count of exercises in the countdown loop.
countdown_exercise = ""  # The current exercise during the countdown loop.
countdown_after = None  # Return value of after function, used to keep loops running simultaneously.
countdown_epoch = None  # Timestamp used to keep track of time when stopping countdown loop.
countdown_pause = 0  # Time to wait when resuming countdown loop.
countdown_init_time = 10  # Initial time to wait during the "Get Ready" stage.

# Exercise Setup.
exercises = [
    "Planks",  # PL.
    "Mountain Climbers",  # MC.
    "Push Ups",  # PU.
    "Bear Crawls",  # BR.
    "Burpees",  # BU.
    "Chest Flys",  # CF.
    "Back Rows",  # BA.
    "Side Planks",  # SP.
    "Plank Walk Outs",  # PW.
    "Squats",  # SQ.
    "Sumo Squats",  # SS.
    "Reverse Lunges",  # RL.
    "Lunge Jumps",  # LJ.
    "Deadlifts",  # DL.
    "Calf Raises",  # CR.
    "Lateral Lunges",  # LL.
    "Crusty Lunge",  # CL.
    "Dumbbell Glute Bridge",  # DB.
    "Skull Crushers",  # SC.
    "Bicep Curls",  # BC.
    "Hammer Curls",  # HC.
    "Sit-Ups",  # SU.
    "V-Ups",  # VU.
    "Lying Leg Raises",  # LR.
    "Russian Twists",  # RT.
]
exercises_selected = []
exercise_button_images = {}
for name in t_names + ["default"]:
    frame_array = []
    for i in range(len(exercises)):
        root = "\\images\\trainer\\" + name + "\\exercise\\"
        if name == "default":
            root = "\\images\\exercise\\"
        frame_array.append(tk.PhotoImage(file=path(root + str(i) + ".png")))
    exercise_button_images[name] = frame_array

# Exercise Buttons Setup.
exercise_button_canvas = tk.Canvas(w, width=360, height=300, highlightthickness=0)
exercise_button_canvas.bind("<Leave>", func=lambda e: exercise_button_mouse("leave"))
exercise_buttons = []
s_x = 36
i_x = s_x
i_y = 0
for i in range(len(exercises)):
    exercise_button = tk.Button(
        exercise_button_canvas,
        image=exercise_button_images["default"][i],
        command=lambda i=i: toggle_exercise_button(i),
    )
    exercise_button.bind("<Enter>", func=lambda e, i=i: exercise_button_mouse("enter", i))
    exercise_buttons.append(exercise_button)
    if i % 5 == 0:
        i_y = i_y + 60
        i_x = s_x
    else:
        i_x = i_x + 72
    exercise_button.place(x=i_x, y=i_y, height=60, width=72, anchor="s")

# Canvas Loop Setup.
fps = 8  # Frames per second.
loop_time = 2.5  # Total time for each loop.
frame_time = int(1000 / fps)  # Time between frames.
num_frames = int((fps * loop_time)) + 1  # Total number of frames.
total_loops = len(exercises) + 1  # The number of canvas loops per trainer.

# Trainer Canvas Setup.
t_canvas = tk.Canvas(w, highlightthickness=0)  # Canvas to display trainer frames in loops.
t_canvas.config(height=360, width=360)
t_canvas_frame = t_canvas.create_image(180, 360, anchor="s")  # Frame displayed in trainer canvas.
t_canvas_index = 0  # Index of the current frame in the canvas loop.
t_canvas_direction = 1  # Direction of canvas loop. 1 for forward. -1 for backwards.
t_canvas_loop_id = 0  # Priority id used to keep canvas loops from running simultaneously.
t_canvas_temp_image = tk.PhotoImage(file=path("\\images\\loading.png"))
t_canvas_frames = [t_canvas_temp_image] * num_frames * total_loops * len(t_names)  # Canvas frames.

# Outline Setup.
menu_outline_image = tk.PhotoImage(file=path("\\images\\menu_outline.png"))
menu_outline_label = tk.Label(w)

# Custom Scales Setup.
scale_style = ttk.Style(w)
scale_exercise_trough_image = tk.PhotoImage(master=w, file=path("\\images\\exercise_trough.png"))
scale_exercise_slider_image = tk.PhotoImage(master=w, file=path("\\images\\exercise_slider.png"))
scale_style.element_create("exercise.Scale.trough", "image", scale_exercise_trough_image)
scale_rest_trough_image = tk.PhotoImage(master=w, file=path("\\images\\rest_trough.png"))
scale_rest_slider_image = tk.PhotoImage(master=w, file=path("\\images\\rest_slider.png"))
scale_style.element_create("rest.Scale.trough", "image", scale_rest_trough_image)
scale_exercise_trainer_slider_images = []
scale_rest_trainer_slider_images = []
scale_time = time.time()  # Timestamp used to limit the slider sound from playing too often.
for i, name in enumerate(t_names):  # Creating custom scale for each trainer.
    scale_exercise_trainer_slider_images.append(
        tk.PhotoImage(master=w, file=path("\\images\\trainer\\" + name + "\\exercise.png"))
    )
    scale_style.element_create(
        name + ".exercise.Scale.slider",
        "image",
        scale_exercise_slider_image,
        ("pressed", scale_exercise_trainer_slider_images[i]),
    )
    scale_style.layout(
        name + ".exercise.Horizontal.TScale",
        [
            ("exercise.Scale.trough", {"sticky": "we"}),
            (
                name + ".exercise.Scale.slider",
                {
                    "side": "left",
                    "sticky": "",
                    "children": [("exercise.Horizontal.Scale.label", {"sticky": ""})],
                },
            ),
        ],
    )
    scale_rest_trainer_slider_images.append(
        tk.PhotoImage(
            master=w,
            file=path("\\images\\trainer\\" + name + "\\rest.png"),
        )
    )
    scale_style.element_create(
        name + ".rest.Scale.slider",
        "image",
        scale_rest_slider_image,
        ("pressed", scale_rest_trainer_slider_images[i]),
    )
    scale_style.layout(
        name + ".rest.Horizontal.TScale",
        [
            ("rest.Scale.trough", {"sticky": "we"}),
            (
                name + ".rest.Scale.slider",
                {
                    "side": "left",
                    "sticky": "",
                    "children": [("rest.Horizontal.Scale.label", {"sticky": ""})],
                },
            ),
        ],
    )

# Interval And Scale Setup.
exercise_time = tk.StringVar()
exercise_time.set("60")
exercise_time_int = 60
exercise_time_title = tk.Label(w, font=sm, text="Exercise Length: 60 seconds")
exercise_time_scale = ttk.Scale(
    w,
    variable=exercise_time,
    from_=10,
    to=120,
    orient="horizontal",
    command=lambda e: handle_scale_slide(e, "exercise"),
    cursor="hand2",
)
rest_time = tk.StringVar()
rest_time.set("60")
rest_time_int = 60
rest_time_title = tk.Label(w, font=sm, text="Rest Length: 60 seconds")
rest_time_scale = ttk.Scale(
    w,
    variable=rest_time,
    from_=10,
    to=120,
    orient="horizontal",
    command=lambda e: handle_scale_slide(e, "rest"),
    cursor="hand2",
)

# Workout Setup.
pause_button_image = tk.PhotoImage(file=path("\\images\\pause.png"))
resume_button_image = tk.PhotoImage(file=path("\\images\\resume.png"))
start_button_image = tk.PhotoImage(file=path("\\images\\start.png"))
stop_button_image = tk.PhotoImage(file=path("\\images\\stop.png"))
workout_button = tk.Button(w, command=toggle_exercise_start_stop)
workout_interval_title = tk.Label(w, font=sm)
timer_title = tk.Label(w, font=lg, fg="black")
workout_progress_title = tk.Label(w, font=sm)

# Pre-Workout Memes.
num_memes = 4
meme_images = []
for i in range(num_memes):
    meme_images.append(tk.PhotoImage(file=path("\\images\\meme\\" + str(i + 1) + ".png")))

# Asset Loading Setup.
loading_title = tk.Label(w, text="loading assets...", font=md)
loading_label = tk.Label(w)
loading_images = []
for i in range(11):
    loading_images.append(tk.PhotoImage(file=path("\\images\\loading\\" + str(i * 10) + ".png")))

# Initializing Application.
toggle_trainer(t_names[random.randint(0, len(t_names) - 1)])  # Selecting a random trainer.
game_title.place(x=360, y=60, anchor="s")
if sound_on:
    mute_volume_button.config(image=volume_image)
else:
    mute_volume_button.config(image=mute_image)
mute_volume_button.place(x=690, y=60, anchor="s")
splash_page("load")
threading.Thread(target=load_canvas_images).start()  # Separate thread for loading images.

# Run Application.
w.mainloop()
