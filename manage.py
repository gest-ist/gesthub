#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""


def main() -> None:
    from core.cli import manage

    manage()


if __name__ == "__main__":
    main()
