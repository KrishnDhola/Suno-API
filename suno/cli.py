# import json
import os

# import requests
import suno
import typer
from rich import print

VERSION = "0.1.1"
COOKIE = os.getenv("ajs_anonymous_id=92370b46-2d41-4b0c-ae6d-c219061fbd2e; __client=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNsaWVudF8yeWRkdTNKZnhrcDNiUUpEbHlmcWhGcDBOMEQiLCJyb3RhdGluZ190b2tlbiI6Imd1bWJoeDR0M3l4azZuazZoMml1dHl6MmYzZHp5eGExNWpjOXNlc2oifQ.Ew16s8AXNY6FHJyed3tUyATeB1vRhkAYDO2pRrzQFTz2oTMnqAUFIOhg1m-sl7N5HlZlXNlAhoLOPIYGKXuqGxLjI8S223UjNOj59QpjEhXOVEBZSChV73ILvWxEBMZ261UjZN0a801KgvTiLB1T9-UB6NYKp9vY02TYvq1uUUotDeriluX_jgQUkYC-tYxg1A_BatKi0nWwcdqpEOqzVEyLYQqeqEKASe1FxEg8Aw2Miks7oLCC7v6w1_Ee4Y4HwoIeZnhsVP4tboNfVKHF19bbIj5EzTVwi1CEEFYPJRV5SX5SFXZNQzXWV2LZ1TRJF38LDqMntZn07b4Y-tLzjw; __client_uat=1750168648; __client_uat_U9tcbTPE=1750168648; __stripe_mid=4af87fcc-0844-40a8-9bfb-b9ae5e3a59414579cb; __cf_bm=IetgipKnglsG0_5kkEeEwPxz6B3uEZR2jSQEpqJ5VVw-1752065447-1.0.1.1-DkiwlhIyuISPXBD2sgI5TTKEb3d.53dcmUlK1wHKY0ZyVWdkVOSw69puoF2mBEvfonK8jfcHTUukkcBvyv81iWQMcqU0HZW1DpJWzMPQLZ4; _cfuvid=S09IStPPavNKMdXQbSPr7N_K_qESPCKl.wpYEow_cdE-1752065447462-0.0.1.1-604800000")
# HOST = "127.0.0.1"
# PORT = 8000


# Suno API client
client = suno.Suno(cookie=COOKIE)


def version_callback(value: bool):
    if value:
        print(f"Suno {VERSION}: make a song with Suno using v3 🥳")
        raise typer.Exit()


# Typer app
app = typer.Typer()
app_songs = typer.Typer()
app.add_typer(
    app_songs,
    name="songs",
    help="Make your songs with Suno.",
)
app_credits = typer.Typer()
app.add_typer(
    app_credits,
    name="credits",
    help="Check your remaining credits on Suno.",
)


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    )
) -> None:
    pass


@app_songs.command(help="Generate your songs.")
def generate(
    prompt: str,
    custom: bool = typer.Option(
        prompt="Are you sure you want to create a song in custom mode?",
        help="Create a song in custom mode.",
    ),
    tags: str = "",
    instrumental: bool = typer.Option(
        prompt="Are you sure you want to create a song without lyrics?",
        help="Create a song without lyrics.",
    ),
) -> None:
    songs = client.songs.generate(
        prompt,
        custom=custom,
        tags=tags,
        instrumental=instrumental,
    )
    data = [song.model_dump() for song in songs]
    # data = json.dumps(
    #     {
    #         "prompt": prompt,
    #         "custom": custom,
    #         "tags": tags,
    #         "instrumental": instrumental,
    #     }
    # )
    # response = requests.post(f"http://{HOST}:{PORT}/v1/songs", data=data)
    # if not response.ok:
    #     raise Exception(f"failed to generate songs: {response.status_code}")
    # data = response.json()
    print(data)


@app_songs.command(help="List all your created songs in the library.")
def list() -> None:
    songs = client.get_songs()
    data = [song.model_dump() for song in songs]
    # response = requests.get(f"http://{HOST}:{PORT}/v1/songs")
    # if not response.ok:
    #     raise Exception(f"failed to get songs: {response.status_code}")
    # data = response.json()
    print(data)


@app_songs.command(help="Get a song by its ID.")
def get(id: str) -> None:
    song = client.get_song(id)
    data = song.model_dump()
    # response = requests.get(f"http://{HOST}:{PORT}/v1/song/{id}")
    # if not response.ok:
    #     raise Exception(f"failed to get song: {response.status_code}")
    # data = response.json()
    print(data)


@app_songs.command(help="Download a song on Suno.")
def download(song: str, root: str = ".") -> None:
    suno.download(song, root=root)


@app_credits.command(help="Display your remaining credits.")
def display() -> None:
    credits = client.get_credits()
    data = {"total_credits_left": credits}
    # response = requests.get(f"http://{HOST}:{PORT}/v1/credits")
    # if not response.ok:
    #    raise Exception(f"failed to get credits: {response.status_code}")
    # data = response.json()
    print(data)


if __name__ == "__main__":
    app(prog_name="suno")
