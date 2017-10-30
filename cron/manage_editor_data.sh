#!/usr/bin/env bash
source `which virtualenvwrapper.sh`
workon iwwa
cd /home/nuser/wikiwho_api/cron
# create last month's editor data
last_ym="$(date -u +"%Y-%m" --date="$(date +%Y-%m-15) last month")"
logs_folder='/home/nuser/dumps/xmls_7z/editor_data_logs_'
logs_folder=$logs_folder$last_ym
current_ym=$(date -u +%Y-%m)
python ../manage.py fill_editor_tables -from last_ym -to current_ym -m 12 -log logs_folder -lang 'en,de,eu'
echo 'fill_editor_tables is finished, starting manage_editor_tables'
python ../manage.py manage_editor_tables -from last_ym -to current_ym -m 12 -log logs_folder -lang 'en,de,eu'
echo 'manage_editor_tables is finished, starting empty_editor_tables'
python ../manage.py empty_editor_tables -m 12 -log logs_folder -lang 'en,de,eu'
echo 'empty_editor_tables is finished'
echo 'Editor data scripts are finished!'