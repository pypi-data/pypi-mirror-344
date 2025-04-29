# Jikan (時間) - Minimalist Time Tracker for the CLI

**Jikan** (時間, “time” in Japanese) is a sleek and powerful CLI-based time tracker designed for developers, freelancers, and anyone who wants to monitor their time efficiently — without distractions.

## ✨ Features

- ⏱️ Start/stop timers with custom names  
- 📋 View recorded timers per day  
- 🗓️ Generate reports by day, week, month, or year  
- 📁 Export reports as JSON, CSV, or TXT  
- 🏷️ Tag timers with predefined categories (e.g., `work`, `break`, `exercise`)  
- 🎯 Autocompletion for tags in CLI  
- 📊 View rounded durations (nearest 5min)  
- 📦 Store reports in customizable output paths  
- 🔄 Flush and seed the database easily  

## 🚀 Installation

```bash
git clone https://gitlab.com/amoriceau/jikan.git
cd jikan
./install.sh
source .venv/bin/activate
```

## 🧠 Usage

### Start/stop a timer

```bash
jikan start "Feature implementation" -t work dev
jikan stop
```

> You can also start a timer if there's already one running timer, this will ask if you want to stop the currently active timer first.

### View today's records

```bash
jikan records
```

Or a specific day:

```bash
jikan records --date 31/03/2025
```

Filter by tag:

```bash
jikan records --tag work
```

### Generate a report

```bash
jikan report day --sdate 2025-04-01 --json
jikan report week --sdate 2025-04-01 --csv
jikan report month --sdate 2025-04-01 --txt
```

Specify output folder and filename:

```bash
jikan report week --output report.csv --output-path ~/myreports/
```

### Tag management

```bash
jikan tags list
jikan tags add 3 work
jikan tags remove 3 break
```

### Dev tools

```bash
jikan update --flush      # Flush and recreate DB
jikan update --seed      # Seed the database (Dev only)
```

## 🏷️ Tags

Tags are predefined categories (e.g., `work`, `exercise`, `learning`) with associated background colors. Tags can be referenced by ID, label, or `#label`.

Example:

```bash
jikan start "Weekly sync" -t #meeting break
```

## 💾 Data Storage

- All data is stored in `~/.jikan/`
- SQLite is used under the hood
- Reports are saved by default in `~/.jikan/reports`

## 🛠️ Tech Stack

- Python 3.11+
- SQLite3
- Rich (for beautiful CLI UI)
- Click + rich-click

## 🌱 Development & Contribution

Contributions are welcome! Fork the project and submit a merge request on GitLab:  
👉 https://gitlab.com/amoriceau/jikan

## 📄 License

MIT License.
