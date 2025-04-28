import json

from cli.cloud.rest_helper import RestHelper
from cli.typer import typer_utils

app = typer_utils.create_typer()


@app.command(name="list", help="List your available organisations")
def list_orgs() -> None:
    r = RestHelper.handle_get("/api/bu", return_response=True)
    orgs = [{"uid": org["organisation"]["uid"], "displayName": org["organisation"]["displayName"]} for org in r.json()]
    print(json.dumps(orgs))
