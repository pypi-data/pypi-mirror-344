# Пакет task_6_report

`task_6_report` — Python package for analyzing Formula 1 race results: loading logs, building reports, output via CLI.

---

## Installation

```bash
pip install task_6_report
```

---

## Using

```python
from race_report.report import RaceData
from pathlib import Path

folder = Path(r"C:\Users\dzirt\PycharmProjects\task_6_report\Data")
data = RaceData(folder)
data.load_data()
report = data.build_report(order='asc')
data.print_report(report)
```

### Required data files:
abbreviations.txt:
```
DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER
SVF_Sebastian Vettel_FERRARI
LHM_Lewis Hamilton_MERCEDES
```

start.log:
```
DRR2018-05-24_12:14:12.054
SVF2018-05-24_12:14:15.145
LHM2018-05-24_12:14:18.035
```

end.log:
```
DRR2018-05-24_12:15:26.399
SVF2018-05-24_12:15:29.750
LHM2018-05-24_12:15:33.082
```

### An example of a report:

```
1. DRR_Daniel Ricciardo | RED BULL RACING TAG HEUER | 1:14.345
2. SVF_Sebastian Vettel | FERRARI | 1:14.788
...
```

---

## Call in GitBash GitBash (CLI)

To run your report.py file with the --order option, use the following command:

```bash
python your folder path\report.py --order asc
```

Or in reverse order:

```bash
python your folder path\report.py --order desc
```

---

## The structure of the project

```
task_6_report/

src/
└── race_report/
    ├── __init__.py
    └── report.py

├── tests/
│   ├── __init__.py
│   ├── tests_load_data/
│   ├── tests_build_report/
│   ├── tests_print_report/
│   ├── tests_read_abbreviations/
│   ├── test_race_report(CLI)/


├── LICENSE
├── pyproject.toml
├── README.md
└── .gitignore
```

## License

This project is licensed under the MIT License.