import pygame, sys, random, math, pyautogui, pygame_gui, time
from pygame.locals import QUIT
pygame.font.init()
pygame.freetype.init()
pygame.init()

#!aim trainer function
def aimTrainer(radius,timeRemaining,scoreMultiplier):

  #!variables:
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  #?creating clock?
  clock = pygame.time.Clock()
  #initialising clickCount, which stores the amount of times the user clicks
  clickCount = 0
  #initialising targetCount, which stores the amount of targets the user has hit
  targetCount = 0
  #assigning the font to timerFont
  timerFont = pygame.font.Font('digital-7.ttf',36)
  #assigning the font to mainFont
  scoreFont = pygame.font.SysFont('tahoma',36)
  #running gets assigned True so the rest of the game can be run
  running = True
  
  #!function to put timer onto screen
  def timerDisplay():
    #calculating the amount of minutes and seconds left until the timer reaches 0
    mins = timeRemaining//6000
    secs = (timeRemaining % 6000)//100
    #formatting and rendering the timer 
    timer = ' {:>02d}:{:>02d}'.format(mins,secs)
    timerScreen = timerFont.render(f"{timer}", 1, (0,0,255))
    #displaying the timer
    pygame.draw.rect(aimScreen,(255,255,255),(((screenWidth - timerScreen.get_width())//2),0,timerScreen.get_width() + 10,timerScreen.get_height() + 10))
    #creates a small background for the timer to make it stand out more
    aimScreen.blit(timerScreen,(((screenWidth - timerScreen.get_width())//2),5))
    pygame.display.update()

  #!function to create the target
  def createTarget(circleX,circleY,radius):
    # creates the outer red circle
    pygame.draw.circle(aimScreen, (255,0,0), (circleX,circleY), radius)
    #creates the middle white layer
    pygame.draw.circle(aimScreen, (255,255,255), (circleX,circleY), radius//3*2)
    #creates the red centre
    pygame.draw.circle(aimScreen, (255,0,0), (circleX,circleY), radius//3)


  #initialises imported pygame modules
  pygame.init()
  #creates a display with the dimensions of the users screen
  aimScreen = pygame.display.set_mode((screenWidth,screenHeight),pygame.SCALED)
  pygame.display.set_caption('Reflex tester program')



  #changes the mouse icon to a crosshair
  pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
  #calculating the amount of minutes and seconds left until the timer reaches 0
  mins = timeRemaining//6000
  secs = (timeRemaining % 6000)//100
  #formatting and rendering the timer 
  timer = ' {:>02d}:{:>02d}'.format(mins,secs)
  timerScreen = timerFont.render(f"{timer}", 1, (0,0,255))
  #generating the x and y co ordinates for the first circle
  circleX = random.randint(radius,screenWidth-radius)
  circleY = random.randint(radius + timerScreen.get_height(),screenHeight-50-radius)
  #draws the first circle
  createTarget(circleX,circleY,radius)
  #draws a button onto the screen that the user can press to quit the aim trainer
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager=manager)



  while running:
    #gets the x and y coordinates of where the mouse is
    mouseX,mouseY = pygame.mouse.get_pos()
    #using pythagoras' theorem to find the distance between the mouse click and the centre of the circle in a straight line which is a**2 + b**2 = c**2
    distanceX = (mouseX - circleX)**2 #a**2
    distanceY = (mouseY - circleY)**2 #b**2

    #code to close the program
    for event in pygame.event.get():
      #if the user clicks the x button on the window, then it closes the program
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      #increase clickCount by 1 everytime the user clicks
      if event.type == pygame.MOUSEBUTTONDOWN:
        clickCount += 1
      #loop to check if the user has clicked on the target and if they have clicked, whether or not they clicked on the circle
      if event.type == pygame.MOUSEBUTTONDOWN and math.sqrt(distanceX + distanceY) <= radius:
        #clears the screen
        aimScreen.fill((0,0,0))
        #generates the new location of the circle
        circleX = random.randint(radius + 10 ,screenWidth-radius)
        circleY = random.randint(radius + timerScreen.get_height(),screenHeight-50-radius)
        #draws the circle
        createTarget(circleX,circleY,radius)
        targetCount += 1
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(aimScreen)
    #calculate how much time the user has and displays it
    if timeRemaining > 0:
      timerDisplay()
      #decreasing timeRemaining by 1 every second
      timeRemaining -= 1
    #once timer reaches 0, closes the program
    if timeRemaining == 0:
      running = False
      finished = True

    clock.tick(100)
    pygame.display.update()
  
  while finished:
    score = ((targetCount/clickCount) * targetCount)
    score = ((score * scoreMultiplier)//0.1)/10
    scoreText = scoreFont.render(f"your score is: {score}", 1, (0,255,0))
    aimScreen.blit(scoreText,(((screenWidth - scoreText.get_width())//2),((screenHeight - scoreText.get_height())//2)))
    pygame.display.update()
    print(f"te score is {score}")
    time.sleep(5)
    finished = False
    aimScreen.fill((0,0,0))
    pygame.display.update()


#!aimTrainMenu() function
def aimTrainMenu():
  #!variables
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  easyButton = pygame_gui.elements.UIButton(relative_rect =pygame.Rect((((screenWidth-screenWidth//7)//2)-screenWidth//14-screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='easy',manager=manager)
  mediumButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//5), (screenWidth//7, screenHeight//10)),text='medium',manager=manager)
  hardButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='hard',manager=manager)
  unlimitedButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//14)//2 - screenWidth//7, screenHeight//2), (screenWidth//7, screenHeight//10)),text='unlimited time',manager=manager)
  timeButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth+screenWidth//14)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='timed',manager=manager)
  runButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight-(screenHeight//5)), (screenWidth//7, screenHeight//10)),text='run game',manager=manager)
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager=manager)


  #creates a display with the dimensions of the users screen
  menuScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  pygame.display.set_caption('Main Menu')

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == easyButton:
          print("EASY chosen")
          radius = 24
          #!?!?!?!?!?! YOU NEED OT PUT CODE HERE TO DRAW RECTANGLE AROUND ALL THE DIFFICULTY BUTONS SO U CAN COPY PASTE AS THIS THING COVERS UP THE CHOSEN DIFFICULTY
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//5-3,screenWidth,screenHeight//5+6))
          #draws red reactangle aroundthe ui button to show it has been selected 
          pygame.draw.rect(menuScreen, (255,0,0), (((screenWidth-screenWidth//7)//2)-screenWidth//14-screenWidth//7-3,screenHeight//5-3,screenWidth//7+6,screenHeight//10+6))
          scoreMultiplier = 0.25
        if event.ui_element == mediumButton:
          print("MEDIUM chosen")
          radius = 18
          scoreMultiplier = 0.5
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//5-3,screenWidth,screenHeight//5+6))
          pygame.draw.rect(menuScreen, (255,0,0), (((screenWidth-screenWidth//7)//2)-3,screenHeight//5-3,screenWidth//7+6,screenHeight//10+6))
        if event.ui_element == hardButton:
          print("HARD chosen")
          radius = 12
          scoreMultiplier = 1
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//5-3,screenWidth,screenHeight//5+6))
          pygame.draw.rect(menuScreen, (255,0,0), ((screenWidth-screenWidth//7)//2+screenWidth//14 + screenWidth//7-3,screenHeight//5-3,screenWidth//7+6,screenHeight//10+6))
        if event.ui_element == unlimitedButton:
          print("UNLIMITED chosen")
          timeRemaining = -1
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//2-3,screenWidth,screenHeight//10+6))
          pygame.draw.rect(menuScreen, (255,0,0), (((screenWidth-screenWidth//14)//2 - screenWidth//7)-3,screenHeight//2-3,screenWidth//7+6,screenHeight//10+6))
        if event.ui_element == timeButton:
          print("TIMED chosen")
          timeRemaining = 3000
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//2-3,screenWidth,screenHeight//10+6))
          pygame.draw.rect(menuScreen, (255,0,0), (((screenWidth+screenWidth//14)//2)-3,screenHeight//2-3,screenWidth//7+6,screenHeight//10+6))
        if event.ui_element == runButton:
          aimTrainer(radius,timeRemaining,scoreMultiplier)
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(menuScreen)
    pygame.display.update()

#!global
#getting the dimensions of the users display
screenWidth, screenHeight = pyautogui.size()


def reactionMenu():
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  runButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='run game',manager=manager)
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager=manager)  

  #creates a display with the dimensions of the users screen
  menuScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  pygame.display.set_caption('Reaction Menu')

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == runButton:
          print("you chose reaction speed tester")
          rTester()
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(menuScreen)
    pygame.display.update()

def rTester():
  pygame.display.update()
  reactScreen = pygame.display.set_mode((screenWidth,screenHeight),pygame.SCALED)
  reactionFont = pygame.font.SysFont('tahoma',36)

  #creating the quit button
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager=manager)
  #initialising the variable reactionState
  reactionState = "start"
  #generates a random delay fro when the screen changes colour
  randTime = random.randint(2000,10000)
  #gets the starting time for when the user runs the reaction tester
  startTime = pygame.time.get_ticks()
  #gets the time that the background changes colour
  changeTime = startTime + randTime

  running = True
  while  running:
    #gets the current amount of ticks
    currentTime = pygame.time.get_ticks()
    #changing the reaction state to "wait" as this is when the user waits for the screen to change colour
    if reactionState == "start":
      reactionState = "wait"
      reactScreen.fill((0,0,255))
    #changing the reaction state to be react when delay has finished
    if currentTime >= changeTime:
      reactionState = "react"
      reactScreen.fill((255,0,0))

    for event in pygame.event.get():
      #displays the quit button
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        #code to detect if the user clicks before the scren changes colour
        if reactionState == "wait":
          print("you no play more u cheater")
          scoreText = reactionFont.render(f"You clicked too early, try again", 1, (0,255,0))
          reactScreen.blit(scoreText,(((screenWidth - scoreText.get_width())//2),((screenHeight - scoreText.get_height())//2)))
          pygame.display.update()
          time.sleep(5)
          reactionMenu()
        #code to detect if the user clicks after the screen has changed colour
        if reactionState == "react":
          clickTime = pygame.time.get_ticks()
          running = False
          finished = True
          reactScreen.fill((0,0,0))
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(reactScreen)
    pygame.display.update()

  while finished:
    scoreTime = (clickTime - changeTime)
    scoreText = reactionFont.render(f"you took {scoreTime}ms", 1, (0,255,0))
    reactScreen.blit(scoreText,(((screenWidth - scoreText.get_width())//2),((screenHeight - scoreText.get_height())//2)))
    pygame.display.update()
    time.sleep(5)
    reactScreen.fill((0,0,0))
    pygame.display.update()
    finished = False



reactionMenu()