{
  description = "Local development and deployment environment for the GEST website";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python314;

        server = pkgs.writeShellApplication {
          name = "gest-server";
          runtimeInputs = [ pkgs.uv python ];
          text = ''
            set -euo pipefail

            export DJANGO_SETTINGS_MODULE="core.settings.dev"
            export DJANGO_DEBUG="true"
            export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,[::1]"

            uv sync --locked --no-dev --python "${python}/bin/python"
            exec uv run --locked --no-dev fastpysgi core.wsgi:application \
              --host 127.0.0.1 --port 8000
          '';
        };

        migrate = pkgs.writeShellApplication {
          name = "gest-migrate";
          runtimeInputs = [ pkgs.uv python ];
          text = ''
            set -euo pipefail
            export DJANGO_SETTINGS_MODULE="core.settings.dev"
            uv sync --locked --no-dev --python "${python}/bin/python"
            exec uv run --locked --no-dev manage.py migrate
          '';
        };
      in
      {
        apps = {
          default = {
            type = "app";
            program = "${server}/bin/gest-server";
          };

          migrate = {
            type = "app";
            program = "${migrate}/bin/gest-migrate";
          };
        };

        devShells.default = pkgs.mkShell {
          packages = [ pkgs.uv python ];
          shellHook = ''
            export DJANGO_SETTINGS_MODULE="core.settings.dev"
            export DJANGO_DEBUG="true"
          '';
        };
      });
}