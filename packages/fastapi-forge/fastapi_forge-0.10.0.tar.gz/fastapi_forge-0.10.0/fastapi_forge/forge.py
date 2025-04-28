from pathlib import Path, PurePath
from time import perf_counter

from cookiecutter.main import cookiecutter

from fastapi_forge.logger import logger
from fastapi_forge.project_io import ProjectBuilder
from fastapi_forge.schemas import ProjectSpec


def _get_template_path() -> Path:
    """Return the absolute path to the project template directory with validation."""
    template_path = Path(__file__).resolve().parent / "template"
    if not template_path.exists():
        raise RuntimeError(f"Template directory not found: {template_path}")
    if not template_path.is_dir():
        raise RuntimeError(f"Template path is not a directory: {template_path}")
    return template_path


def _validate_project_name(project_name: str) -> None:
    """Validate that the project name is safe to use in paths."""
    if not project_name:
        msg = "Project name cannot be empty"
        raise ValueError(msg)
    if PurePath(project_name).name != project_name:
        raise ValueError(
            f"Invalid project name: {project_name} (contains path traversal)"
        )
    if not project_name.isidentifier():
        logger.warning(
            f"Project name '{project_name}' may not be a valid Python identifier"
        )


async def build_project(spec: ProjectSpec) -> None:
    """Create a new project using the provided template and specifications."""
    start_time = perf_counter()
    project_name = spec.project_name

    try:
        _validate_project_name(project_name)
        logger.info(f"Building project '{project_name}'...")

        builder = ProjectBuilder(spec)
        await builder.build_artifacts()

        extra_context = {
            **spec.model_dump(exclude={"models"}),
            "models": {
                "models": [model.model_dump() for model in spec.models],
            },
        }

        if spec.use_builtin_auth:
            auth_user = spec.get_auth_model()
            if auth_user:
                extra_context["auth_model"] = auth_user.model_dump()
            else:
                logger.warning("No auth model found. Skipping authentication setup.")
                extra_context["use_builtin_auth"] = False

        logger.info("Running cookiecutter...")
        cookiecutter(
            template=str(_get_template_path()),
            output_dir=str(Path.cwd().resolve()),
            no_input=True,
            overwrite_if_exists=True,
            extra_context=extra_context,
        )
        logger.info("Cookiecutter completed successfully.")

        build_time = perf_counter() - start_time
        logger.info(
            f"Project '{project_name}' created successfully in {build_time:.2f} seconds."
        )

    except Exception as error:
        logger.error(f"Failed to create project '{project_name}': {error}")

        raise
