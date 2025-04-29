"""Command-line interface."""
import fire

from saas_ips.collector import Collector


def main() -> None:
    """Main entry point for the command line interface of Saas Data Collector."""
    fire.Fire(Collector)


if __name__ == "__main__":
    main()
