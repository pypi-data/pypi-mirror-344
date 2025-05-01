import re
import sys
import click
from .validators import VALIDATORS


# ───────────────────────── GCP helper ───────────────────────── #
def prompt_sa_json() -> str:
    """
    1. Show copy-paste instructions.
    2. Wait for the user to press <Enter>.
    3. Launch a completely blank $EDITOR buffer (no template lines).
    4. Return ONLY the first JSON object found in the buffer.
    """
    click.echo(
        "\n📋  Copy the ENTIRE service-account JSON blob."
        "\nPaste it into the editor that opens next."
        "\n  • Save & exit :  :wq  <Enter>   |   Ctrl-O ↵ Ctrl-X (nano)"
        "\n  • Abort       :  :q! <Enter>   |   Ctrl-X       (nano)"
    )
    click.prompt("\nPress <Enter> to launch the editor",
                 default="", show_default=False)

    edited = click.edit()           # launches $EDITOR with an empty file
    if edited is None:              # user quit without saving
        click.secho("Aborted – no JSON provided.", fg="red")
        sys.exit(1)

    match = re.search(r"\{.*\}", edited, re.S)   # DOTALL
    if not match:
        click.secho("No JSON object found – aborting.", fg="red")
        sys.exit(1)

    return match.group(0).strip()


# ─────────────────────── main CLI entry-point ─────────────────────── #
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-H",
    "--hide-input",
    is_flag=True,
    default=False,
    help="Mask secret input (default shows what you type).",
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
    for param in validator.params:
        if param == "sa_json":
            params[param] = prompt_sa_json()
            continue

        hide = hide_input and any(tok in param for tok in ("token", "key", "secret"))
        params[param] = click.prompt(param.replace("_", " "), hide_input=hide)

    rotated, message = validator(**params)
    click.echo(message)
    if rotated:
        click.secho("✅ Secret appears to be rotated/disabled.", fg="green")
    else:
        click.secho("⚠️ Secret is still live", fg="red")


if __name__ == "__main__":
    main()
