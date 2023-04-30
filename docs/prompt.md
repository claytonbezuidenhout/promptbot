# Class PromptBot

A class for generating a prompt and retrieving a response from GPT OpenAI.

## Attributes
- `name`: `str`
    name of the `PromptBot`.
    
- `execute_output`: `bool`
    boolean value representing whether the output should be executed or not.
    
- `version_limit`: `int`
    limit for the versions of output `PromptBot` can have
    
- `goal`: `str`
    the goal of `PromptBot`
    
- `result`: `str`
    the result of the last `PromptBot` execution
    
- `prompt`: `str`
    the prompt for the OpenAI API
    
- `improve_prompt`: `str`
    the prompt for improving the previous output
    
- `improve`: `str`
    the improvement to be made
    
- `rules`: `list`
    a list of `PromptBot` rules
    
- `commands`: `list`
    a list of commands that define `PromptBot`'s behavior
    
- `versions`: `list`
    a list of `PromptBot` versions, builds automatically as you execute `PromptBot`
    
## Methods
- `__init__(self, name=None, execute_output=False, version_limit=3)`
    Initializes the `PromptBot` object.
    
- `set_goal(self, goal)`
    Sets the goal of `PromptBot`.
    
- `add_rule(self, rule)`
    Adds a rule to the list of `PromptBot` rules.
    
- `set_example_output(self, output)`
    Sets the example output.
    
- `add_cmd(self, command)`
    Adds a command to the list of commands `PromptBot` accepts.
    
- `get_prompt(self)`
    Creates the prompt for the OpenAI API.
    
- `set_and_return_improve_prompt(self)`
    Creates the prompt for improving the previous output.
    
- `set_improve(self, improve)`
    Sets the improvement made between two different versions.
    
- `run_ai(self, improve=False)`
    Runs OpenAI API on the prompt and retrieves the result.
    
- `start_improvements(self)`
    Starts the improvement process.
    
- `execute_code(self)`
    Executes the output if `execute_output` is `True`.
    
- `save_to_file(self, file_name)`
    Saves the result to a file.
    
- `save_versions(self, file_name)`
   Saves all versions of output to a file.

## __init__(self, name=None, execute_output=False, version_limit=3)
Initializes the `PromptBot` object.

### Parameters
- `name`: `str`, optional
    name of the `PromptBot`
    
- `execute_output`: `bool`, optional
    boolean value representing whether the output should be executed or not
    
- `version_limit`: `int`, optional
    limit for the versions of output `PromptBot` can have
    

## set_goal(self, goal)
Sets the goal of `PromptBot`.

### Parameters
- `goal`: `str`
    the goal of `PromptBot`.

### Returns
- `self`


## add_rule(self, rule)
Adds a rule to the list of `PromptBot` rules.

### Parameters
- `rule`: `str`
    the new rule to be added
    
### Returns
- `self`


## set_example_output(self, output)
Sets the example output.

### Parameters
- `output`: `str`
    the example output to be set
    
### Returns
- `self`


## add_cmd(self, command)
Adds a command to the list of commands `PromptBot` accepts.

### Parameters
- `command`: `str`
    the new command to be added
    
### Returns
- `self`


## get_prompt(self)
Creates the prompt for the OpenAI API.

### Returns
- `prompt`: `str`
    the prompt for the OpenAI API


## set_and_return_improve_prompt(self)
Creates the prompt for improving the previous output.

### Returns
- `improve_prompt`: `str`
    the prompt for improving the previous output


## set_improve(self, improve)
Sets the improvement made between two different versions.

### Parameters
- `improve`: `str`
    the improvement made between two different versions
    
### Returns
- `self`


## run_ai(self, improve=False)
Runs OpenAI API on the prompt and retrieves the result.

### Parameters
- `improve`: `bool`
    boolean value representing whether `PromptBot` will improve its output or not
    
### Returns
- `result`: `str`
    the result of the OpenAI API call


## start_improvements(self)
Starts the improvement process.


## execute_code(self)
Executes the output if `execute_output` is `True`.


## save_to_file(self, file_name)
Saves the result to a file.

### Parameters
- `file_name`: `str`
    the name of the file
    

## save_versions(self, file_name)
Saves all versions of output to a file.

### Parameters
- `file_name`: `str`
    the name of the file