# Nova

**Nova** is a higly-configurable voice-integrated assistant.
[Different voices for Nova](https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462)

---

## Main principles:

Program must be as least code as possible, and main features are only thru modules. But code must support all modules and normally run them. 

1. **_Modularity_** - all functions, that Nova can execute, must be written and put as `$module_name$.py` file in `data/modules/` directory. For Nova to be able to execute this function, it must have **`"ask" keywords`** in config and have __this structure:__
   ```python
   def main(config, command, result):
       # Something that your function must do...
       # For example:
       print("Deleting 'System32' is in progress... ")
       return config, {} # <- your function must return config, that you had as 1st argument and format data as {"key1":"value1", ...} for foramting `result`
   ```
   __Keywords example:__
   ```json
   {
     "$module_name$": {
       "ask": ["Can you kill my PC, pls?"], // <- ask keywords
       "answer": [
         "With a big excitement, {user_nickname}. {name} was made for this job!"
       ]
     }
     // other modules' keywords
   }
   ```
2. **_Configurabilty_** - with bare minimum of base functionality and maximum configurability Nova can be shaped into anyone's perfect personal assistant. So configs must be detailed, and code must be minimum and working with configs and modules. 
