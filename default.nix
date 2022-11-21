{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/ce6aa13369b667ac2542593170993504932eb836.tar.gz") {} }:

let
	packages = python-packages: with python-packages; [
		black
		isort
		virtualenv
		pip
		setuptools
	];
	my-python = pkgs.python310.withPackages packages;
in
pkgs.mkShell {
	buildInputs = with pkgs; [ my-python bash ];
}

