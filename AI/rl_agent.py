import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 32)
        self.fc2 = nn.Linear(32, 32)
        self.fc3 = nn.Linear(32, output_dim)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.capacity = capacity
        self.buffer = []
        self.position = 0
    
    def push(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

class DeepRLAgent:
    def __init__(self, input_dim=4, output_dim=2, lr=1e-3, gamma=0.9, epsilon=0.2):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.gamma = gamma
        self.epsilon = epsilon
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DQN(input_dim, output_dim).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.replay_buffer = ReplayBuffer(capacity=10000)
        self.batch_size = 32
    
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_dim)
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        return int(torch.argmax(q_values).item())
    
    def update(self):
        if len(self.replay_buffer) < self.batch_size:
            return
        transitions = self.replay_buffer.sample(self.batch_size)
        batch = list(zip(*transitions))
        states = torch.FloatTensor(np.array(batch[0])).to(self.device)
        actions = torch.LongTensor(batch[1]).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(batch[2]).unsqueeze(1).to(self.device)
        next_states = torch.FloatTensor(np.array(batch[3])).to(self.device)
        dones = torch.FloatTensor(batch[4]).unsqueeze(1).to(self.device)
        
        q_values = self.model(states).gather(1, actions)
        with torch.no_grad():
            next_q_values = self.model(next_states).max(1)[0].unsqueeze(1)
        target = rewards + self.gamma * next_q_values * (1 - dones)
        loss = nn.MSELoss()(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def train_agent(self, episodes=1000, steps_per_episode=10):
        for episode in range(episodes):
            state = np.array([random.randint(0,20), random.randint(0,20), random.random(), random.random()])
            for _ in range(steps_per_episode):
                action = self.choose_action(state)
                ns, ew, weather, conn = state
                reward = - (ew + weather * 2) if action == 0 else - (ns + weather * 2)
                next_state = np.array([random.randint(0,20), random.randint(0,20), random.random(), random.random()])
                done = False
                self.replay_buffer.push(state, action, reward, next_state, done)
                state = next_state
                self.update()
    
    def get_optimal_signals(self, traffic_data, config):
        rl_signals = {}
        base_duration = config.get("base_duration", 10)
        extension_factor = config.get("extension_factor", 0.5)
        max_extension = config.get("max_extension", 20)
        for inter_no, roads in traffic_data.items():
            ns = roads.get("north", {}).get("car", 0) + roads.get("south", {}).get("car", 0)
            ew = roads.get("east", {}).get("car", 0) + roads.get("west", {}).get("car", 0)
            weather = random.random()
            connected = random.random()
            state = np.array([ns, ew, weather, connected])
            action = self.choose_action(state)
            effective_count = ns if action == 1 else ew
            dynamic_duration = base_duration + min(effective_count * extension_factor, max_extension)
            rl_signals[inter_no] = {}
            for road in roads.keys():
                if (action == 0 and road in ["north", "south"]) or (action == 1 and road in ["east", "west"]):
                    signal = "GREEN"
                else:
                    signal = "RED"
                rl_signals[inter_no][road] = {
                    "signal": signal,
                    "dynamic_duration": round(dynamic_duration, 1)
                }
        return rl_signals

# For backwards compatibility.
RLAgent = DeepRLAgent
