from pathlib import Path

import toml
import openai

"""
Get source lang

Open toml file
Parse file (
    remove all rows that starts not with [ 
    or source lang ('eng = "' or 'rus = "')
    ) 

Translate by batches 
    save translated batches to result with append
    
** batch must be ~ 8 times less than 
    
Prompt:

"""

