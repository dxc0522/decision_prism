"""Prompt templates and Jinja2 loader."""

from jinja2 import Environment, FileSystemLoader


def get_env() -> Environment:
    return Environment(
        loader=FileSystemLoader("prompts"),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_prompt(template_name: str, **context: str) -> str:
    return get_env().get_template(template_name).render(**context)
