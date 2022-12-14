{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/ce6aa13369b667ac2542593170993504932eb836.tar.gz") {} }:

let
  packages = python-packages: with python-packages; [
    black
    isort
    virtualenv
    pip
    setuptools
    poetry
  ];
  my-python = pkgs.python310.withPackages packages;
in
pkgs.mkShell {
  buildInputs = with pkgs; [ my-python postgresql ];
  shellHook = ''
    # Tells pip to put packages into $PIP_PREFIX instead of the usual locations.
    # See https://pip.pypa.io/en/stable/user_guide/#environment-variables.
    export PIP_PREFIX=$(pwd)/_build/pip_packages
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    unset SOURCE_DATE_EPOCH
  '';
}

