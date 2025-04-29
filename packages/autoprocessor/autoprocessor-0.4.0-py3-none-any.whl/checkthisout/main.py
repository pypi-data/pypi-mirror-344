#ml 1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
#We do not want to see warnings
warnings.filterwarnings("ignore")

data = pd.read_csv("uber.csv")

df = data.copy()

df.head

df.info()

df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])

df.info()

df.describe()
df.isnull().sum()
df.drop(['key', 'Unnamed: 0'],axis = 1,inplace=True)
df2=df.drop(["pickup_datetime"],axis = 1)
df2
df2.corr()

fig,axis = plt.subplots(figsize = (10,6))
sns.heatmap(df2.corr(),annot = True)

df.dropna(inplace=True)
df.plot(kind = "box",subplots = True,layout = (7,2),figsize=(15,20)) #Boxplot shows that dataset is free from outliers


def remove_outlier(df1, col):
    Q1 = df1[col].quantile(0.25)
    Q3 = df1[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_whisker = Q1 - 1.5 * IQR
    upper_whisker = Q3 + 1.5 * IQR
    df[col] = np.clip(df1[col], lower_whisker, upper_whisker)
    return df1


def treat_outliers_all(df1, col_list):
    for c in col_list:
        df1 = remove_outlier(df, c)
    return df1


df = treat_outliers_all(df, df.iloc[:, 0::])

df.plot(kind="box", subplots=True, layout=(7, 2), figsize=(15, 20))  # Boxplot shows that dataset is free from outliers

#Check the missing values now
df.isnull().sum()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

datatime_column = df['pickup_datetime']
df.drop('pickup_datetime', axis=1, inplace=True)

# Scale the DataFrame without the datetime column
standard_scaler = StandardScaler()
df_scaled_array = standard_scaler.fit_transform(df)

# Convert the scaled array back to a DataFrame
df_scaled = pd.DataFrame(df_scaled_array, columns=df.columns)

# Add the pickup_datetime column back
df_scaled['pickup_datetime'] = datatime_column.reset_index(drop=True)

#Take x as predictor variable
x = df_scaled.drop("fare_amount", axis = 1)
#And y as target variable
y = df_scaled['fare_amount']

x['pickup_datetime'] = pd.to_numeric(pd.to_datetime(x['pickup_datetime']))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 1)

from sklearn.linear_model import LinearRegression

lrmodel = LinearRegression()
lrmodel.fit(x_train, y_train)

predict = lrmodel.predict(x_test)

from sklearn.metrics import mean_squared_error , r2_score
lrmodelrmse = np.sqrt(mean_squared_error(y_test,predict))
r2 = r2_score(y_test,predict)
print("RMSE error for the model is ", lrmodelrmse)
print("R2 score for the model is ", r2)

#Let's Apply Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor
rfrmodel = RandomForestRegressor(n_estimators = 100, random_state = 101)

#Fit the Forest
rfrmodel.fit(x_train, y_train)
rfrmodel_pred = rfrmodel.predict(x_test)

#Errors for the forest
rfrmodel_rmse = np.sqrt(mean_squared_error(y_test , rfrmodel_pred))
rf_r2 = r2_score(y_test,rfrmodel_pred)
print("RMSE value for Random Forest is:",rfrmodel_rmse)
print("R2 score for the model is ", rf_r2)



# code
#
#
# #include <iostream>
# #include <omp.h>
# #include <vector>
# #include <time.h>
#
# using namespace std;
#
# void bubbleSort(vector<int> &arr)
# {
#     int n = arr.size();
#     bool swapped = false;
#
#     while (swapped)
#     {
#         swapped = false;
# #pragma omp parallel for
#         for (int i = 0; i < n - 1; i++)
#         {
#             if (arr[i] > arr[i + 1])
#             {
#                 swap(arr[i], arr[i + 1]);
#                 swapped = true;
#             }
#         }
#     }
# }
#
# void merge(vector<int> &array, int left, int middle, int right)
# {
#     vector<int> merged;
#     int left_iter = left;
#     int right_iter = middle + 1;
#
#     while (left_iter <= left && right_iter <= right)
#     {
#         if (array[left_iter] < array[right_iter])
#         {
#             merged.push_back(array[left_iter]);
#             left_iter++;
#         }
#         else
#         {
#             merged.push_back(array[right_iter]);
#             right_iter++;
#         }
#     }
#
#     while (left_iter <= middle)
#     {
#         merged.push_back(array[left_iter]);
#         left_iter++;
#     }
#
#     while (right_iter <= right)
#     {
#         merged.push_back(array[right_iter]);
#         right_iter++;
#     }
#
#     for (int i = left; i <= right; i++)
#     {
#         array[i] = merged[i - left];
#     }
# }
#
# void mergeSort(vector<int> &arr, int left, int right)
# {
#     if (left < right)
#     {
#         int middle = left + (right - left) / 2;
# #pragma omp parallel sections
#         {
# #pragma omp section
#             mergeSort(arr, left, middle);
# #pragma omp section
#             mergeSort(arr, middle + 1, right);
#         }
#         merge(arr, left, middle, right);
#     }
# }
#
# int main()
# {
#     vector array = {14, 12, 8, 7, 10};
#     for (int i = 0; i < 5; i++)
#     {
#         cout << array[i] << ", ";
#     }
#     cout << "\n";
#     clock_t bubbleStart = clock();
#     bubbleSort(array);
#     clock_t bubbleEnd = clock();
#     clock_t mergeStart = clock();
#     mergeSort(array, 0, 4);
#     for (int i = 0; i < 5; i++)
#     {
#         cout << array[i] << ", ";
#     }
#     clock_t mergeEnd = clock();
#     cout << "\n";
#     for (int i = 0; i < 5; i++)
#     {
#         cout << array[i] << ", ";
#     }
#     double bubbleDuration = double(bubbleEnd - bubbleStart) / CLOCKS_PER_SEC;
#     cout << "Bubble sort time in seconds: " << bubbleDuration << endl;
#     double mergeDuration = double(mergeEnd - mergeStart) / CLOCKS_PER_SEC;
#     cout << "Merge sort time in seconds: " << mergeDuration << endl;
#     return 0;
# }
#
#
#
#
#
#
# code
# #include <iostream>
# #include <omp.h>
# #include <vector>
# #include <queue>
#
# using namespace std;
#
# class Graph
# {
# private:
#     int V;
#     vector<vector<int>> adjancentNodes;
#
# public:
#     Graph(int V)
#     {
#         this->V = V;
#         adjancentNodes.resize(V);
#     }
#
#     void addEdge(int source, int destination)
#     {
#         this->adjancentNodes[source].push_back(destination);
#         this->adjancentNodes[destination].push_back(source);
#     }
#
#     void bfs(int node)
#     {
#         vector<bool> visited(V, false);
#         queue<int> q;
#         visited[node] = true;
#         q.push(node);
#
#         while (!q.empty())
#         {
#             int new_node = q.front();
#             q.pop();
#             cout << new_node << " ";
#
#             #pragma omp parallel for
#             for (int i = 0; i < adjancentNodes[node].size(); i++)
#             {
#                 int v = adjancentNodes[new_node][i];
#                 if (!visited[v])
#                 {
#                     visited[v] = true;
#                     q.push(v);
#                 }
#             }
#         }
#         cout << endl;
#     }
#
#     void dfs(int node, vector<bool> &visited)
#     {
#         visited[node] = true;
#         cout << node << " ";
#
#         #pragma omp parallel for
#         for (int i = 0; i < adjancentNodes[node].size(); i++)
#         {
#             int next_node = adjancentNodes[node][i];
#             if (!visited[next_node])
#             {
#                 dfs(next_node, visited);
#             }
#         }
#     }
# };
#
# int main()
# {
#     int numNodes = 6; // Number of nodes in the graph
#     Graph graph(numNodes);
#     vector<bool> visited(numNodes, false);
#
#     // Adding edges to the graph
#     graph.addEdge(0, 1);
#     graph.addEdge(0, 2);
#     graph.addEdge(1, 3);
#     graph.addEdge(1, 4);
#     graph.addEdge(2, 4);
#     graph.addEdge(3, 5);
#     graph.addEdge(4, 5);
#
#     cout << "BFS starting from node 0: ";
#     graph.bfs(0);
#     cout << endl;
#
#     cout << "DFS starting from node 0: ";
#     graph.dfs(0, visited);
#     cout << endl;
#
#     return 0;
# }
#
#
#
#
#
# code
#
# #include <iostream>
# #include <vector>
# #include <omp.h>
#
# using namespace std;
#
# int parallelMin(vector<int> arr) {
#     int min_val = arr[0];
#
#     #pragma omp parallel for
#     for (int i = 1; i < arr.size(); i++) {
#         if (arr[i] < min_val) {
#             min_val = arr[i];
#         }
#     }
#     return min_val;
# }
#
# int parallelMax(vector<int> arr) {
#     int max_val = arr[0];
#
#     #pragma omp parallel for
#     for (int i = 1; i < arr.size(); i++) {
#         if (arr[i] > max_val) {
#             max_val = arr[i];
#         }
#     }
#     return max_val;
# }
#
# int parallelSum(vector<int> arr) {
#     int sum = 0;
#     #pragma omp parallel for
#     for (int i = 0; i < arr.size(); i++) {
#         sum += arr[i];
#     }
#     return sum;
# }
#
# float parallelAverage(vector<int> arr) {
#     int sum = parallelSum(arr);
#     float avg = float(sum) / arr.size();
#     return avg;
# }
#
# int main() {
#     int n;
#     cout << "Enter the number of elements: ";
#     cin >> n;
#
#     vector<int> arr(n);
#     cout << "Enter the elements: ";
#     for (int i = 0; i < n; ++i) {
#         cin >> arr[i];
#     }
#
#     int min_val = parallelMin(arr);
#     int max_val = parallelMax(arr);
#     int sum = parallelSum(arr);
#     float avg = parallelAverage(arr);
#
#     cout << "Minimum value: " << min_val << endl;
#     cout << "Maximum value: " << max_val << endl;
#     cout << "Sum of values: " << sum << endl;
#     cout << "Average of values: " << avg << endl;
#
#     return 0;
# }