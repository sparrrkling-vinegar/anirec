# anirec - Anime Recodemdations!

## Description

This project was designed and built for the course of Software Quality and
Reliability at Innopolis University 2024 Spring semester.

This project gives the end user the ability to search for some anime titles,
save the chosen titles to their personal library and then get corresponding
recommendations based on user's personal favoutite anime.

## Deployment

You can access deployed application at
[anirec.ddns.net](http://anirec.ddns.net)

Reliability of the deployment is achieved by deploying the application using
docker compose and setting the restart policy.

## Installation

### Build & run from source (*nix, MacOS)

To run the project locally from the sources, run the following:

```sh
git clone git@github.com:sparrrkling-vinegar/anirec.git
cd anirec
poetry install --no-root
poetry run uvicorn main:app
```

This will run the project locally on port `8000`

### Use docker

If you want to run the docker version of the application, you can either build
the docker image by yourself, or pull it from the GitHub container registry.

To build the docker image locally, run:

```sh
git clone git@github.com:sparrrkling-vinegar/anirec.git
cd anirec
docker build -t anirec .
docker run anirec
```

To use already pushed docker image:

```sh
docker pull ghcr.io/sparrrkling-vinegar/anirec:latest
docker run ghcr.io/sparrrkling-vinegar/anirec:latest
```


## Technology stack

For the application itself we used Fastapi, Jinja templates, SQLite+SQLCipher,
Docker, docker-compose and Bootstrap library.

Since we considered different test types during the course, we have implemented
extensive testing for our application and integrated them into the CI pipeline,
for tests we used Pytest, Selenium, Flake8, Bandit and Semgrep.


## Testing

We have successfully leveraged the usage of the following tests:
1. Unit tests
1. Stess testing with locust, results can be seen [here](screenshots/locust.jpg)
1. Integration tests
1. Codestyle tests
1. Mutation testing
1. SAST scanning using bandit & semgrep

## License 

All the source code is licensed under the GPL-2.0 license 

anirec team @ 2024
