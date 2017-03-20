from tkinter import *
from time import sleep
from random import randint, choice
from sys import exit
class Game:
    planets = {}
    asteroids = {}
    asteroid_number = 0
    current_planet = 1
    planet_number = 0
    time = 10
    time2 = False
    do = False
    first = True
    def __init__(self,canvas, width, height, colors):
        self.colors = colors
        self.canvas_width = width
        self.canvas_height = height
        self.canvas = canvas
    def check_collision(self, coords_1, coords_2):
        if (coords_1[0] <= coords_2[2] and coords_1[0] >= coords_2[0]) or (coords_1[2] <= coords_2[2] and coords_1[2] >= coords_2[0]):
            if (coords_1[1] <= coords_2[3] and  coords_1[1] >= coords_2[1]) or (coords_1[3] <= coords_2[3] and coords_1[3] >= coords_2[1]):
                return True
    def draw(self):
        self.ship = self.canvas.create_rectangle(self.find_center(self.planets[1][1], 15))
        self.coordinates = self.canvas.coords(self.ship)
        self.center = self.coordinates
        self.canvas.itemconfig(self.ship, fill = 'white')
        self.canvas.bind_all('<space>', self.initiate)  
    def scroll(self, distance):
        for planet in self.planets:
            self.canvas.move(self.planets[planet][0], -distance, 0)
        for asteroid in self.asteroids:
            self.canvas.move(self.asteroids[asteroid][0], -distance, 0)
            #self.asteroids[asteroid][0][0] += -distance
            #self.asteroids[asteroid][0][2] += -distance
            #print(self.asteroids[asteroid][0][0])
            #print(self.asteroids[asteroid][0][2])
    def initiate(self, event):
        self.do = True
    def move(self):
        if self.center[0] - 5 <= self.coordinates[0] <= self.center[0] + 5 and self.center[1] - 5 <= self.coordinates[1] <= self.center[1] + 5:
            if self.time2:
                self.do = False
                self.time2 = False
            elif self.time > 5:
                self.time = 0
                self.current_planet += 1
                self.center = self.find_center(self.planets[self.current_planet][1], 15)
                x_difference = self.center[0] - self.coordinates[0]
                y_difference = self.center[1] - self.coordinates[1]
                self.x_slope = x_difference/(abs(abs(x_difference) + abs(y_difference)) / 3)
                self.y_slope = y_difference/(abs(abs(x_difference) + abs(y_difference)) / 3)
                self.time2 = True
        self.canvas.move(self.ship, 0, self.y_slope)                       
        self.scroll(self.x_slope)
        self.time += 1
    def find_center(self, coords, size):
        dif = coords[2] - coords[0]
        down_dif = (dif - size) / 2
        up_dif = (dif + size) / 2
        return [coords[0] + down_dif, coords[1] + down_dif, coords[0] + up_dif, coords[1] + up_dif] 
    def update(self):
        self.coordinates[1] = self.canvas.coords(self.ship)[1]
        self.coordinates[3] = self.canvas.coords(self.ship)[3]
        self.coordinates[0] += self.x_slope 
        self.coordinates[2] += self.x_slope
    def create_planet(self):
        try:
            x = self.planets[self.planet_number][1][2] + 30
        except:
            x = 1
        self.planet_number += 1   
        sizes = [randint(30, 90), randint(30, 120), randint(50, 140), randint(60, 300)]
        random_size = choice(sizes)
        #planet = self.canvas.create_oval(0, 0, random_size, random_size)
        planet_x =  randint(x, x + 300)
        planet_y =  randint(0, self.canvas_height-random_size)
        planet_coords = (planet_x, planet_y, planet_x + random_size, planet_y + random_size)
        planet = self.canvas.create_oval(planet_coords)
        #self.canvas.coords(planet, planet_coords)
        self.canvas.itemconfig(planet, fill = choice(self.colors))
        self.planets[self.planet_number] = [planet, planet_coords]
        '''
        if self.first:
            self.first = False
        else:
            asteroid_choice = randint(0,1)
            if asteroid_choice == 0:
                print(1)
            
                asteroid_x = randint(self.asteroids[self.asteroid_number][1][2] + 10, self.planets[self.planet_number][1][0] - 10)
            elif asteroid_choice == 1:
                print(2)
                asteroid_x = randint(self.planets[self.planet_number - 1][1][2] + 10, self.planets[self.planet_number][1][0] - 20)
        '''
        while True:
            asteroid_choice = randint(0,3)
            if asteroid_choice > 0:
                try:
                    asteroid_x = randint(self.asteroids[self.asteroid_number][1][2] + 10, self.planets[self.planet_number - 1][1][0] - 30)
                    self.create_asteroid(asteroid_x)
                    continue
                except:
                    break
            else:
                break
        try:
            asteroid_x = randint(self.planets[self.planet_number - 1][1][2] + 10, self.planets[self.planet_number][1][0] - 20)
            self.create_asteroid(asteroid_x)
        except:
            return
    def create_asteroid(self, asteroid_x):
        self.asteroid_number += 1 
        direction = choice((1, -1))
        if direction == 1:
            asteroid_coordinates = [asteroid_x, -15, asteroid_x + 15, 0]
        elif direction == -1:
            asteroid_coordinates = [asteroid_x, self.canvas_height, asteroid_x + 15,  self.canvas_height - 15]
        asteroid = self.canvas.create_oval(asteroid_coordinates)
        self.canvas.itemconfig(asteroid, fill = 'grey60')
        self.asteroids[self.asteroid_number] = [asteroid, asteroid_coordinates, randint(1, 6), direction]
    def move_asteroid(self):
        for asteroid in self.asteroids:
            if self.asteroids[asteroid][3] == 1:
                if self.asteroids[asteroid][1][1] >= self.canvas_height:
                    self.canvas.move(self.asteroids[asteroid][0], 0, -(self.canvas_height + (self.asteroids[asteroid][1][3] - self.canvas_height)))
                    #print(self.asteroids[asteroid][1][1])
                    #print(self.asteroids[asteroid][1][3])
                    self.asteroids[asteroid][1][1] = -15
                    self.asteroids[asteroid][1][3] = 0
                else:
                    self.canvas.move(self.asteroids[asteroid][0], 0, self.asteroids[asteroid][2])

                    self.asteroids[asteroid][1][1] += self.asteroids[asteroid][2]
                    self.asteroids[asteroid][1][3] += self.asteroids[asteroid][2]
            elif self.asteroids[asteroid][3] == -1:
                if self.asteroids[asteroid][1][3] <= 0:
                    self.canvas.move(self.asteroids[asteroid][0], 0,  (self.canvas_height - self.asteroids[asteroid][1][1]))#+ (0 - self.asteroids[asteroid][1][1])))
                    #print(self.asteroids[asteroid][1][1])
                    #print(self.asteroids[asteroid][1][3])
                    self.asteroids[asteroid][1][1] = self.canvas_height
                    self.asteroids[asteroid][1][3] = self.canvas_height + 15
                else:
                    self.canvas.move(self.asteroids[asteroid][0], 0, -self.asteroids[asteroid][2])
                    self.asteroids[asteroid][1][1] -= self.asteroids[asteroid][2]
                    self.asteroids[asteroid][1][3] -= self.asteroids[asteroid][2]
            if self.check_collision(self.asteroids[asteroid][1], self.coordinates):
                exit()        
            '''
            if self.asteroids[asteroid][1][1] < 0:
                self.canvas.move(self.asteroids[asteroid][0], 0, self.canvas_height - self.asteroids[1][1])
                self.asteroids[asteroid][1][1] = self.canvas_height - 15 
                self.asteroids[asteroid][1][3] = self.canvas_height
            elif self.asteroids[asteroid][1][3] > self.canvas_height:
                print(self.asteroids[asteroid][1][3])
                print(1)
                self.canvas.move(self.asteroids[asteroid][0], 0, -(self.canvas_height + self.asteroids[asteroid][1][3] - self.canvas_height))
                self.asteroids[asteroid][1][1] = 0
                self.asteroids[asteroid][1][3] = 15
            
            else:
                #print(1)
                self.canvas.move(self.asteroids[asteroid][0], 0, self.asteroids[asteroid][2] * self.asteroids[asteroid][3])
                self.asteroids[asteroid][1][1] += self.asteroids[asteroid][2]
                self.asteroids[asteroid][1][3] += self.asteroids[asteroid][2]
                #print(self.asteroids[asteroid][0][1])
                #print(self.asteroids[asteroid][0][3])
            #if self.check_collision2(self.asteroids[asteroid][0], self.coordinates) and self.check_collision1(self.asteroids[asteroid][0], self.coordinates):
                #print('x')
            #if self.check_collision1(self.asteroids[asteroid][0], self.coordinates):
               # print('y')
            if self.check_collision(self.asteroids[asteroid][1], self.coordinates):
                exit()
               ''' 
colors = [ 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3', 'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4',  'thistle2', 'thistle3', 'thistle4',
     'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12',  'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    ]
root = Tk()
root.title('Through the Galaxy')
root.resizable(0, 0)
root.wm_attributes("-topmost", 1)
canvas = Canvas(root, background = 'grey15', width = 1000, height = 500)
canvas.pack()
game = Game(canvas, 1000, 500, colors)
for x in range(10):
    game.create_planet()
#game.create_planet()
#game.create_planet()
game.draw()
while True:
    if game.do:
        game.move()
        game.update()
    #game.scroll(5)
    game.move_asteroid()
    root.update()
    root.update_idletasks()
    sleep(.01)
