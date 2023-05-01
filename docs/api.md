# exec_openai
Executes an OpenAI model with the provided prompt and returns the response.

### Parameters
- `prompt` (`str`): The prompt to pass to the OpenAI model.
- `role` (`str`, optional): The role of the prompt. Default is "system".
- `model` (`str`, optional): The OpenAI model to use. Default is "gpt-3.5-turbo".
- `messages` (`list`, optional): A list of messages to pass to the OpenAI model. Default is None.

### Returns
- `str`: The response from the OpenAI model.

### Example
```python
response = exec_openai(prompt="Hello", role="user")
print(response)
```

### Function Details
```python
def exec_openai(prompt, role="system", model=config["openai"]["model"], messages=None):
    msgs = [{"role": role, "content": prompt}] if messages is None else messages

    # execute openai model
    response = openai.ChatCompletion.create(
        model=model,
        messages=msgs,
    )

    # get response from openai
    answer = response.choices[0].message.content.strip()
    return answer
```
The `exec_openai` function takes in a `prompt` string and passes it to the OpenAI `ChatCompletion.create` method along with some optional parameters like `role` and `model`. It then returns the response obtained from the OpenAI model. If the `messages` parameter is provided, it is included as a list of messages to pass to the OpenAI model.

The `msgs` variable is created by converting the `messages` parameter to a list of messages in the required format for OpenAI. This is then passed to the `ChatCompletion.create` method which returns a response object.

The `answer` variable is then used to get the response content from the response object, and returned to the calling function.