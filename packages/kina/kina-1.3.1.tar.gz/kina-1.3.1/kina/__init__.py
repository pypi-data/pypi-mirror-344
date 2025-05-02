"""Initialization module for the Kina CLI."""

from typing import Annotated

import typer
from azure.identity import DefaultAzureCredential
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

from kina.azure.helpers import get_default_subscription_id

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)
kubectl = typer.Typer(no_args_is_help=True, help="Manage local Kubectl Configuration")
app.add_typer(kubectl, name="kubectl")

credential = DefaultAzureCredential()
subscription_id = get_default_subscription_id()


@app.command(name="create")
def cluster_create(
    locations: Annotated[
        str,
        typer.Option(
            "--locations",
            "--location",
            "-l",
            help="Azure Locations to create Kubernetes Clusters in, comma seperated",
        ),
    ] = "uksouth",
    no_cni: Annotated[
        bool,
        typer.Option(
            "--no-cni",
            help="Disable CNI for the AKS clusters. This is useful for testing purposes.",
        ),
    ] = False,
    network_dataplane: Annotated[
        str | None,
        typer.Option(
            "--network-dataplane",
            "--dataplane",
            "-d",
            help=" Network Dataplane to use. Defaults to None.",
        ),
    ] = None,
) -> None:
    """Create a new Kina AKS Cluster.

    Args:
        locations (str): Azure Locations to create Kubernetes Clusters in, comma separated.
        no_cni (bool): Disable CNI for the AKS clusters. This is useful for testing purposes.
        network_dataplane (str | None): Network Dataplane to use. Defaults to None.

    """
    from kina.azure.kubernetes import configure_network_iam, create_aks_clusters
    from kina.azure.resource_groups import create_resource_group
    from kina.azure.virtual_networks import create_virtual_networks
    from kina.kubectl import add_cluster_to_kubeconfig, set_current_context

    locations = locations.split(",")
    cluster_count = len(locations)

    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TimeElapsedColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        rg_task = progress.add_task("Creating Resource Group...", total=1)
        vnet_task = progress.add_task("Creating Virtual Networks...", total=cluster_count + 1)
        aks_task = progress.add_task("Creating AKS Clusters...", total=cluster_count + 1)
        network_iam = progress.add_task("Configuring Network IAM...", total=cluster_count + 1)
        kubectl_task = progress.add_task("Adding AKS Cluster to Kubeconfig...", total=cluster_count + 1)

        rg_name = create_resource_group(
            credential=credential,
            subscription_id=subscription_id,
            locations=locations,
        )
        progress.update(rg_task, description=f"Created Resource Group: {rg_name}", advance=1)
        vnets = create_virtual_networks(
            credential=credential,
            subscription_id=subscription_id,
            locations=locations,
            resource_group_name=rg_name,
            rich_progress=progress,
            rich_task=vnet_task,
        )
        progress.update(vnet_task, description=f"Created Virtual Networks: {', '.join(vnets)}", advance=1)
        clusters = create_aks_clusters(
            credential=credential,
            subscription_id=subscription_id,
            virtual_network_names=vnets,
            resource_group_name=rg_name,
            no_cni=no_cni,
            network_dataplane=network_dataplane,
            rich_progress=progress,
            rich_task=aks_task,
        )
        progress.update(aks_task, description=f"Created AKS Clusters: {', '.join(clusters)}", advance=1)
        for cluster in clusters:
            progress.update(network_iam, description=f"Configuring Network IAM: {cluster}", advance=1)
            configure_network_iam(
                credential=credential,
                subscription_id=subscription_id,
                resource_group=rg_name,
                cluster_name=cluster,
            )
        progress.update(network_iam, description=f"Configured Network IAM: {', '.join(clusters)}", advance=1)
        for cluster in clusters:
            progress.update(kubectl_task, description=f"Adding AKS Cluster to Kubeconfig: {cluster}", advance=1)
            add_cluster_to_kubeconfig(
                credential=credential,
                subscription_id=subscription_id,
                resource_group_name=rg_name,
                cluster_name=cluster,
            )
        set_current_context(clusters[0])
        progress.update(
            kubectl_task,
            description=f"Added AKS Clusters to Kubeconfig: {', '.join(clusters)}, set current context to {clusters[0]}",  # noqa: E501
            advance=1,
        )


@app.command(name="delete")
def cluster_delete(name: Annotated[str, typer.Argument()]) -> None:
    """Delete an existing Kina AKS Cluster.

    Args:
        name (str): The name of the Kina AKS Cluster to delete.

    """
    from kina.azure.resource_groups import delete_resource_group

    deleted = delete_resource_group(credential, subscription_id, name)
    if deleted:
        typer.echo(f"Deleted Resource Group: {name}")
    else:
        typer.echo(f"Resource Group '{name}' not found or not managed by Kina.")


@app.command(name="list")
def cluster_list(
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output format. Allowed values: json, table, names"),
    ] = "table",
) -> None:
    """List all Kina AKS Clusters.

    Args:
        output (str): Output format. Allowed values: json, table, names.

    """
    from kina.azure.resource_groups import list_resource_groups

    resource_groups = list_resource_groups(credential, subscription_id)
    console = Console()

    if output == "table":
        t = Table()
        t.add_column("Name")
        t.add_column("Location(s)")
        t.add_column("Created By")

        for resource_group_name, locations, username in resource_groups:
            t.add_row(resource_group_name, locations, username)
        console.print(t)
    elif output == "json":
        import json

        resource_groups_json = [
            {
                "name": resource_group_name,
                "locations": locations,
                "created_by": username,
            }
            for resource_group_name, locations, username in resource_groups
        ]
        console.print(json.dumps(resource_groups_json, indent=2))
    elif output == "names":
        resource_group_names = [resource_group_name for resource_group_name, _, _ in resource_groups]
        console.print("\n".join(resource_group_names))


@kubectl.command()
def cleanup() -> None:
    """Clean up the kubectl configuration by removing all Kina instances."""
    from kina.kubectl import cleanup_kubeconfig

    cleanup_kubeconfig()
    typer.echo("Cleaned up kubectl configuration")


@kubectl.command()
def remove(name: str) -> None:
    """Remove a Kina instance from the kubectl configuration.

    Args:
        name (str): The name of the Kina instance to remove.

    """
    from kina.kubectl import remove_from_kubeconfig

    remove_from_kubeconfig(name)
    typer.echo(f"Removed Kina Instance from Kubeconfig: {name}")


@app.command(name="version")
def version() -> None:
    """Display the installed version of Kina."""
    from importlib.metadata import version

    import requests

    console = Console()
    current_version = version("kina")
    try:
        latest_version = requests.get("https://pypi.org/pypi/kina/json", timeout=2).json()["info"]["version"]
    except requests.RequestException:
        latest_version = None

    if latest_version is None or current_version == latest_version:
        console.print(f"Kina version: [green]{current_version}[/]")
    else:
        console.print(f"Kina version: [red]{current_version}[/]")
        if latest_version:
            console.print(f"Latest version: [green]{latest_version}[/]")
            console.print('Update available! Run [bold]"uv tool update kina"[/] to update to the latest version.')
        else:
            console.print("Unable to check for updates.")


if __name__ == "__main__":
    app()
