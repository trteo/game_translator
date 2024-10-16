from pathlib import Path

import toml
import openai

"""
Get source lang

Open rpy file
Parse file (
        select context
        split text on blocks by \n\n

        If starts with \t:
            1 row is a name
            other lines are speeches

        If no \t at the beginning :
            its KAYOSHI thoughts block
    ) 

    unite blocks to batches. Each batch must be ~ 80% max response size
    translate each batch oon other languages and 
    save to independent files with lang postfix 

Prompt:

"""