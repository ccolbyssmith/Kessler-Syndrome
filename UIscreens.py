from pgx import *

def garageinitUI(screen, ShipLv, inventory):
    screen.fill((0,0,0))
    pygame.mouse.set_visible(True)
    Texthelper.write(screen, [(0, 0), "sat1:" + str(inventory[0]) + "     sat2:" + str(inventory[1]) + "     sat3:" + str(inventory[2]) + "     sat4:" + str(inventory[3]), 3])
    Texthelper.write(screen, [("center", 540-136), "garage", 6])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [(600, 540-55), "Armor:", 3])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [(800, 540-55), "lv " + str(ShipLv[0]), 3])
    pygame.display.flip()
    pygame.time.wait(200)
    if inventory[0] >= ShipLv[0]*3:
        Texthelper.write(screen, [(1000, 540-55), "Upgrade", 3])
        pygame.display.flip()
        pygame.time.wait(200)
    else:
        Texthelper.write(screen, [(1000, 540-55), "sorry", 3])
        pygame.display.flip()
        pygame.time.wait(200)
    Texthelper.write(screen, [(1300, 540-55), "cost:" + str(ShipLv[0]*3)+ " sat1", 3])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [(600, 540), "Fuel:", 3])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [(800, 540), "lv " + str(ShipLv[1]), 3])
    pygame.display.flip()
    pygame.time.wait(200)
    if inventory[1] >= ShipLv[1]*3:
        Texthelper.write(screen, [(1000, 540), "Upgrade", 3])
        pygame.display.flip()
        pygame.time.wait(200)
    else:
        Texthelper.write(screen, [(1000, 540), "sorry", 3])
        pygame.display.flip()
        pygame.time.wait(200)
    Texthelper.write(screen, [(1300, 540), "cost:" + str(ShipLv[1]*3)+ " sat2", 3])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [("center", 540+55), "Resume", 3])
    pygame.display.flip()

def GarageUI(screen, ShipLv, inventory):
    status = "garage"
    if Texthelper.writeButton(screen, [(1000, 540-55), "Upgrade", 3]) and inventory[0] >= ShipLv[0]*3:
        inventory[0] = inventory[0] - (ShipLv[0]*3)
        ShipLv[0] += 1
        status = "garageinit"
    elif Texthelper.writeButton(screen, [(1000, 540), "Upgrade", 3]) and inventory[1] >= ShipLv[1]*3:
        inventory[1] = inventory[1] - (ShipLv[1]*3)
        ShipLv[1] += 1
        status = "garageinit"
    elif Texthelper.writeButton(screen, [("center", 540+55), "Resume", 3]):
        status = "game"
    return [status, ShipLv, inventory]

def pauseinitUI(screen):
    Texthelper.write(screen, [("center", 540-136), "Paused", 6])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [("center", 540-55), "Resume", 2])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [("center", 540-20), "Restart", 2])
    pygame.display.flip()
    pygame.time.wait(200)            
    Texthelper.write(screen, [("center", 540+15), "Quit to desktop", 2])
    pygame.display.flip()
    pygame.time.wait(200)
    Texthelper.write(screen, [("center", 540+50), "Quit to menu", 2])
    pygame.display.flip()

def gameoverinitUI(screen):
    text_input = [("center", 540-136), "Game over", 6]
    Texthelper.write(screen, text_input)            
    pygame.display.flip()
    pygame.time.wait(200)
    text_input = [("center", 540-55), "Play again", 2]
    Texthelper.write(screen, text_input)
    pygame.display.flip()
    pygame.time.wait(200)
    text_input = [("center", 540-20), "Quit to desktop", 2]
    Texthelper.write(screen, text_input)
    pygame.display.flip()
    pygame.time.wait(200)
    text_input = [("center", 540+15), "Quit to menu", 2]
    Texthelper.write(screen, text_input)
    pygame.display.flip()    

def pauseUI(screen):
    status = "paused"
    if Texthelper.writeButton(screen, [("center", 540-55), "Resume", 2]):
        pygame.mouse.set_visible(False)
        status = "game"
    elif Texthelper.writeButton(screen, [("center", 540-20), "Restart", 2]):
        status = "gameinit"   
    elif Texthelper.writeButton(screen, [("center", 540+15), "Quit to desktop", 2]):
        status = "exiting"
    elif Texthelper.writeButton(screen, [("center", 540+50), "Quit to menu", 2]):
        status = "menuinit"
    return status

def gameoverUI(screen):
    status = "gameover"
    if Texthelper.writeButton(screen, [("center", 540-55), "Play again", 2]):
        status = "gameinit"                
    elif Texthelper.writeButton(screen, [("center", 540-20), "Quit to desktop", 2]):
        status = "exiting"            
    elif Texthelper.writeButton(screen, [("center", 540+15), "Quit to menu", 2]):
        status = "menuinit"
    return status

def mapscreenUI(screen):
    status = "mapscreen"
    if Texthelper.writeButton(screen, [(180, 520), "[Commence Flying]", 2.5]):
        status = "game"
    return status
    