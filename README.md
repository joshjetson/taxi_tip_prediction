# ![Taxi Tip Prediction Model](https://i.imgur.com/maWyDKI.jpeg)
<table>
<tr>
<td>
This is a predictive model that can predict, with a high measure of accuracy, what a given tip might be based on real data from previous taxi trips.
</td>
</tr>
</table>


## Data
## [Data](https://www.kaggle.com/datasets/microize/newyork-yellow-taxi-trip-data-2020-2019?select=yellow_tripdata_2019-06.csv)
The data in this model is sourced from real taxi rides and is provided by the yellow cab company via kaggle.


## Main Concept
Based on independent variables such as:
- Driver ID
- Total trip cost
- Pick up location
- Drop off location
- Payment type
- Pickup time
- Drop off time

Can we determine what a new rider might tip for a taxi ride?

## Use cases
This code can be used to apply these same methods on another similar data set in an aim to predict what a specific value might be based on a number of different independent variables.


## [Usage](https://colab.research.google.com/) 
- Anyone could use google Colaboratory to use this code and modify it to their data needs.
### Development
Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b improve-feature`)
- Make the appropriate changes in the files
- Add changes to reflect the changes made
- Commit your changes (`git commit -am 'Improve feature'`)
- Push to the branch (`git push origin improve-feature`)
- Create a Pull Request 

### Bug / Feature Request

If you find a bug in this code please let me know.

## Built with 

- [Scikit-Learn](https://scikit-learn.org/) - For their models and tools
- [Python](https://www.python.org/) - For its flexibility and abundant amount of resources
- [Numpy](https://numpy.org/) - For computation
- [Pandas](https://pandas.pydata.org/) - For organization, processing and data visualization
- [Matplotlib](https://matplotlib.org/) - For data visualization
- [Snapml](https://www.zurich.ibm.com/snapml/) For their decision tree model regressor


## To-do
- Build an accompanying gui or webapp as to make this an actual application anyone can use.
- Create more data visualizations



