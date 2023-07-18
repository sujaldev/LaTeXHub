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

* Run the container on your server:

```bash
mkdir -p ~/latexhub/build ~/latexhub/repos # create these before hand or the container won't start
cd latexhub
touch docker-compose.yaml # copy the example present in this repository and edit variables
sudo docker compose up -d
```

* Set up your reverse proxy to proxy requests to the container, example for apache:

```apacheconf
<VirtualHost *:443>
        ServerName pdf.example.com
        DocumentRoot /var/www/html/pdf/
        ...
        ProxyPass / http://localhost:54321/
        ProxyPassReverse / http://localhost:54321/
</VirtualHost>
```

* Set up a webhook for push events in your latex repository by going to https://github.com/USER/REPO/settings/hooks
    * set the URL in the following format: https://pdf.example.com/webhook/USER/REPO
    * set the secret same as the one you set in your docker-compose.yaml

* Add a `build.sh` to your repository.
* Add the `build/` directory to your `.gitignore` file.

### Config

You can add a `latexhub.toml` file to your repository to customize the path to `build.sh` and `build/` directory:

```toml
[build]
script = "build.sh"
artifact_dir = "build/"
```