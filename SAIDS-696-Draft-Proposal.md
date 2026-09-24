# Impacts of Data Centers on Electrical Utilities

**Team Members:** Cody Bauer, Matthew Chess, Lidiya Shutaya

### Background

There is growing concern about the rise of data centers in communities across the United States. Their impact on utility systems such as water and electricity has increased anxiety among local residents. Electricity provides a particularly interesting case study because the exact amount used by data centers is still up for debate. Existing datasets, like FracTracker (FracTracker Alliance, 2026), generally categorize sites on a logarithmic scale producing wide intervals and high variance when used as a direct input for predicting energy grid impact or a single new data center. Lawrence Berkeley National Laboratory's 2024 United States Data Center Energy Usage Report (Shehabi et al., 2024\) estimates the amount of energy consumed, but with some notable caveats. Its methodology estimates consumption largely from the estimated number of servers installed, and it excludes cryptocurrency mining from its main estimate.

As artificial intelligence has increased demand for compute and the price of cryptocurrency has fluctuated, some crypto-mining facilities are turning to AI for profitability (Tidy, 2026). We began by asking whether data centers are increasing regional electricity demand. Texas provides a unique case study: it has the second-most tracked data centers of any state, after Virginia, and its grid, ERCOT (Electric Reliability Council of Texas, Inc.), serves about 90% of the state's electricity load while operating separately from the rest of the U.S. grid. Out of 214 data centers in Texas, 22 are denoted as hyper or mega scale (100MW+) and are currently operating along the Austin \- Dallas Fort Worth corridor powered exclusively by the South region of the Texas power grid. Improving on the Lawrence Berkeley usage report that evaluates usage based solely on plant size/number of servers, we will incorporate historical utility generation and consumption within a known region to predict a link between data center start up and operational purpose with its associated toll on the electrical grid. 

### Project Datasets

| Dataset | Size | Purpose | Link |
| :---- | :---- | :---- | :---- |
| FracTracker U.S. Data Centers | 1,670 facilities, 53 fields (location, status, MW, acres, sq ft, operator, free text) | Primary list of data centers | [Link](https://fractracker.org/data-centers/%20) |
| FracTracker Alliance Cryptocurrency Mining Operations | 302 Data Centers | FracTracker's separate crypto-mining tracker | [Link](https://docs.google.com/spreadsheets/d/e/2PACX-1vRIG7TvcdFYbBnqUl2--Y7qPwl-9AixBXPPKeMrnr0X_1SnPLGxhJx6PAZZ5Ppi02u_4vNMsdazES3p/pub) |
| EIA-860 Plant and Generator Data | 3090 unique power plants | Electric supply data for the US’s power plants of at least 50MW, Operating Year, Energy Source, Sector Type, Node Location | [Link](https://www.eia.gov/electricity/data/eia860/%20) |
| EIA-930 Demand and Generation Data | 4094 days, 21 fields (source, demand, forecast, interchange, emissions) | Daily Demand since July 1, 2015 across Texas regions and Breakdown of Energy Source | [Link](https://www.eia.gov/electricity/data/eia930/) (requires API or FTP for download) |
| EIA-826, EIA-861 Retail Sales of Electricity Monthly | 6 sectors, 295 fields (last 25 years)  | MillionKWH sold to ultimate customers by sector | [Link](https://tinyurl.com/5h8db5px) |

### Part A: Supervised Learning

FracTracker has an incomplete listing of crypto-centric data centers from 2022\. It includes labels for the data that we will use to try and train a model to generalize on the full, more current list of data centers. 

The goal of this classification task is to identify crypto mining facilities not explicitly labeled by the FracTrack datasets to uncover how well facility and location attributes distinguish mining from non-mining facilities. These insights will help us understand the key differences between crypto and AI centric data centers, potentially uncovering their relationship with electricity demand. The result will allow us to investigate whether regions with greater concentrations of crypto mining operations exhibit different electricity demand than those with greater concentrations of AI data centers.

| Dataset | Count |
| :---- | :---- |
| FracTracker U.S. Data Centers | 1670 |
| Crypto Mining Tracker | 302 |

FracTracker: Property Size (acres), Facility Size (square feet), Capacity, Status, Size Rank, State, Purpose, MW, Cooling Source, and Project Cost are all potential attributes for classification

EIA-930: Demand, Generation,  Fuel Type (gas, coal, wind, solar) for the grid region each facility sits in can be additional attributes for the classification task.

A limited number of crypto mining centers could create a class imbalance between the classification examples, limiting the model’s ability to generalize to new unseen data. Therefore, during the data preparation phase, we will join the datasets to get a more comprehensive list of known crypto and non-crypto data centers for our analysis, filling in any missing data fields. The data center database is updated weekly while the cryptomining tracker is from 2022\. As a result, we will need our preparation script to prioritize which dataset value to accept. During the exploratory data analysis (EDA) stage, we will include location, capacity, size and energy demand distributions for further investigation of the data center features.

After this EDA stage, a decision will be made on which categorical features require one hot encoding. The plan would be to shoot for logistic regression as it gives us an interpretable equation that is easy to explain. During the data splitting phase, our team will consider grouping by geographic or company specific features to ensure predictions are not overestimated. After validating between our test and train split we will make a final decision. GridSearchCV will be performed to evaluate the best model between logistic regression and random forest. Learning curve analysis will be performed before and after modeling to first determine sufficient sample size and then understand potential drivers if model scores across the board show over/underfitting.

### Part B: Unsupervised Learning

For our unsupervised learning task, we will combine attributes from the FracTracker U.S. Data Centers with the EIA-860 plant and generator data in order to create a comprehensive list of features associated with each data center. We will join the two datasets using location data, assigning energy generation and demand information to centers using a pre-defined power plant spatial proximity rule (e.g. 10 mile radius) or using additional energy production information (e.g. fuel type). To handle situations where centers are both in close proximity and of the same type we may need to average the statistics before adding these fields to the dataset.

The goal of this unsupervised learning task is to determine whether distinct archetypes of data centers emerge naturally without providing any information related to the type or use of the data center. This will help us investigate the individual types of data centers that exist and the attributes that differentiate them. 

Throughout our data preparation phase, we will need to clean the FracTracker dataset, imputing missing values from existing data and hiding any predefined labels to ensure the clusters formed are based solely on infrastructural characteristics. Using the plant data from EIA-860, we may also choose to engineer additional features to benefit our analysis.  Because the plant and generator data are broken into multiple files, we will need to merge them together to generate our final comprehensive dataset.

We will implement and compare unsupervised clustering approaches such as K-means or Gaussian Mixture Models to determine if meaningful groups form from the data provided. To evaluate the models, we can use existing labels or compare the within-group variance with the between-group variance. We will also use other methods of evaluation such as silhouette score or Davies-Bouldin index for further investigation of performance. For visualizations, we’ll use PCA to reduce the dimensionality of our data and make it more interpretable when plotting. This will allow us to visualize whether distinct archetypes exist and how clearly those groups are separated.

### Work plan

The project will be broken down into multiple phases including data cleaning and preparation, model development, model evaluation, and explanation of results. For each stage of the project, we will divide the tasks among group members to ensure equal contribution. Team members will collaborate on key decisions such as feature selection, model choice, and evaluation methods. We will communicate and review each other's findings to ensure they are well supported and consistently presented in the final report.

| Date | Task | Lead | Support |
| ----- | ----- | ----- | ----- |
| Sep 14 | Draft proposal | Full Team |  |
| Sep 21 | Revised proposal | Full Team |  |
| Sep 24 | Stand up environment \- Deepnote | Lidiya Shutaya |  |
| Sep 28 | Final Datasets for Model \- Clean and combine FracTracker Datasets Clean and combine EIA Datasets. Check geographical spread and align datasets by county | Matthew Chess | Cody Bauer |
| Sep 29 | Assign / engineer additional attributes based on power plant proximity and energy type. Impute missing features based on available data to form a final comprehensive dataset. | Cody Bauer | Lidiya Shutaya |
| Oct 1 | Evaluate supervised learning datasets and provide breakdown of features, whether or not the sample size is enough to train/test a classification model effectively. Split data into train/test/validate bins with a % of each state’s counties as hold outs. | Matthew Chess | Cody Bauer |
| Oct 5 | **First Slack stand-up** |  |  |
| Oct 9 | Complete GridSearchCV and start evaluating different model performance | Lidiya Shutaya | Cody Bauer |
| Oct 12 | Evaluate unsupervised models using Silhouette Score / Davies-Bouldin Index. | Cody Bauer | Matthew Chess |
| Oct 16 | Finalize supervised model. Complete feature importance and ablation analysis and sensitivity analysis. | Lidiya Shutaya | Matthew Chess |
| Oct 17 | Finalize unsupervised model. Identify any discovered data center archetypes. | Cody Bauer | Lidiya Shutaya |
| Oct 19 | **Second Slack stand-up** |  |  |
| Oct 19 | Assign each section according to the lead and supporting roles for equal responsibility (background, feature engineering, supervised, unsupervised, discussion, ethical considerations) | Full Team, to be broken down closer to the due date. |  |
| Oct 21 | Complete failure analysis | Matthew Chess | Lidiya Shutaya |
| Oct 26 | **Final Project & Written Report Due** |  |  |

### Work Cited

Tidy, J. (2026, August 25). AI gold rush draws crypto firms away from Bitcoin. BBC News. [https://www.bbc.com/news/articles/c07ler8x9kpo](https://www.bbc.com/news/articles/c07ler8x9kpo) 

Shehabi, A., Smith, S. J., Hubbard, A., Newkirk, A., Lei, N., Siddik, M. A. B., Holecek, B., Koomey, J., Masanet, E., & Sartor, D. (2024). 2024 United States data center energy usage report (Report No. LBNL-2001637). Lawrence Berkeley National Laboratory. [https://escholarship.org/uc/item/32d6m0d1](https://escholarship.org/uc/item/32d6m0d1) 