from jinja2 import Environment, FileSystemLoader

def render_template(template_name: str, variables: dict) -> str:
    env = Environment(
        loader=FileSystemLoader("prompts"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_name)
    return template.render(**variables)