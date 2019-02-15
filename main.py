import math
import random

import pygame
from pygame import gfxdraw
from pygame import Surface

from pgx import *
from level1 import *
from game import *
from UIscreens import *

def printer2(object_list, scalar1, scalar3, graphlist, scalarscalar, specialpics):
    for i in range(int(len(object_list)/8)):
        xpos = object_list[(i * 8)]        
        ypos = object_list[1 + (i * 8)]
        object_number = object_list[4 + (i * 8)] #object type
        rotation = object_list[5+(i*8)]
        
        if object_number == 100:
            screen.blit(specialpics[0], (xpos, ypos))
        if object_number == 0:
            screen.blit(specialpics[1], (xpos, ypos))
                
        if object_number == 1: #draws main ship
            ship_pointlist = [[xpos, ypos-30*scalar3], [xpos+15*scalar3, ypos+10*scalar3], [xpos, ypos], [xpos-15*scalar3, ypos+10*scalar3]]
            ship_pointlist = Rotate(xpos, ypos, ship_pointlist, rotation)
            pygame.gfxdraw.aapolygon(screen, ship_pointlist, (255,255,255))
            pygame.gfxdraw.filled_polygon(screen, ship_pointlist, (255,255,255))
        if object_number == 2 or object_number == 8: #draws missiles (id 8 are alien missiles)
            pygame.draw.circle(screen, (255, 255, 255), (int(xpos), int(ypos)), 2, 0)

        #reserve ships no longer a thing
        #if object_number == 3: #draws reserve ships
        #    res_ship_pointlist = [[xpos, ypos-30*scalar3], [xpos+15*scalar3, ypos+10*scalar3], [xpos, ypos], [xpos-15*scalar3, ypos+10*scalar3]]
        #    pygame.gfxdraw.aapolygon(screen, res_ship_pointlist, (255,255,255))
        #    pygame.gfxdraw.filled_polygon(screen, res_ship_pointlist, (255,255,255))

        if object_number == 4: #draws explosion effects
            pygame.draw.circle(screen, (255, 255, 255), (int(xpos), int(ypos)), 1, 0)
        if object_number == 5: #draws shielded ship
            ship_pointlist = [[xpos, ypos-30*scalar3], [xpos+15*scalar3, ypos+10*scalar3], [xpos, ypos], [xpos-15*scalar3, ypos+10*scalar3]]
            ship_pointlist = Rotate(xpos, ypos, ship_pointlist, rotation)
            pygame.gfxdraw.aapolygon(screen, ship_pointlist, (100,100,100))
            pygame.gfxdraw.filled_polygon(screen, ship_pointlist, (100,100,100))
        if object_number == 6: #draws alien
            alien_pointlist = [[xpos-25*scalar1, ypos], [xpos-18*scalar1, ypos], [xpos-10*scalar1, ypos+8*scalar1], [xpos+10*scalar1, ypos+8*scalar1], [xpos+18*scalar1, ypos], [xpos+25*scalar1, ypos], [xpos-18*scalar1, ypos],
                            [xpos-10*scalar1, ypos], [xpos-7*scalar1, ypos-7*scalar1], [xpos, ypos-10*scalar1], [xpos+7*scalar1, ypos-7*scalar1], [xpos+10*scalar1, ypos]]
            pygame.draw.aalines(screen, (255,255,255), True, alien_pointlist, False)
        if 9 < object_number < 40: #draws satellites
            image = rotatePixelArt(graphlist[object_number-10], rotation)
            screen.blit(image, (xpos, ypos))
        if 69 < object_number < 100: #draws asteroids
            AsteroidList = Asteroid.getPoints(xpos, ypos, object_number)
            newAsteroidList = Rotate(xpos, ypos, AsteroidList, rotation)
            pygame.draw.aalines(screen, (255,255,255), True, newAsteroidList, 4)
            


def portalcollision(object_list, portalcoords):
    if (portalcoords[0] < object_list[0] < portalcoords[0] + portalcoords[2] and portalcoords[1] < object_list[1] < portalcoords[1] + portalcoords[3]
        and (object_list[4] == 1 or object_list[4]==5)):
        return True
    else:
        return False

def getHitbox(object_list, object_location, scalar3, specialpics, graphlist):
    xpos = object_list[object_location*8]
    ypos = object_list[1+object_location*8]
    objectID = object_list[4+object_location*8]
    
    hitBox = [xpos, ypos, 0,0]
    if objectID == 1: #main ship
        hitBox = [xpos-15*scalar3, ypos-15*scalar3, 30*scalar3, 30*scalar3]
    elif objectID == 2 or objectID == 8: #shots
        hitBox = [xpos-2, ypos-2, 4, 4]
    elif objectID == 6: #aliens
        hitBox = [xpos, ypos, 60, 60]
    elif objectID == 0: #zvezda
        hitBox = [xpos, ypos, specialpics[1].get_size()[0], specialpics[1].get_size()[1]]
    elif 9 < objectID < 40: #pixel things
        image = rotatePixelArt(graphlist[objectID-10], object_list[object_location*8+5])
        hitBox = [xpos, ypos, image.get_size()[0], 
                   image.get_size()[1]]
    elif 69 < objectID < 100: #asteroids
        hitBox = Asteroid.getHitbox(xpos, ypos, objectID)
    return hitBox

def collinfo(object_number1, object_number2, object_list, scalar3, specialpics, graphlist, DEVMODE):
    intersection = False
    if object_number1 != object_number2: #exempts object intersecting itself
        #hitBox = [xpos, ypos, width, height]

        hitBox1 = getHitbox(object_list, object_number1, scalar3, specialpics, graphlist)
        hitBox2 = getHitbox(object_list, object_number2, scalar3, specialpics, graphlist)

        # shows all the hitboxes
        if DEVMODE:
            if hitBox1[2] != 0 and hitBox1[3] != 0:
                pygame.draw.rect(screen, (255,255,255), hitBox1, 3)
            if hitBox2[2] != 0 and hitBox1[3] != 0:
                pygame.draw.rect(screen, (255,255,255), hitBox2, 3)
        
        if hitBox1[2] != 0 and hitBox1[3] != 0 and hitBox2[2] != 0 and hitBox1[3] != 0:
            if pygame.Rect(hitBox1).colliderect(pygame.Rect(hitBox2)):
                intersection = True
    return intersection

def explosion_sounds():
    explosion1 = pygame.mixer.Sound(handlePath("Assets\\Bomb1.wav"))
    explosion2 = pygame.mixer.Sound(handlePath("Assets\\Bomb2.wav"))
    explosion1.set_volume(0.05)
    explosion2.set_volume(0.05)
    explosion_picker = random.randint(0,1)
    if explosion_picker == 0:
        explosion1.play()
    if explosion_picker == 1:
        explosion2.play()

def saveGame(sectornum, object_list, width, height):
    if sectorGeneration(sectornum):
        saveObjects(sectornum, [-1], width, height)
    else:
        saveObjects(sectornum, object_list[:], width, height)

def saveObjects(sectornum, save_list, width, height):
    for i in range(len(save_list)):
        if isinstance(save_list[i], float):
            save_list[i] = round(save_list[i], 1)
        if len(save_list) >= 8:
            # turning x and y coords into float percentages
            if i % 8 == 0:
                save_list[i] = round(save_list[i]/width, 3)
            if i % 8 == 1:
                save_list[i] = round(save_list[i]/height, 3)
                        
    if len(save_list) >= 1000:
        save_list = save_list[:1000]
        print("Error: overflow in Main/saveObjects")
    savelist = []
    listhelper = int(len(save_list)/200) #200 = entities per level
    for i in range(listhelper):
        savelist.append(save_list[:200])
        save_list = save_list[200:]
    savelist.append(save_list)    
    listhelper = 5- len(savelist)
    for i in range(listhelper):
        savelist.append([])    
    for i in range(5):
        filehelper.set(savelist[i], sectornum*5+i)

def getObjects(sectornum, width, height):
    object_list = []
    for i in range(5):
        object_list += filehelper.get(sectornum*5+i)
    if object_list != []:
        while object_list[-1] == '':
            object_list.pop()
    # turning x and y float percentages back into coords
    if len(object_list) >= 8:
        for i in range(len(object_list)):
            if i % 8 == 0:
                object_list[i] = round(object_list[i]*width)     
            if i % 8 == 1:
                object_list[i] = round(object_list[i]*height)
    for i in range(int(len(object_list)/8)):
        if object_list[4+i*8] == 2 or object_list[4+i*8] == 8:
            object_list[6+i*8] = -10 #gets rid of shots and alien shots when entering a sector
    return object_list

def drawSector(location, number, currentsector):
    secsize = 80 #side length of the cubes
    if number != currentsector:
        pygame.draw.rect(screen, (255,255,255), (location[0]-secsize/2, location[1]-secsize/2, secsize, secsize), 4)
    if number == currentsector:
        pygame.draw.rect(screen, (255,15,25), (location[0]-secsize/2, location[1]-secsize/2, secsize, secsize), 4)
        Texthelper.write(screen, [(location[0]-35, location[1]-35), "U R Here", 1])
    if len(str(number)) == 1:
        Texthelper.write(screen, [(location[0]-10, location[1]-15), str(number), 2])
    else:
        Texthelper.write(screen, [(location[0]-20, location[1]-15), str(number), 2])
        
#just for generating backgrounds for manually built levels
def generateStars(width, height):
    object_list = []
    for i in range(20):
        object_list += [random.randint(0,100)/100*width, random.randint(0,100)/100*height, 0, 0, 100, "NA", 1, False]
    print(object_list)
    
def main():
    global screen
    file_settings = filehelper.get(0) #grabs settings from file

    #sets adjustable settings
    width = int(file_settings[0])
    height = int(file_settings[1])
    max_asteroids = 8
    drag = [1,5]

    #graphical setup
    graphlist = [loadImage("Assets\\sat1.tif"), loadImage("Assets\\sat2.tif"), loadImage("Assets\\sat3.tif"),
                 loadImage("Assets\\sat4.tif"), "s", "d", "f", "h", "j", "k", "l", "a", "s", "e", "as", "4", "3", "2", "1", #random elements to pad indices
                 loadImage("Assets\\solarpanel.tif")]
    fuelpic = scaleImage(loadImage("Assets\\fuelcanister.tif"), 2)
    armorpic = loadImage("Assets\\armor.tif")
    earthpic = loadImage("Assets\\earth.tif")
    specialpics = [loadImage("Assets\\star.tif"), scaleImage(loadImage("Assets\\zvezda.tif"), 2)]
    infinitypic = loadImage("Assets\\infinity.tif")

    #scaling
    scalarscalar = height / 1080
    scalar2 = 1.5 * scalarscalar # controls asteroid size
    scalar3 = 1.2 * scalarscalar # controls ship size
    alien_size = [1.2 * scalarscalar, 1.8 * scalarscalar]

    # settings
    max_speed = 4 * scalarscalar
    missile_lifespan = 130 * scalarscalar
    missile_accel = 7 * scalarscalar
    step_x = 0.08 * scalarscalar
    step_y = 0.08 * scalarscalar
    step_r = 2.3
    step_drag = 0.004 * scalarscalar
    max_asteroid_spd = 270 * scalarscalar
    color = (0, 0, 0) # for background
    shield_lifespan = 300
    DEVMODE = False

    # pygame setup
    pygame.init()
    pygame.display.set_caption("Kessler Syndrome")
    logo = loadImage("Assets\\earth2.png")
    pygame.display.set_icon(logo)
    if width == 0 or height == 0:
        screen_sizes = pygame.display.list_modes()
        screen_sizes = screen_sizes[0]
        width = screen_sizes[0]
        height = screen_sizes[1]
    if file_settings[2]:
        screen = pygame.display.set_mode([width, height], pygame.NOFRAME | pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([width, height])
        
    # variable setup
    d_parts = [30]
    d_sats = [10, 11, 12, 13, 71, 72, 73, 80, 81, 82, 91]
    d_only_sats = [10, 11, 12, 13]
    status = "menuinit"
    flame = False
    menu_music_fadeout_OG = 1200
    menu_music_fadeout = menu_music_fadeout_OG
    clock = pygame.time.Clock()
    sectornum = 1
    portalcoords = [(0, height/2-75, 25, 150), (width/2-75, 0, 150, 25), (width-25, height/2-75, 25, 150), (width/2-75, height-25, 150, 25)]
    lasttransit = 0

    # class setup
    Asteroid(scalar2) #sets up Asteroid class to return lists of the appropriate scale
    Screenhelper(width,height)
    #texthelper setup for scaling
    Texthelper.scalar = scalarscalar
    Texthelper.width = width
    Texthelper.height = height
    #announcementbox setup
    AnnouncementBox.width = width
    AnnouncementBox.height = height
    
    
    running = True
    while running:
        clock.tick(100)
     
        if status == "menuinit":
            # sound
            pygame.mixer.init()
            menu_music = pygame.mixer.Sound(handlePath("Assets\\AsteroidsTitle.wav"))
            menu_music.play(-1)
            menu_music.set_volume(0.4)
            menu_music_fadeout = menu_music_fadeout_OG

            pygame.mouse.set_visible(True)
            screen.fill(color)
            status = "menu" 

        if status == "menu": #if game is in menu
            # actual text
            text_input = [(300, 540-200), "Kessler Syndrome", 7]
            Texthelper.write(screen, text_input)
            
            # buttons
            text_input = [(410, 540-50), "[Play]", 3]
            if Texthelper.writeButton(screen, text_input):
                status = "gameinit"
                menu_music.fadeout(menu_music_fadeout)
            text_input = [(410, 550), "[Quit to desktop]", 3]
            if Texthelper.writeButton(screen, text_input): #if "quit to desktop" is clicked           
                pygame.quit() #stop the program
                raise SystemExit #close the program            
            screen.blit(earthpic, (1500,800))
            pygame.display.flip()
            
        if status == "pauseinit":
            filehelper.set([currentarmor, currentfuel, ammunition], 4)
            pygame.mouse.set_visible(True)
            Screenhelper.greyOut(screen)
            pauseinitUI(screen)
            pygame.display.flip()
            saveGame(sectornum, object_list[:], width, height)
            status = "paused"

        if status == "paused":
            status = pauseUI(screen)
            pygame.display.flip()

        if status == "gameoverinit":            
            pygame.mouse.set_visible(True)
            gameoverinitUI(screen)
            pygame.display.flip()
            status = "gameover"

        if status == "gameover":
            status = gameoverUI(screen)
            pygame.display.flip()

        if status == "mapscreeninit":
            pygame.mouse.set_visible(True)
            Screenhelper.greyOut(screen)
            #consider automating connection drawing by using a map drawing method that would look at sectordesinations
            drawSector((960, 990), 1, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (960-40, 990), (820+40, 970))
            drawSector((820, 970), 2, sectornum)
            screen.blit(infinitypic, (800,855)) #x-10, y+15
            pygame.draw.aaline(screen, (255,255,255), (820, 970-40), (810, 840+40))
            drawSector((810, 840), 4, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (960, 990-40), (970, 830+40))
            pygame.draw.aaline(screen, (255,255,255), (810+40, 840), (970-40, 830))
            drawSector((970, 830), 5, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (960+40, 990), (1110-40, 980))
            drawSector((1110, 980), 3, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (970, 830-40), (965, 690+40))
            drawSector((965, 690), 6, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (965+40, 690), (1115-40, 680))
            drawSector((1115, 680), 7, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (965-40, 690), (830+40, 675))
            drawSector((830, 675), 8, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (830, 675-40), (865, 535+40))
            drawSector((865, 535), 10, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (1115, 680-40), (1060, 525+40))
            pygame.draw.aaline(screen, (255,255,255), (865+40, 535), (1060-40, 525))
            drawSector((1060, 525), 9, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (1060, 525-40), (1095, 385+40))         
            drawSector((1095, 385), 14, sectornum)
            screen.blit(infinitypic, (1085,400)) #x-10, y+15
            drawSector((700, 630), 12, sectornum)
            screen.blit(infinitypic, (690,645)) #x-10, y+15
            pygame.draw.aaline(screen, (255,255,255), (830-40, 675), (700+40, 630))
            pygame.draw.aaline(screen, (255,255,255), (865, 535-40), (830, 400+40))
            drawSector((830, 400), 11, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (700,630-40), (690,455+40))
            pygame.draw.aaline(screen, (255,255,255), (690+40, 455), (830-40, 400))
            drawSector((690, 455), 13, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (830+40, 400), (965-40, 415))
            drawSector((965, 415), 17, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (1095, 385-40), (1055, 250+40))
            drawSector((1055, 250), 15, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (840+40,245), (1055-40,250))
            pygame.draw.aaline(screen, (255,255,255), (830,400-40), (840,245+40))
            drawSector((840, 245), 16, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (840,245-40), (870,105+40))
            drawSector((870, 105), 18, sectornum)
            pygame.draw.aaline(screen, (255,255,255), (870+40,105), (1030-40,90))
            drawSector((1030, 90), 19, sectornum)
            status = mapscreenUI(screen)            
            pygame.display.flip()
            status = "mapscreen"

        if status == "mapscreen":
            status = mapscreenUI(screen)
            pygame.display.flip()

        if status == "exiting":
            pygame.quit()
            raise SystemExit

        if status == "homeinit":
            filehelper.set([currentarmor, currentfuel, ammunition], 4)
            fuelHelp = upgrades.get(ShipLv[1]+20)
            totalfuel = fuelHelp[4]
            armorHelp = upgrades.get(ShipLv[0])
            totalarmor = armorHelp[4]
            totalammunition = 0
            if ShipLv[2] == 0:
                totalammunition = 0
            else:
                ammunitionHelp = upgrades.get(ShipLv[2]+40)
                totalammunition = ammunitionHelp[4]
            screen.fill(color)
            homeinitUI(screen, homeInventory)
            pygame.display.flip()
            status = "home"

        if status == "home":
            homeHelp = homeUI(screen, shipInventory, homeInventory)
            pygame.display.flip()
            status = homeHelp[0]
            shipInventory = homeHelp[1]

        if status == "shopinit":
            screen.fill(color)
            currentStats = filehelper.get(4)
            totalStats = (totalarmor, totalfuel, totalammunition)
            drawRepairScreen(screen, ShipLv, currentStats, totalStats, homeInventory, True)
            status = "shop"

        if status == "shop":
            status = drawRepairScreen(screen, ShipLv, currentStats, totalStats, homeInventory, False)
            currentarmor, currentfuel, ammunition = filehelper.get(4) #not very elegant to do this every tick
            pygame.display.flip()

        if status == "garageinit":
            #ship lv [armor, fuel]
            screen.fill(color)
            ShipLv = filehelper.get(3)
            homeInventory = filehelper.get(2)
            garageinitUI(screen, ShipLv, homeInventory)
            pygame.display.flip()
            status = "garage"

        if status == "garage":
            status = GarageUI(screen)
            pygame.display.flip()
                
        if status == "armorUpgradeinit":
            screen.fill(color)
            armorUpgradeinitUI(screen, ShipLv, homeInventory)
            pygame.display.flip()
            status = "armorUpgrade"

        if status == "armorUpgrade":
            status = armorUpgradeUI(screen, ShipLv, homeInventory)
            pygame.display.flip()

        if status == "fuelUpgradeinit":
            screen.fill(color)
            fuelUpgradeinitUI(screen, ShipLv, homeInventory)
            pygame.display.flip()
            status = "fuelUpgrade"

        if status == "fuelUpgrade":
            status = fuelUpgradeUI(screen, ShipLv, homeInventory)
            pygame.display.flip()

        if status == "ammoUpgradeinit":
            screen.fill(color)
            ammoUpgradeinitUI(screen, ShipLv, homeInventory)
            pygame.display.flip()
            status = "ammoUpgrade"

        if status == "ammoUpgrade":
            status = ammoUpgradeUI(screen, ShipLv, homeInventory)
            pygame.display.flip()

        if status == "gameinit":       
            # changing variable setup
            object_list = getObjects(sectornum, width, height)
            previous_tick = 0
            previous_tick2 = 0
            scalar1 = 0

            # sound
            beat_timer = 250
            max_beat_timer = beat_timer
            beat1 = pygame.mixer.Sound(handlePath("Assets\\Beat1loud.wav"))
            beat1.set_volume(0.9)
            beat2 = pygame.mixer.Sound(handlePath("Assets\\Beat2loud.wav"))
            beat2.set_volume(0.9)
            missilesound = pygame.mixer.Sound(handlePath("Assets\\missilesound.wav"))
            missilesound.set_volume(0.35)
            enginesound = pygame.mixer.Sound(handlePath("Assets\\enginesoundloud.wav"))
            enginesound.set_volume(0.2)
            timer1 = 0

            pygame.mouse.set_visible(False)
            
            #inventory
            homeInventory = filehelper.get(2)
            shipInventory = [0,0,0,0,0]

            #fuel and armor and ammunition
            upgrades = Filehelper("assets\\upgrades.txt")
            ShipLv = filehelper.get(3)
            fuelHelp = upgrades.get(ShipLv[1]+20)
            totalfuel = fuelHelp[4]
            currentfuel = filehelper.get(4)[1]
            armorHelp = upgrades.get(ShipLv[0])
            totalarmor = armorHelp[4]
            currentarmor = filehelper.get(4)[0]
            totalammunition = 0
            if ShipLv[2] == 0:
                totalammunition = 0
            else:
                ammunitionHelp = upgrades.get(ShipLv[2]+40)
                totalammunition = ammunitionHelp[4]
            ammunition = filehelper.get(4)[2]

            if file_settings[3] == 0:
                level1(screen, width, height)
                file_settings[3] = 1
                filehelper.set(file_settings, 0)
                file_settings = filehelper.get(0)

            if file_settings[3] == 1:
                AnnouncementBox(loadImage("Assets\\announcements\\warden.png"), pygame.mixer.Sound(file="Assets\\announcements\\prototype.wav"),
                                "Hey you, still alive out there? Then go pick up some space debris like a good prisoner")
                file_settings[3] = 2
                filehelper.set(file_settings, 0)
            
            status = "game"

        if status == "game":
            screen.fill(color)
            AnnouncementBox.play(screen)
            Font.timerhelper() #once a game loop update to a scramble timer

            # sound
            if menu_music_fadeout >= 0:
                menu_music_fadeout -= 10
            if menu_music_fadeout < 0:
                if beat_timer == max_beat_timer:
                    beat2.stop()
                    beat1.play()
                beat_timer -= 1
                if beat_timer == int(max_beat_timer/2):
                    beat1.stop()
                    beat2.play()
                if beat_timer <= 0:
                    beat_timer = max_beat_timer    
            # sound
            
            # input handling
            inputvar = keyboard()
            thrust_vector = (math.cos(math.radians(object_list[5]-90)), math.sin(math.radians(object_list[5]+90)))
            ticks = pygame.time.get_ticks()
            if inputvar:
                if object_list[4] == 1 or object_list[4] == 5:
                    if "w" in inputvar or "uparrow" in inputvar:
                        object_list[2] += step_x * thrust_vector[0]
                        object_list[3] += step_y * thrust_vector[1]
                        flame = True
                    if "e" in inputvar or "rightarrow" in inputvar:
                        object_list[5] += step_r
                    if "q" in inputvar or "leftarrow" in inputvar:
                        object_list[5] -= step_r
                    if "space" in inputvar and (ticks - previous_tick) > 360 and ammunition > 0:
                        ammunition -= 1
                        xmom_miss = object_list[2] + (thrust_vector[0] * missile_accel)
                        ymom_miss = object_list[3] + (thrust_vector[1] * missile_accel)
                        front_pointlist = RotatePoint(object_list[0], object_list[1], [object_list[0], object_list[1]-30*scalar3], object_list[5])
                        object_list_addition = [front_pointlist[0][0], front_pointlist[0][1], xmom_miss, ymom_miss, 2, "NA", "NA", missile_lifespan]
                        object_list += object_list_addition
                        previous_tick = ticks
                        missilesound.stop()
                        missilesound.play()
                if "shift" in inputvar and "c" in inputvar and (ticks - previous_tick2) > 360:
                    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    while color[0] + color[1] + color[2] > 150:
                        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    previous_tick2 = ticks
                if "m" in inputvar:
                    status = "mapscreeninit"
                if "escape" in inputvar or "p" in inputvar or "windows" in inputvar and len(inputvar) == 1:
                    status = "pauseinit"
                lasttransit += 1
                if "a" in inputvar and "d" in inputvar:
                    destinations = sectorDestinations(sectornum)
                    for i in range(4):
                        if destinations[i] != -1:
                            pygame.draw.rect(screen, (120,22,78), portalcoords[i])
                            if portalcollision(object_list, portalcoords[i]) and lasttransit > 150:
                                saveGame(sectornum, object_list, width, height)
                                sectornum = destinations[i]
                                lasttransit = 0
                                new_objects = getObjects(sectornum, width, height)
                                if new_objects[0] == -1 and len(new_objects)<8:
                                    object_list = leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, shield_lifespan)
                                else:
                                    object_list = object_list[:8] + new_objects[8:]
                if "shift" in inputvar and "d" in inputvar and (ticks - previous_tick2) > 360:
                    DEVMODE = not DEVMODE #switches booleans
                    previous_tick2 = ticks
                if "shift" in inputvar and "f" in inputvar and (ticks - previous_tick2) > 360:
                    colorA = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    while colorA[0] + colorA[1] + colorA[2] > 150:
                        colorA = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                    Font.changeColor(colorA)
                    previous_tick2 = ticks
            # input handling

            # collision detection                         
            for i in range(int(len(object_list)/8)):
                i2 = i + 1
                while i2 < int(len(object_list)/8):                   
                    if collinfo(i,i2,object_list, scalar3, specialpics, graphlist, DEVMODE) == True:
                        printerlist_add = []
                        if object_list[4 + (i * 8)] == 1 and object_list[4 + (i2 * 8)] in d_only_sats: #ship v satellite collision
                            printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)], object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                            object_list[(i2*8)+7] = -1
                            if ShipLv[2] == 0:
                                shipInventory[random.randint(0,1)] += 1
                            else:
                                shipInventory[random.randint(0,2)] += 1
                        elif object_list[4 + (i * 8)] == 1 and object_list[4 + (i2 * 8)] == 0: #going to garage
                            #InGameTextBox(screen, 800, 500, 150, 50, "press enter", 1)
                            Texthelper.writeBox(screen, [(800,500), "press enter", 1], color = (0,100,200))
                            if "enter" in inputvar:
                                status = "homeinit"
                        elif object_list[4 + (i * 8)] == 1 and 69 < object_list[4 + (i2 * 8)] < 100: #ship v asteroid collision
                            xForce = abs(object_list[2+(i*8)] - object_list[2+(i2*8)]) 
                            yForce = abs(object_list[3+(i*8)] - object_list[3+(i2*8)])
                            force = xForce + yForce
                            printerlist_add += particlemaker(object_list[(i2 * 8)], object_list[1+(i2 * 8)], object_list[2+(i2 * 8)], object_list[3+(i2 * 8)])
                            object_list[(i2*8)+7] = -1
                            currentarmor = currentarmor - force
                            Font.scramble(100) #scrambles text for 100 ticks
                        elif object_list[4 + (i2 * 8)] == 2 and 69 < object_list[4 + (i * 8)] < 100: #missile v asteroid collision
                            printerlist_add += particlemaker(object_list[(i * 8)], object_list[1+(i * 8)], object_list[2+(i * 8)], object_list[3+(i * 8)])
                            object_list[(i2*8)+7] = -1
                            object_list[(i*8)+7] = -1
                        elif object_list[4 + (i2 * 8)] == 2 and object_list[4 + (i * 8)] in d_only_sats: #missile v satellite collision
                            printerlist_add += particlemaker(object_list[(i * 8)], object_list[1+(i * 8)], object_list[2+(i * 8)], object_list[3+(i * 8)])
                            object_list[(i2*8)+7] = -1
                            object_list[(i*8)+7] = -1
                        object_list += printerlist_add
                    i2 += 1
                        
            # collision detection

            #inventory
            Texthelper.write(screen, [(0, 0), "metal:" + str(shipInventory[0]) + "   gas:" + str(shipInventory[1]) + "   circuits:" + str(shipInventory[2]) + "    currency:" + str(shipInventory[3]) + "    torpedoes:" + str(shipInventory[4]),3])

            # deaderizer
            object_list = deaderizer(object_list)
            
            # fuel consumption
            if flame == True:
                currentfuel -= 1

            #ship death
            if currentarmor <= 0 or currentfuel <= 0:
                saveGame(sectornum, object_list, width, height)
                object_list[6] = -10
                sectornum = 1
                object_list = getObjects(sectornum, width, height)
                currentfuel = totalfuel
                currentarmor = totalarmor
                shipInventory = [0,0,0,0,0]
                lasttransit = 0
                object_list[0] = width/2 - width*0.3
                object_list[1] = height/2 - height*0.2
                object_list[2] = 0
                object_list[3] = 0

            #physics!
            object_list = doPhysics(object_list, width, height, max_speed, drag, step_drag)
            
            # printer and flame and score            
            printer2(object_list, scalar1, scalar3, graphlist, scalarscalar, specialpics)
            if flame == True and (object_list[4] == 1 or object_list[4] == 5):
                #flame_pointlist = [[50 + 6, 50 + 5], [50, 50 + 20], [50 - 6, 50 + 5]]
                flame_pointlist = [[object_list[0], object_list[1]], [object_list[0]+6*scalar3, object_list[1]+5*scalar3], [object_list[0], object_list[1]+20*scalar3],
                                   [object_list[0]-6*scalar3, object_list[1]+5*scalar3]]
                flame_pointlist = Rotate(object_list[0], object_list[1], flame_pointlist, object_list[5])
                pygame.gfxdraw.aapolygon(screen, flame_pointlist, (255,100,0))
                pygame.gfxdraw.filled_polygon(screen, flame_pointlist, (255,100,0))
            if flame == True and timer1 == 0:
                enginesound.stop()
                enginesound.play()
            if flame == True and timer1 < 21:
                timer1 += 1
            if flame == True and timer1 == 21:
                timer1 = 0
            if flame == False:
                enginesound.fadeout(10)
            flame = False
            #fuel
            screen.blit(fuelpic, (1600, 1000))
            pygame.draw.rect(screen, (178,34,34), [1650, 1000, 200, 50])
            pygame.draw.rect(screen, (139,0,0), [1650, 1000, 200*currentfuel/totalfuel, 50])
            #armor
            screen.blit(armorpic, (1600, 930))
            pygame.draw.rect(screen, (128,128,128), [1650, 930, 200, 50])
            pygame.draw.rect(screen, (64,64,64), [1650, 930, 200*currentarmor/totalarmor, 50])
            #ammunition
            Texthelper.write(screen,[(1650,860), "shots:" + str(ammunition),3])
            if DEVMODE:
                Texthelper.write(screen, [(1800, 20), str(round(clock.get_fps())),3])
            pygame.display.flip()
            # printer and flame and score
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                raise SystemExit


#checks if it needs to run setupper
if filehelper.get(0)[0] == "?":
    from setupper import *
    
main()
