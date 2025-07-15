from openai import OpenAI
from .types import SummarizerOptions
from .logger import Logger


class FileSummarizer:
    def __init__(self, options: SummarizerOptions, logger: Logger):
        self.options = options
        self.openai = OpenAI(api_key=self.options.api_key)
        self.logger = logger

    async def summarize_file(self, file_path: str, content: str) -> str:
        try:
            self.logger.debug(f"Summarizing file: {file_path}")
            
            prompt = f"Please provide a concise summary of the following file content. Focus on the main purpose, key functionality, and important details:\n\nFile: {file_path}\n\nContent:\n{content}"

            response = self.openai.chat.completions.create(
                model=self.options.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.options.max_tokens,
                temperature=self.options.temperature
            )

            summary = response.choices[0].message.content
            
            if not summary:
                raise Exception("No summary generated from OpenAI response")

            summary = summary.strip()
            self.logger.debug(f"Successfully summarized file: {file_path}")
            return summary
            
        except Exception as error:
            self.logger.error(f"Failed to summarize file {file_path}", error)
            raise Exception(f"Summarization failed for {file_path}: {str(error)}")

    async def test_connection(self) -> bool:
        try:
            self.openai.models.list()
            self.logger.info("OpenAI connection test successful")
            return True
        except Exception as error:
            self.logger.error("OpenAI connection test failed", error)
            return False