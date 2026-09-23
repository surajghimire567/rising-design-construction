# Rising Design and Construction — Django starter

Production-oriented Django website starter for Rising Design and Construction. The starter is tailored to the supplied logo and flyer: navy/orange palette, the tagline “We design. We plan. We build. We deliver.”, and the contact details shown in the supplied artwork. Service records are seeded by a data migration; portfolio, testimonials, and team profiles are managed through Django admin.

## Important deployment reality

The code is designed for production settings, but **Render's free infrastructure is demo/staging, not reliable production hosting**: free web services sleep and have ephemeral filesystems; Render Free Postgres expires after 30 days and is eventually deleted; and free web services cannot make outbound SMTP connections on ports 25/465/587. Keep customer inquiries on a persistent database and use an HTTPS email API (the included Resend option) before taking real leads. For a true production site, use a paid persistent database/service or an external managed PostgreSQL provider, plus backups. The app's `DATABASE_URL` accepts any PostgreSQL URL.

## Stack and intentional choices

- Django 6.1.x (latest stable at project generation; supported on Python 3.12–3.14), PostgreSQL, Django templates, HTMX 2, WhiteNoise, `django-storages`/S3 API, Cloudflare R2.
- Function-based views are used for the small set of pages and the form: their explicit request/response flow is easier to learn and maintain than introducing generic class-based-view abstractions here.
- `Inquiry.project_type` is a foreign key to `Service`, not a hard-coded choice list. This keeps the dropdown current when an admin adds or deactivates a service.
- Service requests are private: the inquiry attachment uses a separate private R2 bucket and signed URLs; public portfolio images/reports use a public media bucket. Do not put confidential customer drawings in the public bucket.
- User text is rendered through Django's normal auto-escaping. Do not add `|safe` to database or form content.
- The Tailwind browser CDN is used only in `DEBUG` development mode. Tailwind explicitly describes Play CDN as development-only; production uses a compiled, minified local CSS file built by the pinned Tailwind CLI. This keeps the requested CDN workflow convenient without shipping the development runtime in production.

## Run locally

1. Install Python 3.13 (Django 6.1 supports 3.12–3.14) and Node.js 20+.
2. Copy `.env.example` to `.env`; set a long random `SECRET_KEY`. Local development defaults to SQLite for a quick first run; set `DATABASE_URL` to PostgreSQL when available. R2 is optional locally; files go to `media/` unless `USE_R2=True`.
3. Install/build:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   npm install
   npm run build:css
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. Visit `/`, `/services/`, `/projects/`, `/about/`, `/consultation/`, and `/admin/`. The initial migration adds the eight supplied service types.
5. In local `DEBUG=True`, Tailwind's browser CDN is loaded. The local build command is still useful to verify the production stylesheet.

## 1. Project map

```text
rising-design-construction/
├── assets/css/input.css             # Tailwind v4 source + brand tokens
├── config/                          # WSGI, URL config, split settings
│   └── settings/{base,development,production}.py
├── content/                         # Service, CaseStudy, Testimonial, TeamMember
│   └── migrations/                  # schema + initial service data
├── core/                            # public pages, context, shared validators/storage
├── inquiries/                       # private requests, validation, notification
├── templates/                       # base, pages, partial form
├── static/images/                   # supplied logo/flyer assets
├── .env.example
├── package.json
├── render.yaml
├── requirements.txt
└── Procfile
```

## 2. Data model and admin notes

`content/models.py` defines the public editorial content; `inquiries/models.py` stores consultation leads. Slugs are unique and stable URLs. Text is stored as plain text (not arbitrary HTML). A case study's service uses `PROTECT`, so an admin cannot accidentally delete a service still referenced by a published project. Inquiry service choices also use `PROTECT` to preserve lead history. Inquiry status is intentionally editable while the submitted contact/message fields are read-only in admin.

Image fields use `ImageField` so Django/Pillow verifies image content. Portfolio PDFs are public because they are explicitly part of the public case study; inquiry uploads are private. File validators check size, extension, and content signature. Client-provided MIME headers are not trusted.

## 3. Consultation form + HTMX

The form uses standard Django CSRF middleware and a hidden CSRF token. HTMX sends the normal form POST asynchronously; Django returns a same-page partial for success or validation errors. The response intentionally uses HTTP 200 for validation errors because HTMX does not swap most error responses by default. If JavaScript is disabled, the form has a normal POST/redirect-free success page fallback. The form's honeypot is a low-friction spam speed bump, not a replacement for rate limiting if the site is targeted.

Upload cap: 10 MiB per inquiry file (PDF, JPEG, PNG, or WebP). SVG and unsupported formats are rejected. The file is saved to the private storage alias only after form validation.

## 4. Settings and secrets

Settings are split into `base.py`, `development.py`, and `production.py`. Render selects `config.settings.production`; startup fails if `DEBUG=True`, a wildcard/empty host list is configured, the secret key is still the development placeholder, or R2 credentials are incomplete. `ALLOWED_HOSTS` contains hostnames only; `CSRF_TRUSTED_ORIGINS` contains full `https://` origins.

Never commit `.env`. Render environment variables are the production secret store. Generate a key with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## 5. Cloudflare R2 media storage

Create **two** R2 buckets:

1. `rising-public-media`: configure a public custom domain in Cloudflare for case-study cover images and intentionally-public PDFs. Put only approved public material here.
2. `rising-private-inquiries`: keep public access disabled; it stores client uploads. Private file URLs are short-lived signed URLs generated by `django-storages` for authenticated admin use.

Create an R2 API token with the minimum object read/write permissions for those buckets. Set account ID, access key ID, secret access key, bucket names, and the public custom-domain hostname in Render (or `.env` for local testing). The endpoint format is `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`; `region_name=auto` is used for R2's S3-compatible endpoint. Configure the custom domain in Cloudflare before setting `R2_PUBLIC_CUSTOM_DOMAIN`. Do not use the temporary `r2.dev` URL as a permanent production domain.

The public/private storage split is deliberate: making the whole media bucket public would expose drawings attached to incoming leads. The private bucket has no public domain; Django generates expiring signed URLs.

## 6. Email notifications

On a local development setup, the default email backend prints messages to the terminal. Standard SMTP variables are supported for local or paid hosting. **Render free web services block outbound SMTP ports 25, 465, and 587**, so a free Render demo should use the included HTTPS Resend API path: set `RESEND_API_KEY`, `DEFAULT_FROM_EMAIL` to a sender domain verified with Resend, and `INQUIRY_NOTIFY_EMAIL` to the recipient. If the API call fails, the inquiry remains saved, the visitor still sees confirmation, and the failure is logged for follow-up.

The `.env.example` uses `demo@example.com` as the requested demonstration recipient. It will not receive email; replace it with a real inbox and configure a verified sender before launch.

## 7. Render deployment

1. Commit this folder to a GitHub repository and connect it to Render as a Blueprint (`render.yaml`) or create a web service manually.
2. Use Python 3.13. `render.yaml` builds Tailwind CSS, installs Python dependencies, runs `collectstatic`, and applies database migrations. The start command launches Gunicorn on Render's `$PORT`.
3. Set `DATABASE_URL` to PostgreSQL. For a short demo, Render Free Postgres is possible but expires after 30 days; do not store the only copy of real inquiry data there. Use a persistent database and backups for a business launch.
4. Set `ALLOWED_HOSTS` to the exact Render hostname (and any custom hostname), and set matching full `CSRF_TRUSTED_ORIGINS` such as `https://your-service.onrender.com`.
5. Add the R2 credentials/buckets/custom domain, `INQUIRY_NOTIFY_EMAIL`, `RESEND_API_KEY`, and a verified `DEFAULT_FROM_EMAIL`. If using paid-host SMTP instead, set `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `EMAIL_USE_TLS`.
6. Deploy. Verify `/health/`, submit a test inquiry with a valid/invalid file, verify the email provider log, confirm the inquiry in `/admin/`, and confirm the private R2 object is not publicly accessible.

Exact commands (also in `render.yaml`):

```bash
# Build
npm install --no-audit --no-fund && npm run build:css
pip install -r requirements.txt
python manage.py collectstatic --noinput --settings=config.settings.production
python manage.py migrate --noinput --settings=config.settings.production

# Start
 gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 90
```

For local/one-off operations, set `DJANGO_SETTINGS_MODULE=config.settings.development`; use `python manage.py makemigrations` only when you intentionally change model fields, commit the resulting migration, and then deploy with `migrate`. Do not run `makemigrations` on Render as part of deployment.

## 8. Before accepting real inquiries

- Replace the demo notification recipient and verify the sender domain with an HTTPS email provider.
- Use a persistent PostgreSQL database with a backup/restore plan; Render's free database expires.
- Configure a custom domain, R2 public custom domain, and correct origins/hosts.
- Review legal/privacy notices for document uploads and retention; restrict admin accounts and enable strong authentication.
- Add rate limiting/abuse monitoring and a retention/deletion policy if this is exposed to the public.

## References

- Django downloads/releases: https://www.djangoproject.com/download/ and https://docs.djangoproject.com/en/6.1/releases/6.1/
- Render Django deployment: https://render.com/docs/deploy-django
- Render free plan limits: https://render.com/docs/free
- Cloudflare R2: https://developers.cloudflare.com/r2/ and https://django-storages.readthedocs.io/en/latest/backends/s3_compatible/cloudflare-r2.html
- Tailwind CDN: https://tailwindcss.com/docs/installation/play-cdn
