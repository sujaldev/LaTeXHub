# LaTeXHub

Quickly build a PDF from your latex repository and publish it to your website.

LaTeXHub can:

- Automatically compile a PDF from your repository on GitHub.
- Generate preview images of your PDF that you can link it in your README file.
    - Clear GitHub's image cache to update the preview in the README.
- Move the compiled PDF to a desired location (example: /var/www/html/)
- Show compilation status in GitHub environments.

### Why not use GitHub Actions?

- It's slow
- You can't make the output pdf the default page for your site.

## Usage

### Initial Installation

You only have to run the steps in this section once on your sever.

* Generate a personal access token by going to https://github.com/settings/tokens?type=beta, allow for all repositories
  or select the ones you want and allow the deployment permission in either case. Use this token while editing
  `docker-compose.yaml` in the next step for the `GITHUB_TOKEN` variable.

* Run the container on your server:

```bash
mkdir -p ~/latexhub/build ~/latexhub/repos # create these before hand or the container won't start
cd ~/latexhub
touch docker-compose.yaml # copy the example present in this repository and edit variables
sudo docker compose up -d
```

* Set up your reverse proxy to proxy requests to the container, example for apache:

```apacheconf
<VirtualHost *:443>
        ServerName pdf.example.com
        DocumentRoot /var/www/html/pdf/
        ...
        # You can also use the root path but it's unnecessary and then DocumentRoot won't work.
        ProxyPass /webhook/ http://localhost:54321/webhook/
        ProxyPassReverse /webhook/ http://localhost:54321/webhook/
</VirtualHost>
```

### Per repository

Steps in this section are to be repeated for every repository you want to auto compile.

* Set up a webhook for push events in your latex repository by going to https://github.com/USER/REPO/settings/hooks
    * set the URL in the following format: https://pdf.example.com/webhook/USER/REPO
    * set the secret same as the one you set in your docker-compose.yaml. The secret is important because if you
      don't use one, then anybody on the internet could trigger a build, and you probably don't want that to happen.

* Add a `build.sh` to your repository.
* Add the `build/` directory to your `.gitignore` file.

## Config

You can add a `latexhub.toml` file to your repository to customize the path to `build.sh` and `build/` directory:

```toml
[build]
script = "build.sh"
artifact_dir = "build/"
```

## Built-in Functions/Variables

Have a look at `src/include.sh`, this script gets prepended to your `build.sh` with the variables filled in. The script
declares some functions that allow you to easily interface with LaTeXHub. You can use the variables declared there in
your build script, and you can use the following functions:

### create_deployment

Generates a new deployment. Call this at the start of your script, it will initialize a new environment with `pending`
status. You can then call `update_deployment` at various stages in your script to change `pending` to other statuses.

### update_deployment

|     parameter     |                                 remarks                                  |
|:-----------------:|:------------------------------------------------------------------------:|
|      `state`      | one of `error`, `failure`, `pending`, `in_progress`, `queued`, `success` |
| `environment_url` |       URL to your generated PDF (only needs to be specified once)        |

Updates the current state of the deployment. `create_deployment` must be called before calling this function.

Example:

```bash
create_deployment
update_deployment in_progress https://pdf.example.com/document.pdf
...
update_deployment success
```

### clear_image_cache

Clear cache for all images present in all the markdown files in your repository. GitHub caches the images present in
your markdown files, so even after updating your image in your web server, it might not show the updated image on
GitHub if you don't call this function.
