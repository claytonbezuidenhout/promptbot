# Config Manager
Below is a summary of the `ConfigManager` Python class. 

## Purpose
The purpose of `ConfigManager` is to manage the configuration file of the project using a singleton pattern. It reads the `prompbot.toml` file in the root directory of the project, if it exists, and stores the contents in memory.  

## Class Methods

### `__new__(cls, *args, **kwargs)`
Create and return a new ConfigManager instance if one does not already exist. If a ConfigManager instance already exists, return that instance instead. This method reads in the `promptbot.toml` file if it exists, otherwise, it raises a `FileNotFoundError`. 

#### Parameters
- `cls`: The class being instantiated.
- `*args`: Any positional arguments to be passed to the class constructor.
- `**kwargs`: Any keyword arguments to be passed to the class constructor.

#### Returns
- An instance of the ConfigManager class.

### `get_config(self)`
Get the configuration file as a dictionary.

#### Parameters
- None

#### Returns
- A dictionary containing the contents of the config file.