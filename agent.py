import torch
import numpy as np
import random
from snake import Snake
from collections import deque
from model import Linear_QNet,QTrainer
from helper import plot

MAX_Mem=100000
BATCH_SIZE=1000
LR=0.0001

class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_Mem) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    def get_state(self,game):
        head = game.snake_pos[0]
        point_l = (head[0] - 20, head[1])
        point_r = (head[0] + 20, head[1])
        point_u = (head[0], head[1] - 20)
        point_d = (head[0], head[1] + 20)
        
        dir_l = game.direction == 4
        dir_r = game.direction == 2
        dir_u = game.direction == 1
        dir_d = game.direction == 3

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food[0] < game.head[0],  # food left
            game.food[0] > game.head[0],  # food right
            game.food[1] < game.head[1],  # food up
            game.food[1] > game.head[1]  # food down
            ]

        return np.array(state, dtype=int)
    
    def remeber(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))

    def train_long_mem(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample=random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample=self.memory

        states,actions,rewards,next_states,dones=zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)    

    def train_short_mem(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)


    def get_action(self,state):
        #random moves: tradeoff exploration / exploitation
        self.epsilon=80-self.n_games
        final_move=[0,0,0]
        if random.randint(0,200)<self.epsilon:
            move=random.randint(0,2)
            final_move[move]=1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores=[]
    plot_mean_scores=[]
    total_score=0
    record=0
    agent=Agent()
    game=Snake()
    while True:
        #get old state
        state_old=agent.get_state(game)

        #get move
        final_move=agent.get_action(state_old)

        #perform move and get new state
        reward,done,score=game.play_step(final_move)
        state_new=agent.get_state(game)

        agent.train_short_mem(state_old,final_move,reward,state_new,done)

        #remeber
        agent.remeber(state_old,final_move,reward,state_new,done)

        if done:
            #train long memory experience replay
            game.reset()
            agent.n_games+=1
            agent.train_long_mem()

            if score>record:
                record=score
                #save model
                agent.model.save()
            print('Game',agent.n_games,'Score:',score,'Record:',record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__=='__main__':
    train()