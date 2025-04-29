"""Static Site Containerizer."""

# ruff: noqa: D301, D401

from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory

import click
from python_on_whales import Builder, DockerClient

from static_site_containerizer.templates import NGINX_DOCKERFILE


def validate_content_path(ctx, param: str, value: str) -> str:
    """Validator for content path.

    :param ctx:
    :param param:
    :param value:
    :return:
    """
    content_path = Path(value)
    if not content_path.exists():
        raise click.BadParameter("Content path does not exist")
    if not content_path.is_dir():
        raise click.BadParameter("Content path must be a directory")
    return value


@click.command()
@click.option(
    "--content",
    required=True,
    callback=validate_content_path,
    help="Directory containing content to serve with web server",
)
@click.option("--registry", required=True, default="docker.io", help="Docker registry")
@click.option(
    "--registry-username",
    help="Docker registry username",
)
@click.option(
    "--registry-password",
    help="Docker registry password",
)
@click.option(
    "--tag",
    multiple=True,
    required=True,
    help='Name and optionally a tag (format: "name:tag")',
)
@click.option(
    "--platform",
    default="linux/amd64",
    type=click.Choice(["linux/amd64", "linux/arm64"], case_sensitive=False),
    help="Set target platform for build",
)
@click.option(
    "--push",
    is_flag=True,
    help="Push image to registry",
)
@click.option(
    "--load",
    is_flag=True,
    help="Load image into Docker",
)
def cli(
    content: str,
    registry: str,
    registry_username: str,
    registry_password: str,
    tag: list[str],
    platform: str,
    push: bool,
    load: bool,
) -> None:
    """Static Site Containerizer CLI tool.

    A CLI tool for producing a Docker container for hosting your static site.

    \f

    :param content:
    :param registry:
    :param registry_username:
    :param registry_password:
    :param tag:
    :param platform:
    :param push:
    :param load:
    :return:
    """
    docker_client: DockerClient = DockerClient()
    builder: Builder = docker_client.buildx.create(
        driver="docker-container", driver_options=dict(network="host")
    )

    if registry_username and registry_password:
        docker_client.login(
            server=registry,
            username=registry_username,
            password=registry_password,
        )

    with TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        content_path = tmpdir_path / "content"
        copytree(content, content_path)

        dockerfile: str = NGINX_DOCKERFILE.substitute(
            {"base_image": "nginx:latest", "content_path": "/content"}
        )
        dockerfile_path = tmpdir_path / "Dockerfile"
        with open(dockerfile_path, "w") as file:
            file.write(dockerfile)

        docker_client.buildx.build(
            context_path=tmpdir_path,
            tags=tag,
            platforms=[platform],
            builder=builder,
            push=push,
            load=load,
        )

    # Cleanup
    docker_client.buildx.stop(builder)
    docker_client.buildx.remove(builder)
