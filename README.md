# LaTeXHub

LaTeXHub can:

- Automatically compile a PDF from your repository on GitHub.
- Generate preview images of your PDF that you can link it in your README file.
    - Clear GitHub's image cache to update the preview in the README.
- Move the compiled PDF to a desired location (example: /var/www/html/)
- Show compilation status in GitHub environments.

### Why not use GitHub Actions?

- It's slow
- You can't make the output pdf the default page for your site.

## Config

Add a `config.toml` file in your `config` directory (see, docker-compose.yaml):

```toml
[webhook-name]  # name used for webhook
repo = "https://github.com/user/repo"
build-script = "build.sh"  # Use `/config/` prefix for a file present in /app/config/.
artifact-dir = "out/"  # directory containing all artifacts, path is relative to the repository.
output-dir = "webhook-name" # will automatically be prefixed by /app/build/.
```

- `webhook-name`:
    - You need to set up a webhook in your repository to make a request on push events.
    - The url is of the format: `https://url.to.latexhub.com/webhook/webhook-name`
    - Calling this url will trigger a rebuild (if changes are detected) of the repository matching the webhook-name in
      the config file.
- `repo`:
    - This is the only **required** option.
    - The default values for the rest of the options are written in the above example.
- `build-script`:
    - path to a bash script present in your repository that contains commands to build your PDF.
    - use "/config/" prefix to declare a build script not present in your repository but is stored in the `/app/config`
      directory.
    - working directory for the script is initialized to be the root of your repository (it's your container, go
      wherever you want, do whatever you want).
- `artifact-dir`: specifies a directory where all the artifacts generated by `build-script` are to be expected.
- `output-dir`: Path to the directory (relative to `/app/build/`) where the generated artifacts should be copied.