from pathlib import Path
from typing import List, Generator

import toml
import openai
from openai import OpenAI

from models.languages import SourceLangsCodes
from settings.config import settings, BASE_DIR

"""
Get source lang

Open txt file
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
    
File structure:

# CONTEXT START
...
# CONTEXT END

**Text block**
if 
    
Prompt:

"""


class ChatGPTTranslateRaw:
    BATCH_MAX_SIZE = 10000
    BASE_LANGUAGE = SourceLangsCodes.RUSSIAN

    ENG_PROMPT_TEMPLATE = """
        I have a visual novel, and I need to translate the dialogue and internal thoughts of the characters 
        of one scene from {source_language} into {target_language}.  
        Maintain formatting as in the file. 
        Pay attention to language idioms. 
        Maintain the mood of the lines. 
        I need an artistic translation, not a literal one. 
        Preserve natural speech. 
        Pay attention to the context block. 
        Translate based on the context block.  
        Do not translate text between them. 
        The text should feel natural, conversational, and fit the mood of each character. 
        Please ensure that speech is informal or formal as appropriate, and that the tone, 
        emotions, and nuances of the original text are preserved. 
        Also, make sure the Ukrainian translation flows 
        well and sounds natural for a native reader.
        Context about the scene:
        {scene_context}
    """
    PROMPT_TEMPLATE = """
        Я делаю визуальную новеллу, и мне нужно перевести диалоги и внутренние мысли персонажей одной сцены с 
        {source_language} языка на {target_language}.
        
        Текст состоит из реплик персонажей и мыслей героя.
        Учитывай блоки контекста и переводи, исходя из них.
        Блоки разделены пустыми строками.
        Мысли героя начинаются блоками без отступа слева.
        Блоки реплик начинаются с отступа слева. 
        В первой строки блока реплики заглавными буквами прописано имя персонажа
        
        Мне нужен художественный перевод, а не дословный.
        Обрати внимание на языковые идиомы.
        Сохраняй настроение реплик и мыслей.
        Сохраняй изначальное форматирование, отступы и переносы строк.
        Перевод должен быть естественным, разговорным и соответствовать характеру каждого персонажа.
        Пожалуйста, убедись, что речь персонажей используется в нужной степени формальности или неформальности, 
        а также что тон, эмоции и нюансы оригинального текста сохранены.
        Кроме того, сделайте так, чтобы перевод был плавным и звучал естественно для носителя языка.
        Контекст о сцене:
        {scene_context}
    """

    def __init__(self, source_file_path: Path):
        self.source_file_path = source_file_path

    def read_file_block(self):
        with open(self.source_file_path, 'r', encoding='utf-8') as f:
            buffer = []
            for line in f:
                buffer.append(line.rstrip())

                if line == '\n':
                    yield '\n'.join(buffer[:-1])  # Yield the text before the double newlines
                    buffer = []

            if buffer:  # Handle any remaining content at the end of the file
                yield '\n'.join(buffer)

    def read_batch(self, block_reader: Generator) -> str:
        batch: List[str] = []
        batch_size = 0

        for text_block in block_reader:
            batch_size += len(text_block)
            batch.append(text_block)

            if batch_size > self.BATCH_MAX_SIZE:
                yield '\n\n'.join(batch)
                batch = []
                batch_size = 0

        if batch:
            yield '\n\n'.join(batch)

    def translate_batch(
            self,
            batch: str,
            target_language: str,
            context_block: str,
    ) -> str:
        if target_language == self.BASE_LANGUAGE:
            return ''
        client = OpenAI(
            api_key=settings.CHAT_GPT_API_KEY,
            organization=settings.OPENAI_ORG_ID,
            project=settings.PROJECT_ID,
        )

        print(f'translate on {target_language}')
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": self.PROMPT_TEMPLATE.format(
                        source_language=self.BASE_LANGUAGE.name,
                        target_language=target_language,
                        scene_context=context_block,
                    )
                },
                {
                    "role": "user",
                    "content": batch
                }
            ],
        )

        return completion.choices[0].message.content

    @staticmethod
    def write_batch(batch: str, language: str) -> None:
        saving_path = Path(
            f'{BASE_DIR}/data/result/{language}/raw_file.txt'
        )

        if not saving_path.exists():
            saving_path.parent.mkdir(parents=True, exist_ok=True)
            saving_path.touch()

        with open(saving_path, "a") as file:
            file.write(batch)

    def run(self) -> None:
        block_reader = self.read_file_block()

        context_block = next(block_reader)
        print(context_block)

        for batch in self.read_batch(block_reader=block_reader):
            for lang in SourceLangsCodes:
                translated_batch = self.translate_batch(
                    batch=batch,
                    target_language=lang.name,
                    context_block=context_block,
                )
                self.write_batch(batch=translated_batch, language=lang.value)
                print(translated_batch)

                print('====')
        # for text batch in file, translate it on all other langguages


if __name__ == '__main__':
    ChatGPTTranslateRaw(
        source_file_path=Path(
            f'{BASE_DIR}/data/source/raw_file_ru.txt'
        )
    ).run()
