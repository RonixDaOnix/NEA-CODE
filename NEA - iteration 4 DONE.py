import pygame, sys, random, math, pyautogui, pygame_gui, time, os
from pygame.locals import QUIT
pygame.font.init()
pygame.freetype.init()
pygame.init()

def aimTrainer(radius,timeRemaining,scoreMultiplier):

  #creating the quit and menu buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  menuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10), (100, 25)),text='menu',manager = manager)
  #creates an object called clock which tracks time
  clock = pygame.time.Clock()
  #initialising clickCount, which stores the amount of times the user clicks
  clickCount = 0
  #initialising targetCount, which stores the amount of targets the user has hit
  targetCount = 0
  #creating a font object for the timer
  timerFont = pygame.font.Font('digital-7.ttf',36)
  #creating a font object for the score
  scoreFont = pygame.font.SysFont('tahoma',36)
  #running gets assigned True so the rest of the aim trainer can be run
  running = True

  #getting the values for loggedIn and accountName
  global loggedIn
  global accountName
  
  #function to put timer onto screen
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

  #function to create the target
  def createTarget(circleX,circleY,radius):
    # creates the outer red circle
    pygame.draw.circle(aimScreen, (255,0,0), (circleX,circleY), radius)
    #creates the middle white layer
    pygame.draw.circle(aimScreen, (255,255,255), (circleX,circleY), radius//3*2)
    #creates the red centre
    pygame.draw.circle(aimScreen, (255,0,0), (circleX,circleY), radius//3)


  #creates a display with the dimensions of the users screen
  aimScreen = pygame.display.set_mode((screenWidth,screenHeight),pygame.SCALED)



  #changes the mouse icon to a crosshair
  pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

  #calculating the amount of minutes and seconds left until the timer reaches 0
  mins = timeRemaining//6000
  secs = (timeRemaining % 6000)//100
  #formatting and rendering the timer 
  timer = ' {:>02d}:{:>02d}'.format(mins,secs)
  timerScreen = timerFont.render(f"{timer}", 1, (0,0,255))

  #generating the x and y co-ordinates for the first circle
  circleX = random.randint(radius,screenWidth-radius)
  circleY = random.randint(radius + timerScreen.get_height(),screenHeight-50-radius)
  #draws the first circle
  createTarget(circleX,circleY,radius)




  while running:
    #gets the x and y coordinates of where the mouse is
    mouseX,mouseY = pygame.mouse.get_pos()
    #using pythagoras' theorem to find the distance between the mouse click and the centre of the circle in a straight line which is a**2 + b**2 = c**2
    distanceX = (mouseX - circleX)**2 #a**2
    distanceY = (mouseY - circleY)**2 #b**2


    for event in pygame.event.get():
      #if the users clicks the x button, it closes the entire program
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      #increase clickCount by 1 everytime the user clicks
      if event.type == pygame.MOUSEBUTTONDOWN:
        clickCount += 1
      #checking if the user has clicked on the target and if they have clicked, whether or not they clicked on the circle
      if event.type == pygame.MOUSEBUTTONDOWN and math.sqrt(distanceX + distanceY) <= radius:
        #clears the screen
        aimScreen.fill((0,0,0))
        #generates the new location of the circle
        circleX = random.randint(radius + 10 ,screenWidth-radius)
        circleY = random.randint(radius + timerScreen.get_height(),screenHeight-50-radius)
        #draws the circle
        createTarget(circleX,circleY,radius)
        #increases targetCount by 1 everytime a new target is created
        targetCount += 1
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #closing the program if the quit button is clicked  
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        #opening the main menu if the menu button is clicked
        if event.ui_element == menuButton:
          mainMenu()
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(aimScreen)
    #calculate how much time the user has and displays it
    if timeRemaining > 0:
      timerDisplay()
      #decreasing timeRemaining by 1 every second
      timeRemaining -= 1
    #once timer reaches 0, it stops running the aim trainer displays the users score
    if timeRemaining == 0:
      running = False
      finished = True

    clock.tick(100)
    pygame.display.update()
  
  while finished:
    #calculating the score and displaying it on screen
    score = ((targetCount/clickCount) * targetCount)
    score = ((score * scoreMultiplier)//0.1)/10
    scoreText = scoreFont.render(f"your score is: {score}", 1, (0,255,0))
    aimScreen.blit(scoreText,(((screenWidth - scoreText.get_width())//2),((screenHeight - scoreText.get_height())//2)))
    pygame.display.update()
    #if the user is logged in, it saves the score in their score file
    if loggedIn == True:
      #creating the file to save the users scores if it doesnt exist
      scoreFile = accountName + 'AimScores.txt'
      if not os.path.exists(scoreFile):
        open(scoreFile, 'w').close()
      #saving the users score on the next line
      with open(scoreFile, 'a') as file:
        file.write(str(score) + "\n")
    #waiting 5 seconds so the user has time to see their score and then terminating the aim trainer
    time.sleep(5)
    finished = False
    aimScreen.fill((0,0,0))
    pygame.display.update()


#!aimTrainMenu() function
def aimTrainMenu():
  #creating all the buttons that the user can click to select which mode they want to play as well as the quit, menu and run game buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  easyButton = pygame_gui.elements.UIButton(relative_rect =pygame.Rect((((screenWidth-screenWidth//7)//2)-screenWidth//14-screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='easy',manager = manager)
  mediumButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//5), (screenWidth//7, screenHeight//10)),text='medium',manager = manager)
  hardButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='hard',manager = manager)
  unlimitedButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//14)//2 - screenWidth//7, screenHeight//2), (screenWidth//7, screenHeight//10)),text='unlimited time',manager = manager)
  timeButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth+screenWidth//14)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='timed',manager = manager)
  runButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight-(screenHeight//5)), (screenWidth//7, screenHeight//10)),text='run game',manager = manager)
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  menuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10), (100, 25)),text='menu',manager = manager)

  #creates a display with the dimensions of the users screen
  menuScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)

  while True:
    for event in pygame.event.get():
      #if the users clicks the x button, it closes the entire program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #changing the radius and score multiplier based on which difficulty the user chooses
        if event.ui_element == easyButton:
          radius = 24
          scoreMultiplier = 0.25
          #draws a black rectangle over the area of all the difficulty buttons which gets rid of the red rectangle that surround the buttons
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//5-3,screenWidth,screenHeight//5+6))
          #draws red reactangle around the button to show it has been selected 
          pygame.draw.rect(menuScreen, (255,0,0), (((screenWidth-screenWidth//7)//2)-screenWidth//14-screenWidth//7-3,screenHeight//5-3,screenWidth//7+6,screenHeight//10+6))
        if event.ui_element == mediumButton:
          radius = 18
          scoreMultiplier = 0.5
          #draws a black rectangle over the area of all the difficulty buttons which gets rid of the red rectangle that surround the buttons
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//5-3,screenWidth,screenHeight//5+6))
          #draws red reactangle around the button to show it has been selected 
          pygame.draw.rect(menuScreen, (255,0,0), (((screenWidth-screenWidth//7)//2)-3,screenHeight//5-3,screenWidth//7+6,screenHeight//10+6))
        if event.ui_element == hardButton:
          radius = 12
          scoreMultiplier = 1
          #draws a black rectangle over the area of all the difficulty buttons which gets rid of the red rectangle that surround the buttons
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//5-3,screenWidth,screenHeight//5+6))
          #draws red reactangle around the button to show it has been selected 
          pygame.draw.rect(menuScreen, (255,0,0), ((screenWidth-screenWidth//7)//2+screenWidth//14 + screenWidth//7-3,screenHeight//5-3,screenWidth//7+6,screenHeight//10+6))
        #changing the time remaining based on what mode th user chooses
        if event.ui_element == unlimitedButton:
          timeRemaining = -1
          #draws a black rectangle over the area of all the time mode buttons which gets rid of the red rectangle that surround the buttons
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//2-3,screenWidth,screenHeight//10+6))
          #draws red reactangle around the button to show it has been selected
          pygame.draw.rect(menuScreen, (255,0,0), (((screenWidth-screenWidth//14)//2 - screenWidth//7)-3,screenHeight//2-3,screenWidth//7+6,screenHeight//10+6))
        if event.ui_element == timeButton:
          timeRemaining = 18000
          #draws a black rectangle over the area of all the time mode buttons which gets rid of the red rectangle that surround the buttons
          pygame.draw.rect(menuScreen, (0,0,0), (0,screenHeight//2-3,screenWidth,screenHeight//10+6))
          #draws red reactangle around the button to show it has been selected
          pygame.draw.rect(menuScreen, (255,0,0), (((screenWidth+screenWidth//14)//2)-3,screenHeight//2-3,screenWidth//7+6,screenHeight//10+6))
        #running the aim trainer function if they click the run game button
        if event.ui_element == runButton:
          aimTrainer(radius,timeRemaining,scoreMultiplier)
        #closing the program if the quit button is clicked
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        #opening the main menu if the menu button is clicked
        if event.ui_element == menuButton:
          mainMenu()
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(menuScreen)
    pygame.display.update()


#getting the dimensions of the users display
screenWidth, screenHeight = pyautogui.size()
#initialising loggedIn as false as the user hasn't logged in yet
loggedIn = False
#initialising accountName
accountName = ''


def reactionMenu():
  #creating the quit, menu and run game buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  runButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='run game',manager = manager)
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)  
  menuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10), (100, 25)),text='menu',manager = manager)

  #creates a display with the dimensions of the users screen
  menuScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)

  while True:
    for event in pygame.event.get():
      #if the users clicks the x button, it closes the entire program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #running the reaction speed tester if the button is clicked
        if event.ui_element == runButton:
          rTester()
        #closing the program if the quit button is clicked
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        #opening the main menu if the menu button is clicked
        if event.ui_element == menuButton:
          mainMenu()
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(menuScreen)
    pygame.display.update()

def rTester():
  pygame.display.update()
  #creates a display with the dimensions of the users screen
  reactScreen = pygame.display.set_mode((screenWidth,screenHeight),pygame.SCALED)
  #creating a font object for the reaction speed tester
  reactionFont = pygame.font.SysFont('tahoma',36)

  #creating the quit button
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  #initialising the variable reactionState
  reactionState = "start"
  #generates a random delay fro when the screen changes colour
  randTime = random.randint(2000,10000)
  #gets the starting time for when the user runs the reaction tester
  startTime = pygame.time.get_ticks()
  #gets the time that the background changes colour
  changeTime = startTime + randTime

  #getting the global values for loggedIn and accountName
  global loggedIn
  global accountName


  running = True
  while  running:
    #gets the current amount of ticks
    currentTime = pygame.time.get_ticks()
    #changing the reaction state to "wait" as this is when the user waits for the screen to change colour
    if reactionState == "start":
      reactionState = "wait"
      reactScreen.fill((0,0,0))
    #changing the reaction state to be react when delay has finished
    if currentTime >= changeTime:
      reactionState = "react"
      reactScreen.fill((255,0,0))

    for event in pygame.event.get():
      #displays the quit button
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #closing the program if the quit button is clicked
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        #detects if the user clicks before the screen changes colour and if they do, it resets the reaction speed tester
        if reactionState == "wait":
          scoreText = reactionFont.render(f"You clicked too early, try again", 1, (0,255,0))
          reactScreen.blit(scoreText,(((screenWidth - scoreText.get_width())//2),((screenHeight - scoreText.get_height())//2)))
          pygame.display.update()
          time.sleep(5)
          reactionMenu()
        #detects when the user clicks after the screen has changed colour
        if reactionState == "react":
          clickTime = pygame.time.get_ticks()
          running = False
          finished = True
          reactScreen.fill((0,0,0))
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(reactScreen)
    pygame.display.update()

  while finished:
    #calculating the time it took for the user to react and displaying it on screen
    scoreTime = (clickTime - changeTime)
    scoreText = reactionFont.render(f"you took {scoreTime}ms", 1, (0,255,0))
    reactScreen.blit(scoreText,(((screenWidth - scoreText.get_width())//2),((screenHeight - scoreText.get_height())//2)))
    #checking if the user is logged in
    if loggedIn == True:
      #creating the file to save the users scores if it doesnt exist
      if not os.path.exists(accountName+'ReactScores.txt'):
        open(accountName+'ReactScores.txt', 'w').close()
      #create the code to write the thingy on new line :(
      scoreFile = accountName + 'ReactScores.txt'
      with open(scoreFile, 'a') as file:
        file.write(str(scoreTime) + "\n")
    #updating the display to show the score and waiting 5 seconds
    pygame.display.update()
    time.sleep(5)
    #making the entire scren black to reset it and then terminating the function
    reactScreen.fill((0,0,0))
    pygame.display.update()
    finished = False



def mainMenu():
  #creates a display with the dimensions of the users screen
  menuScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  #creating all the buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  accountButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//5), (screenWidth//7, screenHeight//10)),text='Account details',manager = manager)
  aimTrainerButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='Aim Trainer',manager = manager)
  reactionTestButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight-(screenHeight//5)), (screenWidth//7, screenHeight//10)),text='Reaction test',manager = manager)
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)


  while True:
    for event in pygame.event.get():
      #if the users clicks the x button, it closes the entire program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #opening the account system if the button is pressed
        if event.ui_element == accountButton:
          account()
        #opening the aim trainer menu if the button is pressed
        if event.ui_element == aimTrainerButton:
          aimTrainMenu()
        #opening the reaction speed tester if the button is pressed
        if event.ui_element == reactionTestButton:
          reactionMenu()
        #closing the program if the quit button is clicked
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(menuScreen)
    pygame.display.update()


def account():
  #getting the global value for loggedIn
  global loggedIn
  #checking to see if the user profile file already exists and creating it if it doesnt
  if not os.path.exists('userProfiles.txt'):
    open('userProfiles.txt', 'w').close()

  #creates a display with the dimensions of the users screen
  accountScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  #creating the quit and menu buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  menuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10), (100, 25)),text='menu',manager = manager)

  #checking if the user is logged in and if they are, creating a button for the user to view their high scores
  if loggedIn == True:
    highScoreButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='High Scores',manager = manager)
  #checking if the user is logged in and if they aren't, creating login and signup buttons
  if loggedIn == False:
    logInButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//14)//2 - screenWidth//7, screenHeight//2), (screenWidth//7, screenHeight//10)),text='Log in',manager = manager)
    signUpButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth+screenWidth//14)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='Sign up',manager = manager)
  
  while True:
    for event in pygame.event.get():
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #closing the program if the quit button is clicked
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        #opening the main menu if the menu button is clicked
        if event.ui_element == menuButton:
            mainMenu()
        #checking if the user is logged in and if they aren't, running the respective functions depending on which button the user clicks
        if loggedIn == False:
          if event.ui_element == logInButton:
            logIn()
          if event.ui_element == signUpButton:
            signUp()
        #checking if the user is logged in and if they are, then it shows them their high scores
        if loggedIn == True:
          if event.ui_element == highScoreButton:
            highScore()
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(accountScreen)
    pygame.display.update()


def highScore():
  #getting the global value for accountName
  global accountName
  #creates a display with the dimensions of the users screen
  highScoreScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  #creating a font object for the high score
  highScoreFont = pygame.font.SysFont('tahoma',36)
  #creating the quit and menu buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  menuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10), (100, 25)),text='menu',manager = manager)

  #initialising the top 3 scores as -1 as that is an unattainable score
  accountMax1 = -1
  accountMax2 = -1
  accountMax3 = -1
  #initialising the lowest 3 scores as 999999 as that is an unattainable score
  reactMin1 = 999999
  reactMin2 = 999999
  reactMin3 = 999999
  #saving the user specific aim trainer score file name in aimFile
  aimFile = accountName + 'AimScores.txt'
  #reading the file and saving all the scores in scores
  with open(aimFile, 'r+') as file:
    scores = file.readlines()
    for line in scores:
      score = float(line.split("\n")[0])
      #finding the highest score
      if score > accountMax1:
        accountMax1 = score
    #finding the second highest score
    for line in scores:
      score = float(line.split("\n")[0])
      if score > accountMax2:
        if score == accountMax1:
          accountMax2 = accountMax2
        if score < accountMax1:
          accountMax2 = score
    #finding the third highest score
    for line in scores:
      score = float(line.split("\n")[0])
      if score > accountMax3:
        if score == accountMax1:
          accountMax3 = accountMax3
        if score < accountMax1:
          if score == accountMax2:
            accountMax3 = accountMax3
          if score < accountMax2:
              accountMax3 = score
    
  #if the user doesn't have 3 or more scores, the variables without a score will save the value ---
  if accountMax1 == -1:
    accountMax1 = "---"
  if accountMax2 == -1:
    accountMax2 = "---"
  if accountMax3 == -1:
    accountMax3 = "---"

  #rendering and displaying the high scores the user has gotten
  highScoreText = highScoreFont.render("Aim Trainer Scores:", 1, (0,255,0))
  highScoreScreen.blit(highScoreText,(screenWidth//6,screenHeight//10))
  accountMax1Text = highScoreFont.render(f"1.  {accountMax1}", 1, (0,255,0))
  highScoreScreen.blit(accountMax1Text,(screenWidth//4,screenHeight//5))
  accountMax2Text = highScoreFont.render(f"2.  {accountMax2}", 1, (0,255,0))
  highScoreScreen.blit(accountMax2Text,(screenWidth//4,screenHeight//2))
  accountMax3Text = highScoreFont.render(f"3.  {accountMax3}", 1, (0,255,0))
  highScoreScreen.blit(accountMax3Text,(screenWidth//4,screenHeight - (screenHeight//5)))




  #saviing the user specific reaction speed score file name in reactFile
  reactFile = accountName + 'ReactScores.txt'
  #reading the file and saving all the scores in scores
  with open(reactFile, 'r+') as file:
    scores = file.readlines()
    for line in scores:
      score = float(line.split("\n")[0])
      #finding the lowest score
      if score < reactMin1:
        reactMin1 = score
    #finding the second lowest score
    for line in scores:
      score = float(line.split("\n")[0])
      if score < reactMin2:
        if score == reactMin1:
          reactMin2 = reactMin2
        if score > reactMin1:
          reactMin2 = score
    #finding the third lowest score
    for line in scores:
      score = float(line.split("\n")[0])
      if score < reactMin3:
        if score == reactMin1:
          reactMin3 = reactMin3
        if score > reactMin1:
          if score == reactMin2:
            reactMin3 = reactMin3
          if score > reactMin2:
            reactMin3 = score

  #if the user doesn't have 3 or more scores, the variables without a score will save the value ---
  if reactMin1 == 999999:
    reactMin1 = "---"
  if reactMin2 == 999999:
    reactMin2 = "---"
  if reactMin3 == 999999:
    reactMin3 = "---"

  #rendering and displaying the high scores the user has gotten
  highScoreText = highScoreFont.render("Reaction Speed Scores:", 1, (0,255,0))
  highScoreScreen.blit(highScoreText,(screenWidth//6 + screenWidth//2,screenHeight//10))
  reactMin1Text = highScoreFont.render(f"1.  {reactMin1}ms", 1, (0,255,0))
  highScoreScreen.blit(reactMin1Text,(screenWidth//4 + screenWidth//2,screenHeight//5))
  reactMin2Text = highScoreFont.render(f"2.  {reactMin2}ms", 1, (0,255,0))
  highScoreScreen.blit(reactMin2Text,(screenWidth//4 + screenWidth//2,screenHeight//2))
  reactMin3Text = highScoreFont.render(f"3.  {reactMin3}ms", 1, (0,255,0))
  highScoreScreen.blit(reactMin3Text,(screenWidth//4 + screenWidth//2,screenHeight - (screenHeight//5)))


  while True:
    for event in pygame.event.get():
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #closing the program if the quit button is clicked
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        #opening the main menu if the menu button is clicked
        if event.ui_element == menuButton:
            mainMenu()
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(highScoreScreen)
    pygame.display.update()



def logIn():
  #getting the values for loggedIn and accountName
  global loggedIn
  global accountName
  #creates a display with the dimensions of the users screen
  logInScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  #creating the buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  logInButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='Log in',manager = manager)
  menuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10), (100, 25)),text='menu',manager = manager)
  #creating the input boxes for the username and the password
  usernameInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight//5, screenWidth//7, screenHeight//10)
  passwordInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight//2, screenWidth//7, screenHeight//10)
  #creating the colours to tell the user whether they have selected the textbox or not
  activeColour = (141,182,205)
  inactiveColour = (255,255,255)
  #initialising colour as inactiveColour
  colour = inactiveColour
  #creating a font object for the account system
  logInFont = pygame.font.SysFont('tahoma',36)
  #rendering the phrase "Log in:" to the left of the input boxes
  logInText = logInFont.render("Log in:", 1, (0,255,0))
  logInScreen.blit(logInText, (((screenWidth-screenWidth//7)//2)-screenWidth//14-screenWidth//7, screenHeight//5))

  #rendering the word "Username:" just above the username text box
  usernameText = logInFont.render("Username:", 1, (0,255,0))
  logInScreen.blit(usernameText,((screenWidth - usernameText.get_width())//2,screenHeight//10))
  #drawing the username text box onto the screen
  pygame.draw.rect(logInScreen, colour, usernameInputBox)

  #rendering the word "Password:" jus above the password text box
  passwordText = logInFont.render("Password:", 1, (0,255,0))
  logInScreen.blit(passwordText,((screenWidth - passwordText.get_width())//2,((screenHeight//2)-screenHeight//10)))
  #drawing the password text box onto the screen
  pygame.draw.rect(logInScreen, colour, passwordInputBox)

  #initialising variables
  usernameActive = False
  passwordActive = False
  username = ''
  usernameInputText = logInFont.render(username, 1, (255,0,0))
  password = ''
  passwordInputText = logInFont.render(password, 1, (255,0,0))
  hiddenPassword = ''

  pygame.display.update()
  while True:
    for event in pygame.event.get():
      #if the users clicks the x button, it closes the entire program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        #if the user clicks onto the username text box, it becomes active
        if usernameInputBox.collidepoint(event.pos):
          usernameActive = True
          #changes the colour of the text box to light blue to indicate ot the user that they have selected it
          pygame.draw.rect(logInScreen, activeColour, usernameInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
        else:
          usernameActive = False
          #changes the colour of the text box to white to indicate to the user that they are no longer selecting it
          pygame.draw.rect(logInScreen, inactiveColour, usernameInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
        if passwordInputBox.collidepoint(event.pos):
          passwordActive = True
          #changes the colour of the text box to light blue to indicate ot the user that they have selected it
          pygame.draw.rect(logInScreen, activeColour, passwordInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
        else:
          passwordActive = False
          #changes the colour of the text box to white to indicate to the user that they are no longer selecting it
          pygame.draw.rect(logInScreen, inactiveColour, passwordInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))

      #if the user has clicked on the username text box
      if usernameActive == True:
        if event.type == pygame.KEYDOWN:
          #if the user presses the enter button, it changes the colour of the text box to the inactive colour and makes it so that anything else typed isnt saved
          if event.key == pygame.K_RETURN:
            usernameActive = False
            pygame.draw.rect(logInScreen, inactiveColour, usernameInputBox)
            #rendering and displaying the username on screen
            logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
          #if the user presses the backspace button, it removes the last character that was inputted
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(logInScreen, activeColour, usernameInputBox)
            username = username [:-1]
            #rendering and displaying the username on screen
            usernameInputText = logInFont.render(username, 1, (255,0,0))
            logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
          #if any other key is pressed, it saves the inputs in username
          else:
            username += event.unicode
            usernameInputText = logInFont.render(username, 1, (255,0,0))
            #dynamically changing the size of the text box if the users input is longer than the text box
            usernameInputBox.w = max(screenWidth//7, usernameInputText.get_width()+10)
            pygame.draw.rect(logInScreen, activeColour, usernameInputBox)
            #rendering and displaying the username on screen
            logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))

      if passwordActive == True:
        if event.type == pygame.KEYDOWN:
          #if the user presses the enter button, it changes the colour of the text box to the inactive colour and makes it so that anything else typed isnt saved
          if event.key == pygame.K_RETURN:
            passwordActive = False
            pygame.draw.rect(logInScreen, inactiveColour, passwordInputBox)
            #dynamically changing the size of the text box if the users input is longer than the text box
            logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
          #if the user presses the backspace button, it removes the last character that was inputted
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(logInScreen, activeColour, passwordInputBox)
            password = password [:-1]
            #removes an asterisk so the user knows that the backspace has removed the last character
            hiddenPassword = hiddenPassword [:-1]
            #rendering and printing the asterisks onto the screen
            passwordInputText = logInFont.render(hiddenPassword, 1, (255,0,0))
            #dynamically changing the size of the text box if the users input is longer than the text box
            logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
          #if any other key is pressed, it saves the inputs in password
          else:
            password += event.unicode
            #adds an asterisk to the string
            hiddenPassword = hiddenPassword + '*'
            #rendering and printing the asterisks onto the screen
            passwordInputText = logInFont.render(hiddenPassword, 1, (255,0,0))
            #dynamically changing the size of the text box if the users input is longer than the text box
            passwordInputBox.w = max(screenWidth//7, passwordInputText.get_width()+10)
            pygame.draw.rect(logInScreen, activeColour, passwordInputBox)
            logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))

      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #closing the program if the quit button is clicked
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        #opening the main menu if the menu button is clicked
        if event.ui_element == menuButton:
          mainMenu()
        if event.ui_element == logInButton:
          #checking if the username or password fields were left empty. If they were, an error message is displayed
          if username == '' or password == '':
            emptyFieldsError1 = logInFont.render("ERROR: Please fill", 1, (255,0,0))
            emptyFieldsError2 = logInFont.render("in all the fields", 1, (255,0,0))
            logInScreen.blit(emptyFieldsError1,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2))
            logInScreen.blit(emptyFieldsError2,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + 40))
          #checking if the username or password fields were not left empty
          if username != '' and password != '':
            #checking to see if an account with the same username is in the database. If it isn't, an error message is displayed
            with open('userProfiles.txt', 'r') as file:
              fileContents = file.read()
              if username not in fileContents:
                usernameNotFound = logInFont.render("Account not found", 1, (255,0,0))
                #creates a black rectangle that covers the message area so that the messages dont overlap
                pygame.draw.rect(logInScreen,(0,0,0),(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//2, screenWidth - (((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7), screenHeight//2))
                #draws the error message onto the screen
                logInScreen.blit(usernameNotFound,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
              #checking if the username is in the database
              if username in fileContents:
                #checking if the password also matches
                if password in fileContents:
                  #changing loggedIn to true so that all the other functions now know that the user has logged in
                  loggedIn = True
                  usernameSuccess = logInFont.render("Successfully logged in", 1, (255,0,0))
                  #creates a black rectangle that covers the message area so that the messages dont overlap
                  pygame.draw.rect(logInScreen,(0,0,0),(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//2, screenWidth - (((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7), screenHeight//2))
                  #draws the success message onto the screen
                  logInScreen.blit(usernameSuccess,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
                  accountName = username
                  #checking to see if the user profile file already exists
                  if not os.path.exists(accountName+'AimScores.txt'):
                    #creating it if it doesnt exist
                    open(accountName+'AimScores.txt', 'w').close()
                  #checking to see if the user profile file already exists
                  if not os.path.exists(accountName+'ReactScores.txt'):
                    #creating it if it doesnt exist
                    open(accountName+'ReactScores.txt', 'w').close()
                  pygame.display.update()
                  time.sleep(3)
                  mainMenu()
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(logInScreen)
    pygame.display.flip()













def signUp():
  #creates a display with the dimensions of the users screen
  signUpScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  #creating the buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  signUpButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='Sign up',manager = manager)
  menuButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,10), (100, 25)),text='menu',manager = manager)
  #creating the input boxes for the username, password and the confirm password
  usernameInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight//5, screenWidth//7, screenHeight//10)
  passwordInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight//2, screenWidth//7, screenHeight//10)
  confirmPasswordInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight-(screenHeight//5), screenWidth//7, screenHeight//10)
  #creating the colours to tell the user whether they have selected the textbox or not
  activeColour = (141,182,205)
  inactiveColour = (255,255,255)
  #initialising colour as inactiveColour
  colour = inactiveColour
  #creating a font object for the sign up system
  signUpFont = pygame.font.SysFont('tahoma',36)
  #rendering the phrase "Sign up:" to the left of the input boxes
  signUpText = signUpFont.render("Sign up:", 1, (0,255,0))
  signUpScreen.blit(signUpText, (((screenWidth-screenWidth//7)//2)-screenWidth//14-screenWidth//7, screenHeight//5))


  #rendering the word "Username:" just above the username text box
  usernameText = signUpFont.render("Username:", 1, (0,255,0))
  signUpScreen.blit(usernameText,((screenWidth - usernameText.get_width())//2,screenHeight//10))
  #drawing the username text box onto the screen
  pygame.draw.rect(signUpScreen, colour, usernameInputBox)

  #rendering the word "Password:" jus above the password text box
  passwordText = signUpFont.render("Password:", 1, (0,255,0))
  signUpScreen.blit(passwordText,((screenWidth - passwordText.get_width())//2,((screenHeight//2)-screenHeight//10)))
  #drawing the password text box onto the screen
  pygame.draw.rect(signUpScreen, colour, passwordInputBox)

  #rendering the word "Confirm Password:" jus above the password text box
  confirmPasswordText = signUpFont.render("Confirm password:", 1, (0,255,0))
  signUpScreen.blit(confirmPasswordText,((screenWidth - confirmPasswordText.get_width())//2,((screenHeight-screenHeight//10)-screenHeight//5)))
  #drawing the confirm password text box onto the screen
  pygame.draw.rect(signUpScreen, colour, confirmPasswordInputBox)

  #initialising variables
  usernameActive = False
  passwordActive = False
  confirmPasswordActive = False
  username = ''
  usernameInputText = signUpFont.render(username, 1, (255,0,0))
  password = ''
  passwordInputText = signUpFont.render(password, 1, (255,0,0))
  hiddenPassword = ''
  confirmPassword = ''
  confirmPasswordInputText = signUpFont.render(password, 1, (255,0,0))
  confirmHiddenPassword = ''


  pygame.display.update()
  while True:
    for event in pygame.event.get():
      #if the users clicks the x button, it closes the entire program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        #if the user clicks onto the username text box, it becomes active
        if usernameInputBox.collidepoint(event.pos):
          usernameActive = True
          #changes the colour of the text box to light blue to indicate ot the user that they have selected it
          pygame.draw.rect(signUpScreen, activeColour, usernameInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
        else:
          usernameActive = False
          #changes the colour of the text box to white to indicate to the user that they are no longer selecting it
          pygame.draw.rect(signUpScreen, inactiveColour, usernameInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
        if passwordInputBox.collidepoint(event.pos):
          passwordActive = True
          #changes the colour of the text box to light blue to indicate ot the user that they have selected it
          pygame.draw.rect(signUpScreen, activeColour, passwordInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
        else:
          passwordActive = False
          #changes the colour of the text box to white to indicate to the user that they are no longer selecting it
          pygame.draw.rect(signUpScreen, inactiveColour, passwordInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
        if confirmPasswordInputBox.collidepoint(event.pos):
          confirmPasswordActive = True
          #changes the colour of the text box to light blue to indicate ot the user that they have selected it
          pygame.draw.rect(signUpScreen, activeColour, confirmPasswordInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))
        else:
          confirmPasswordActive = False
          #changes the colour of the text box to white to indicate to the user that they are no longer selecting it
          pygame.draw.rect(signUpScreen, inactiveColour, confirmPasswordInputBox)
          #dynamically changing the size of the text box if the users input is longer than the text box
          signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))

      if usernameActive == True:
        #username stuff
        if event.type == pygame.KEYDOWN:
          #if the user presses the enter button, it changes the colour of the box to the inactive colour and makes it so that anything else typed isnt saved
          if event.key == pygame.K_RETURN:
            usernameActive = False
            pygame.draw.rect(signUpScreen, inactiveColour, usernameInputBox)
            #rendering and displaying the username on screen
            signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
          #if the user presses the backspace button, it removes the last character that was inputted
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(signUpScreen, activeColour, usernameInputBox)
            username = username [:-1]
            #rendering and displaying the username on screen
            usernameInputText = signUpFont.render(username, 1, (255,0,0))
            signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
          #if any other key is pressed, it saves the inputs in username
          else:
            username += event.unicode
            usernameInputText = signUpFont.render(username, 1, (255,0,0))
            #dynamically changing the size of the text box if the users input is longer than the text box
            usernameInputBox.w = max(screenWidth//7, usernameInputText.get_width()+10)
            pygame.draw.rect(signUpScreen, activeColour, usernameInputBox)
            #rendering and displaying the username on screen
            signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))

      if passwordActive == True:
        if event.type == pygame.KEYDOWN:
          #if the user presses the enter button, it changes the colour of the text box to the inactive colour and makes it so that anything else typed isnt saved
          if event.key == pygame.K_RETURN:
            passwordActive = False
            pygame.draw.rect(signUpScreen, inactiveColour, passwordInputBox)
            #dynamically changing the size of the text box if the users input is longer than the text box
            signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
          #if the user presses the backspace button, it removes the last character that was inputted
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(signUpScreen, activeColour, passwordInputBox)
            #removes the last character in the password string
            password = password [:-1]
            #removes an asterisk so the user knows that the backspace has removed the last character
            hiddenPassword = hiddenPassword [:-1]
            #rendering and printing the asterisks onto the screen
            passwordInputText = signUpFont.render(hiddenPassword, 1, (255,0,0))
            #dynamically changing the size of the text box if the users input is longer than the text box
            signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
          #if any other key is pressed, it saves the inputs in password
          else:
            password += event.unicode
            #adds an asterisk to the string
            hiddenPassword = hiddenPassword + '*'
            #rendering and printing the asterisks onto the screen
            passwordInputText = signUpFont.render(hiddenPassword, 1, (255,0,0))
            #dynamically changing the size of the text box if the users input is longer than the text box
            passwordInputBox.w = max(screenWidth//7, passwordInputText.get_width()+10)
            pygame.draw.rect(signUpScreen, activeColour, passwordInputBox)
            signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))

      if confirmPasswordActive == True:
        if event.type == pygame.KEYDOWN:
          #if the user presses the enter button, it changes the colour of the text box to the inactive colour and makes it so that anything else typed isnt saved
          if event.key == pygame.K_RETURN:
            confirmPasswordActive = False
            pygame.draw.rect(signUpScreen, inactiveColour, confirmPasswordInputBox)
            #dynamically changing the size of the text box if the users input is longer than the text box
            signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))
          #if the user presses the backspace button, it removes the last character that was inputted
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(signUpScreen, activeColour, confirmPasswordInputBox)
            #removes the last character in the confirmPassword string
            confirmPassword = confirmPassword [:-1]
            #removes an asterisk so the user knows that the backspace has removed the last character
            confirmHiddenPassword = confirmHiddenPassword [:-1]
            #rendering and printing the asterisks onto the screen
            confirmPasswordInputText = signUpFont.render(confirmHiddenPassword, 1, (255,0,0))
            #dynamically changing the size of the text box if the users input is longer than the text box
            signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))
          #if any other key is pressed, it saves the inputs in confirmPassword
          else:
            confirmPassword += event.unicode
            #adds an asterisk to the string
            confirmHiddenPassword = confirmHiddenPassword + '*'
            #rendering and printing the asterisks onto the screen
            confirmPasswordInputText = signUpFont.render(confirmHiddenPassword, 1, (255,0,0))
            #dynamically changing the size of the text box if the users input is longer than the text box
            confirmPasswordInputBox.w = max(screenWidth//7, confirmPasswordInputText.get_width()+10)
            pygame.draw.rect(signUpScreen, activeColour, confirmPasswordInputBox)
            signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))

      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #closing the program if the quit button is clicked
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        #opening the main menu if the menu button is clicked
        if event.ui_element == menuButton:
          mainMenu()
        if event.ui_element == signUpButton:
          #checking if the username, password or confirmPassword fields were left empty. If they were, an error message is displayed
          if username == '' or password == '' or confirmPassword == '':
            emptyFieldsError1 = signUpFont.render("ERROR: Please fill", 1, (255,0,0))
            emptyFieldsError2 = signUpFont.render("in all the fields", 1, (255,0,0))
            signUpScreen.blit(emptyFieldsError1,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2))
            signUpScreen.blit(emptyFieldsError2,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + 40))
          #checking if the passowrd matches the confirmation pasword. If they don't, an error message is displayed
          if password != confirmPassword:
            passwordError1 = signUpFont.render("ERROR: Your passwords", 1, (255,0,0))
            passwordError2 = signUpFont.render("don't match", 1, (255,0,0))
            signUpScreen.blit(passwordError1,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
            signUpScreen.blit(passwordError2,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10 + 40))
          #checking if the username field was not left empty and if the password matches the confirmation password
          if username != '' and password == confirmPassword:
            #checking to see if an account with the same username is in the database. If it isn't, the username and password are saved to the database
            with open('userProfiles.txt', 'r') as file:
              fileContents = file.read()
              if username not in fileContents:
                with open('userProfiles.txt', 'a') as file:
                  file.write(username + ',' + password + "\n")
                  #creates a black rectangle that covers the message area so that the messages dont overlap
                  pygame.draw.rect(signUpScreen,(0,0,0),(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//2, screenWidth - (((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7), screenHeight//2))
                  #draws the success message onto the screen
                  usernameSuccess = signUpFont.render("Account successfully created", 1, (255,0,0))
                  signUpScreen.blit(usernameSuccess,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
                  pygame.display.update()
                  time.sleep(3)
                  mainMenu()
              #if an account with the same username already exists, an error message is displayed
              else:
                usernameError1 = signUpFont.render("ERROR: This username", 1, (255,0,0))
                usernameError2 = signUpFont.render("is already in use", 1, (255,0,0))
                #creates a black rectangle that covers the message area so that the messages dont overlap
                pygame.draw.rect(signUpScreen,(0,0,0),(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//2, screenWidth - (((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7), screenHeight//2))
                #draws the error  message onto the scren
                signUpScreen.blit(usernameError1,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
                signUpScreen.blit(usernameError2,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10 + 40))
    #prcoessing and rendering the buttons onto the screen
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(signUpScreen)
    pygame.display.flip()






#running the main menu when the user runs the program
mainMenu()