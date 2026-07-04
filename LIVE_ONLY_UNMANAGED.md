# LIVE_ONLY_UNMANAGED.md

Files present on the live server (`business185:/public_html/`, chatgptdisaster.com docroot) but **intentionally NOT managed by this git repo**. Recorded so any future automated deploy/mirror **never deletes or overwrites them**. Generated 2026-07-04 (Phase A) from a read-only live FTP inventory (union of 3 walk passes: [477, 477, 477]).

Live files (union): 477. Live-only after Phase A import: 168. The 5 real CGD articles that were live-only are imported into the repo and NOT listed here.

**Rule:** Any `lftp mirror` MUST run WITHOUT `--delete`, or with an explicit exclude-list covering every path below, until each block is reviewed and approved by the site owner.

### Ownership / domain-verification / SSL — NEVER delete or overwrite  (4)
- `.well-known/pki-validation/0965D30A969034B13F16360338DF4BA0.txt`
- `google6f74b54ecd988601 (2).html`
- `google6f74b54ecd988601.html`
- `parking-page.shtml`

### Legacy betting project: consensus_library/ (not in CGD sitemap)  (57)
- `consensus_library/README_AUTO_UPDATE.md`
- `consensus_library/README_CONSISTENCY.md`
- `consensus_library/UPDATE_CONSENSUS.bat`
- `consensus_library/archive/2025-11-06/covers_contest_picks.csv`
- `consensus_library/archive/2025-11-06/covers_contest_picks_aggregated.csv`
- `consensus_library/archive/2025-11-06/covers_contest_picks_summary.txt`
- `consensus_library/archive/2025-11-06/sharp-consensus.html`
- `consensus_library/archive/2025-11-07/covers_contest_picks_aggregated.csv`
- `consensus_library/archive/2025-11-07/sharp-consensus.html`
- `consensus_library/archive/index.html`
- `consensus_library/consensus_js_data.txt`
- `consensus_library/covers-consensus.html`
- `consensus_library/covers_contest_picks.csv`
- `consensus_library/covers_contest_picks_aggregated.csv`
- `consensus_library/covers_contest_picks_aggregated_filtered.csv`
- `consensus_library/covers_contest_picks_summary.txt`
- `consensus_library/history/2025-11-06_23-44/covers_contest_picks.csv`
- `consensus_library/history/2025-11-06_23-44/covers_contest_picks_aggregated.csv`
- `consensus_library/history/2025-11-06_23-44/covers_contest_picks_summary.txt`
- `consensus_library/history/2025-11-06_23-44/sharp-consensus.html`
- `consensus_library/history/index.html`
- `consensus_library/live-sports-board.html`
- `consensus_library/picks_database.json`
- `consensus_library/sharp-consensus-2025-11-08.html`
- `consensus_library/sharp-consensus-2025-11-09.html`
- `consensus_library/sharp-consensus-2025-11-10.html`
- `consensus_library/sharp-consensus-2025-11-12.html`
- `consensus_library/sharp-consensus-2025-11-13.html`
- `consensus_library/sharp-consensus-2025-11-14.html`
- `consensus_library/sharp-consensus-2025-11-15.html`
- `consensus_library/sharp-consensus-2025-11-17.html`
- `consensus_library/sharp-consensus-2025-12-02.html`
- `consensus_library/sharp-consensus-2025-12-03.html`
- `consensus_library/sharp-consensus-2025-12-04.html`
- `consensus_library/sharp-consensus-2025-12-05.html`
- `consensus_library/sharp-consensus-2025-12-06.html`
- `consensus_library/sharp-consensus-2025-12-07.html`
- `consensus_library/sharp-consensus-2025-12-08.html`
- `consensus_library/sharp-consensus-2025-12-09.html`
- `consensus_library/sharp-consensus-2025-12-10.html`
- `consensus_library/sharp-consensus-2025-12-11.html`
- `consensus_library/sharp-consensus-2025-12-12.html`
- `consensus_library/sharp-consensus-2025-12-13.html`
- `consensus_library/sharp-consensus-2025-12-14.html`
- `consensus_library/sharp-consensus-2025-12-15.html`
- `consensus_library/sharp-consensus-2025-12-16.html`
- `consensus_library/sharp-consensus-BACKUP.html`
- `consensus_library/sharp-consensus-page2.html`
- `consensus_library/sharp-consensus-page3.html`
- `consensus_library/sharp-consensus-page4.html`
- `consensus_library/sharp-consensus-page5.html`
- `consensus_library/sharp-consensus-sportsbettingprime.html`
- `consensus_library/sharp-consensus-template.html`
- `consensus_library/sharp-consensus.html`
- `consensus_library/temp_consensus_data.json`
- `consensus_library/temp_data.json`
- `consensus_library/update_consensus_page.py`

### Legacy betting project: covers-consensus pages (Nov-Dec 2025)  (28)
- `covers-consensus-2025-11-20.html`
- `covers-consensus-2025-11-21.html`
- `covers-consensus-2025-11-22.html`
- `covers-consensus-2025-11-23.html`
- `covers-consensus-2025-11-24.html`
- `covers-consensus-2025-11-25.html`
- `covers-consensus-2025-11-26.html`
- `covers-consensus-2025-11-27.html`
- `covers-consensus-2025-11-28.html`
- `covers-consensus-2025-11-29.html`
- `covers-consensus-2025-12-01.html`
- `covers-consensus-2025-12-03.html`
- `covers-consensus-2025-12-04.html`
- `covers-consensus-2025-12-05.html`
- `covers-consensus-2025-12-06.html`
- `covers-consensus-2025-12-07.html`
- `covers-consensus-2025-12-08.html`
- `covers-consensus-2025-12-09.html`
- `covers-consensus-2025-12-10.html`
- `covers-consensus-2025-12-11.html`
- `covers-consensus-2025-12-12.html`
- `covers-consensus-2025-12-13.html`
- `covers-consensus-2025-12-14.html`
- `covers-consensus-2025-12-15.html`
- `covers-consensus-2025-12-16.html`
- `covers-consensus-nov20.html`
- `covers-consensus.html`
- `covers_contest_picks_aggregated.csv`

### Legacy betting project: sportsbettingprime  (3)
- `sportsbettingprime-covers-consensus-2025-12-01.html`
- `sportsbettingprime-covers-consensus-2025-12-02.html`
- `sportsbettingprime.html`

### Legacy betting project: sports oracle/hub/directive pages  (12)
- `college-basketball.html`
- `college-football.html`
- `handicapping-hub-calendar.html`
- `handicapping-hub.html`
- `mlb-prime-directives-page2.html`
- `mlb-prime-directives.html`
- `nba-court-vision.html`
- `nfl-gridiron-oracles.html`
- `nhl-ice-oracles.html`
- `performance-telemetry.html`
- `the-data-stream.html`
- `the-prime-protocol.html`

### Colocated other-site copy: mlbprops.com/ subtree  (10)
- `mlbprops.com/advanced-stats-mlb-props.html`
- `mlbprops.com/hitter-props-strategy.html`
- `mlbprops.com/how-sportsbooks-price-props.html`
- `mlbprops.com/index.html`
- `mlbprops.com/mlb-player-props-explained.html`
- `mlbprops.com/mlb-win-totals-2026.html`
- `mlbprops.com/other-mlb-props-of-interest-may-5-2026.html`
- `mlbprops.com/pitcher-props-strategy.html`
- `mlbprops.com/todays-picks.html`
- `mlbprops.com/variance-bankroll-management.html`

### Neocities-style asset bundle (may be referenced by legacy pages)  (45)
- `916.png`
- `black_gold_styles.css`
- `nc_assets/css/style.css`
- `nc_assets/fonts/museo-sans-300-italic-webfont.eot`
- `nc_assets/fonts/museo-sans-300-italic-webfont.svg`
- `nc_assets/fonts/museo-sans-300-italic-webfont.ttf`
- `nc_assets/fonts/museo-sans-300-italic-webfont.woff`
- `nc_assets/fonts/museo-sans-300-webfont.eot`
- `nc_assets/fonts/museo-sans-300-webfont.svg`
- `nc_assets/fonts/museo-sans-300-webfont.ttf`
- `nc_assets/fonts/museo-sans-300-webfont.woff`
- `nc_assets/fonts/museo-sans-500-italic-webfont.eot`
- `nc_assets/fonts/museo-sans-500-italic-webfont.svg`
- `nc_assets/fonts/museo-sans-500-italic-webfont.ttf`
- `nc_assets/fonts/museo-sans-500-italic-webfont.woff`
- `nc_assets/fonts/museo-sans-500-webfont.eot`
- `nc_assets/fonts/museo-sans-500-webfont.svg`
- `nc_assets/fonts/museo-sans-500-webfont.ttf`
- `nc_assets/fonts/museo-sans-500-webfont.woff`
- `nc_assets/fonts/museo-sans-700-italic-webfont.eot`
- `nc_assets/fonts/museo-sans-700-italic-webfont.svg`
- `nc_assets/fonts/museo-sans-700-italic-webfont.ttf`
- `nc_assets/fonts/museo-sans-700-italic-webfont.woff`
- `nc_assets/fonts/museo-sans-700-webfont.eot`
- `nc_assets/fonts/museo-sans-700-webfont.svg`
- `nc_assets/fonts/museo-sans-700-webfont.ttf`
- `nc_assets/fonts/museo-sans-700-webfont.woff`
- `nc_assets/img/featured/600/ready-to-go.png`
- `nc_assets/img/icons/checkmark-hd.png`
- `nc_assets/img/icons/icon-info-hd.png`
- `nc_assets/img/logos/namecheap-hd.png`
- `nc_assets/img/nc-icon/favicon.ico`
- `nc_assets/img/nc-icon/namecheap-icon-114x114.png`
- `nc_assets/img/nc-icon/namecheap-icon-120x120.png`
- `nc_assets/img/nc-icon/namecheap-icon-144x144.png`
- `nc_assets/img/nc-icon/namecheap-icon-152x152.png`
- `nc_assets/img/nc-icon/namecheap-icon-57x57.png`
- `nc_assets/img/nc-icon/namecheap-icon-72x72.png`
- `nc_assets/img/nc-icon/namecheap-icon-76x76.png`
- `nc_assets/img/pictograms/150/browser-red.png`
- `nc_assets/img/pictograms/150/email-red.png`
- `nc_assets/img/pictograms/150/news-red.png`
- `nc_assets/img/pictograms/150/server-red.png`
- `nc_assets/img/pictograms/150/support-red.png`
- `nc_assets/img/pictograms/150/tools-red.png`

### Legacy homepage variants  (1)
- `index-new.html`

### Redesign concept archive  (3)
- `_redesign-concepts-archive/CONCEPT-A-Editorial-Magazine.html`
- `_redesign-concepts-archive/CONCEPT-B-Vibrant-Tech.html`
- `_redesign-concepts-archive/CONCEPT-C-Bold-Colorful.html`

### Legacy scripts / protocol docs  (4)
- `DAILY_UPDATE.bat`
- `PROTOCOL_COVERS_CONSENSUS.md`
- `README.md`
- `SETUP_DAILY_TASK.bat`

### Other stray content pages  (1)
- `stories-page-2.html`
