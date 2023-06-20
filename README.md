# PixelsJournal Data Processing
 Processes data exported from [Teo Vogel's "Pixels Journal" app](https://teovogel.me/pixels/) to find correlation information and more advanced statistics. 

---

## The Goal-
To parse a json file exported from the _Pixels Journal_ app and use Pandas to process the data  
I am hoping to implement the following features:
- [ ] 1-variable statistics on the score attribute
- [ ] Basic 2-variable stats on the score against the date
- [ ] Configurable linear and quadratic interpolation of the score between available data points
- [ ] Graphing of score over time
- [ ] Graphing of categorical variables (tags) and average scores
- [ ] Rolling average smoothing of score
- [ ] Correlation analysis of categorical variables (tags) against each other and against the score / first and second derivative of the score

Ideally, parameterization will occur through a configuration file that will be passed in with the json file.