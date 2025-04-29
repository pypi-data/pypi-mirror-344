# fastapi_pluggable_auth/email/templates.py
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader("fastapi_pluggable_auth", "email/templates"))


def render_template(name: str, **ctx):
    return env.get_template(name).render(**ctx)
