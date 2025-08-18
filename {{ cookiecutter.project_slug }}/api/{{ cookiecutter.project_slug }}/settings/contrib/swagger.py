SPECTACULAR_SETTINGS = {
    "TITLE": "{{ cookiecutter.project_name }} API",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "AUTHENTICATION_EXTENSIONS": [
        "{{ cookiecutter.project_slug }}.apps.accounts.api.authentication.CustomSessionAuthenticationScheme",
    ],
    "COMPONENT_SPLIT_REQUEST": True,
}
