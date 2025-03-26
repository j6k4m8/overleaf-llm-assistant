import sys
import time
from overphloem import Project
from openai import OpenAI
from pydantic import BaseModel, Field


class EditResponse(BaseModel):
    new_content: str = Field(
        ...,
        description="The new content of the file after editing.",
    )
    is_valid: bool = Field(
        ...,
        description="Whether the edit is valid.",
    )
    error_message: str = Field(
        ...,
        description="Error message if the edit is invalid.",
    )


def main():
    def on_change(project: Project):
        for file in project.files:
            if file.name.endswith(".tex"):
                print(f"Modifying {file.name}")

                # Search for any line that starts with "@ai".
                for line in file.content.splitlines():
                    if line.startswith("@ai"):
                        # Extract the prompt from the line.
                        prompt = line[3:].strip()
                        print(f"Prompt: {prompt}")

                        # Call the OpenAI API to get the edit.
                        response = (
                            OpenAI()
                            .beta.chat.completions.parse(
                                model="gpt-4o",
                                messages=[
                                    {
                                        "role": "system",
                                        "content": "You are a helpful assistant that modifies LaTeX files.",
                                    },
                                    {
                                        "role": "user",
                                        "content": "```" + file.content + "```",
                                    },
                                    {
                                        "role": "user",
                                        "content": prompt,
                                    },
                                    {
                                        "role": "user",
                                        "content": "Please return EXACTLY the modified file content, without any additional text.",
                                    },
                                ],
                                response_format=EditResponse,
                            )
                            .choices[0]
                            .message.parsed
                        )

                        # Check if the response is valid.
                        if response.is_valid:
                            file.content = response.new_content
                            print(f"New content: {file.content}")
                        else:
                            print(f"Error: {response.error_message}")
        return True

    # Start the project with the specified file
    project = Project(sys.argv[-1], "temp-project-directory")
    project.pull()
    while True:
        time.sleep(5)
        on_change(project)
        project.push()


if __name__ == "__main__":
    main()
