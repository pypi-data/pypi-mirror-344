import sys
import click
from .validators import VALIDATORS


# ───────────────────────── helper for GCP JSON ──────────────────────────
def prompt_sa_json() -> str:
    """
    Opens $EDITOR so the user can paste very long service-account JSON without
    hitting the terminal’s 1024-byte line limit.
    """
    template = (
        "# Paste the FULL service-account JSON here.\n"
        "# Save & exit: :wq <Enter>   |   Abort without saving: :q! <Enter>\n"
    )
    edited = click.edit(text=template)
    if edited is None:
        click.secho("No JSON provided – aborting.", fg="red")
        sys.exit(1)

    # Strip comment lines
    json_blob = "\n".join(
        ln for ln in edited.splitlines() if not ln.lstrip().startswith("#")
    ).strip()
    if not json_blob:
        click.secho("File was empty – aborting.", fg="red")
        sys.exit(1)

    return json_blob


# ───────────────────────── main CLI ──────────────────────────
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-H",
    "--hide-input",
    is_flag=True,
    default=False,
    help="Mask secret input (asterisks). Default is to show what you type.",
)
@click.version_option(package_name="secretverify")
def main(hide_input: bool) -> None:
    """Validate leaked secrets by making test API calls."""
    apps = sorted(VALIDATORS.keys())
    click.echo("Select a secret type to validate:")
    for i, app in enumerate(apps, 1):
        click.echo(f"  {i}. {app}")

    idx = click.prompt("Enter number", type=int)
    if not 1 <= idx <= len(apps):
        click.secho("Invalid selection.", fg="red")
        sys.exit(1)

    app = apps[idx - 1]
    validator = VALIDATORS[app]

    params: dict[str, str] = {}
    for p in validator.params:
        if p == "sa_json":
            params[p] = prompt_sa_json()
            continue

        # Hide only if user asked for it
        hide = hide_input and any(tok in p for tok in ("token", "key", "secret"))
        params[p] = click.prompt(p.replace("_", " "), hide_input=hide)

    rotated, msg = validator(**params)
    click.echo(msg)
    if rotated:
        click.secho("✅ Secret appears to be rotated/disabled", fg="green")
    else:
        click.secho("⚠️ Secret is still live", fg="red")


if __name__ == "__main__":
    main()
