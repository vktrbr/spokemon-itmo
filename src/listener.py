import click

from src.speech_to_text import set_assistant


@click.command()
@click.option("--session_id", help="Session id")
def main(session_id: str) -> None:
    """
    Main function
    :param session_id:
    :return:
    """
    assistant = set_assistant(session_id)
    assistant.start()


if __name__ == "__main__":
    main()
