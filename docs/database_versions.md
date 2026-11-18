# Database version history

The earlier versions below are reconstructed from the existing Git history. DB v6
is the first version also recorded in `database/VERSION`.

## DB v1

- Integrated public university data and simulated student data into one SQLite database.

## DB v2

- Replaced simulated course offerings with actual course offerings.

## DB v3

- Expanded syllabi, textbooks, weekly plans, and prerequisite data.

## DB v4

- Added official general-education graduation requirements.

## DB v5

- Enriched professor email and office information and rebuilt the database.

## DB v6 — 2026.11.13

- Added the official 2020-2021 Computer Science and Software Convergence curricula.
- Preserved existing common graduation-requirement IDs 1-15.
- Added 2020-2021 common requirement IDs 16-19.
- Added official AI track rows for the 2022-2024 research and industry tracks.
- Added official Software Convergence track rows for the 2020-2026 cohorts.
- Reflected the 2023 track-name change from `미래자동차·로봇트랙` to `로봇·비전트랙`.
- Kept the existing simulated students and their `공통` track unchanged.
- Rebuilt the SQLite database and verified foreign keys and integrity.

The current version string is stored in `database/VERSION`. Future database
updates should add a new entry here instead of rewriting this history.
