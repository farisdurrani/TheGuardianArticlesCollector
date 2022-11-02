from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

CSV_FILE_TO_ANALYZE = "../outputs/test.csv"


def run():
    print(1)
    df = pd.read_csv(CSV_FILE_TO_ANALYZE)
    analyzer = SentimentIntensityAnalyzer()
    sentimentColumns = []

    for i, bodyContent in enumerate(df["bodyContent"]):
        if i % 100 == 0:
            print(f"Analyzing article {i} / {len(df['bodyContent'])}")
        vs = analyzer.polarity_scores(bodyContent)
        sentimentColumns.append(vs)

    df = pd.concat([df, pd.DataFrame(sentimentColumns)], axis=1)

    df.to_csv(f"{CSV_FILE_TO_ANALYZE[:-4]}-sentiments.csv")


def main():
    run()


if __name__ == "__main__":
    main()
