import numpy as np

# This appears to be a message indicating a syntax error, but no code was provided to fix. Please provide the actual Python code that needs fixing.


class DataCollector:
```
    def __init__(self, max_samples=10000):
        self.max_samples = max_samples
        self.states = []
        self.actions = []

```python
def add_sample(self, state, action):
```
        if len(self.states) >= self.max_samples:
            self.states.pop(0)
            self.actions.pop(0)
        
        self.states.append(state)
```python
self.actions.append(action)  # This action has been appended to the list.
```

    def get_data(self):
```python
return np.array(self.states), np.array(self.actions)

```

    def save_data(self, filename):
        np.savez(filename, states=np.array(self.states), actions=np.array(self.actions))

    @staticmethod
    def load_data(filename):
        data = np.load(filename)
        return data['states'], data['actions']