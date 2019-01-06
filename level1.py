from pgx import *
def level1(screen, width, height):
    import pygame
    import random
    clock = pygame.time.Clock()
    soyuz = loadImage("Assets\\soyuz2.tif")  
    soyuzscalar = 1
    soyuz = scaleImage(soyuz, soyuzscalar)
    soyuzsize = soyuz.get_size()    

    mountains = loadImage("Assets\\cutsceneback.tif")
    mountainsize = mountains.get_size()
    mountains = pygame.transform.scale(mountains, (width, int(width/mountainsize[0]*mountainsize[1])))
    mountainsize = mountains.get_size()

    flame1 = scaleImage(loadImage("Assets\\FlameAnimation\\flame1.tif"), soyuzscalar*2)
    flame2 = scaleImage(loadImage("Assets\\FlameAnimation\\flame2.tif"), soyuzscalar*2)
    flame3 = scaleImage(loadImage("Assets\\FlameAnimation\\flame3.tif"), soyuzscalar*2)
    flame4 = scaleImage(loadImage("Assets\\FlameAnimation\\flame4.tif"), soyuzscalar*2)
    flame5 = scaleImage(loadImage("Assets\\FlameAnimation\\flame5.tif"), soyuzscalar*2)
    flame6 = scaleImage(loadImage("Assets\\FlameAnimation\\flame6.tif"), soyuzscalar*2)
    flame7 = scaleImage(loadImage("Assets\\FlameAnimation\\flame7.tif"), soyuzscalar*2)
    flame8 = scaleImage(loadImage("Assets\\FlameAnimation\\flame8.tif"), soyuzscalar*2)
    startflamelist = [flame1, flame2]
    flame_list = [flame3, flame4, flame5, flame6, flame7, flame8]      

    def randomflame(ypos):
        if (ypos+1400) < (height - height*0.2):
           return flame_list[random.randint(0, len(flame_list)-1)]
        else:
            return startflamelist[random.randint(0, len(startflamelist)-1)]
    
    xpos = width/2 - soyuzsize[0]/2
    ypos = height
    dy = height/700
    namebox = InputGetter([("center", 200), "name", 3], "str")
    running = True
    while running:
        clock.tick(100)
        screen.fill((0,191,255))
        screen.blit(mountains, (0, height-mountainsize[1]))

        Texthelper.write(screen, [("center", ypos+000), "The year is 2023", 3])
        Texthelper.write(screen, [("center", ypos+100), "76 years after the aliens came", 3])
        Texthelper.write(screen, [("center", ypos+200), "and crashed in New Mexico", 3])
        Texthelper.write(screen, [("center", ypos+300), "more aliens came to investigate", 3])
        Texthelper.write(screen, [("center", ypos+400), "and thought the humans responsible", 3])
        Texthelper.write(screen, [("center", ypos+500), "so they bombarded Earth", 3])
        Texthelper.write(screen, [("center", ypos+600), "the humans managed to repel them", 3])
        Texthelper.write(screen, [("center", ypos+700), "but the retreating aliens were angry", 3])
        Texthelper.write(screen, [("center", ypos+800), "and filled the orbitals with debris", 3])
        Texthelper.write(screen, [("center", ypos+900), "you have been framed for treason", 3])
        Texthelper.write(screen, [("center", ypos+1000), "and your sentence is to clean up space", 3])
        Texthelper.write(screen, [("center", ypos+1100), "until it is safe enough", 3])
        Texthelper.write(screen, [("center", ypos+1200), "for non expendable humans", 3])

        screen.blit(soyuz, (xpos, ypos+1400))
        screen.blit(randomflame(ypos), (xpos-4*soyuzscalar, ypos+soyuzsize[1]+1400))
        screen.blit(randomflame(ypos), (xpos+6*soyuzscalar, ypos+soyuzsize[1]+1400))
        screen.blit(randomflame(ypos), (xpos+10*soyuzscalar, ypos+soyuzsize[1]+1400))
        screen.blit(randomflame(ypos), (xpos+20*soyuzscalar, ypos+soyuzsize[1]+1400))

        if ypos+1700 > height/2-100:
            namebox.currenttext = [("center", ypos+1750), namebox.getData()[1], namebox.getData()[2]]
            Texthelper.write(screen, [("center", ypos+1700), "enter name to continue", 2])
        else:
            namebox.currenttext = [("center", height/2-50), namebox.getData()[1], namebox.getData()[2]]
            namebox.clicked = True
            Texthelper.write(screen, [("center", height/2-100), "enter name to continue", 2])
            if Texthelper.writeButton(screen, [("center", height/2), "then press here or enter", 2]):
                running = False
                filehelper.set([namebox.getText()], 1)
            if len(keyboard()) == 1 and keyboard()[0] == "enter" and namebox.getText() != "name":
                running = False
                filehelper.set([namebox.getText()], 1)                
            
        #namebox.currenttext = [("center", ypos+1850), namebox.getData()[1], namebox.getData()[2]]
        namebox.update(screen)
        
        ypos -= dy        
        pygame.display.flip()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                raise SystemExit
        