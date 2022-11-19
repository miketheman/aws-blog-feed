# aws-blog-feed

Web application to read the AWS Container Blog RSS feed and filter results.

## Getting Started

Check out code, run `docker compose up --build` and navigate to <http://localhost:8080>

## Deployment

Use [AWS Copilot](https://aws.github.io/copilot-cli/) to deploy.

```shell
copilot deploy
```

## Built With

- [Python 3.11](https://www.python.org/)
- Backend:
	- [FastAPI](https://fastapi.tiangolo.com/)
	- [uvicorn](https://www.uvicorn.org/)
	- [feedparser](https://feedparser.readthedocs.io/)
	- [cachetools](https://cachetools.readthedocs.io/)
- Frontend:
	- [Jinja](https://jinja.palletsprojects.com/)
	- [Water.css](https://watercss.kognise.dev/)


## Authors

- [Mike Fiedler](https://mike.fiedler.me)

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
