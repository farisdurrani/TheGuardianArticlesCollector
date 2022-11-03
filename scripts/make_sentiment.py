from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import multiprocessing as mp

CSV_FILES = [
    "g-month10-page429final-9655.csv",
    "g-month11-page433final-8842.csv"
]
ORIGINAL_SAMPLES_DIR = "../outputs/original/"
SENTIMENTS_DIR = "../outputs/sentiments/"
analyzer = SentimentIntensityAnalyzer()
ee = [0]


def produce_sentiment(text):
    print(ee)
    ee[0] += 1
    return analyzer.polarity_scores(text)


def analyze_one_file(filename):
    df = pd.read_csv(ORIGINAL_SAMPLES_DIR + filename)

    p = mp.Pool(mp.cpu_count())
    sentimentColumns = p.map(produce_sentiment, df['bodyContent'])
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
