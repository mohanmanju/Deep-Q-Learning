
import pygame
import random


FPS = 60	


WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400


PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

PADDLE_BUFFER = 15


BALL_WIDTH = 10
BALL_HEIGHT = 10


PADDLE_SPEED = 2
BALL_X_SPEED = 1
BALL_Y_SPEED = 1


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def drawBall(ballXPos, ballYPos, BallCol):
    #small rectangle, create it
    ball = pygame.Rect(ballXPos, ballYPos, BALL_WIDTH, BALL_HEIGHT)
    #draw it
    pygame.draw.rect(screen, BallCol, ball)


def drawPaddle1(paddle1YPos):
    #create it
    paddle1 = pygame.Rect(PADDLE_BUFFER, paddle1YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    #draw it
    pygame.draw.rect(screen, YELLOW, paddle1)


def drawPaddle2(paddle2YPos):
    #create it, opposite side
    paddle2 = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, paddle2YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    #draw it
    pygame.draw.rect(screen, WHITE, paddle2)


#update the ball, using the paddle posistions the balls positions and the balls directions
def updateBall(paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection,dft,BallColour):
	dft =7.5
	#update the x and y position
	ballXPos = ballXPos + ballXDirection * BALL_X_SPEED*dft
	ballYPos = ballYPos + ballYDirection * BALL_Y_SPEED*dft
	score = 0
	NewBallColor = BallColour;
   
	if (ballXPos <= PADDLE_BUFFER + PADDLE_WIDTH and ballYPos + BALL_HEIGHT >= paddle1YPos and ballYPos - BALL_HEIGHT <= paddle1YPos + PADDLE_HEIGHT and ballXDirection == -1):
		
		ballXDirection = 1
		
		score = 10.0
		#NewBallColor = BLUE
		NewBallColor = WHITE
	
	elif (ballXPos <= 0):
		
		ballXDirection = 1
		
		score = -10.0
		#NewBallColor = RED
		NewBallColor = WHITE
		return [score, ballXPos, ballYPos, ballXDirection, ballYDirection,NewBallColor]


	if (ballXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and ballYPos + BALL_HEIGHT >= paddle2YPos and ballYPos - BALL_HEIGHT <= paddle2YPos + PADDLE_HEIGHT):
		
		ballXDirection = -1
		NewBallColor = WHITE
	
	elif (ballXPos >= WINDOW_WIDTH - BALL_WIDTH):
	
		ballXDirection = -1
		NewBallColor = WHITE
		return [score, ballXPos, ballYPos, ballXDirection, ballYDirection,NewBallColor]

	
	if (ballYPos <= 0):
		ballYPos = 0;
		ballYDirection = 1;
	
	elif (ballYPos >= WINDOW_HEIGHT - BALL_HEIGHT):
		ballYPos = WINDOW_HEIGHT - BALL_HEIGHT
		ballYDirection = -1
	return [score, ballXPos, ballYPos, ballXDirection, ballYDirection,NewBallColor]

def updatePaddle1(action, paddle1YPos,dft):
   
	dft =7.5
	if (action == 1):
		paddle1YPos = paddle1YPos - PADDLE_SPEED*dft
	
	if (action == 2):
		paddle1YPos = paddle1YPos + PADDLE_SPEED*dft

	
	if (paddle1YPos < 0):
		paddle1YPos = 0
	if (paddle1YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
		paddle1YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
	return paddle1YPos


def updatePaddle2(paddle2YPos, ballYPos,dft):
	dft =7.5
   
	if (paddle2YPos + PADDLE_HEIGHT/2 < ballYPos + BALL_HEIGHT/2):
		paddle2YPos = paddle2YPos + PADDLE_SPEED*dft

	if (paddle2YPos + PADDLE_HEIGHT/2 > ballYPos + BALL_HEIGHT/2):
		paddle2YPos = paddle2YPos - PADDLE_SPEED*dft

	if (paddle2YPos < 0):
		paddle2YPos = 0

	if (paddle2YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
		paddle2YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
	return paddle2YPos


class PongGame:
	def __init__(self):

		
		pygame.init()
		pygame.display.set_caption('Pong')
		
		num = random.randint(0,9)

		
		self.paddle1YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
		self.paddle2YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
		
		self.ballXDirection = 1
		self.ballYDirection = 1
		
		self.ballXPos = WINDOW_WIDTH/2 - BALL_WIDTH/2

		self.clock = pygame.time.Clock()
		self.BallColor = WHITE
		self.GTimeDisplay = 0
		self.GScore = -10.0
		self.GEpsilonDisplay = 1.0

		self.font = pygame.font.SysFont("calibri",20)
		
		if(0 < num < 3):
			self.ballXDirection = 1
			self.ballYDirection = 1
		if (3 <= num < 5):
			self.ballXDirection = -1
			self.ballYDirection = 1
		if (5 <= num < 8):
			self.ballXDirection = 1
			self.ballYDirection = -1
		if (8 <= num < 10):
			self.ballXDirection = -1
			self.ballYDirection = -1
		
		num = random.randint(0,9)
		
		self.ballYPos = num*(WINDOW_HEIGHT - BALL_HEIGHT)/9


	def InitialDisplay(self):
		
		pygame.event.pump()
		
		screen.fill(BLACK)
		
		drawPaddle1(self.paddle1YPos)
		drawPaddle2(self.paddle2YPos)
		
		drawBall(self.ballXPos, self.ballYPos,WHITE)
		
		pygame.display.flip()


   
	def PlayNextMove(self, action):
		
		DeltaFrameTime = self.clock.tick(FPS)

		pygame.event.pump()
		score = 0
		screen.fill(BLACK)
		
		self.paddle1YPos = updatePaddle1(action, self.paddle1YPos,DeltaFrameTime)
		drawPaddle1(self.paddle1YPos)
		
		self.paddle2YPos = updatePaddle2(self.paddle2YPos, self.ballYPos,DeltaFrameTime)
		drawPaddle2(self.paddle2YPos)
		
		[score, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection,self.BallColor] = updateBall(self.paddle1YPos, self.paddle2YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection,DeltaFrameTime,self.BallColor)
		
		drawBall(self.ballXPos, self.ballYPos,self.BallColor)
		

		if(score >0.5 or score < -0.5):
			self.GScore = 0.05*score + self.GScore*0.95

		
		ScoreDisplay = self.font.render("Score: "+ str("{0:.2f}".format(self.GScore)), True,(255,255,255))
		screen.blit(ScoreDisplay,(50.,20.))
		TimeDisplay = self.font.render("Time: "+ str(self.GTimeDisplay), True,(255,255,255))
		screen.blit(TimeDisplay,(50.,40.))
		#EpsilonDisplay = self.font.render("Ep: "+ str("{0:.4f}".format(self.GEpsilonDisplay)), True,(255,255,255))
		#screen.blit(EpsilonDisplay,(50.,60.))

		
		pygame.display.flip()

		
		return [score,self.paddle1YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection]

	
	def ReturnCurrentState(self):
		
		score = 0
		return [self.paddle1YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection]

	def UpdateGameDisplay(self,GTime,Epsilon):
		self.GTimeDisplay = GTime
		self.GEpsilonDisplay = Epsilon
