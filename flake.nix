{
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-22.11;
    flake-utils.url = github:numtide/flake-utils;
    poetry2nix.url = github:nix-community/poetry2nix;
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }@attrs: flake-utils.lib.eachSystem [ "x86_64-linux" ] (system: let
    inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication mkPoetryEnv;
    pkgs = nixpkgs.legacyPackages.${system};
    add-setuptools = super: name: {
      ${name} = super.${name}.overridePythonAttrs (
        old: {
          buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
        }
      );
    };
  in let
    common = {
      projectDir = ./.;
      python = pkgs.python312;
      overrides = pkgs.poetry2nix.defaultPoetryOverrides.extend
        (self: super:
          (add-setuptools super "martor")
          // (add-setuptools super "alt-profanity-check")
        );
      preferWheels = true;
      editablePackageSources = {
        metropolis = ./.;
      };
    };
  in {
    devShells.default = (mkPoetryEnv common).env.overrideAttrs (prev: {
      buildInputs = with pkgs; [
        python312
        poetry
        openssl
        black
        isort
        mypy
        act
      ];
    });
    apps.default.type = "app";
    apps.default.program = "" + pkgs.writeShellScript "run.sh" ''
      set -eux
      trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
      #docker run -d -p 5672:5672 rabbitmq &
      ./manage.py runserver &
      celery -A metropolis worker -B --loglevel=DEBUG &
      wait
    '';
  });
}
