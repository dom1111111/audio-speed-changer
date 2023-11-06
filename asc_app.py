from kivy.app import App
from kivy import require
from kivy.uix.widget import Widget
# from kivy.lang import Builder
from plyer import filechooser
from wave import open
import os

require('2.1.0')    # same as `kivy.require`


# list to store the file path of the WAV file to be modified
filepath_list = []


# the class that instatiates the MainWidget and all your kvlang code
class MainWidget(Widget):

    # function to access list
    def show_list(self):
        if filepath_list:
            return filepath_list[0]                 # only return file path if list is not empty
        else:
            pass

    # file chooser
    def choose_file(self):
        file = filechooser.open_file(
            title="Choose a WAV file...", 
            filters=[("WAV files", "*.wav")])
        if file:                                    # checks if a file was chosen -> checks if `file` (the file chooser dialogue) is not empty
            filepath_list.clear()
            filepath_list.append(file[0])           # must include the indexof 0, as `filechooser returns a list`

    # gives the `display_file_label` label the selected filename, if there is one
    def label_filename(self):
        if filepath_list:                           # if `filepath_list` is not empty:
            filename = os.path.basename(filepath_list[0])
            self.ids.display_file_label.text = f"you have selected: [b]{filename}[/b]"     # updates the text of the label widget with id "display_file_label" to this new text

    # for enabing the execute button only if file path and speed is provided
    def check_execute_enable(self):
        if filepath_list and self.ids.speed_percentage.text:
            self.ids.execute_button.disabled = False
        else:
            self.ids.execute_button.disabled = True

    # the main audio manipulating method
    def change_audio(self, file_path, speed):
        original_audio = open(file_path)                    # open audio from file_path given
        params = original_audio.getparams()                 # "Returns a namedtuple() (nchannels, sampwidth, framerate, nframes, comptype, compname)"
        audio_data = original_audio.readframes(params[3])   # reads the frames (essentially the main data) of the audio file - index 3 of getparams is the number of frames, which is needed as argument for the readframes function

        # code relating to the newly created modified (output) audio file
        frame_rate = params[2]
        percentage = int(speed)                             # the percentage of original speed that the new file should be      # `int()` makes sure that this is an interger                    
        new_rate = frame_rate * (percentage / 100)          # sets the rate for the new modified audio file
        file_name = os.path.splitext(os.path.basename(file_path))[0]    # use `os.path.basename(file_path)` for file name WITH extension
        new_file = file_name + f' @ {percentage}% speed.wav'# name of the new file
        modified_audio = open(new_file, 'w')                # the 'w' is to specificy that this is to *write* a file (so create a new file, rather than read an existing one) 
        modified_audio.setparams(params)
        modified_audio.setframerate(new_rate)
        modified_audio.writeframes(audio_data)

        original_audio.close()
        modified_audio.close()

        path = os.path.dirname(file_path)                   # get the directory path from the original file path
        new_path = os.path.join(path, new_file)             # create the full file path for the new file)
        os.startfile(new_path)                              # runs the newly created file!


# standard stuff: creates a subclass (main_app) of `App` - build function, return app code
class MainApp(App):                             # `MainApp` is following kivy convention (kv file would be 'Main.kv' - the same as this, but without 'App')
    def build(self):
        self.title = "Audio Speed Changer"      # title of the application
        return MainWidget()


# runs the app
if __name__ == '__main__':
    try:
        MainApp().run()
    except Exception as e:
        print(e)
        input("Press enter...")
