from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import multiprocessing as mp

CSV_FILE_TO_ANALYZE = "../outputs/original/test.csv"
analyzer = SentimentIntensityAnalyzer()


def produce_sentiment(text):
    return analyzer.polarity_scores(text)


def run():
    df = pd.read_csv(CSV_FILE_TO_ANALYZE)

    p = mp.Pool(mp.cpu_count())
    sentimentColumns = p.map(produce_sentiment, df['bodyContent'])
    df = pd.concat([df, pd.DataFrame(sentimentColumns)], axis=1)

    df.to_csv(f"{CSV_FILE_TO_ANALYZE[:-4]}-sentiments.csv")


def main():
    run()


if __name__ == "__main__":
    main()
