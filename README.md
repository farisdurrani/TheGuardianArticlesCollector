# [The Guardian](https://www.theguardian.com) News Article Collector
Collecting web articles from The Guardian using [The Guardian Open Platform API](https://open-platform.theguardian.com/access/) exporting into a CSV file

> Author: Faris Durrani

## How to Use
Prerequisites:
1. Use Python 3.10
2. Install requirements in `requirements.txt`

Running:
1. Get API key from [The Guardian Open Platform API](https://open-platform.theguardian.com/access/), putting the API key in a new `.env` file in the root directory as follows:
    ```
    API_KEY="00c0eb00-c0fe-4c1e-a312-000000"
    ```
2. Run `python main.py`
3. See the results in new CSV files written to the `outputs/` directory

# License

The Guardian News Article Collector is MIT licensed, as found in the [LICENSE](./LICENSE) file.

The Guardian News Article Collector documentation is Creative Commons licensed, as found in the [LICENSE-docs](./.github/LICENSE-docs) file.
