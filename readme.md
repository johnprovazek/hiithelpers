# hiithelpers

## Description

This application was designed to be used at home for doing high intensity interval training exercises. You can download the application for Windows devices now at [johnprovazek.com/hiithelpers](https://www.johnprovazek.com/hiithelpers/).

Developed with Python utilizing the [tkinter](https://docs.python.org/3/library/tkinter.html) package.

## Installation

### Download

If you are using a Windows device you can easily download and install this application at [johnprovazek.com/hiithelpers](https://www.johnprovazek.com/hiithelpers/). If you are using a Mac or Linux device there is not an easy installation process available at this time. To run this application you will need to build the Python application by following the instructions below.

This application was developed using Python version 3.11. To run the application, from the root directory run the following command:

```
python hiithelpers.py
```

If you were able to successfully run the Python application from the command line, the next step is to build the application as a packaged application. This is so you no longer need to launch the application from the command line every time you want to run it. To build the packaged application you can use the tool [PyInstaller](https://pyinstaller.org/en/stable/). This has been tested to work on a Windows device, but the [PyInstaller](https://pyinstaller.org/en/stable/) documentation states it supports both Mac and Linux as well. Run this command from the root directory to create the packaged application:
```
pyinstaller hiithelpers.py --noconsole --add-data "images;images" --add-data "sounds;sounds" --icon=images/hh.ico --onefile --distpath release/windows && rm hiithelpers.spec && rm -rf build
```
This command may need to slightly altered for Mac and Linux devices.

## Credits

[Sounds](https://www.dropbox.com/sh/42lbwv1qfyp7ox2/AABtBgnW36HJba6T8R70SvJXa?dl=0) from [KidPix 2](https://en.wikipedia.org/wiki/Kid_Pix) were used in this application.

This [Inno Setup Wizard setup guide](https://www.pythonguis.com/tutorials/packaging-pyside6-applications-windows-pyinstaller-installforge/) on the [Inno application](https://github.com/jrsoftware/issrc) was followed for setting up the Windows application installer.


## Bugs & Improvements

- Current images in the application are placeholders. Need to film and create frames for the trainers with [EbSynth](https://www.youtube.com/watch?v=tq_KOmXyVDo&ab_channel=JoelHaver).
- Add sounds for each trainer.
- Balance the volume on all the applications sounds.
- Investigate why the application has issues moving the window while the frames are loading.
- Investigate a way to load the frames in parallel while the application is running.
- The countdown_loop function counting is off by milliseconds for each exercise.
- Use a linter and a style guide.