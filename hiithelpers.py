import tkinter as tk # Main application tkinter library.
from tkinter import ttk # Used to create themed scales.
from tkinter import messagebox # Used to display error messages.
import os # Used to override the GUI exit button functionality.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Disabling terminal pygame welcome message.
import pygame # Used for game audio.
import time # Used to keep track of exercise time.
import random # Used to select a random meme.
import threading # Used to run the canvas image loading thread.

# Handles loading and tearing down the splash page to then launch the main application.
def splash_page(action):
  if action == "load":
    loading_title.place(x=360, y=340, anchor="s")
    loading_bar_label.config(image=loading_bar_images[0])
    loading_bar_label.place(x=360, y=420, anchor="s")
  elif action == "remove":
    loading_title.place_forget()
    loading_bar_label.place_forget()
    # Starts main application.
    menu_title.place(x=540, y=120, anchor="s")
    trainer_canvas.place(x=180, y=480, anchor="s")
    trainer_title.place(x=180, y=120, anchor="s")
    canvas_loop(canvas_loop_id, 0)
    trainer_select("load")

# Handles loading all the canvas images and updating a progress bar. This is ran in separate thread.
def load_canvas_images():
  # trainer_canvas_frames is an array of frames used in the trainer canvas_loop.
  # trainer_canvas_frames is ordered in groups by each trainer.
  # Each trainer next has frames ordered in loops.
  # The first loop of each trainer is the waiting frames loop.
  # The rest of the loops for each trainer are ordered by exercise number.
  # This trainer_canvas_frames structure could see changes in the future.
  # Keeping this structure while testing out alternative ways to load the images.
  total_count_frames = len(trainer_canvas_frames)
  for i in range(total_count_frames):
    if (i+1) % (total_count_frames/10) == 0:
      loading_bar_label.config(image=loading_bar_images[int((i+1) / (total_count_frames/10))])
      window.update()
    trainer_frames_count = num_frames * total_loops
    trainer_index = i // trainer_frames_count
    adjusted_frame_index = i - (trainer_index * trainer_frames_count)
    trainer_name = trainer_names[trainer_index]
    loop_index = int(adjusted_frame_index / num_frames)
    frame_index = int(adjusted_frame_index % num_frames)
    trainer_canvas_frames[i] = tk.PhotoImage(file=path("\\images\\trainer\\" + trainer_name + "\\canvas\\" + str(loop_index) + "_" + str(frame_index) + ".png"))
  window.after(300, splash_page, "remove")

# Handles navigating backwards in game states.
def navigate_back():
  global game_state
  if game_state == "exercise_select_state":
    exercise_select("remove")
    trainer_select("load")
    game_state = "trainer_select_state"
    play(click_audio)
  elif game_state == "time_select_state":
    time_select("remove")
    exercise_select("load")
    game_state = "exercise_select_state"
    play(click_audio)
  elif game_state == "workout_state":
    workout("remove")
    time_select("load")
    game_state = "time_select_state"
    play(click_audio)
  else:
    messagebox.showerror("hiithelpers application error", "navigate_back called with an invalid state. Closing application.", command=window.destroy())

# Handles navigating forwards in game states.
def navigate_next():
  global game_state
  if game_state == "trainer_select_state":
    trainer_select("remove")
    exercise_select("load")
    game_state = "exercise_select_state"
    play(click_audio)
  elif game_state == "exercise_select_state":
    if len(exercises_selected) < 1: # At least one exercise needs to be selected.
      no_exercise_button_flash(7)
    else:
      exercise_select("remove")
      time_select("load")
      game_state = "time_select_state"
      play(click_audio)
  elif game_state == "time_select_state":
    time_select("remove")
    workout("load")
    game_state = "workout_state"
    play(click_audio)
  else:
    messagebox.showerror("hiithelpers application error", "navigate_next called with an invalid state. Closing application.", command=window.destroy())

# Handles loading and removing of tkinter elements for the trainer_select_state.
def trainer_select(action):
  if action == "load":
    menu_title.config(text="Select Trainer")
    next_button.place(x=630, y=480, height=60, width=180, anchor="s")
    i_y = 180
    for i in range(len(trainer_names)):
      trainer_buttons[i].place(x=540, y=i_y, height=60, width=360, anchor="s")
      i_y = i_y + 60
    audio_index = trainer_audio[selected_trainer]["index"]
    play(trainer_audio[selected_trainer]["sounds"][audio_index])
  elif action == "remove":
    next_button.place_forget()
  else:
    messagebox.showerror("hiithelpers application error", "trainer_select called with an invalid action. Closing application.", command=window.destroy())

# Handles loading and removing of tkinter elements for the exercise_select_state.
def exercise_select(action):
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
    messagebox.showerror("hiithelpers application error", "exercise_select called with an invalid action. Closing application.", command=window.destroy())

# Handles loading and removing of tkinter elements for the time_select_state.
def time_select(action):
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
    messagebox.showerror("hiithelpers application error", "time_select called with an invalid action. Closing application.", command=window.destroy())

# Handles loading and removing of tkinter elements for the workout_state.
def workout(action):
  global canvas_loop_id
  if action == "load":
    back_button.place(x=450, y=480, height=60, width=180, anchor="s")
    menu_title.config(text="Workout Time")
    workout_button.config(image=start_button_image)
    workout_button.place(x=630, y=480, height=60, width=180, anchor="s")
    menu_outline_label.place(x=540 ,y=420, anchor="s")
    menu_outline_label.config(image=preworkout_images[random.randint(0,num_preworkout_memes-1)])
    reset_countdown_vars()
  elif action == "remove":
    trainer_title.config(text="")
    workout_button.place_forget()
    menu_outline_label.place_forget()
    workout_interval_title.place_forget()
    timer_title.place_forget()
    workout_progress_title.place_forget()
    canvas_loop_id = canvas_loop_id + 1
    canvas_loop(canvas_loop_id, 0)
    reset_countdown_vars()
  else:
    messagebox.showerror("hiithelpers application error", "workout called with an invalid action. Closing application.", command=window.destroy())

# Flashes the colors of the exercise buttons to indicate one needs to be selected.
def no_exercise_button_flash(count):
  if count > 0:
    if (count % 2) == 0:
      for i, button in enumerate(exercise_buttons):
        button.config(image=exercise_button_images[selected_trainer][i])
        play(error_audio)
    else:
      for i, button in enumerate(exercise_buttons):
        button.config(image=exercise_button_images["default"][i])
    count = count - 1
    window.after(125, no_exercise_button_flash, count)
  else:
    # Reset colors incase a button was selected during the flashing.
    for exercise_num in exercises_selected:
      exercise_buttons[exercise_num].config(image=exercise_button_images[selected_trainer][exercise_num])

# Handles when exercise buttons are moused over or when the mouse has left the exercise button canvas.
def exercise_button_mouse(action,exercise_num=None):
  global canvas_loop_id
  canvas_loop_id = canvas_loop_id + 1
  if action == "enter":
    if exercise_num == None:
      messagebox.showerror("hiithelpers application error", "exercise_button_mouse called without an exercise_num. Closing application.", command=window.destroy())
    canvas_loop(canvas_loop_id, exercise_num + 1)
    trainer_title.config(text=exercise_names[exercise_num])
  elif action == "leave":
    canvas_loop(canvas_loop_id, 0)
    trainer_title.config(text="")

# Handles selecting and unselecting exercises.
def toggle_exercise_button(exercise_num):
  global wow_easter_egg
  if exercise_num in exercises_selected:
    exercises_selected.remove(exercise_num)
    exercise_buttons[exercise_num].config(image=exercise_button_images["default"][exercise_num])
    play(unpop_audio)
  else:
    exercises_selected.append(exercise_num)
    exercise_buttons[exercise_num].config(image=exercise_button_images[selected_trainer][exercise_num])
    if wow_easter_egg and len(exercises_selected) == len(exercise_names):
      wow_easter_egg = False
      play(wow_audio) # Excuse to play the "wow" kidpix sound
    else:
      play(pop_audio)

# Trainer canvas loop.
def canvas_loop(id, loop_index):
  global trainer_canvas_index, trainer_canvas_direction
  if id == canvas_loop_id:
    base_index = trainer_names.index(selected_trainer) * num_frames * total_loops
    trainer_canvas.itemconfigure(trainer_canvas_frame, image=trainer_canvas_frames[base_index + (num_frames * loop_index) + trainer_canvas_index])
    if trainer_canvas_index == 20:
      trainer_canvas_direction = -1
    elif trainer_canvas_index == 0:
      trainer_canvas_direction = 1
    trainer_canvas_index = trainer_canvas_index + trainer_canvas_direction
    window.after(frame_time, canvas_loop, id, loop_index)

# Handles the exercise/rest workout countdown loop.
def countdown_loop():
  global workout_status, countdown_stage, countdown_timer, countdown_exercises, countdown_exercise, countdown_exercises_len, countdown_after, countdown_epoch, canvas_loop_id
  if workout_status == "start":
    window.after_cancel(countdown_after) # Killing all the after functions to handle scenario where pause and resume are clicked within a second of each other.
    timer_title.config(text=countdown_timer)
    workout_interval_title.config(text=countdown_stage)
    if countdown_stage == "Exercise" and countdown_timer == exercise_time_int: # Exercise stage just started.
      progress_string = "(" + str(countdown_exercises_len - len(countdown_exercises)) + "/" + str(countdown_exercises_len) + ")"
      workout_progress_title.config(text=progress_string)
      play(start_audio)
    elif countdown_stage == "Rest" and countdown_timer == rest_time_int: # Rest stage just started.
      if len(countdown_exercises) != 0:
        countdown_exercise = countdown_exercises[-1]
      trainer_title.config(text=exercise_names[countdown_exercise])
      canvas_loop_id = canvas_loop_id + 1
      canvas_loop(canvas_loop_id, countdown_exercise + 1)
      play(rest_audio)
    elif countdown_stage == "Get Ready" and countdown_timer == get_ready_time_int: # Get Ready stage just started.
      if len(countdown_exercises) != 0:
        countdown_exercise = countdown_exercises[-1]
      trainer_title.config(text=exercise_names[countdown_exercise])
      canvas_loop_id = canvas_loop_id + 1
      canvas_loop(canvas_loop_id, countdown_exercise + 1)
    if countdown_timer <= 5 and countdown_timer > 0:
      play(countdown_audio)
    if countdown_timer > 1:
        countdown_timer = countdown_timer - 1
        countdown_epoch = time.time()
        countdown_after = window.after(1000, countdown_loop)
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
      countdown_after = window.after(1000, countdown_loop)
    elif countdown_timer == 0:
      reset_countdown_vars()
      workout_interval_title.place(x=540 , y=280, anchor="s")
      workout_interval_title.config(text="Workout Complete!")
      trainer_title.config(text="")
      canvas_loop_id = canvas_loop_id + 1
      canvas_loop(canvas_loop_id, 0)
      timer_title.place_forget()
      workout_progress_title.place_forget()
      workout_status = "stop"
      workout_button.config(image=start_button_image)

# Resets the countdown variables.
def reset_countdown_vars():
  global workout_status, countdown_stage, countdown_timer, countdown_exercises, countdown_exercise, countdown_exercises_len, countdown_pause
  workout_status = "stop"
  countdown_stage = "Get Ready"
  countdown_timer = get_ready_time_int
  countdown_exercises = exercises_selected.copy()
  countdown_exercises_len = len(countdown_exercises)
  countdown_exercise = ""
  countdown_pause = 0
  workout_interval_title.config(text=countdown_stage)
  timer_title.config(text=countdown_timer)
  workout_progress_title.config(text="")

# Handles the start-resume-pause buttons.
def toggle_exercise_start_stop():
  global workout_status, countdown_pause, countdown_after
  if workout_status == "stop":
    workout_button.config(image=pause_button_image)
    workout_status = "start"
    menu_outline_label.config(image=menu_outline_image)
    workout_interval_title.place(x=540, y=220, anchor="s")
    timer_title.place(x=540, y=310, anchor="s")
    workout_progress_title.place(x=540, y=355, anchor="s")
    countdown_after = window.after(countdown_pause, countdown_loop)
  elif workout_status == "start":
    workout_button.config(image=resume_button_image)
    workout_status = "stop"
    countdown_pause = int(1000*(1.0 - float(time.time() - countdown_epoch)))
  play(click_audio)

# Handles toggling the mute/volume button.
def toggle_mute_volume():
  global audio_on
  if audio_on:
    audio_on = False
    play(mute_audio)
    mute_volume_button.config(image=mute_image)
  else:
    audio_on = True
    play(unmute_audio)
    mute_volume_button.config(image=volume_image)

# Handles playing game audio.
def play(audio):
  if audio_on or audio == mute_audio:
    pygame.mixer.Sound.play(audio)

# Handles changing the trainer.
def toggle_trainer(trainer_name):
  global selected_trainer
  if trainer_name in trainer_names:
    if selected_trainer != trainer_name:
      selected_trainer = trainer_name
      exercise_time_scale.configure(style=selected_trainer + ".exercise.Horizontal.TScale") # Updating scale color to correspond to selected trainer.
      rest_time_scale.configure(style=selected_trainer + ".rest.Horizontal.TScale") # Updating scale color to correspond to selected trainer.
      # Updating selected exercise buttons color to correspond to selected trainer.
      for exercise_num in exercises_selected:
        exercise_buttons[exercise_num].config(image=exercise_button_images[selected_trainer][exercise_num])
      # Updating trainer button colors to correspond with the selected trainer.
      for i, name in enumerate(trainer_names):
        if trainer_name == name:
          trainer_buttons[i].config(image=selected_trainer_button_images[i])
        else:
          trainer_buttons[i].config(image=default_trainer_button_images[i])
    new_index = (trainer_audio[selected_trainer]["index"] + 1) % num_trainer_sounds
    trainer_audio[selected_trainer]["index"] = new_index
    play(trainer_audio[selected_trainer]["sounds"][new_index])
  else:
    messagebox.showerror("hiithelpers application error", "toggle_trainer called with an invalid trainer. Closing application.", command=window.destroy())

# Handles the exercise/rest interval scales.
def handle_scale_slide(value, scale):
  global exercise_time_int, rest_time_int, scale_last_tick_time
  formatted_value = 5 * round(int(float(value))/5)
  cur_time = time.time()
  if scale == "exercise":
    if formatted_value != exercise_time_int and cur_time - scale_last_tick_time > 0.05:
      play(tick_audio)
      scale_last_tick_time = cur_time
    exercise_time_int = formatted_value
    exercise_time_title.config(text="Exercise Length: " + str(formatted_value) + " seconds")
  elif scale == "rest":
    if formatted_value != rest_time_int and cur_time - scale_last_tick_time > 0.05:
      play(tick_audio)
      scale_last_tick_time = cur_time
    rest_time_int = formatted_value
    rest_time_title.config(text="Rest Length: " + str(formatted_value) + " seconds")

# Overrides the GUI exit button function. This allows for the terminal to exit cleanly.
def kill_app():
  os._exit(1)

# Returns absolute path for files. Needed for building application as an executable through nuitka.
def path(relative_path):
  return root_dir + relative_path

# File Setup.
root_dir = os.path.dirname(__file__) # Absolute path of the directory for this file.

# Window Setup.
window = tk.Tk() # Initializing tkinter window.
window.geometry("720x480") # Setting window height and width.
window.resizable(False, False) # Disabling resizing the window.
window.configure(bg="#FFFFFF") # Configuring the window background color.
window.protocol('WM_DELETE_WINDOW', kill_app) # Overriding the GUI exit button function.
window.title("hiithelpers") # Overriding the tkinter window title.
window.iconbitmap(path("\\images\\hh.ico"))

# Game Fonts.
comic_sans_large = ("Comic Sans MS", 40, "bold") # Large font used in main heading.
comic_sans_medium = ("Comic Sans MS", 25, "bold") # Medium font used in sub heading.
comic_sans_small = ("Comic Sans MS", 15, "bold") # Small font used in text.

# Audio Settings.
pygame.mixer.init() # Initializing pygame mixer.
pygame.mixer.set_num_channels(3) # Setting up three audio channels.
audio_on = False # Boolean value to maintain if application volume is muted.
scale_last_tick_time = time.time() # Timestamp used to limit the slider audio from playing too often.
mute_audio = pygame.mixer.Sound(path("\\sounds\\mute.wav")) # Muting application sound.
unmute_audio = pygame.mixer.Sound(path("\\sounds\\unmute.wav")) # Unmuting application sound.
click_audio = pygame.mixer.Sound(path("\\sounds\\click.wav")) # Button click sound.
pop_audio = pygame.mixer.Sound(path("\\sounds\\pop.wav")) # Adding an exercise sound.
unpop_audio = pygame.mixer.Sound(path("\\sounds\\unpop.wav")) # Removing an exercise sound.
tick_audio = pygame.mixer.Sound(path("\\sounds\\tick.wav")) # Rest and exercise scale slider sound.
start_audio = pygame.mixer.Sound(path("\\sounds\\start.wav")) # Prompt user exercises are starting sound.
rest_audio = pygame.mixer.Sound(path("\\sounds\\rest.wav")) # Prompts user to rest sound.
countdown_audio = pygame.mixer.Sound(path("\\sounds\\countdown.wav")) # Countdown sound between exercise and rest periods.
wow_audio = pygame.mixer.Sound(path("\\sounds\\wow.wav")) # Easter Egg sound only played first time all exercises are selected.
wow_easter_egg = True
error_audio = pygame.mixer.Sound(path("\\sounds\\error.wav")) # Error message sound.
error_audio.set_volume(0.35) # Lowering the error audio volume.
num_trainer_sounds = 5 # The number of selection sounds per each trainer.
trainer_audio = { # Trainer selection sounds. Contains an index to cycle through the sounds without repeating them.
  "arnold" : {
    "sounds": [pygame.mixer.Sound(path("\\sounds\\arnold" + str(i+1) + ".wav")) for i in range(num_trainer_sounds)],
    "index": random.randint(0,num_trainer_sounds-1)
  },
  "rex" : {
    "sounds" : [pygame.mixer.Sound(path("\\sounds\\rex" + str(i+1) + ".wav")) for i in range(num_trainer_sounds)],
    "index": random.randint(0,num_trainer_sounds-1)
  },
  "shaq" : {
    "sounds" : [pygame.mixer.Sound(path("\\sounds\\shaq" + str(i+1) + ".wav")) for i in range(num_trainer_sounds)],
    "index": random.randint(0,num_trainer_sounds-1)
  },
  "shrek" : {
    "sounds" : [pygame.mixer.Sound(path("\\sounds\\shrek" + str(i+1) + ".wav")) for i in range(num_trainer_sounds)],
    "index": random.randint(0,num_trainer_sounds-1)
  },
  "spiderman" : {
    "sounds" : [pygame.mixer.Sound(path("\\sounds\\spiderman" + str(i+1) + ".wav")) for i in range(num_trainer_sounds)],
    "index": random.randint(0,num_trainer_sounds-1)
  },
}

# Game Colors.
hiit_blue = "#BAE1FF" # Arnold.
hiit_orange = "#FFDFBA" # Rex.
hiit_yellow = "#FFFFBA" # Shaq.
hiit_green = "#BAFFC9" # Shrek.
hiit_red = "#FFB3BA" # Spider-man.

# Game State (trainer_select_state,exercise_select_state,time_select_state,workout_state).
game_state = "trainer_select_state" # Used to keep track of changing between different game states.

# Titles.
game_title = tk.Label(window, text="H.I.I.T. Helpers!", font=comic_sans_large, bg=window["bg"]) # Main Heading.
menu_title = tk.Label(window, text="", font=comic_sans_medium, bg=window["bg"]) # Sub heading on the right.
trainer_title = tk.Label(window, text="", font=comic_sans_small, bg=window["bg"]) # Trainer heading on the left.

# Navigation Buttons.
back_button_image = tk.PhotoImage(file=path("\\images\\back.png"))
back_button = tk.Button(window, image=back_button_image, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=navigate_back, cursor="hand2")
next_button_image = tk.PhotoImage(file=path("\\images\\next.png"))
next_button = tk.Button(window, image=next_button_image, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=navigate_next, cursor="hand2")

# Audio Buttons.
mute_image = tk.PhotoImage(file=path("\\images\\mute.png"))
volume_image = tk.PhotoImage(file=path("\\images\\volume.png"))
mute_volume_button = tk.Button(window, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=toggle_mute_volume, cursor="hand2")

# Canvas Loop Setup.
fps = 8 # Frames per second.
loop_time = 2.5 # Total time for each loop.
frame_time = int(1000/fps) # Time between frames.
num_frames = int((fps * loop_time)) + 1 # Total number of frames.

# Exercise Setup.
exercise_names = [
  "Planks", #PL.
  "Mountain Climbers", #MC.
  "Push Ups", #PU.
  "Bear Crawls", #BR.
  "Burpees", #BU.
  "Chest Flys", #CF.
  "Back Rows", #BA.
  "Side Planks", #SP.
  "Plank Walk Outs", #PW.
  "Squats", #SQ.
  "Sumo Squats", #SS.
  "Reverse Lunges", #RL.
  "Lunge Jumps", #LJ.
  "Deadlifts", #DL.
  "Calf Raises", #CR.
  "Lateral Lunges", #LL.
  "Crusty Lunge", #CL.
  "Dumbbell Glute Bridge", #DB.
  "Skull Crushers", #SC.
  "Bicep Curls", #BC.
  "Hammer Curls", #HC.
  "Sit-Ups", #SU.
  "V-Ups", #VU.
  "Lying Leg Raises", #LR.
  "Russian Twists" #RT.
]
total_loops = len(exercise_names) + 1
exercises_selected = []
exercise_button_images = {
  "default": [tk.PhotoImage(file=path("\\images\\exercise\\" + str(i) + ".png")) for i in range(25)],
  "arnold": [tk.PhotoImage(file=path("\\images\\trainer\\arnold\\exercise\\" + str(i) + ".png")) for i in range(25)],
  "rex": [tk.PhotoImage(file=path("\\images\\trainer\\rex\\exercise\\" + str(i) + ".png")) for i in range(25)],
  "shaq": [tk.PhotoImage(file=path("\\images\\trainer\\shaq\\exercise\\" + str(i) + ".png")) for i in range(25)],
  "shrek": [tk.PhotoImage(file=path("\\images\\trainer\\shrek\\exercise\\" + str(i) + ".png")) for i in range(25)],
  "spiderman": [tk.PhotoImage(file=path("\\images\\trainer\\spiderman\\exercise\\" + str(i) + ".png")) for i in range(25)]
}

# Trainer Setup.
trainer_canvas = tk.Canvas(window, highlightthickness=0, bg=window["bg"])
trainer_canvas.config(height=360, width=360)
trainer_canvas_frame = trainer_canvas.create_image(180,360, anchor="s")
trainer_canvas_index = 0
trainer_canvas_direction = 1
selected_trainer = ""
canvas_loop_id = 0
trainer_names = ["arnold","rex","shaq","shrek","spiderman"]
loading_image = tk.PhotoImage(file=path("\\images\\loading.png"))
trainer_canvas_frames = [loading_image] * num_frames * total_loops * len(trainer_names)
default_trainer_button_images = []
selected_trainer_button_images = []
trainer_buttons = []
for name in trainer_names:
  default_image = tk.PhotoImage(file=path("\\images\\trainer\\" + name + "\\default.png"))
  default_trainer_button_images.append(default_image)
  selected_image = tk.PhotoImage(file=path("\\images\\trainer\\" + name + "\\selected.png"))
  selected_trainer_button_images.append(selected_image)
  trainer_button = tk.Button(window, image=default_image, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=lambda name=name: toggle_trainer(name), cursor="hand2")
  trainer_buttons.append(trainer_button)

# Exercise buttons setup.
exercise_button_canvas = tk.Canvas(window, width=360, height=300, bg=window["bg"], highlightthickness=0)
exercise_button_canvas.bind("<Leave>", func=lambda e: exercise_button_mouse("leave"))
exercise_buttons = []
s_x = 36
i_x = s_x
i_y = 0
for i in range(25):
  exercise_button = tk.Button(exercise_button_canvas, image=exercise_button_images["default"][i], borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=lambda i=i: toggle_exercise_button(i), cursor="hand2")
  exercise_button.bind("<Enter>", func=lambda e,i=i: exercise_button_mouse("enter",i))
  exercise_buttons.append(exercise_button)
  if i % 5 == 0:
    i_y = i_y + 60
    i_x = s_x
  else:
    i_x = i_x + 72
  exercise_button.place(x=i_x, y=i_y, height=60, width=72, anchor="s")

# Outline image for later game states.
menu_outline_image = tk.PhotoImage(file=path("\\images\\menu_outline.png"))
menu_outline_label = tk.Label(window, borderwidth=0)

# Custom Scales Setup (Each trainer has a custom scale).
custom_ttk_style = ttk.Style(window)
exercise_trough_image = tk.PhotoImage(master=window, file=path("\\images\\exercise_trough.png"))
exercise_slider_image = tk.PhotoImage(master=window, file=path("\\images\\exercise_slider.png"))
custom_ttk_style.element_create("exercise.Scale.trough", "image", exercise_trough_image)
rest_trough_image = tk.PhotoImage(master=window, file=path("\\images\\rest_trough.png"))
rest_slider_image = tk.PhotoImage(master=window, file=path("\\images\\rest_slider.png"))
custom_ttk_style.element_create("rest.Scale.trough", "image", rest_trough_image)
exercise_trainer_slider_images = []
rest_trainer_slider_images = []
for i in range(5):
  exercise_trainer_slider_images.append(tk.PhotoImage(master=window, file=path("\\images\\trainer\\" +  trainer_names[i] + "\\exercise.png")))
  custom_ttk_style.element_create( trainer_names[i] + ".exercise.Scale.slider", "image", exercise_slider_image, ('pressed', exercise_trainer_slider_images[i]))
  custom_ttk_style.layout(trainer_names[i] + ".exercise.Horizontal.TScale",
    [("exercise.Scale.trough", {"sticky": "we"}),
      ( trainer_names[i] + ".exercise.Scale.slider",
      {"side": "left", "sticky": "",
        "children": [("exercise.Horizontal.Scale.label", {"sticky": ""})]
      })])
  rest_trainer_slider_images.append(tk.PhotoImage(master=window, file=path("\\images\\trainer\\" +  trainer_names[i] + "\\rest.png")))
  custom_ttk_style.element_create( trainer_names[i] + ".rest.Scale.slider", "image", rest_slider_image, ('pressed', rest_trainer_slider_images[i]))
  custom_ttk_style.layout( trainer_names[i] + ".rest.Horizontal.TScale",
    [("rest.Scale.trough", {"sticky": "we"}),
      ( trainer_names[i] + ".rest.Scale.slider",
      {"side": "left", "sticky": "",
        "children": [("rest.Horizontal.Scale.label", {"sticky": ""})]
      })])

# Intervals Setup.
exercise_time = tk.StringVar()
exercise_time.set("60")
exercise_time_int = 60
exercise_time_title = tk.Label(window, font=comic_sans_small, bg=window["bg"], text="Exercise Length: 60 seconds")
exercise_time_scale = ttk.Scale(window, variable = exercise_time, from_ = 10, to = 120, orient = "horizontal", command=lambda e: handle_scale_slide(e, "exercise"), cursor="hand2")
rest_time = tk.StringVar()
rest_time.set("60")
rest_time_int = 60
rest_time_title = tk.Label(window, font=comic_sans_small, bg=window["bg"], text="Rest Length: 60 seconds")
rest_time_scale = ttk.Scale(window, variable = rest_time, from_ = 10, to = 120, orient = "horizontal", command=lambda e: handle_scale_slide(e, "rest"), cursor="hand2")

# Workout Setup.
pause_button_image = tk.PhotoImage(file=path("\\images\\pause.png"))
resume_button_image = tk.PhotoImage(file=path("\\images\\resume.png"))
start_button_image = tk.PhotoImage(file=path("\\images\\start.png"))
stop_button_image = tk.PhotoImage(file=path("\\images\\stop.png"))
workout_button = tk.Button(window, font=comic_sans_small, borderwidth=0, activebackground=window["bg"], command=toggle_exercise_start_stop, cursor="hand2")
workout_interval_title = tk.Label(window, font=comic_sans_small, bg=window["bg"])
timer_title = tk.Label(window, font=comic_sans_large, bg=window["bg"], fg="black")
workout_progress_title = tk.Label(window, font=comic_sans_small, bg=window["bg"])

# Preworkout Memes.
num_preworkout_memes = 4
preworkout_images = []
for i in range(num_preworkout_memes):
  preworkout_images.append(tk.PhotoImage(file=path("\\images\\preworkout\\" + str(i+1) + ".png")))

# Workout variables used in countdown_loop.
workout_status = "" # ("stop","start").
countdown_stage = "" # ("Get Ready", "Exercise", "Rest").
countdown_timer = 0
countdown_exercises = []
countdown_exercises_len = 0
countdown_exercise = ""
countdown_after = None # Return value of after function, used to keep loops running simultaneously.
countdown_epoch = None
countdown_pause = 0
get_ready_time_int = 10

# Asset loading screen.
loading_title = tk.Label(window, text="loading assets...", font=comic_sans_medium, bg=window["bg"])
loading_bar_label = tk.Label(window, borderwidth=0)
loading_bar_images = []
for i in range(11):
  loading_bar_images.append(tk.PhotoImage(file=path("\\images\\loading\\" + str(i*10) + ".png")))

# Initializing Application.
game_state = "trainer_select_state"
rand_trainer = trainer_names[random.randint(0,4)]
toggle_trainer(rand_trainer)
game_title.place(x=360, y=60, anchor="s")
if audio_on:
  mute_volume_button.config(image=volume_image)
else:
  mute_volume_button.config(image=mute_image)
mute_volume_button.place(x=690, y=60, anchor="s")
splash_page("load")
threading.Thread(target=load_canvas_images).start()

# Run Application.
window.mainloop()