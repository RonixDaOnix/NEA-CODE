import pygame, sys, random, math, pyautogui, pygame_gui, time, csv, os
from pygame.locals import QUIT
pygame.font.init()
pygame.freetype.init()
pygame.init()

#!aim trainer function
def aimTrainer(radius,timeRemaining,scoreMultiplier):

  #!variables:
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  #creates an object called clock which tracks time
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


  #creates a display with the dimensions of the users screen
  aimScreen = pygame.display.set_mode((screenWidth,screenHeight),pygame.SCALED)
  pygame.display.set_caption('Reflex tester program')



  #changes the mouse icon to a crosshair
  pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

  #!initialising all the variable for timer()
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
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)



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
  easyButton = pygame_gui.elements.UIButton(relative_rect =pygame.Rect((((screenWidth-screenWidth//7)//2)-screenWidth//14-screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='easy',manager = manager)
  mediumButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//5), (screenWidth//7, screenHeight//10)),text='medium',manager = manager)
  hardButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='hard',manager = manager)
  unlimitedButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//14)//2 - screenWidth//7, screenHeight//2), (screenWidth//7, screenHeight//10)),text='unlimited time',manager = manager)
  timeButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth+screenWidth//14)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='timed',manager = manager)
  runButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight-(screenHeight//5)), (screenWidth//7, screenHeight//10)),text='run game',manager = manager)
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)


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
loggedIn = False
accountName = ''


def reactionMenu():
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  runButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='run game',manager = manager)
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)  

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

  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
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


#!Iteration 3 - making accounts and the menu
# okay so we are gonna have 4 buttons displayed, account, aim trainer, react tester, quit. basically once user logs in, they just click on account buon ad then they can sign out and then walah.
#ACCOUNT SYSTEM - when login in it checks to see if a score file exists.
#  If not, it will make an aim traim score file and an react test score file. 
#  Then when user plays, their score just gets saved as an array or sumn with the settings they also chose
#  Also when the user clicks account, their wil be  view previous scores button for aim and react testers



def mainMenu():
  menuScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  #creating all the buttons
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  accountButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//5), (screenWidth//7, screenHeight//10)),text='Account details',manager = manager)
  aimTrainerButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='Aim Trainer',manager = manager)
  reactionTestButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight-(screenHeight//5)), (screenWidth//7, screenHeight//10)),text='Reaction test',manager = manager)
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)


  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == accountButton:
          account()
        if event.ui_element == aimTrainerButton:
          aimTrainMenu()
        if event.ui_element == reactionTestButton:
          reactionMenu()
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(menuScreen)
    pygame.display.update()


def account():
  #checking to see if the user profile file already exists
  if not os.path.exists('userProfiles.txt'):
    #creating it if it doesnt
    open('userProfiles.txt', 'w').close()
  accountScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  accountFont = pygame.font.SysFont('tahoma',36)
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  if loggedIn == True:
    highScoreButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//7)//2, screenHeight-(screenHeight//5)), (screenWidth//7, screenHeight//10)),text='High Scores',manager = manager)
  if loggedIn == False:
    logInButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth-screenWidth//14)//2 - screenWidth//7, screenHeight//2), (screenWidth//7, screenHeight//10)),text='Log in',manager = manager)
    signUpButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screenWidth+screenWidth//14)//2, screenHeight//2), (screenWidth//7, screenHeight//10)),text='Sign up',manager = manager)
  
  while True:
    for event in pygame.event.get():
      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        if event.ui_element == logInButton:
          logIn()
        if event.ui_element == signUpButton:
          signUp()
        if event.ui_element == highScoreButton:
          highScore()
      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(accountScreen)
    pygame.display.update()

def highScore():
  print("get a score first B)")

def logIn():
  #creating the window
  logInScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  #creating the quit button
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  logInButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='Sign up',manager = manager)
  #creating the input boxes for the username and the password
  usernameInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight//5, screenWidth//7, screenHeight//10)
  passwordInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight//2, screenWidth//7, screenHeight//10)
  #creating the colours to tell the user whether they have selected the textbox or not
  activeColour = (141,182,205)
  inactiveColour = (255,255,255)
  colour = inactiveColour
  #selecting which font this function will use
  accountFont = pygame.font.SysFont('tahoma',36)

  #rendering the word "Username:" just above the username text box so the user knows what the text box is for
  usernameText = accountFont.render("Username:", 1, (0,255,0))
  logInScreen.blit(usernameText,((screenWidth - usernameText.get_width())//2,screenHeight//10))
  #drawing the username text box onto the screen
  pygame.draw.rect(logInScreen, colour, usernameInputBox)

  #rendering the word "Password:" jus above the password text box so the user knows what the text box is for
  passwordText = accountFont.render("Password:", 1, (0,255,0))
  logInScreen.blit(passwordText,((screenWidth - passwordText.get_width())//2,((screenHeight//2)-screenHeight//10)))
  #drawing the password text box onto the screen
  pygame.draw.rect(logInScreen, colour, passwordInputBox)

  usernameActive = False
  passwordActive = False
  username = ''
  usernameInputText = accountFont.render(username, 1, (255,0,0))
  password = ''
  passwordInputText = accountFont.render(password, 1, (255,0,0))
  hiddenPassword = ''

  pygame.display.update()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        #if the user clicks onto the username text box, it becomes active
        if usernameInputBox.collidepoint(event.pos):
          usernameActive = True
          #changes the colour of the text box to light blue to indicate ot the user that they have selected it
          pygame.draw.rect(logInScreen, activeColour, usernameInputBox)
          logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
        else:
          usernameActive = False
          #changes the colour of the text box to white to indicate to the user that they are no longer selecting it
          pygame.draw.rect(logInScreen, inactiveColour, usernameInputBox)
          logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
        if passwordInputBox.collidepoint(event.pos):
          passwordActive = True
          pygame.draw.rect(logInScreen, activeColour, passwordInputBox)
          logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
        else:
          passwordActive = False
          pygame.draw.rect(logInScreen, inactiveColour, passwordInputBox)
          logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))

      #username stuff
      if usernameActive == True:
        #username stuff
        if event.type == pygame.KEYDOWN:
          #if the user presses the enter button, it changes the colour of the box to the inactive colour and makes it so that anything else typed isnt saved
          if event.key == pygame.K_RETURN:
            usernameActive = False
            pygame.draw.rect(logInScreen, inactiveColour, usernameInputBox)
            logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(logInScreen, activeColour, usernameInputBox)
            username = username [:-1]
            usernameInputText = accountFont.render(username, 1, (255,0,0))
            logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
          else:
            username += event.unicode
            usernameInputText = accountFont.render(username, 1, (255,0,0))
            usernameInputBox.w = max(screenWidth//7, usernameInputText.get_width()+10)
            pygame.draw.rect(logInScreen, activeColour, usernameInputBox)
            logInScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))

      #password stuff
      if passwordActive == True:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            passwordActive = False
            pygame.draw.rect(logInScreen, inactiveColour, passwordInputBox)
            logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(logInScreen, activeColour, passwordInputBox)
            #removes the last character in the password string
            password = password [:-1]
            #removes an asterisk so the user knows that the backspace has removed the last character
            hiddenPassword = hiddenPassword [:-1]
            #rendering and printing the asterisks onto the screen
            passwordInputText = accountFont.render(hiddenPassword, 1, (255,0,0))
            logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
          else:
            hiddenPassword = hiddenPassword + '*'
            password += event.unicode
            passwordInputText = accountFont.render(hiddenPassword, 1, (255,0,0))
            passwordInputBox.w = max(screenWidth//7, passwordInputText.get_width()+10)
            pygame.draw.rect(logInScreen, activeColour, passwordInputBox)
            logInScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))

      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        if event.ui_element == logInButton:
          if username == '' or password == '':
            emptyFieldsError1 = accountFont.render("ERROR: Please fill", 1, (255,0,0))
            emptyFieldsError2 = accountFont.render("in all the fields", 1, (255,0,0))
            logInScreen.blit(emptyFieldsError1,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2))
            logInScreen.blit(emptyFieldsError2,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + 40))
          if username != '' and password != '':
            with open('userProfiles.txt', 'r') as file:
              fileContents = file.read()
              if username not in fileContents:
                with open('userProfiles.txt', 'a') as file:
                  usernameNotFound = accountFont.render("Account not found", 1, (255,0,0))
                  #creates a black rectangle that covers the message area so that the messages dont overlap
                  pygame.draw.rect(logInScreen,(0,0,0),(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//2, screenWidth - (((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7), screenHeight//2))
                  #draws the success message onto the screen
                  logInScreen.blit(usernameNotFound,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
              if username in fileContents:
                if password in fileContents:
                  loggedIn = True
                  usernameSuccess = accountFont.render("Successfulyy logged in", 1, (255,0,0))
                  #creates a black rectangle that covers the message area so that the messages dont overlap
                  pygame.draw.rect(logInScreen,(0,0,0),(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//2, screenWidth - (((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7), screenHeight//2))
                  #draws the success message onto the screen
                  logInScreen.blit(usernameSuccess,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
                  accountName = username
                  pygame.display.update()
                  time.sleep(3)
                  mainMenu()
                  




            

      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(logInScreen)
    pygame.display.flip()













def signUp():
  #creating the window
  signUpScreen = pygame.display.set_mode((screenWidth, screenHeight),pygame.SCALED)
  #creating the quit button
  manager = pygame_gui.UIManager((screenWidth, screenHeight),'theme.json')
  quitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenWidth-110,10), (100, 25)),text='quit',manager = manager)
  signUpButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//5), (screenWidth//7, screenHeight//10)),text='Sign up',manager = manager)
  #creating the input boxes for the username and the password
  usernameInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight//5, screenWidth//7, screenHeight//10)
  passwordInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight//2, screenWidth//7, screenHeight//10)
  confirmPasswordInputBox = pygame.Rect((screenWidth-screenWidth//7)//2, screenHeight-(screenHeight//5), screenWidth//7, screenHeight//10)
  #creating the colours to tell the user whether they have selected the textbox or not
  activeColour = (141,182,205)
  inactiveColour = (255,255,255)
  colour = inactiveColour
  #selecting which font this function will use
  accountFont = pygame.font.SysFont('tahoma',36)

  signUpText = accountFont.render("Sign up:", 1, (0,255,0))
  signUpScreen.blit(signUpText, (((screenWidth-screenWidth//7)//2)-screenWidth//14-screenWidth//7, screenHeight//5))


  #rendering the word "Username:" just above the username text box so the user knows what the text box is for
  usernameText = accountFont.render("Username:", 1, (0,255,0))
  signUpScreen.blit(usernameText,((screenWidth - usernameText.get_width())//2,screenHeight//10))
  #drawing the username text box onto the screen
  pygame.draw.rect(signUpScreen, colour, usernameInputBox)

  #rendering the word "Password:" jus above the password text box so the user knows what the text box is for
  passwordText = accountFont.render("Password:", 1, (0,255,0))
  signUpScreen.blit(passwordText,((screenWidth - passwordText.get_width())//2,((screenHeight//2)-screenHeight//10)))
  #drawing the password text box onto the screen
  pygame.draw.rect(signUpScreen, colour, passwordInputBox)

  #rendering the word "Confirm Password:" jus above the password text box so the user knows what the text box is for
  confirmPasswordText = accountFont.render("Confirm password:", 1, (0,255,0))
  signUpScreen.blit(confirmPasswordText,((screenWidth - confirmPasswordText.get_width())//2,((screenHeight-screenHeight//10)-screenHeight//5)))
  #drawing the password text box onto the screen
  pygame.draw.rect(signUpScreen, colour, confirmPasswordInputBox)

  usernameActive = False
  passwordActive = False
  confirmPasswordActive = False
  username = ''
  usernameInputText = accountFont.render(username, 1, (255,0,0))
  password = ''
  passwordInputText = accountFont.render(password, 1, (255,0,0))
  hiddenPassword = ''
  confirmPassword = ''
  confirmPasswordInputText = accountFont.render(password, 1, (255,0,0))
  confirmHiddenPassword = ''


  pygame.display.update()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        #if the user clicks onto the username text box, it becomes active
        if usernameInputBox.collidepoint(event.pos):
          usernameActive = True
          #changes the colour of the text box to light blue to indicate ot the user that they have selected it
          pygame.draw.rect(signUpScreen, activeColour, usernameInputBox)
          signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
        else:
          usernameActive = False
          #changes the colour of the text box to white to indicate to the user that they are no longer selecting it
          pygame.draw.rect(signUpScreen, inactiveColour, usernameInputBox)
          signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
        if passwordInputBox.collidepoint(event.pos):
          passwordActive = True
          pygame.draw.rect(signUpScreen, activeColour, passwordInputBox)
          signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
        else:
          passwordActive = False
          pygame.draw.rect(signUpScreen, inactiveColour, passwordInputBox)
          signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
        if confirmPasswordInputBox.collidepoint(event.pos):
          confirmPasswordActive = True
          pygame.draw.rect(signUpScreen, activeColour, confirmPasswordInputBox)
          signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))
        else:
          confirmPasswordActive = False
          pygame.draw.rect(signUpScreen, inactiveColour, confirmPasswordInputBox)
          signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))

      if usernameActive == True:
        #username stuff
        if event.type == pygame.KEYDOWN:
          #if the user presses the enter button, it changes the colour of the box to the inactive colour and makes it so that anything else typed isnt saved
          if event.key == pygame.K_RETURN:
            usernameActive = False
            pygame.draw.rect(signUpScreen, inactiveColour, usernameInputBox)
            signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(signUpScreen, activeColour, usernameInputBox)
            username = username [:-1]
            usernameInputText = accountFont.render(username, 1, (255,0,0))
            signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))
          else:
            username += event.unicode
            usernameInputText = accountFont.render(username, 1, (255,0,0))
            usernameInputBox.w = max(screenWidth//7, usernameInputText.get_width()+10)
            pygame.draw.rect(signUpScreen, activeColour, usernameInputBox)
            signUpScreen.blit(usernameInputText,((usernameInputBox.x+5, ((screenHeight//10 - usernameInputText.get_height())//2)  + screenHeight//5)))

      #password stuff
      if passwordActive == True:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            passwordActive = False
            pygame.draw.rect(signUpScreen, inactiveColour, passwordInputBox)
            signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(signUpScreen, activeColour, passwordInputBox)
            #removes the last character in the password string
            password = password [:-1]
            #removes an asterisk so the user knows that the backspace has removed the last character
            hiddenPassword = hiddenPassword [:-1]
            #rendering and printing the asterisks onto the screen
            passwordInputText = accountFont.render(hiddenPassword, 1, (255,0,0))
            signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))
          else:
            hiddenPassword = hiddenPassword + '*'
            password += event.unicode
            passwordInputText = accountFont.render(hiddenPassword, 1, (255,0,0))
            passwordInputBox.w = max(screenWidth//7, passwordInputText.get_width()+10)
            pygame.draw.rect(signUpScreen, activeColour, passwordInputBox)
            signUpScreen.blit(passwordInputText,((passwordInputBox.x+5, ((screenHeight//10 - passwordInputText.get_height())//2)  + screenHeight//2)))

      #confirmation password stuff
      if confirmPasswordActive == True:
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
            #dont save to file this is all we had to do i think
            confirmPasswordActive = False
            pygame.draw.rect(signUpScreen, inactiveColour, confirmPasswordInputBox)
            signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))
          elif event.key == pygame.K_BACKSPACE:
            pygame.draw.rect(signUpScreen, activeColour, confirmPasswordInputBox)
            #removes the last character in the password string
            confirmPassword = confirmPassword [:-1]
            #removes an asterisk so the user knows that the backspace has removed the last character
            confirmHiddenPassword = confirmHiddenPassword [:-1]
            #rendering and printing the asterisks onto the screen
            confirmPasswordInputText = accountFont.render(confirmHiddenPassword, 1, (255,0,0))
            signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))
          else:
            confirmHiddenPassword = confirmHiddenPassword + '*'
            confirmPassword += event.unicode
            confirmPasswordInputText = accountFont.render(confirmHiddenPassword, 1, (255,0,0))
            confirmPasswordInputBox.w = max(screenWidth//7, confirmPasswordInputText.get_width()+10)
            pygame.draw.rect(signUpScreen, activeColour, confirmPasswordInputBox)
            signUpScreen.blit(confirmPasswordInputText,((confirmPasswordInputBox.x+5, ((screenHeight//10 - confirmPasswordInputText.get_height())//2)  + screenHeight - screenHeight//5)))

      if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == quitButton:
          pygame.quit()
          sys.exit()
        if event.ui_element == signUpButton:
          if username == '' or password == '' or confirmPassword == '':
            emptyFieldsError1 = accountFont.render("ERROR: Please fill", 1, (255,0,0))
            emptyFieldsError2 = accountFont.render("in all the fields", 1, (255,0,0))
            signUpScreen.blit(emptyFieldsError1,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2))
            signUpScreen.blit(emptyFieldsError2,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + 40))
          if password != confirmPassword:
            passwordError1 = accountFont.render("ERROR: Your passwords", 1, (255,0,0))
            passwordError2 = accountFont.render("don't match", 1, (255,0,0))
            signUpScreen.blit(passwordError1,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
            signUpScreen.blit(passwordError2,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10 + 40))
          if username != '' and password == confirmPassword:
            with open('userProfiles.txt', 'r') as file:
              fileContents = file.read()
              if username not in fileContents:
                with open('userProfiles.txt', 'a') as file:
                  file.write(username + ',' + password + "\n")
                  usernameSuccess = accountFont.render("Account successfully created", 1, (255,0,0))
                  #creates a black rectangle that covers the message area so that the messages dont overlap
                  pygame.draw.rect(signUpScreen,(0,0,0),(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//2, screenWidth - (((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7), screenHeight//2))
                  #draws the success message onto the screen
                  signUpScreen.blit(usernameSuccess,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
                  pygame.display.update()
                  time.sleep(3)
                  mainMenu()
              else:
                usernameError1 = accountFont.render("ERROR: This username", 1, (255,0,0))
                usernameError2 = accountFont.render("is already in use", 1, (255,0,0))
                #creates a black rectangle that covers the message area so that the messages dont overlap
                pygame.draw.rect(signUpScreen,(0,0,0),(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7, screenHeight//2, screenWidth - (((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7), screenHeight//2))
                #draws the error  message onto the scren
                signUpScreen.blit(usernameError1,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10))
                signUpScreen.blit(usernameError2,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10 + 40))
            




#            with open('userProfiles.txt', 'r') as profile:
 #             for line in profile:
  #              if username in line:
   #               print("impasta located >:)")
    #            
     #       with open('userProfiles.txt', 'w') as profile:
      #        
       #         else:
        #          profile.write(username + "," + password)
         #         successText = accountFont.render("you've been registered", 1, (255,0,0))
          #        signUpScreen.blit(successText,(((screenWidth-screenWidth//7)//2)+screenWidth//14 + screenWidth//7 , screenHeight//2 + screenHeight//10 + 100))
            #with open('profiles.txt', 'w',newline='') as profile:
            #  profile.write(username + "," + password)

      manager.process_events(event)
    manager.update(100)
    manager.draw_ui(signUpScreen)
    pygame.display.flip()





mainMenu()
