from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import multiprocessing as mp

CSV_FILE_TO_ANALYZE = "g-month3-page625final-2184.csv"
ORIGINAL_SAMPLES_DIR = "../outputs/original/"
SENTIMENTS_DIR = "../outputs/sentiments/"
analyzer = SentimentIntensityAnalyzer()
ee = [0]


def produce_sentiment(text):
    print(ee)
    ee[0] += 1
    return analyzer.polarity_scores(text)


def run():
    df = pd.read_csv(ORIGINAL_SAMPLES_DIR + CSV_FILE_TO_ANALYZE)

    p = mp.Pool(mp.cpu_count() * 3 // 4)
    sentimentColumns = p.map(produce_sentiment, df['bodyContent'])
    df = pd.concat([df, pd.DataFrame(sentimentColumns)], axis=1)

    df.to_csv(f"{SENTIMENTS_DIR}{CSV_FILE_TO_ANALYZE[:-4]}-sentiments.csv")


def main():
    run()


if __name__ == "__main__":
    main()
