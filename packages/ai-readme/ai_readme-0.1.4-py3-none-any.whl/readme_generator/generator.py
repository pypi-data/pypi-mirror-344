import os
from readme_generator.ai_client import get_client
from readme_generator.utils import read_project_files
from readme_generator.prompt_templates import get_prompt


class ReadmeGenerator:
    def __init__(self, lang: str, provider: str, max_chars: int = 10000):
        self.lang = lang
        self.provider = provider
        self.max_chars = max_chars
        self.client = get_client(provider)

    def run(self):
        project_summary = read_project_files(max_chars=self.max_chars)
        prompt = get_prompt(self.lang, project_summary)
        readme_content = self.client.chat(prompt)
        output_path = f"README_{self.lang}.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"✅ {output_path} created successfully!")
