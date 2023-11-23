# Metropolis (Backend)
Make sure you have python 3.9 - 3.10 installed;
As of now, the project is only compatible with versions between python 3.9 and 3.10.11.

## Running Locally

### Nix 
Install [Nix](https://nixos.org/download) and [direnv](https://direnv.net) and run:
###### if using direnv
```sh
make
direnv allow
./manage.py migrate
nix run
```
###### If not using direnv:
```sh
nix develop # and run `./manage.py migrate` inside
nix run
```


### Anything besides Nix
If you do not want to use Nix:
(Note: only tested on Unix-like platforms)
```
python -m pip install poetry
poetry install
make # can remove for windows 
poetry run python ./manage.py migrate
poetry run python ./manage.py runserver
```

### Errors
#### Windows
###### poetry ModuleNotFoundError: No module named 'charset_normalizer'
reinstall poetry and run poetry install in an elevated (admin) terminal 
#### OpenSSL isn't found
Git installs it, so you can just add git's programs to path
- add git's path (defualt: C:\Program Files\Git\usr\bin\) to your user path
Since OpenSSL isn't installed, make probably isn't so below are the steps to bypass make
- `cd ./metropolis`
- `openssl genrsa -out local_rsa_privkey.pem 4096`
- `cp .\local_settings_sample.py .\local_settings.py`
## Additional setup/config

copy `./metropolis/local_settings_sample.py` to `./metropolis/local_settings.py` and read the file to change some of the values.


##### Creating your account
1. run `poetry run python ./manage.py createsuperuser` and enter the values
2. Look in your console to see the email that was printed out and find the email confirmation url
3. paste that url into your browser
4. sign in using the values you provided in step 1