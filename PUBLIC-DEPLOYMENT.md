# Public deployment

The repository contains both public website pages and internal working files. Do not publish the repository root directly.

`scripts/build-public.sh` creates an allowlisted artifact from the pages in `sitemap.xml`, the shared public assets and the three legacy offer redirects. It deliberately excludes the Digital Hub, strategy documents, prototypes, email previews and standalone internal tools.

## One-time GitHub setup

1. Add a repository Actions secret named `WEB3FORMS_ACCESS_KEY` containing the production Web3Forms access key.
2. In **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source.
3. Merge the deployment workflow to `main` and confirm the first run completes successfully.
4. Verify one brief and one newsletter signup end to end, including receipt by the intended inbox.

The workflow refuses to deploy if the form key is missing or if the placeholder remains in the generated pages. Until the repository secret and Pages source are configured, the website will show an honest contact fallback instead of claiming that an enquiry or subscription succeeded.

## Local artifact check

Run:

```sh
./scripts/build-public.sh /tmp/cvbs-public-check
```

Pass `WEB3FORMS_ACCESS_KEY` only when validating a configured artifact. Use a new destination path for each run; the script will not overwrite an existing directory.
