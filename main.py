from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.button import Button
import random
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock

level = 2

class MenuScreen(Screen):
    def start_game(self):
        app = App.get_running_app()
        game_over_screen = app.root.get_screen("GameOverScreen")
        game_over_screen.game_restart()
        app.root.current = "MainScreen"

class LevelCompletedScreen(Screen):
    def back(self,event):
        app = App.get_running_app()
        app.root.current = "MenuScreen"

    def on_pre_enter(self, *args): 
        super().on_pre_enter(*args)
        Clock.schedule_once(self.back,2)
    


class GameOverScreen(Screen):
    def game_restart(self):
        MainScreen.gen_num = 0
        MainScreen.gen_num_clicked = False
        app = App.get_running_app()
        main_screen = app.root.get_screen("MainScreen")
        for button in main_screen.ids.scrollable_buttons.buttons[1:]:
            button.stored_num = None
            button.text = button.old_text
            button.disabled = False
                       

        app.root.current = "MenuScreen"


class MainScreen(Screen):
    gen_num_label = StringProperty("Generate first number to start")
    gen_num = 0
    gen_num_clicked = False
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
    def rand_butt_press(self,button):
        if not self.gen_num_clicked:
            print("button pressed")
            MainScreen.gen_num = random.randint(1,100)
            MainScreen.gen_num_clicked = True
            self.gen_num_label = f"{MainScreen.gen_num}"
            print(self.gen_num_label)
    

        
class GameArea(BoxLayout):
    def __init__(self, **kwargs):
        super(GameArea, self).__init__(**kwargs)
        
        
class ScrollableButtons(BoxLayout):
    def __init__(self, **kwargs):
        super(ScrollableButtons, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(10)
        self.buttons = [None,]
        for i in range(level):
            old_text = f" {i+1}. Number"
            button = Button(text=old_text,size_hint_y=None, height=100)
            button.old_text = old_text
            button.id = f"b{i+1}"
            button.bind(on_press=self.entered_value)
            button.stored_num = None
            self.buttons.append(button)
            self.add_widget(button)

    def entered_value(self,button):
        if MainScreen.gen_num_clicked:  
            button.text = str(MainScreen.gen_num)
            print(button.id)
            button.disabled = True
            button.stored_num = MainScreen.gen_num
            MainScreen.gen_num = 0
            MainScreen.gen_num_clicked = False
            
        for i in range(1,int(button.id[1:])): #checking game over if some number before stored number is bigger
            if self.buttons[i].stored_num:
                if self.buttons[i].stored_num > button.stored_num:
                    print("Game over")
                    app = App.get_running_app()
                    app.root.current = "GameOverScreen"
                    break

        
        for i in range(int(button.id[1:]),len(self.buttons)): #checking game over if some number after stored number is smaller
            if self.buttons[i].stored_num:
                if self.buttons[i].stored_num < button.stored_num:
                    print("Game over")
                    app = App.get_running_app()
                    app.root.current = "GameOverScreen"
                    break
        
        #checking for victory
        solved_num = 0
        for button in self.buttons[1:]: 
            if not button.stored_num:
                break
            else:
                solved_num += 1

        if solved_num == len(self.buttons)-1:
            app = App.get_running_app()
            app.root.current = "LevelCompletedScreen"
            global level
            level += 1
            print(level)
        else:
            solved_num = 0



class ScreenManager(ScreenManager):
    pass

kv = Builder.load_file("mainscreen.kv")

class MyApp(App):
    def build(self):
        return kv
    

if __name__ == '__main__':
    MyApp().run()