
import MyPong 
import MyAgent
import numpy as np 
import random 
import matplotlib.pyplot as plt



ACTIONS = 3 
STATECOUNT = 5 
TOTAL_GAMETIME = 25000


def CaptureNormalisedState(PlayerYPos, BallXPos, BallYPos, BallXDirection, BallYDirection):
	gstate = np.zeros([STATECOUNT])
	gstate[0] = PlayerYPos/400.0	
	gstate[1] = BallXPos/400.0	
	gstate[2] = BallYPos/400.0	
	gstate[3] = BallXDirection/1.0	
	gstate[4] = BallYDirection/1.0	
	
	return gstate


def PlayExperiment():
	GameTime = 0
    
	GameHistory = []
	
	
	TheGame = MyPong.PongGame()
    
	TheGame.InitialDisplay()
	
	TheAgent = MyAgent.Agent(STATECOUNT, ACTIONS)
	
	
	BestAction = 0
	
	
	GameState = CaptureNormalisedState(200.0, 200.0, 200.0, 1.0, 1.0)
	
    
	for gtime in range(TOTAL_GAMETIME):    
	
		
		if GameTime % 100 == 0:
			TheGame.UpdateGameDisplay(GameTime,TheAgent.epsilon)

		
		BestAction = TheAgent.Act(GameState)
		
		
		
		
		[ReturnScore,PlayerYPos, BallXPos, BallYPos, BallXDirection, BallYDirection]= TheGame.PlayNextMove(BestAction)
		NextState = CaptureNormalisedState(PlayerYPos, BallXPos, BallYPos, BallXDirection, BallYDirection)
		
		
		TheAgent.CaptureSample((GameState,BestAction,ReturnScore,NextState))
		
		
		TheAgent.Process()
		
		
		GameState = NextState
		
		
		GameTime = GameTime+1

        
		if GameTime % 1000 == 0:
        
			donothing =0

		if GameTime % 200 == 0:
			#print("Game Time: ", GameTime,"  Game Score: ", "{0:.2f}".format(TheGame.GScore), "   EPSILON: ", "{0:.4f}".format(TheAgent.epsilon))
			print("iteration:  ",GameTime,"  Score:   ",TheGame.GScore)
			GameHistory.append((GameTime,TheGame.GScore,TheAgent.epsilon))
			
	
	x_val = [x[0] for x in GameHistory]
	y_val = [x[1] for x in GameHistory]

	plt.plot(x_val,y_val)
	plt.xlabel("Game Time")
	plt.ylabel("Score")
	plt.show()

	
	
def main():
    
	PlayExperiment()
	
	
if __name__ == "__main__":
    main()
