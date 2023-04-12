import tkinter as tk
import time
import datetime #import datetime for our clock
import tkinter.font as font
from tkinter import ttk
import math
import random
import pygame
import sys

# Handles navigating back game states.
def navigate_back():
  global game_state
  if game_state == "exercise_select_state":
    for button in exercise_dict["buttons"]:
      button.place_forget()
    exercise_title.place_forget()
    back_button.place_forget()
    next_button.place_forget()
    trainer_canvas.place_forget()
    menu_title.place_forget()
    menu_title.config(text='')
    trainer_canvas.delete(trainer_dict[selected_trainer]["canvas_image"])
    trainer_canvas.config(height=340, width=720, bg=window["bg"])
    trainer_canvas.place(x=360, y=480, anchor='s')
    trainer_increment = -1
    if trainer_dict[selected_trainer]["slide_start"] > trainer_dict[selected_trainer]["slide_end"]:
      trainer_increment = 1
    shift_trainer(game_state, trainer_dict[selected_trainer]["slide_end"], trainer_dict[selected_trainer]["slide_start"], trainer_increment)
    game_state = "trainer_select_state"
  elif game_state == "time_select_state":
    exercise_time_title.place_forget()
    exercise_time_scale.place_forget()
    rest_time_title.place_forget()
    rest_time_scale.place_forget()
    menu_outline_label.place_forget()
    menu_title.config(text='Select Exercises')
    exercise_title.place(x=trainer_dict[selected_trainer]["exercise_x"], y=155, anchor='s')
    load_exercise_buttons()
    game_state = "exercise_select_state"
  elif game_state == "workout_state":
    workout_button.place_forget()
    menu_outline_label.place_forget()
    workout_interval_title.place_forget()
    timer_title.place_forget()
    workout_progress_title.place_forget()
    exercise_title.place_forget()
    reset_countdown_vars()
    menu_outline_label.config(image=menu_outline_image)
    menu_outline_label.place(x=trainer_dict[selected_trainer]["title_x"],y=420, anchor='s')
    next_button.place(x=trainer_dict[selected_trainer]["next_x"], y=480, height=60, width=180, anchor='s')
    exercise_time_title.place(x=trainer_dict[selected_trainer]["scale_x"], y=200, height=30, width=300, anchor='s')
    exercise_time_scale.place(x=trainer_dict[selected_trainer]["scale_x"], y=280, height=60, width=300, anchor='s')
    rest_time_title.place(x=trainer_dict[selected_trainer]["scale_x"], y=320, height=30, width=300, anchor='s')
    rest_time_scale.place(x=trainer_dict[selected_trainer]["scale_x"], y=390, height=60, width=300, anchor='s')
    game_state = "time_select_state"
  play("click_audio")

# Handles navigating to the next game state.
def navigate_next(trainer="default"):
  global game_state, selected_trainer
  if game_state == "trainer_select_state":
    juan_shadow_title.place_forget()
    juan_button.place_forget()
    carson_shadow_title.place_forget()
    carson_button.place_forget()
    selected_trainer = trainer
    if selected_trainer == "juan" or selected_trainer == "carson":
      menu_title.config(text='')
      menu_title.place_forget()
      trainer_canvas.config(height=340,width=720, bg=window["bg"])
      trainer_canvas.place(x=360, y=480, anchor='s')
      trainer_increment = 1 
      if trainer_dict[selected_trainer]["slide_start"] > trainer_dict[selected_trainer]["slide_end"]:
        trainer_increment = -1
      shift_trainer(game_state, trainer_dict[selected_trainer]["slide_start"], trainer_dict[selected_trainer]["slide_end"], trainer_increment)
    else:
      sys.exit('Trainer Selected has not been implemented. Exiting.')
    game_state = "exercise_select_state"
  elif game_state == "exercise_select_state":
    if len(exercise_dict["selected"]) == 0: #Can't move to time_select_state until at least on exercise has been selected.
      no_exercise_button_flash(7)
    else:
      for button in exercise_dict["buttons"]:
        button.place_forget()
      menu_outline_label.config(image=menu_outline_image)
      menu_outline_label.place(x=trainer_dict[selected_trainer]["title_x"],y=420, anchor='s')
      menu_title.config(text='Select Intervals')
      exercise_time_title.place(x=trainer_dict[selected_trainer]["scale_x"], y=200, height=30, width=300, anchor='s')
      exercise_time_scale.place(x=trainer_dict[selected_trainer]["scale_x"], y=280, height=60, width=300, anchor='s')
      rest_time_title.place(x=trainer_dict[selected_trainer]["scale_x"], y=320, height=30, width=300, anchor='s')
      rest_time_scale.place(x=trainer_dict[selected_trainer]["scale_x"], y=390, height=60, width=300, anchor='s')
      game_state = "time_select_state"
      play("click_audio")
  elif game_state == "time_select_state":
    exercise_time_title.place_forget()
    exercise_time_scale.place_forget()
    rest_time_title.place_forget()
    rest_time_scale.place_forget()
    next_button.place_forget()
    menu_title.config(text='Workout Time')
    workout_button.config(image=start_button_image)
    workout_button.place(x=trainer_dict[selected_trainer]["next_x"], y=480, height=60, width=180, anchor='s')
    menu_outline_label.place(x=trainer_dict[selected_trainer]["title_x"],y=420, anchor='s')
    menu_outline_label.config(image=preworkout_images[random.randint(0,num_preworkout_memes-1)])
    reset_countdown_vars()
    game_state = "workout_state"
    play("click_audio")

# Flashes the colors of the exercise buttons to indicate one needs to be selected.
def no_exercise_button_flash(count):
  if count > 0:
    if (count % 2) == 0:
      for i, button in enumerate(exercise_dict["buttons"]):
        button.config(image=exercise_dict["button_images"][selected_trainer][i])
        play("error_audio")
    else:
      for i, button in enumerate(exercise_dict["buttons"]):
        button.config(image=exercise_dict["button_images"]["default"][i])
    count = count - 1
    window.after(125, no_exercise_button_flash, count)
  else:
    # Reset Colors. This is needed incase a button was selected during the flashing.
    for exercise_num in exercise_dict["selected"]:
      exercise_dict["buttons"][int(exercise_num)-1].config(image=exercise_dict["button_images"][selected_trainer][int(exercise_num)-1])

# Handles shifting the trainer image between states
def shift_trainer(state, iter, end, unit):
  trainer_canvas.delete(trainer_dict[selected_trainer]["canvas_image"])
  trainer_dict[selected_trainer]["canvas_image"] = trainer_canvas.create_image(iter, 340, anchor='s', image=trainer_dict[selected_trainer]["trainer_image"])
  if (iter != end):
    iter = iter + unit
    window.after(1,shift_trainer, state, iter, end, unit)
  else:
    if state == "trainer_select_state":
      menu_title.config(text='Select Exercises')
      menu_title.place(x=trainer_dict[selected_trainer]["title_x"], y=120, anchor='s')
      trainer_canvas.place_forget()
      trainer_canvas.delete(trainer_dict[selected_trainer]["canvas_image"])
      trainer_canvas.config(height=360, width=360, bg=window["bg"])
      trainer_canvas.place(x=trainer_dict[selected_trainer]["canvas_x"], y=480, anchor='s')
      trainer_dict[selected_trainer]["canvas_image"] = trainer_canvas.create_image(180, 360, anchor='s', image=trainer_dict[selected_trainer]["trainer_image"])
      back_button.place(x=trainer_dict[selected_trainer]["back_x"], y=480, height=60, width=180, anchor='s')
      next_button.place(x=trainer_dict[selected_trainer]["next_x"], y=480, height=60, width=180, anchor='s')
      exercise_title.place(x=trainer_dict[selected_trainer]["exercise_x"], y=155, anchor='s')
      load_exercise_buttons()
      play("select_audio")
    elif state == "exercise_select_state":
      trainer_canvas.delete(trainer_dict[selected_trainer]["canvas_image"])
      load_trainer_select()

# Places the exercise buttons in a grid on the application
def load_exercise_buttons():
  for exercise_num in exercise_dict["selected"]:
    exercise_dict["buttons"][int(exercise_num)-1].config(image=exercise_dict["button_images"][selected_trainer][int(exercise_num)-1])
  b_x = trainer_dict[selected_trainer]["button_x"]
  b_y = 220
  i_x = b_x
  i_y = b_y - 100
  for i, button in enumerate(exercise_dict["buttons"]):
    if i % 5 == 0:
      i_y = i_y + 60
      i_x = b_x
    else:
      i_x = i_x + 72
    button.place(x=i_x, y=i_y, height=60, width=72, anchor='s')

# Loads in the items needed in the trainer_select_state
def load_trainer_select():
  menu_title.config(text='Select trainer')
  menu_title.place(x=360, y=120, anchor='s')
  juan_button.place(x=200, y=480, height=300, width=200, anchor='s')
  carson_button.place(x=520, y=480, height=300, width=200, anchor='s')
  play("trainer_audio")

# Sets the exercise title when a exercise button is moused over
def toggle_exercise_title(action,iter):
  if action == "enter":
    exercise_title.config(text=exercise_dict["names"][iter])
  if action == "leave":
    exercise_title.config(text="")

# Handles selecting and unselecting exercises
def toggle_exercise_button(exercise):
  if exercise in exercise_dict["selected"]:
    exercise_dict["selected"].remove(exercise)
    exercise_dict["buttons"][int(exercise)-1].config(image=exercise_dict["button_images"]["default"][int(exercise)-1])
    play("unpop_audio")
  else:
    exercise_dict["selected"].append(exercise)
    exercise_dict["buttons"][int(exercise)-1].config(image=exercise_dict["button_images"][selected_trainer][int(exercise)-1])
    play("pop_audio")

# Handles mousing over the trainer and applying the trainer shadow and title
def toggle_trainer_shadow(action,trainer_name,trainer_button,toggle_image,shadow_title,audio):
  trainer_button.config(image=toggle_image)
  if action == "enter":
    shadow_title.place(x=trainer_dict[trainer_name]["shadow_x"], y=178, anchor='s')
    play(audio)
  if action == "leave":
    shadow_title.place_forget()

# Handles the countdown exercise functionality
def countdown():
    global workout_status,countdown_stage,countdown_timer,countdown_exercises,countdown_exercise,countdown_exercises_len,countdown_after,countdown_epoch
    if workout_status == "start":
      window.after_cancel(countdown_after) # Killing all the after functions to handle scenario where pause and resume are clicked within a second of each other
      timer_title.config(text=countdown_timer)
      if countdown_stage == "Exercise" and countdown_timer == exercise_time_int: # Exercise stage just started
        workout_interval_title.config(text=countdown_stage)
        progress_string = "(" + str(countdown_exercises_len - len(countdown_exercises)) + "/" + str(countdown_exercises_len) + ")"
        workout_progress_title.config(text=progress_string)
        timer_title.config(fg="black")
        play("start_audio")
        exercise_title.config(text=exercise_dict["names"][countdown_exercise])
      elif countdown_stage == "Rest" and countdown_timer == rest_time_int: # Rest stage just started
        workout_interval_title.config(text=countdown_stage)
        if len(countdown_exercises) != 0:
          countdown_exercise = countdown_exercises[-1]
        exercise_title.config(text=exercise_dict["names"][countdown_exercise])
        timer_title.config(fg="black")
        play("rest_audio")
      elif countdown_stage == "Get Ready" and countdown_timer == get_ready_time_int: # Get Ready stage just started
        workout_interval_title.config(text=countdown_stage)
        if len(countdown_exercises) != 0:
          countdown_exercise = countdown_exercises[-1]
        exercise_title.config(text=exercise_dict["names"][countdown_exercise])
        timer_title.config(fg="black")
      if countdown_timer <= 5 and countdown_timer > 0:
        timer_title.config(fg=trainer_dict[selected_trainer]["trainer_color"])
        play("countdown_audio")
      if countdown_timer > 1:
          countdown_timer = countdown_timer - 1
          countdown_epoch = time.time()
          countdown_after = window.after(1000, countdown)
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
        countdown_after = window.after(1000, countdown)
      elif countdown_timer == 0:
        reset_countdown_vars()
        workout_interval_title.place(x=trainer_dict[selected_trainer]["title_x"], y=280, anchor='s')
        workout_interval_title.config(text="Workout Complete!")
        exercise_title.config(text="")
        timer_title.place_forget()
        workout_progress_title.place_forget()
        workout_status = "stop"
        workout_button.config(image=start_button_image)

# Resets the countdown variables
def reset_countdown_vars():
  global workout_status,countdown_stage,countdown_timer,countdown_exercises,countdown_exercise,countdown_exercises_len, countdown_pause
  workout_status = "stop"
  countdown_stage = "Get Ready"
  countdown_timer = get_ready_time_int
  countdown_exercises = exercise_dict["selected"].copy()
  countdown_exercises_len = len(countdown_exercises)
  countdown_exercise = ""
  countdown_pause = 0
  workout_interval_title.config(text=countdown_stage)
  timer_title.config(text=countdown_timer)
  workout_progress_title.config(text="")

# Handles the start-resume-pause buttons
def toggle_exercise_start_stop():
  global workout_status, countdown_pause, countdown_epoch, countdown_after
  if workout_status == "stop":
    workout_button.config(image=pause_button_image)
    workout_status = "start"
    menu_outline_label.config(image=menu_outline_image)
    workout_interval_title.place(x=trainer_dict[selected_trainer]["title_x"], y=220, anchor='s')
    timer_title.place(x=trainer_dict[selected_trainer]["title_x"], y=310, anchor='s')
    workout_progress_title.place(x=trainer_dict[selected_trainer]["title_x"], y=355, anchor='s')
    exercise_title.place(x=trainer_dict[selected_trainer]["exercise_x"], y=155, anchor='s')
    countdown_after = window.after(countdown_pause, countdown)
  elif workout_status == "start":
    workout_button.config(image=resume_button_image)
    workout_status = "stop"
    countdown_pause = int(1000*(1.0 - float(time.time() - countdown_epoch)))
  play("click_audio")

#Handles toggling the mute/volume button
def toggle_mute_volume():
  global audio_on
  if audio_on:
    audio_on = False
    play("mute_audio")
    mute_volume_button.config(image=mute_image)
  else:
    audio_on = True
    play("unmute_audio")
    mute_volume_button.config(image=volume_image)

# Handles playing game audio, uses priorities to decide if audio can interrupt other audio
def play(audio):
  global last_played_audio
  if (audio_on and (pygame.mixer.music.get_busy() == False or (pygame.mixer.music.get_busy() == True and audio_dict[last_played_audio]["priority"] > audio_dict[audio]["priority"]))) or audio == "mute_audio":
    pygame.mixer.stop()
    pygame.mixer.music.load(audio_dict[audio]["path"])
    pygame.mixer.music.play()
    last_played_audio = audio

# Handles the exercise/rest interval scales
def handle_scale_slide(value, scale):
  global exercise_time_int, rest_time_int
  formatted_value = 5 * round(int(float(value))/5)
  if scale == "exercise":
    if formatted_value != exercise_time_int:
      play("tick_audio")
    exercise_time_int = formatted_value
    exercise_time_title.config(text="Exercise Length: " + str(formatted_value) + " seconds")
  elif scale == "rest":
    if formatted_value != rest_time_int:
      play("tick_audio")
    rest_time_int = formatted_value
    rest_time_title.config(text="Rest Length: " + str(formatted_value) + " seconds")

# Window Setup
window = tk.Tk()
window.geometry("720x480")
window.resizable(False, False)
window.configure(bg='#FFFFFF')

# Game Fonts
comic_sans_large = font.Font(family='Comic Sans MS', size=40, weight='bold')
comic_sans_medium = font.Font(family='Comic Sans MS', size=25, weight='bold')
comic_sans_small = font.Font(family='Comic Sans MS', size=15, weight='bold')

# Audio Settings 
audio_on = False
last_played_audio = None
audio_dict = {
  "mute_audio": {
    "path": "./sounds/mute.wav",
    "priority": 1
  },
  "unmute_audio" : {
    "path": "./sounds/unmute.wav",
    "priority": 2
  },
  "select_audio" : {
    "path": "./sounds/select.wav",
    "priority": 3
  },
  "trainer_audio" : {
    "path": "./sounds/trainer.wav",
    "priority": 3
  },
  "juan_audio" : {
    "path": "./sounds/juan.wav",
    "priority": 4
  },
  "carson_audio" : {
    "path": "./sounds/carson.wav",
    "priority": 4
  },
  "click_audio": {
    "path": "./sounds/click.wav",
    "priority": 5
  },
  "error_audio" : {
    "path": "./sounds/error.wav",
    "priority": 6
  },
  "pop_audio" : {
    "path": "./sounds/pop.wav",
    "priority": 7
  },
  "unpop_audio" : {
    "path": "./sounds/unpop.wav",
    "priority": 7
  },
  "tick_audio": {
    "path": "./sounds/tick.wav",
    "priority": 8
  },
  "start_audio" : {
    "path": "./sounds/start.wav",
    "priority": 9
  },
  "rest_audio" : {
    "path": "./sounds/rest.wav",
    "priority": 9
  },
  "countdown_audio": {
    "path": "./sounds/countdown.wav",
    "priority": 10
  },
}

# Game Colors
adidas_purple = '#6a62c4'
adidas_green = '#477466'

# Game State (trainer_select_state,exercise_select_state,time_select_state,workout_state)
game_state = ""

# Titles
game_title = tk.Label(window, text='H.I.I.T. Helpers!', font=comic_sans_large, bg=window["bg"])
menu_title = tk.Label(window, text='', font=comic_sans_medium, bg=window["bg"])

# Navigation Buttons
back_button_image = tk.PhotoImage(file='./images/back.png')
back_button = tk.Button(window, image = back_button_image, font=comic_sans_small, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=lambda: navigate_back(), cursor="hand2")
next_button_image = tk.PhotoImage(file='./images/next.png')
next_button = tk.Button(window, image = next_button_image, font=comic_sans_small, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=lambda: navigate_next(), cursor="hand2")

# Audio Buttons
mute_image = tk.PhotoImage(file='./images/mute.png')
volume_image = tk.PhotoImage(file='./images/volume.png')
mute_volume_button = tk.Button(window, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=toggle_mute_volume, cursor="hand2")

# Trainer Setup
trainer_canvas = tk.Canvas(window, highlightthickness=0, bg="pink")
selected_trainer = ""

# Trainer: juan
juan_image = tk.PhotoImage(file='./images/juan.png')
juan_greyscale_image = tk.PhotoImage(file='./images/juan_greyscale.png')
juan_shadow_image = tk.PhotoImage(file='./images/juan_shadow.png')
juan_shadow_title = tk.Label(window, text='Juanski', font=comic_sans_small, bg=window["bg"], fg=adidas_green)
juan_button = tk.Button(window, image=juan_image, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=lambda: navigate_next("juan"), cursor="hand2")
juan_button.bind("<Enter>", func=lambda e: toggle_trainer_shadow("enter","juan",juan_button,juan_shadow_image,juan_shadow_title,"juan_audio"))
juan_button.bind("<Leave>", func=lambda e: toggle_trainer_shadow("leave","juan",juan_button,juan_image,juan_shadow_title,"juan_audio"))

# Trainer: carson
carson_image = tk.PhotoImage(file='./images/carson.png')
carson_greyscale_image = tk.PhotoImage(file='./images/carson_greyscale.png')
carson_shadow_image = tk.PhotoImage(file='./images/carson_shadow.png')
carson_shadow_title = tk.Label(window, text='McCarson', font=comic_sans_small, bg=window["bg"], fg=adidas_purple)
carson_button = tk.Button(window, image=carson_image, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=lambda: navigate_next("carson"), cursor="hand2")
carson_button.bind("<Enter>", func=lambda e: toggle_trainer_shadow("enter","carson",carson_button,carson_shadow_image,carson_shadow_title,"carson_audio"))
carson_button.bind("<Leave>", func=lambda e: toggle_trainer_shadow("leave","carson",carson_button,carson_image,carson_shadow_title,"carson_audio"))

trainer_dict = {
  "juan": {
    "trainer_image": juan_image,
    "canvas_image": trainer_canvas.create_image(0, 0, anchor='s'),
    "trainer_color": adidas_purple,
    "slide_start": 200,
    "slide_end": 550,
    "title_x": 180,
    "shadow_x": 170,
    "button_x": 36,
    "canvas_x": 560,
    "exercise_x": 550,
    "back_x": 90,
    "next_x": 270,
    "scale_x": 180
  },
  "carson":{
    "trainer_image": carson_image,
    "canvas_image": trainer_canvas.create_image(0, 0, anchor='s'),
    "trainer_color": adidas_green,
    "slide_start": 520,
    "slide_end": 180,
    "title_x": 540,
    "shadow_x": 525,
    "button_x": 396,
    "canvas_x": 180,
    "exercise_x": 180,
    "back_x": 450,
    "next_x": 630,
    "scale_x": 540
  }
}

# Exercise Setup
exercise_title = tk.Label(window, text='', font=comic_sans_small, bg=window["bg"])
exercise_dict = {
  "buttons": [],
  "selected": [],
  "button_images": {
    "default": [],
    "juan" : [],
    "carson": []
  },
  "names": {
    "1": "Planks",
    "2": "Mountain Climbers",
    "3": "Push Ups",
    "4": "Bear Crawls",
    "5": "Burpees",
    "6": "Chest flys",
    "7": "Back Rows",
    "8": "Push Ups",
    "9": "Plank Walk Outs",
    "10": "Squats",
    "11": "Sumo Squats",
    "12": "Reverse Lunges",
    "13": "Lunge Jumps",
    "14": "Deadlifts",
    "15": "Calf Raises",
    "16": "Lateral Lunges",
    "17": "Crusty Lunge",
    "18": "Dumbell Glute Bridge",
    "19": "Skull Crushers",
    "20": "Bicep Curls",
    "21": "Hammer Curls",
    "22": "Sit-Ups",
    "23": "V-Ups",
    "24": "Lying Leg Raises",
    "25": "Russian Twists",
    "":""
  }
}

for i in range(25):
  exercise_dict["button_images"]["default"].append(tk.PhotoImage(file="./images/exercise/" + str(i+1) + ".png"))
  exercise_dict["button_images"]["juan"].append(tk.PhotoImage(file="./images/exercise/" + str(i+1) + "_juan.png"))
  exercise_dict["button_images"]["carson"].append(tk.PhotoImage(file="./images/exercise/" + str(i+1) + "_carson.png"))
  l_button = tk.Button(window, image=exercise_dict["button_images"]["default"][i], font=comic_sans_small, borderwidth=0, bg=window["bg"], activebackground=window["bg"], command=lambda i=i: toggle_exercise_button(str(i+1)), cursor="hand2")
  l_button.bind("<Enter>", func=lambda e,i=i: toggle_exercise_title("enter",str(i+1)))
  l_button.bind("<Leave>", func=lambda e,i=i: toggle_exercise_title("leave",str(i+1)))
  exercise_dict["buttons"].append(l_button)

# Outline Image for later game states
menu_outline_image = tk.PhotoImage(file='./images/menu_outline.png')
menu_outline_label = tk.Label(window, borderwidth=0)

# Custom Scales Setup
scale_style = ttk.Style(window)
exercise_trough_image = tk.PhotoImage(master=window, file='./images/exercise_trough.png')
exercise_slider_image = tk.PhotoImage(master=window, file='./images/exercise_slider.png')
scale_style.element_create('exercise.Scale.trough', 'image', exercise_trough_image)
scale_style.element_create('exercise.Scale.slider', 'image', exercise_slider_image)
scale_style.layout('exercise.Horizontal.TScale',
              [('exercise.Scale.trough', {'sticky': 'we'}),
                ('exercise.Scale.slider',
                {'side': 'left', 'sticky': '',
                  'children': [('exercise.Horizontal.Scale.label', {'sticky': ''})]
                })])
rest_trough_image = tk.PhotoImage(master=window, file='./images/rest_trough.png')
rest_slider_image = tk.PhotoImage(master=window, file='./images/rest_slider.png')
scale_style.element_create('rest.Scale.trough', 'image', rest_trough_image)
scale_style.element_create('rest.Scale.slider', 'image', rest_slider_image)
scale_style.layout('rest.Horizontal.TScale',
              [('rest.Scale.trough', {'sticky': 'we'}),
                ('rest.Scale.slider',
                {'side': 'left', 'sticky': '',
                  'children': [('rest.Horizontal.Scale.label', {'sticky': ''})]
                })])

# Intervals Setup
exercise_time = tk.StringVar()
exercise_time.set("60")
exercise_time_int = 60
exercise_time_title = tk.Label(window, font=comic_sans_small, bg=window["bg"], text="Exercise Length: 60 seconds")
exercise_time_scale = ttk.Scale(window, variable = exercise_time, from_ = 10, to = 120, orient = "horizontal", command=lambda e: handle_scale_slide(e, "exercise"), style="exercise.Horizontal.TScale", cursor="hand2")

rest_time = tk.StringVar()
rest_time.set("60")
rest_time_int = 60
rest_time_title = tk.Label(window, font=comic_sans_small, bg=window["bg"], text="Rest Length: 60 seconds")
rest_time_scale = ttk.Scale(window, variable = rest_time, from_ = 10, to = 120, orient = "horizontal", command=lambda e: handle_scale_slide(e, "rest"), style="rest.Horizontal.TScale", cursor="hand2")

# Workout Setup
pause_button_image = tk.PhotoImage(file='./images/pause.png')
resume_button_image = tk.PhotoImage(file='./images/resume.png')
start_button_image = tk.PhotoImage(file='./images/start.png')
stop_button_image = tk.PhotoImage(file='./images/stop.png')
workout_button = tk.Button(window, font=comic_sans_small, borderwidth=0, activebackground=window["bg"], command=lambda: toggle_exercise_start_stop(), cursor="hand2")
workout_interval_title = tk.Label(window, font=comic_sans_small, bg=window["bg"])
timer_title = tk.Label(window, font=comic_sans_large, bg=window["bg"])
workout_progress_title = tk.Label(window, font=comic_sans_small, bg=window["bg"])

# Preworkout memes
num_preworkout_memes = 4
preworkout_images = []
for x in range(num_preworkout_memes):
  preworkout_images.append(tk.PhotoImage(file='./images/preworkout/' + str(x+1) + '.png'))

# Workout variables used in countdown()
workout_status = "" # ("stop","start")
countdown_stage = "" # ("Get Ready", "Exercise", "Rest")
countdown_timer = 0
countdown_exercises = []
countdown_exercises_len = 0
countdown_exercise = ""
countdown_after = None
countdown_epoch = None
countdown_pause = 0
get_ready_time_int = 10

# Initializing Music
pygame.mixer.init()
pygame.mixer.music.set_volume(0.30)

# Initializing Application
game_state = "trainer_select_state"
game_title.place(x=360, y=60, anchor='s')
if audio_on:
  mute_volume_button.config(image=volume_image)
else:
  mute_volume_button.config(image=mute_image)
mute_volume_button.place(x=690, y=60, anchor='s')
load_trainer_select()

# Run Application
window.mainloop()
