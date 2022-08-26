# BiasInRecommendation
In this repository, we are working on studying propagation of bias towards author groups in a book recommendation setting.

We are applying our research methods to the Book-Crossing dataset, as processed in our repository <a href =https://github.com/SavvinaDaniil/EnrichBookCrossing> EnrichBookCrossing</a>. 

Our overall goal is to evaluate hidden bias towards author characteristics that comes as a direct result of popularity bias. In this work, we are looking into author country of citizenship. We find that popularity is not independent to author country of citizenship. Specifically, American-authored books tend to be more popular in the data. We also find that certain algorithms on average recommend more American-authored books compared to the users' profile. Finally, we find that these are the same algorithms that propagate popularity bias according to previous work by <a href = https://www.researchgate.net/publication/358895745_The_Unfairness_of_Popularity_Bias_in_Book_Recommendation> Naghiaei et al</a>.

## Order
1. Book data analysis
2. Book Recommendation (on Colab)
3. Book results analysis

Certain code segments taken from <a href = "https://github.com/rahmanidashti/FairBook"> Fairbook </a>.
