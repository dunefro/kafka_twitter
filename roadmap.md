# ROADMAP

```
Phase Alpha 1 -> Collecting tweets and producing them to kafka based on some keywords (Completed)
            1.0.1 -> Add acks, retries and callback for producer (Completed)
            1.0.2 -> Added logging and flush mechnaism on termination (Completed)
Phase Alpha 2.0.0 -> Consuming the tweet details and putting them in elasticsearch.
                A) Tweet or retweet
                B) Query Keyword as index name
                C) Actual Tweet 
                D) Tweet id as the id of data in elasticsearch
                E) Offsets and Partitions value
            2.0.1 (Optional) -> Using Elasticsearch Sink connect
            2.0.2 -> Adding header list along with the tweets. Header list include
                A) For tweets ->  Tweet ID, Hashtags, tweet timestamp
                B) For Retweets -> Tweet ID, Retweet ID, Hashtags, retweet hashtags tweet timestamp , retweet timestamp
            2.0.3 -> Change Elastisearch data to be passed to header list
Phase Beta 1 -> Creating Flask API 
Phase Alpha 2.1 -> Using Twitter Stream API to stream the tweets continously http://docs.tweepy.org/en/latest/streaming_how_to.html
            A) Using Apache Spark
Phase Stable 1 -> Training some models based on twitter feed
```

