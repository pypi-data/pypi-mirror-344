from dotenv import dotenv_values
from pathlib import Path
import questionary
from typing import Dict

from zev.config.types import (
    SetupQuestion,
    SetupQuestionSelect,
    SetupQuestionText,
    SetupQuestionSelectOption,
)
from zev.constants import LLMProviders
from zev.llms.ollama.setup import questions as ollama_questions
from zev.llms.openai.setup import questions as openai_questions
from zev.llms.gemini.setup import questions as gemini_questions

setup_questions = [
    SetupQuestionSelect(
        name="LLM_PROVIDER",
        prompt="Pick your LLM provider:",
        options=[
            SetupQuestionSelectOption(
                value=LLMProviders.OPENAI,
                label="OpenAI",
                follow_up_questions=openai_questions,
            ),
            SetupQuestionSelectOption(
                value=LLMProviders.OLLAMA,
                label="Ollama",
                follow_up_questions=ollama_questions,
            ),
            SetupQuestionSelectOption(
                value=LLMProviders.GEMINI,
                label="Gemini",
                follow_up_questions=gemini_questions,
            ),
        ],
    )
]


def prompt_question(question: SetupQuestion, answers: Dict[str, str]) -> Dict[str, str]:
    existing_answer = answers.get(question.name)
    if type(question) == SetupQuestionSelect:
        # Find the matching option for the default value
        default_option = None
        if existing_answer:
            default_option = next((opt for opt in question.options if opt.value == existing_answer), None)

        answer: SetupQuestionSelect = questionary.select(
            question.prompt,
            choices=[
                questionary.Choice(option.label, description=option.description, value=option)
                for option in question.options
            ],
            default=default_option,
        ).ask()
        answers[question.name] = answer.value
        for q in answer.follow_up_questions:
            answers.update(prompt_question(q, answers=answers))
    elif type(question) == SetupQuestionText:
        answer = questionary.text(
            question.prompt, default=existing_answer or question.default, validate=question.validator
        ).ask()
        answers[question.name] = answer
    else:
        raise Exception("Invalid question type")
    return answers


def run_setup():
    config_path = Path.home() / ".zevrc"
    answers = dotenv_values(config_path)  # load in current values and then override as necessary
    for question in setup_questions:
        answers.update(prompt_question(question, answers))

    new_file = ""
    for env_var_name, value in answers.items():
        new_file += f"{env_var_name}={value}\n"

    with open(config_path, "w") as f:
        f.write(new_file)
