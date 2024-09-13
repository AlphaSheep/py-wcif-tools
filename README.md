# py-WCIF-tools

A set of types and some basic tools for working with World Cube Association (WCA) Competition Interchange Format (WCIF) data in Python.

The primary use case is manual manipulation of competition data, such as manual group and staff assignments, or manual analysis of competition results.

## Set up

By default, the tool assumes that you're running the developer version of the [WCA website](https://github.com/thewca/worldcubeassociation.org) at `http://localhost:3000`.

To use it with the production version of [www.worldcubeassociation.org](https://www.worldcubeassociation.org), you'll need to set environment variables to point to the correct host and API keys. See the `.env.sample` file for an example. You will need to create your own API key, for which instructions are available [here](https://docs.worldcubeassociation.org/knowledge_base/v0_api.html#staging-oauth-application).


## Usage

You can call import types and call functions from the `py_wcif_tools` module.

```python
from py_wcif_tools import get_public_wcif

competition = get_public_wcif("competition-id")
```

Some functions require authentication. If you have not logged in before or if your token has expired (typically after 2 hours), calling the function will open a browser window and prompt you to log in. You will need to authorize the application to access your WCA account.

By default, the tool listens for a response on port 4299, but this can be changed by setting the `PY_WCIF_TOOLS_PORT` environment variable.

Once you have authorized the application, a `.token` file will be created in the current directory, containing your access token. Treat this file as a secret, and do not share it with anyone.

If you have logged in before, then the code will run silently with no user interaction required.

```python
competitions = get_competitions_managed_by_me()
```

## Functions

| Function | Description |
| --- | --- |
| `get_me() -> User` | Get information about the current user |
| `get_competitions_managed_by_me() -> list[Competition]` | Get a list of competitions managed by the current user |
| `get_user_by_wca_id(wca_id: str) -> User` | Get information about a user by their WCA ID |
| `get_wcif(competition_id: str) -> Competition` | Get the WCIF data for a competition |
| `get_public_wcif(competition_id: str) -> Competition` | Get the public WCIF data for a competition |
| `patch_wcif(competition_id: str, wcif: Competition) -> None` | Patch the WCIF data for a competition |
| `load_wcif_from_file(filename: str) -> Competition` | Load WCIF data from a file |
| `save_wcif_to_file(filename: str, wcif: Competition) -> None` | Save WCIF data to a file |


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.