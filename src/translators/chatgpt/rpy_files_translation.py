from pathlib import Path

import toml
import openai

"""
Get source lang

Open rpy file
Parse file (
    source text like '\t# * "'
    result must be placed at '\t * "' after above
    
    
    codes after "translate *" must be replaced to short lang codes
    ) 

    unite blocks to batches. Each batch must be ~ 80% max response size
    translate each batch on other languages and 
    save to independent file into lang folder

Prompt:

"""