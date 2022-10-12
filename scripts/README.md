## Monta Scripts

This folder contains the scripts used to build Monta.

### build.sh

This script is used to build Monta from scratch.

### convert_to_avif.sh

This script is used to convert all the images in the `static` folder to the AVIF format.

### build_settings_file.sh

This script is used to build a settings.py file for Monta.

### create_cbv.sh

This script is used to generate a class-based view boilerplate.

### create_test.sh

This script is used to generate a django test boilerplate.

### process_static_files.sh

This script is used to process the static files. It runs the following scripts:

- `python manage.py compress --force` to compress the static files
- `python manage.py collectstatic --noinput` to collect the static files