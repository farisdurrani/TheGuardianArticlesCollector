from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import multiprocessing as mp

CSV_FILES = [
    "sample_output.csv",
]
ORIGINAL_SAMPLES_DIR = "../outputs/"
SENTIMENTS_DIR = "../outputs/"
TARGET_COLUMN = "bodyContent"
analyzer = SentimentIntensityAnalyzer()
count = [0]


def produce_sentiment(text):
    print(f"Processing row {count[0]}")
    count[0] += 1
    return analyzer.polarity_scores(text)


def analyze_one_file(filename):
    df = pd.read_csv(ORIGINAL_SAMPLES_DIR + filename)

    p = mp.Pool(mp.cpu_count())
    sentimentColumns = p.map(produce_sentiment, df[TARGET_COLUMN])
    df = pd.concat([df, pd.DataFrame(sentimentColumns)], axis=1)

    df.to_csv(f"{SENTIMENTS_DIR}{filename[:-4]}-sentiments.csv")

def run():
    for filename in CSV_FILES:
        print(f"STARTING: {filename}\n")
        analyze_one_file(filename)
        print(f"DONE: {filename}\n")


def main():
    run()


if __name__ == "__main__":
    main()
