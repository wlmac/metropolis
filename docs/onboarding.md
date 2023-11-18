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
poetry install
make
python -m pip install poetry
poetry run python ./manage.py migrate
poetry run python ./manage.py runserver
```



## Additional setup/config

copy `./metropolis/local_settings_sample.py` to `./metropolis/local_settings.py` and read the file to change some of the values.


##### Creating your account
1. run `poetry run python ./manage.py createsuperuser` and enter the values
2. Look in your console to see the email that was printed out and find the email confirmation url
3. paste that url into your browser
4. sign in using the values you provided in step 1
