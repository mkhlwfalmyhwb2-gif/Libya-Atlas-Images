# Developed by: Belal Faraj Suliman
# Project: Libya Educational Atlas v39.2 (Geography Section & Large Button)
# Date: March 3, 2026

import os, re
from kivy.app import App
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

# Imperial Identity Colors
Window.clearcolor = (1, 1, 1, 1)
MAIN_GREEN = get_color_from_hex('#27ae60')
DARK_GREEN = get_color_from_hex('#1e8449')

def get_num(f):
    n = re.findall(r'\d+', f); return int(n[-1]) if n else 0

class TImg(ButtonBehavior, Image): pass

# --- 1. Image Viewer (Instant Navigation Engine) ---
class ImageBookReader(Screen):
    def __init__(self, **kw):
        super().__init__(**kw); self.current_page = 1; self.book_path = ""; self.mode = "book"
        l = BoxLayout(orientation='vertical')
        self.title = Label(text="", size_hint_y=0.08, color=DARK_GREEN, bold=True, font_size='18sp')
        self.display = Image(allow_stretch=True, keep_ratio=True)
        
        # Navigation Buttons (Green Imperial)
        self.nav = BoxLayout(size_hint_y=0.1, spacing=dp(10), padding=dp(8))
        self.btn_prev = Button(text="< PREVIOUS", background_color=DARK_GREEN, background_normal='', bold=True)
        self.btn_prev.bind(on_release=lambda x: self.change_page(-1))
        
        self.btn_next = Button(text="NEXT >", background_color=DARK_GREEN, background_normal='', bold=True)
        self.btn_next.bind(on_release=lambda x: self.change_page(1))
        
        self.nav.add_widget(self.btn_prev); self.nav.add_widget(self.btn_next)
        
        # Close Button
        btn_close = Button(text="CLOSE", size_hint_y=0.08, background_color=(0.8, 0.2, 0.2, 1), background_normal='', bold=True)
        btn_close.bind(on_release=lambda x: self.go_back())
        
        l.add_widget(self.title); l.add_widget(self.display); l.add_widget(self.nav); l.add_widget(btn_close)
        self.add_widget(l)

    def load_book(self, path, name, mode="book"):
        self.book_path = path; self.mode = mode
        if mode == "map":
            self.display.source = path
            self.title.text = name
            self.nav.opacity = 0 
        else:
            self.current_page = 1
            self.nav.opacity = 1
            self.render_image()

    def change_page(self, step):
        if self.mode == "book":
            new_p = self.current_page + step
            if os.path.exists(os.path.join(self.book_path, f"{new_p}.jpg")):
                self.current_page = new_p; self.render_image()

    def render_image(self):
        img_p = os.path.join(self.book_path, f"{self.current_page}.jpg")
        if os.path.exists(img_p):
            self.display.source = img_p
            total = len([f for f in os.listdir(self.book_path) if f.endswith('.jpg')])
            self.title.text = f"Page {self.current_page} of {total}"

    def go_back(self):
        target = 'maps_screen' if self.mode == "map" else 'library_screen'
        setattr(self.manager, 'current', target)

# --- 2. Welcome Screen (Geography Section & Tactical Large Button) ---
class WelcomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw); l = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(10))
        
        # Imperial Owl Logo
        l.add_widget(Image(source='owl.png', size_hint=(None, None), size=('230dp', '230dp'), pos_hint={'center_x': 0.5}))
        
        # Imperial Titles
        l.add_widget(Label(text="LIBYA ATLAS", font_size='38sp', bold=True, color=DARK_GREEN))
        l.add_widget(Label(text="GEOGRAPHY SECTION", font_size='22sp', bold=True, color=DARK_GREEN))
        l.add_widget(Label(text="Educational Edition", font_size='18sp', color=MAIN_GREEN))
        
        # The Tactical Large Button with Arrow ∆
        btn = Button(text="START JOURNEY   ∆", 
                     size_hint=(1.0, 0.22), # Huge and broad
                     pos_hint={'center_x': 0.5}, 
                     background_color=MAIN_GREEN, 
                     background_normal='', 
                     bold=True, 
                     font_size='28sp')
        btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'maps_screen'))
        l.add_widget(btn)
        
        # Developed by Signature
        l.add_widget(Label(text="Developed by: Belal Faraj Suliman", font_size='14sp', color=(0.3,0.3,0.3,1)))
        self.add_widget(l)

# --- 3. Maps Gallery ---
class MapsScreen(Screen):
    def on_enter(self):
        self.grid.clear_widgets(); path = os.path.join(os.path.dirname(__file__), "Maps")
        if os.path.exists(path):
            for img in sorted(os.listdir(path), key=get_num):
                if img.lower().endswith(('.png', '.jpg', '.jpeg')):
                    box = BoxLayout(orientation='vertical', size_hint_y=None, height='280dp', spacing=dp(5))
                    t_img = TImg(source=os.path.join(path, img), allow_stretch=True)
                    t_img.bind(on_release=lambda x, fn=img: self.view_it(os.path.join(path, fn), fn))
                    box.add_widget(t_img); box.add_widget(Label(text=img, size_hint_y=0.2, color=(0,0,0,1), bold=True))
                    self.grid.add_widget(box)
    def view_it(self, p, n):
        v = self.manager.get_screen('reader'); v.load_book(p, n, mode="map"); self.manager.current = 'reader'
    def __init__(self, **kw):
        super().__init__(**kw); l = BoxLayout(orientation='vertical', padding=dp(10))
        header = BoxLayout(size_hint_y=0.15); header.add_widget(Image(source='owl.png', size_hint_x=0.2))
        header.add_widget(Label(text="MAPS GALLERY", font_size='24sp', bold=True, color=DARK_GREEN))
        l.add_widget(header); self.scroll = ScrollView(); self.grid = GridLayout(cols=2, spacing=dp(20), size_hint_y=None, padding=dp(10))
        self.grid.bind(minimum_height=self.grid.setter('height')); self.scroll.add_widget(self.grid); l.add_widget(self.scroll)
        btn = Button(text="DIGITAL LIBRARY", size_hint_y=0.12, background_color=MAIN_GREEN, background_normal='', bold=True)
        btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'library_screen')); l.add_widget(btn); self.add_widget(l)

# --- 4. Digital Library ---
class LibraryScreen(Screen):
    def on_enter(self):
        self.blist.clear_widgets(); path = os.path.join(os.path.dirname(__file__), "books")
        if os.path.exists(path):
            for f in sorted(os.listdir(path)):
                p = os.path.join(path, f)
                if os.path.isdir(p):
                    btn = Button(text=f"📖 {f}", size_hint_y=None, height=dp(70), background_color=MAIN_GREEN, background_normal='', bold=True)
                    btn.bind(on_release=lambda x, bk=p, n=f: self.open_bk(bk, n)); self.blist.add_widget(btn)
    def open_bk(self, p, n):
        v = self.manager.get_screen('reader'); v.load_book(p, n, mode="book"); self.manager.current = 'reader'
    def __init__(self, **kw):
        super().__init__(**kw); l = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        l.add_widget(Label(text="DIGITAL LIBRARY", size_hint_y=0.1, font_size='28sp', bold=True, color=DARK_GREEN))
        s = ScrollView(); self.blist = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(12))
        self.blist.bind(minimum_height=self.blist.setter('height')); s.add_widget(self.blist); l.add_widget(s)
        back = Button(text="BACK", size_hint_y=0.1, background_color=(0.2, 0.2, 0.2, 1), background_normal='', bold=True)
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'maps_screen')); l.add_widget(back); self.add_widget(l)

class LibyaAtlasApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(WelcomeScreen(name='welcome')); sm.add_widget(MapsScreen(name='maps_screen'))
        sm.add_widget(LibraryScreen(name='library_screen')); sm.add_widget(ImageBookReader(name='reader'))
        return sm

if __name__ == "__main__": LibyaAtlasApp().run()
