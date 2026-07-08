# KAN-trstats

A Python CLI tool for collecting and analyzing **traceroute** latency statistics across multiple runs. It automates repeated traceroute executions toward a target host, aggregates per-hop round-trip times (RTTs), and exports summary statistics plus a box-plot visualization.

## What it does

1. **Run traceroute repeatedly** — Executes `traceroute` toward a domain or IP address a configurable number of times, with an optional delay between runs.
2. **Parse hop data** — Extracts hop number, hostname, and three RTT measurements per hop from each run.
3. **Compute statistics** — For each network hop, calculates **min**, **max**, **average**, and **median** latency across all runs.
4. **Export results** — Writes per-hop stats to a JSON file and generates a PDF box plot of latency distributions.

This is useful for observing route stability, identifying jittery hops, and comparing latency behavior over time without manually parsing traceroute output.

## Requirements

- Python 3
- System `traceroute` command (for live mode)
- Python packages (core dependencies):

  ```
  docopt
  pandas
  numpy
  plotly
  kaleido
  ```

Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** The bundled `requirements.txt` was generated from a full system environment. For a minimal install, the packages listed above are sufficient.

## Usage

### Live mode — run traceroute against a target

```bash
python trstats.py -t www.example.com -o results.json -g latency_graph
```

| Option | Description | Default |
|--------|-------------|---------|
| `-t TARGET` | Target domain name or IP address | *(required)* |
| `-n NUM_RUNS` | Number of traceroute runs | `8` |
| `-d RUN_DELAY` | Seconds to wait between runs | `0` |
| `-m MAX_HOPS` | Maximum hops per traceroute | `20` |
| `-o OUTPUT` | Output JSON file path | *(required)* |
| `-g GRAPH` | Output graph base name (`.pdf` appended) | *(required)* |

Example with custom run count and delay:

```bash
python trstats.py -t 8.8.8.8 -n 10 -d 2 -m 30 -o stats.json -g graph
```

### Test mode — analyze saved traceroute output

If you already have traceroute output files, pass a directory instead of running live traceroute:

```bash
python trstats.py --test test_files -o results.json -g latency_graph
```

The `test_files/` directory in this repo contains sample outputs (`tr_run-1.out` … `tr_run-5.out`) from traceroutes to `www.google.com` for testing without network access.

When `--test` is used, all other options are ignored and no traceroute commands are executed.

## Output

### JSON (`-o`)

Per-hop statistics in the following structure:

```json
{
  "data": [
    {
      "Hop": "1",
      "Host": "gateway.local (192.168.1.1)",
      "Min": 0.333,
      "Max": 0.346,
      "Avg": 0.339,
      "Med": 0.337
    }
  ]
}
```

### PDF graph (`-g`)

A box plot (via Plotly) showing the latency distribution at each hop across all runs. The file is saved as `<GRAPH>.pdf`.

## Project structure

```
KAN-trstats/
├── trstats.py          # Main CLI script
├── requirements.txt    # Python dependencies
├── test_files/         # Sample traceroute outputs for --test mode
└── README.md
```

## How it works

1. Each traceroute run is saved to a temporary text file (`text0.txt`, `text1.txt`, …).
2. Output is parsed with pandas: hop number, hostname, and three RTT values per line.
3. Data from all runs is combined into a matrix (hops × runs).
4. Summary stats are computed per hop and serialized to JSON.
5. A Plotly box plot is rendered and exported to PDF using Kaleido.

## License

No license file is included. Add one if you plan to distribute or open-source this project further.
