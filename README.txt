Church Calendar - automatic updates, no Google API key

Files to upload to the root of your GitHub repository:
- index.html (replace the current index.html)
- calendar-thumbnail.png
- scripts/update_calendars.py
- .github/workflows/update-calendars.yml

The workflow downloads PUBLIC iCalendar feeds directly on GitHub Actions (not in the browser), writes snapshots into data/*.ics, and commits them. It runs every 6 hours and can also be run manually from GitHub > Actions > Update public calendar snapshots > Run workflow.

Important:
- The six Google calendars must be publicly accessible as iCalendar feeds. If they are not public, this no-API-key method cannot read them.
- After uploading these files, open GitHub > Actions and check the workflow run logs. It reports which feeds were downloaded and which were inaccessible.
- GitHub Pages may take a short time to publish new files after the workflow commits them.
- The local index.html uses the published snapshot files from https://tawuhac-oss.github.io/church-calendar/data/ when opened as file://. It therefore needs an internet connection and the snapshot files must already exist on GitHub Pages.
- This package contains no Google API key.
