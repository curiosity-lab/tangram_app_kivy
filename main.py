import kivy
kivy.require('1.9.0')  # replace with your current kivy_tests version !
from kivy.app import App
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.graphics.transformation import Matrix
from os import listdir
from os.path import isfile, join
import math
import copy
from kivy.core.window import Window


class TangramPiece(Rectangle):

    move = False
    img = []
    name = ''
    ang = 0
    base_tran = []
    old_tran = []

    def on_transform_with_touch(self, touch):



        '''
        print("==== changing ", self.name,  "======")
        print(self.transform)
        gx, gy = TangramApp.to_grid(self.transform[12], self.transform[13])
        x,y = TangramApp.to_coor(gx, gy)
        new_gx, new_gy = TangramApp.to_grid(x, y)
        print(gx, new_gx, gy, new_gy)
        #if gx == new_gx and gy == new_gy:
         #   pass
        #else:
        self.transform[12], self.transform[13] = TangramApp.to_coor(gx, gy)
        print(self.transform)

        if self.tran_not_equal(self.old_tran, self.transform):
            print("==== changing ", self.name,  "======")
            print("old", self.old_tran)
            print("tran", self.transform)
            rot = self.get_closest_rot(self.rotation)
            self.clear_widgets()
            self.add_widget(self.img[str(rot)])

            new_transform = copy.deepcopy(self.base_tran)
            new_transform[12] = self.transform[12]
            new_transform[13] = self.transform[13]
            self.transform = self.set_no_rot(new_transform)
            self.apply_transform(Matrix().scale(5,5,1))
            self.old_tran = self.set_no_rot(new_transform)
        '''

    def tran_not_equal(self, t1, t2):
        for k in range(0,16):
            if t1[k] != t2[k]:
                return True
        return False


    def set_no_rot(self, tran):
        tran[0] = 1
        tran[5] = 1
        tran[10] = 1
        tran[15] = 1
        return tran

    def get_closest_rot(self, rot):
        pos_rot = []
        for key, value in self.img.items():
            my_ang = self.ang + rot
            img_ang = int(key)
            d = min([math.fabs(my_ang-img_ang), math.fabs((my_ang-360)-img_ang)])
            pos_rot.append([d, key])
        print(pos_rot, min(pos_rot)[1])
        return min(pos_rot)[1]


class TangramApp(App):
    pieces = []

    def load_pieces(self):
        my_path = 'pieces'
        only_files = [f for f in listdir(my_path) if isfile(join(my_path, f)) and '.png' in f]
        self.pieces = {}
        for f in only_files:
            name = str.split(f, '_')
            print(name)
            self.pieces[name[0]] = TangramPiece(do_scale=False,do_rotation=True,do_translation=True)
            self.pieces[name[0]].img = {}
            self.pieces[name[0]].name = name[0]
            self.pieces[name[0]].rot = 0

        for f in only_files:
            name = str.split(f, '_')
            self.pieces[name[0]].img[name[1]] = Image(source='pieces/' + f)
            self.pieces[name[0]].base_tran = self.pieces[name[0]].set_no_rot(
                copy.deepcopy(self.pieces[name[0]].transform))
            self.pieces[name[0]].old_tran = self.pieces[name[0]].set_no_rot(
                copy.deepcopy(self.pieces[name[0]].base_tran))


        for key, value in self.pieces.items():
            #value.apply_transform(Matrix().scale(2,2,1))#.translate(TangramApp.x0, TangramApp.y0,0))
            value.add_widget(value.img['0'])

    def get_piece(self, name):
        for p in self.pieces:
            if p.name == name:
                return p
        return None

    def build(self):
        self.load_pieces()

        # buttons layout
        button_left = Button()
        button_right = Button()
        button_up = Button()
        button_down = Button()
        button_rotate = Button()
        empty = []
        for k in range(0, 4):
            empty.append(Label())
        buttons_layout = GridLayout(cols=3, rows=3)
        buttons_layout.add_widget(empty[0])
        buttons_layout.add_widget(button_up)
        buttons_layout.add_widget(empty[1])
        buttons_layout.add_widget(button_left)
        buttons_layout.add_widget(button_rotate)
        buttons_layout.add_widget(button_right)
        buttons_layout.add_widget(empty[2])
        buttons_layout.add_widget(button_down)
        buttons_layout.add_widget(empty[3])

        # pieces layout
        pieces_layout = GridLayout(cols=3,rows=3)
        for key, value in self.pieces.items():
            pieces_layout.add_widget(value)

        # task layout

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(pieces_layout)
        root_layout.add_widget(buttons_layout)

        return root_layout

    DISTANCE = 20.0
    x0 = 100.0
    y0 = 100.0

    @staticmethod
    def to_grid(x, y):
        gx = math.floor((x - TangramApp.x0) / TangramApp.DISTANCE)
        gy = math.floor((y - TangramApp.y0) / TangramApp.DISTANCE)

        if gx < 0:
            gx = 0
        if gy < 0:
            gy = 0
        return gx, gy

    @staticmethod
    def to_coor(gx, gy):
        x = gx * TangramApp.DISTANCE + TangramApp.x0
        y = gy * TangramApp.DISTANCE + TangramApp.y0
        return x,y

    def on_pause(self):
        return True

#if __name__ == '__main__':
TangramApp().run()