import json

examples = []

def add(user, silicat):
    examples.append({"messages": [
        {"role": "user", "content": user},
        {"role": "silicat", "content": silicat},
    ]})

def add_multi(turns):
    msgs = []
    for role, content in turns:
        msgs.append({"role": role, "content": content})
    examples.append({"messages": msgs})


# ---------------------------------------------------------------------------
# NUMPY: creation
# ---------------------------------------------------------------------------
add("How do I create a numpy array from a Python list?",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3, 4, 5])\nprint(arr)\n```")

add("Create a numpy array of zeros with shape (3, 4).",
    "```python\nimport numpy as np\n\narr = np.zeros((3, 4))\nprint(arr)\n```")

add("Make an array of ones of length 10.",
    "```python\nimport numpy as np\n\narr = np.ones(10)\nprint(arr)\n```")

add("How can I create a 3x3 identity matrix in numpy?",
    "```python\nimport numpy as np\n\nI = np.eye(3)\nprint(I)\n```")

add("Generate numbers from 0 to 9 with numpy.",
    "`np.arange` gives evenly spaced integers in a half-open range.\n\n```python\nimport numpy as np\n\narr = np.arange(10)\nprint(arr)\n```")

add("Create an array from 0 to 20 stepping by 5.",
    "```python\nimport numpy as np\n\narr = np.arange(0, 21, 5)\nprint(arr)  # [ 0  5 10 15 20]\n```")

add("I need 50 evenly spaced points between 0 and 1.",
    "Use `np.linspace`, which includes both endpoints by default.\n\n```python\nimport numpy as np\n\narr = np.linspace(0, 1, 50)\nprint(arr)\n```")

add("Make a numpy array filled with the value 7, shape (2, 3).",
    "```python\nimport numpy as np\n\narr = np.full((2, 3), 7)\nprint(arr)\n```")

add("How do I create an empty/uninitialized numpy array?",
    "```python\nimport numpy as np\n\narr = np.empty((3, 3))\nprint(arr)  # values are arbitrary until you assign them\n```")

add("Create a numpy array of 5 random floats between 0 and 1.",
    "```python\nimport numpy as np\n\narr = np.random.rand(5)\nprint(arr)\n```")

add("Generate a 3x3 matrix of random numbers from a normal distribution.",
    "```python\nimport numpy as np\n\narr = np.random.randn(3, 3)\nprint(arr)\n```")

add("How do I get random integers between 1 and 100 in numpy?",
    "```python\nimport numpy as np\n\narr = np.random.randint(1, 101, size=10)\nprint(arr)\n```")

add("Set a random seed in numpy so results are reproducible.",
    "```python\nimport numpy as np\n\nnp.random.seed(42)\nprint(np.random.rand(3))\n```")

add("Create an array like another array but filled with zeros.",
    "```python\nimport numpy as np\n\na = np.array([[1, 2], [3, 4]])\nz = np.zeros_like(a)\nprint(z)\n```")

# NUMPY: shape / reshape
add("How do I reshape a numpy array of 12 elements into a 3x4 matrix?",
    "```python\nimport numpy as np\n\narr = np.arange(12).reshape(3, 4)\nprint(arr)\n```")

add("Flatten a 2D numpy array into 1D.",
    "```python\nimport numpy as np\n\narr = np.array([[1, 2], [3, 4]])\nflat = arr.flatten()\nprint(flat)  # [1 2 3 4]\n```")

add("What's the difference between reshape(-1) and flatten?",
    "Both return a 1D view/copy of the data. `reshape(-1)` returns a view when possible (no copy), while `flatten()` always returns a copy.\n\n```python\nimport numpy as np\n\narr = np.array([[1, 2], [3, 4]])\nprint(arr.reshape(-1))   # view if possible\nprint(arr.flatten())     # always a copy\n```")

add("How do I transpose a numpy matrix?",
    "```python\nimport numpy as np\n\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.T)\n```")

add("Get the shape and number of dimensions of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.zeros((3, 4, 5))\nprint(arr.shape)  # (3, 4, 5)\nprint(arr.ndim)   # 3\nprint(arr.size)   # 60\n```")

add("Add a new axis to a numpy array to make it a column vector.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3])\ncol = arr[:, np.newaxis]\nprint(col.shape)  # (3, 1)\n```")

add("Use reshape with -1 so numpy figures out one dimension.",
    "The `-1` tells numpy to infer that dimension from the total size.\n\n```python\nimport numpy as np\n\narr = np.arange(12)\nprint(arr.reshape(4, -1))  # 4x3\n```")

# NUMPY: indexing / slicing
add("How do I slice the first 3 elements of a numpy array?",
    "```python\nimport numpy as np\n\narr = np.array([10, 20, 30, 40, 50])\nprint(arr[:3])  # [10 20 30]\n```")

add("Select every other element of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.arange(10)\nprint(arr[::2])  # [0 2 4 6 8]\n```")

add("Reverse a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3, 4])\nprint(arr[::-1])  # [4 3 2 1]\n```")

add("How do I get a single column from a 2D numpy array?",
    "```python\nimport numpy as np\n\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr[:, 1])  # [2 5]\n```")

add("Get the last row of a numpy matrix.",
    "```python\nimport numpy as np\n\narr = np.array([[1, 2], [3, 4], [5, 6]])\nprint(arr[-1])  # [5 6]\n```")

add("Select a submatrix (rows 0-1, columns 1-2) from a numpy array.",
    "```python\nimport numpy as np\n\narr = np.arange(12).reshape(3, 4)\nprint(arr[0:2, 1:3])\n```")

# NUMPY: boolean indexing / where
add("How do I filter a numpy array to keep only values greater than 5?",
    "```python\nimport numpy as np\n\narr = np.array([2, 6, 1, 9, 4, 7])\nprint(arr[arr > 5])  # [6 9 7]\n```")

add("Replace all negative values in a numpy array with 0.",
    "```python\nimport numpy as np\n\narr = np.array([-1, 2, -3, 4])\narr[arr < 0] = 0\nprint(arr)  # [0 2 0 4]\n```")

add("Use np.where to set values to 1 if positive else -1.",
    "```python\nimport numpy as np\n\narr = np.array([-2, 3, -5, 8])\nresult = np.where(arr > 0, 1, -1)\nprint(result)  # [-1  1 -1  1]\n```")

add("Count how many elements in a numpy array are above the mean.",
    "```python\nimport numpy as np\n\narr = np.array([1, 5, 3, 9, 2])\ncount = np.sum(arr > arr.mean())\nprint(count)\n```")

add("Find the indices where a numpy array equals its maximum.",
    "```python\nimport numpy as np\n\narr = np.array([1, 7, 3, 7, 2])\nidx = np.where(arr == arr.max())[0]\nprint(idx)  # [1 3]\n```")

add("How do I select array elements between 10 and 20 inclusive?",
    "Combine boolean conditions with `&` and wrap each in parentheses.\n\n```python\nimport numpy as np\n\narr = np.array([5, 12, 18, 25, 10, 20])\nmask = (arr >= 10) & (arr <= 20)\nprint(arr[mask])  # [12 18 10 20]\n```")

# NUMPY: reductions along axes
add("Compute the mean of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3, 4, 5])\nprint(arr.mean())  # 3.0\n```")

add("Sum each column of a 2D numpy array.",
    "`axis=0` collapses rows, giving a per-column sum.\n\n```python\nimport numpy as np\n\narr = np.array([[1, 2], [3, 4], [5, 6]])\nprint(arr.sum(axis=0))  # [9 12]\n```")

add("Compute the mean of each row in a numpy matrix.",
    "```python\nimport numpy as np\n\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(arr.mean(axis=1))  # [2. 5.]\n```")

add("Find the max and min of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([3, 9, 1, 7])\nprint(arr.max())  # 9\nprint(arr.min())  # 1\n```")

add("Get the standard deviation and variance of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([2, 4, 4, 4, 5, 5, 7, 9])\nprint(arr.std())  # standard deviation\nprint(arr.var())  # variance\n```")

add("Find the index of the maximum value in a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([3, 9, 1, 7])\nprint(np.argmax(arr))  # 1\n```")

add("Compute the cumulative sum of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3, 4])\nprint(np.cumsum(arr))  # [ 1  3  6 10]\n```")

add("Compute the product of all elements in a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3, 4])\nprint(np.prod(arr))  # 24\n```")

add("Get the median of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([1, 3, 5, 7, 9])\nprint(np.median(arr))  # 5.0\n```")

add("Compute the 90th percentile of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])\nprint(np.percentile(arr, 90))\n```")

# NUMPY: math / broadcasting
add("How does numpy broadcasting work when adding a scalar to an array?",
    "The scalar is applied element-wise to every entry.\n\n```python\nimport numpy as np\n\narr = np.array([1, 2, 3])\nprint(arr + 10)  # [11 12 13]\n```")

add("Add a 1D array to each row of a 2D array using broadcasting.",
    "```python\nimport numpy as np\n\nmat = np.array([[1, 2, 3], [4, 5, 6]])\nrow = np.array([10, 20, 30])\nprint(mat + row)\n```")

add("Multiply two numpy arrays element-wise.",
    "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(a * b)  # [ 4 10 18]\n```")

add("Compute the dot product of two vectors in numpy.",
    "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(np.dot(a, b))  # 32\n```")

add("Do matrix multiplication of two numpy matrices.",
    "Use `@` (matmul) for matrix products rather than `*`, which is element-wise.\n\n```python\nimport numpy as np\n\nA = np.array([[1, 2], [3, 4]])\nB = np.array([[5, 6], [7, 8]])\nprint(A @ B)\n```")

add("Compute the square root of every element of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([1, 4, 9, 16])\nprint(np.sqrt(arr))  # [1. 2. 3. 4.]\n```")

add("Take the natural log and exp of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3])\nprint(np.log(arr))\nprint(np.exp(arr))\n```")

add("Round all values in a numpy array to 2 decimals.",
    "```python\nimport numpy as np\n\narr = np.array([1.23456, 2.71828])\nprint(np.round(arr, 2))  # [1.23 2.72]\n```")

add("Compute the absolute value of a numpy array.",
    "```python\nimport numpy as np\n\narr = np.array([-1, -2, 3])\nprint(np.abs(arr))  # [1 2 3]\n```")

add("Clip the values of a numpy array between 0 and 1.",
    "```python\nimport numpy as np\n\narr = np.array([-0.5, 0.3, 1.2])\nprint(np.clip(arr, 0, 1))  # [0.  0.3 1. ]\n```")

# NUMPY: combining
add("Concatenate two numpy arrays.",
    "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(np.concatenate([a, b]))  # [1 2 3 4 5 6]\n```")

add("Stack two 1D arrays vertically into a 2D array.",
    "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(np.vstack([a, b]))\n```")

add("Stack two arrays horizontally in numpy.",
    "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(np.hstack([a, b]))  # [1 2 3 4 5 6]\n```")

add("Stack arrays along a new axis using np.stack.",
    "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(np.stack([a, b], axis=0).shape)  # (2, 3)\n```")

add("How do I normalize a numpy array to the range 0-1?",
    "Min-max normalization rescales values to [0, 1].\n\n```python\nimport numpy as np\n\narr = np.array([2, 4, 6, 8, 10])\nnorm = (arr - arr.min()) / (arr.max() - arr.min())\nprint(norm)\n```")

add("Standardize a numpy array to zero mean and unit variance.",
    "```python\nimport numpy as np\n\narr = np.array([10, 20, 30, 40, 50])\nstandardized = (arr - arr.mean()) / arr.std()\nprint(standardized)\n```")

add("Compute the correlation coefficient between two numpy arrays.",
    "```python\nimport numpy as np\n\nx = np.array([1, 2, 3, 4, 5])\ny = np.array([2, 4, 5, 4, 5])\nprint(np.corrcoef(x, y)[0, 1])\n```")

add("Find unique values in a numpy array and their counts.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 2, 3, 3, 3])\nvalues, counts = np.unique(arr, return_counts=True)\nprint(values)  # [1 2 3]\nprint(counts)  # [1 2 3]\n```")

add("Sort a numpy array in descending order.",
    "```python\nimport numpy as np\n\narr = np.array([3, 1, 4, 1, 5])\nprint(np.sort(arr)[::-1])  # [5 4 3 1 1]\n```")

add("How do I check if two numpy arrays are equal element-wise?",
    "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([1, 2, 3])\nprint(np.array_equal(a, b))  # True\n```")

add("Compute the inverse of a matrix in numpy.",
    "```python\nimport numpy as np\n\nA = np.array([[1, 2], [3, 4]])\nprint(np.linalg.inv(A))\n```")

add("Solve a linear system Ax = b in numpy.",
    "```python\nimport numpy as np\n\nA = np.array([[3, 1], [1, 2]])\nb = np.array([9, 8])\nx = np.linalg.solve(A, b)\nprint(x)  # [2. 3.]\n```")

add("Compute the determinant of a matrix.",
    "```python\nimport numpy as np\n\nA = np.array([[1, 2], [3, 4]])\nprint(np.linalg.det(A))  # -2.0\n```")

add("Get the eigenvalues of a matrix in numpy.",
    "```python\nimport numpy as np\n\nA = np.array([[2, 0], [0, 3]])\nvals, vecs = np.linalg.eig(A)\nprint(vals)  # [2. 3.]\n```")

# ---------------------------------------------------------------------------
# PANDAS: loading / inspecting
# ---------------------------------------------------------------------------
add("How do I load a CSV file into pandas?",
    "```python\nimport pandas as pd\n\ndf = pd.read_csv('data.csv')\nprint(df.head())\n```")

add("Read a CSV that uses a semicolon as separator.",
    "```python\nimport pandas as pd\n\ndf = pd.read_csv('data.csv', sep=';')\nprint(df.head())\n```")

add("Load a CSV and use the first column as the index.",
    "```python\nimport pandas as pd\n\ndf = pd.read_csv('data.csv', index_col=0)\nprint(df.head())\n```")

add("Read only the first 100 rows of a large CSV.",
    "```python\nimport pandas as pd\n\ndf = pd.read_csv('data.csv', nrows=100)\nprint(df.shape)\n```")

add("Read a CSV with no header row.",
    "```python\nimport pandas as pd\n\ndf = pd.read_csv('data.csv', header=None)\nprint(df.head())\n```")

add("How do I load an Excel file into pandas?",
    "```python\nimport pandas as pd\n\ndf = pd.read_excel('data.xlsx', sheet_name='Sheet1')\nprint(df.head())\n```")

add("Show the first 5 rows of a DataFrame.",
    "```python\nimport pandas as pd\n\ndf = pd.read_csv('data.csv')\nprint(df.head())\n```")

add("Show the last 10 rows of a DataFrame.",
    "```python\nimport pandas as pd\n\nprint(df.tail(10))\n```")

add("Get summary statistics of a DataFrame.",
    "`describe()` reports count, mean, std, min, quartiles and max for numeric columns.\n\n```python\nimport pandas as pd\n\nprint(df.describe())\n```")

add("Show the column types and non-null counts of a DataFrame.",
    "```python\nimport pandas as pd\n\ndf.info()\n```")

add("How many rows and columns does my DataFrame have?",
    "```python\nimport pandas as pd\n\nprint(df.shape)  # (rows, columns)\n```")

add("List the column names of a DataFrame.",
    "```python\nimport pandas as pd\n\nprint(df.columns.tolist())\n```")

add("Get the data types of each column.",
    "```python\nimport pandas as pd\n\nprint(df.dtypes)\n```")

add("Create a DataFrame from a dictionary.",
    "```python\nimport pandas as pd\n\ndf = pd.DataFrame({'name': ['Ann', 'Bob'], 'age': [30, 25]})\nprint(df)\n```")

add("Create a pandas Series from a list.",
    "```python\nimport pandas as pd\n\ns = pd.Series([10, 20, 30], name='values')\nprint(s)\n```")

# PANDAS: selecting
add("Select a single column from a DataFrame as a Series.",
    "```python\nimport pandas as pd\n\nages = df['age']\nprint(ages.head())\n```")

add("Select multiple columns from a DataFrame.",
    "Pass a list of column names inside the brackets.\n\n```python\nimport pandas as pd\n\nsubset = df[['name', 'age']]\nprint(subset.head())\n```")

add("Select a row by its integer position with iloc.",
    "```python\nimport pandas as pd\n\nprint(df.iloc[0])   # first row\nprint(df.iloc[-1])  # last row\n```")

add("Select a row by its label with loc.",
    "```python\nimport pandas as pd\n\nprint(df.loc[5])  # row with index label 5\n```")

add("Select rows 10 to 20 and columns 'a' and 'b'.",
    "```python\nimport pandas as pd\n\nprint(df.loc[10:20, ['a', 'b']])\n```")

add("Get a single cell value at row 3, column 'price'.",
    "```python\nimport pandas as pd\n\nprint(df.at[3, 'price'])\n```")

add("Select the first 4 columns of a DataFrame by position.",
    "```python\nimport pandas as pd\n\nprint(df.iloc[:, :4].head())\n```")

# PANDAS: filtering
add("Filter rows where the column age is greater than 30.",
    "```python\nimport pandas as pd\n\nresult = df[df['age'] > 30]\nprint(result)\n```")

add("Filter a DataFrame where city equals 'London'.",
    "```python\nimport pandas as pd\n\nresult = df[df['city'] == 'London']\nprint(result)\n```")

add("Filter rows where age is between 25 and 40.",
    "Use `between` for an inclusive range filter.\n\n```python\nimport pandas as pd\n\nresult = df[df['age'].between(25, 40)]\nprint(result)\n```")

add("Filter rows with two conditions: age > 30 and salary > 50000.",
    "Wrap each condition in parentheses and combine with `&`.\n\n```python\nimport pandas as pd\n\nresult = df[(df['age'] > 30) & (df['salary'] > 50000)]\nprint(result)\n```")

add("Filter rows where category is either 'A' or 'B'.",
    "```python\nimport pandas as pd\n\nresult = df[df['category'].isin(['A', 'B'])]\nprint(result)\n```")

add("Filter out rows where the name column contains 'test'.",
    "```python\nimport pandas as pd\n\nresult = df[~df['name'].str.contains('test', na=False)]\nprint(result)\n```")

add("Use query() to filter a DataFrame where price < 100.",
    "```python\nimport pandas as pd\n\nresult = df.query('price < 100')\nprint(result)\n```")

add("Filter rows where a date column is after 2023-01-01.",
    "```python\nimport pandas as pd\n\ndf['date'] = pd.to_datetime(df['date'])\nresult = df[df['date'] > '2023-01-01']\nprint(result)\n```")

# PANDAS: groupby / agg
add("Group by a column and compute the sum.",
    "```python\nimport pandas as pd\n\nresult = df.groupby('category')['amount'].sum()\nprint(result)\n```")

add("Group by city and compute the average salary.",
    "```python\nimport pandas as pd\n\nresult = df.groupby('city')['salary'].mean()\nprint(result)\n```")

add("Group by two columns and count the rows in each group.",
    "```python\nimport pandas as pd\n\nresult = df.groupby(['region', 'product']).size()\nprint(result)\n```")

add("Group by a column and apply multiple aggregations at once.",
    "Pass a list of functions to `agg`.\n\n```python\nimport pandas as pd\n\nresult = df.groupby('category')['amount'].agg(['sum', 'mean', 'count'])\nprint(result)\n```")

add("Group by department and get the max and min salary per group.",
    "```python\nimport pandas as pd\n\nresult = df.groupby('department')['salary'].agg(['max', 'min'])\nprint(result)\n```")

add("Use named aggregations in a groupby.",
    "```python\nimport pandas as pd\n\nresult = df.groupby('city').agg(\n    avg_age=('age', 'mean'),\n    total=('salary', 'sum'),\n)\nprint(result)\n```")

add("Group by a column and keep it as a regular column instead of index.",
    "Pass `as_index=False` so the grouping key stays as a column.\n\n```python\nimport pandas as pd\n\nresult = df.groupby('category', as_index=False)['amount'].sum()\nprint(result)\n```")

add("Compute the percentage each group contributes to the total.",
    "```python\nimport pandas as pd\n\ngroup = df.groupby('category')['amount'].sum()\npct = group / group.sum() * 100\nprint(pct)\n```")

add("Apply a custom function to each group with groupby.apply.",
    "```python\nimport pandas as pd\n\nresult = df.groupby('team')['score'].apply(lambda x: x.max() - x.min())\nprint(result)\n```")

# PANDAS: value_counts / unique
add("Count how many times each value appears in a column.",
    "```python\nimport pandas as pd\n\nprint(df['category'].value_counts())\n```")

add("Get the proportion of each value in a column.",
    "```python\nimport pandas as pd\n\nprint(df['category'].value_counts(normalize=True))\n```")

add("Get the unique values in a column.",
    "```python\nimport pandas as pd\n\nprint(df['city'].unique())\n```")

add("Count the number of distinct values in a column.",
    "```python\nimport pandas as pd\n\nprint(df['city'].nunique())\n```")

# PANDAS: sorting
add("Sort a DataFrame by a column in descending order.",
    "```python\nimport pandas as pd\n\nresult = df.sort_values('salary', ascending=False)\nprint(result.head())\n```")

add("Sort a DataFrame by two columns.",
    "```python\nimport pandas as pd\n\nresult = df.sort_values(['department', 'salary'], ascending=[True, False])\nprint(result.head())\n```")

add("Get the top 5 rows by sales.",
    "`nlargest` is a concise way to get the top-N rows by a column.\n\n```python\nimport pandas as pd\n\nprint(df.nlargest(5, 'sales'))\n```")

add("Get the 3 rows with the smallest price.",
    "```python\nimport pandas as pd\n\nprint(df.nsmallest(3, 'price'))\n```")

add("Sort a DataFrame by its index.",
    "```python\nimport pandas as pd\n\nresult = df.sort_index()\nprint(result.head())\n```")

# PANDAS: missing data
add("How do I find missing values in a DataFrame?",
    "```python\nimport pandas as pd\n\nprint(df.isnull().sum())\n```")

add("Drop rows that have any missing values.",
    "```python\nimport pandas as pd\n\nclean = df.dropna()\nprint(clean.shape)\n```")

add("Drop columns that contain missing values.",
    "```python\nimport pandas as pd\n\nclean = df.dropna(axis=1)\nprint(clean.columns.tolist())\n```")

add("Fill missing values in a column with 0.",
    "```python\nimport pandas as pd\n\ndf['amount'] = df['amount'].fillna(0)\nprint(df['amount'].isnull().sum())\n```")

add("Fill missing values with the column mean.",
    "```python\nimport pandas as pd\n\ndf['age'] = df['age'].fillna(df['age'].mean())\nprint(df['age'].isnull().sum())\n```")

add("Forward fill missing values in a DataFrame.",
    "```python\nimport pandas as pd\n\ndf = df.ffill()\nprint(df.isnull().sum())\n```")

add("Drop rows where a specific column is null.",
    "```python\nimport pandas as pd\n\nclean = df.dropna(subset=['email'])\nprint(clean.shape)\n```")

add("Check if a DataFrame has any missing values at all.",
    "```python\nimport pandas as pd\n\nprint(df.isnull().values.any())\n```")

# PANDAS: new columns / apply / map
add("Add a new column that is the sum of two existing columns.",
    "```python\nimport pandas as pd\n\ndf['total'] = df['price'] + df['tax']\nprint(df.head())\n```")

add("Create a new column based on a condition using np.where.",
    "```python\nimport numpy as np\nimport pandas as pd\n\ndf['status'] = np.where(df['score'] >= 60, 'pass', 'fail')\nprint(df.head())\n```")

add("Apply a function to a column to square its values.",
    "```python\nimport pandas as pd\n\ndf['squared'] = df['x'].apply(lambda v: v ** 2)\nprint(df.head())\n```")

add("Map values in a column to new labels.",
    "Use `map` with a dictionary to translate values.\n\n```python\nimport pandas as pd\n\nmapping = {0: 'no', 1: 'yes'}\ndf['label'] = df['flag'].map(mapping)\nprint(df.head())\n```")

add("Apply a function across rows of a DataFrame.",
    "Use `apply` with `axis=1` to operate on each row.\n\n```python\nimport pandas as pd\n\ndf['full_name'] = df.apply(lambda r: f\"{r['first']} {r['last']}\", axis=1)\nprint(df.head())\n```")

add("Convert a column to uppercase strings.",
    "```python\nimport pandas as pd\n\ndf['name'] = df['name'].str.upper()\nprint(df.head())\n```")

add("Bin a numeric column into categories using pd.cut.",
    "```python\nimport pandas as pd\n\ndf['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 60, 100],\n                         labels=['child', 'young', 'adult', 'senior'])\nprint(df['age_group'].value_counts())\n```")

add("Rename a column in a DataFrame.",
    "```python\nimport pandas as pd\n\ndf = df.rename(columns={'old_name': 'new_name'})\nprint(df.columns.tolist())\n```")

add("Drop a column from a DataFrame.",
    "```python\nimport pandas as pd\n\ndf = df.drop(columns=['unwanted'])\nprint(df.columns.tolist())\n```")

add("Change a column's data type to integer.",
    "```python\nimport pandas as pd\n\ndf['count'] = df['count'].astype(int)\nprint(df.dtypes)\n```")

add("Convert a column to datetime.",
    "```python\nimport pandas as pd\n\ndf['date'] = pd.to_datetime(df['date'])\nprint(df['date'].dtype)\n```")

add("Extract the year from a datetime column.",
    "```python\nimport pandas as pd\n\ndf['date'] = pd.to_datetime(df['date'])\ndf['year'] = df['date'].dt.year\nprint(df[['date', 'year']].head())\n```")

# PANDAS: merge / join / concat
add("Merge two DataFrames on a common column.",
    "```python\nimport pandas as pd\n\nmerged = pd.merge(orders, customers, on='customer_id')\nprint(merged.head())\n```")

add("Do a left join between two DataFrames.",
    "```python\nimport pandas as pd\n\nresult = pd.merge(df1, df2, on='id', how='left')\nprint(result.head())\n```")

add("Merge two DataFrames where the key columns have different names.",
    "```python\nimport pandas as pd\n\nresult = pd.merge(df1, df2, left_on='user_id', right_on='id')\nprint(result.head())\n```")

add("Concatenate two DataFrames vertically (stack rows).",
    "```python\nimport pandas as pd\n\ncombined = pd.concat([df1, df2], ignore_index=True)\nprint(combined.shape)\n```")

add("Concatenate DataFrames side by side (add columns).",
    "```python\nimport pandas as pd\n\ncombined = pd.concat([df1, df2], axis=1)\nprint(combined.shape)\n```")

add("Join two DataFrames on their index.",
    "```python\nimport pandas as pd\n\nresult = df1.join(df2, how='inner')\nprint(result.head())\n```")

add("Do an outer join keeping all rows from both DataFrames.",
    "```python\nimport pandas as pd\n\nresult = pd.merge(df1, df2, on='key', how='outer')\nprint(result.head())\n```")

# PANDAS: pivot
add("Create a pivot table summing sales by region and month.",
    "```python\nimport pandas as pd\n\npivot = df.pivot_table(index='region', columns='month',\n                       values='sales', aggfunc='sum')\nprint(pivot)\n```")

add("Pivot a long DataFrame to wide format.",
    "```python\nimport pandas as pd\n\nwide = df.pivot(index='date', columns='product', values='qty')\nprint(wide.head())\n```")

add("Melt a wide DataFrame into long format.",
    "```python\nimport pandas as pd\n\nlong = df.melt(id_vars='id', var_name='variable', value_name='value')\nprint(long.head())\n```")

add("Make a crosstab of two categorical columns.",
    "```python\nimport pandas as pd\n\nprint(pd.crosstab(df['gender'], df['purchased']))\n```")

# PANDAS: export
add("Save a DataFrame to a CSV file without the index.",
    "```python\nimport pandas as pd\n\ndf.to_csv('output.csv', index=False)\n```")

add("Write a DataFrame to an Excel file.",
    "```python\nimport pandas as pd\n\ndf.to_excel('output.xlsx', index=False)\n```")

add("Save a DataFrame to JSON.",
    "```python\nimport pandas as pd\n\ndf.to_json('output.json', orient='records')\n```")

# PANDAS: stats
add("Compute the correlation matrix of a DataFrame.",
    "```python\nimport pandas as pd\n\nprint(df.corr(numeric_only=True))\n```")

add("Get the mean of every numeric column.",
    "```python\nimport pandas as pd\n\nprint(df.mean(numeric_only=True))\n```")

add("Compute the median of a single column.",
    "```python\nimport pandas as pd\n\nprint(df['price'].median())\n```")

add("Get the standard deviation of each column.",
    "```python\nimport pandas as pd\n\nprint(df.std(numeric_only=True))\n```")

add("Find the correlation between two specific columns.",
    "```python\nimport pandas as pd\n\nprint(df['height'].corr(df['weight']))\n```")

add("Compute a rolling 7-day average of a column.",
    "```python\nimport pandas as pd\n\ndf['rolling_avg'] = df['value'].rolling(window=7).mean()\nprint(df.head(10))\n```")

add("Compute the cumulative sum of a column.",
    "```python\nimport pandas as pd\n\ndf['running_total'] = df['amount'].cumsum()\nprint(df.head())\n```")

add("Remove duplicate rows from a DataFrame.",
    "```python\nimport pandas as pd\n\nclean = df.drop_duplicates()\nprint(clean.shape)\n```")

add("Drop duplicates based on a subset of columns, keeping the last.",
    "```python\nimport pandas as pd\n\nclean = df.drop_duplicates(subset=['email'], keep='last')\nprint(clean.shape)\n```")

add("Reset the index of a DataFrame.",
    "```python\nimport pandas as pd\n\ndf = df.reset_index(drop=True)\nprint(df.head())\n```")

add("Set a column as the DataFrame index.",
    "```python\nimport pandas as pd\n\ndf = df.set_index('id')\nprint(df.head())\n```")

add("Sample 10 random rows from a DataFrame.",
    "```python\nimport pandas as pd\n\nsample = df.sample(n=10, random_state=42)\nprint(sample)\n```")

add("Shuffle the rows of a DataFrame.",
    "```python\nimport pandas as pd\n\nshuffled = df.sample(frac=1, random_state=0).reset_index(drop=True)\nprint(shuffled.head())\n```")

# ---------------------------------------------------------------------------
# MATPLOTLIB
# ---------------------------------------------------------------------------
add("How do I make a simple line plot with matplotlib?",
    "```python\nimport matplotlib.pyplot as plt\n\nx = [1, 2, 3, 4]\ny = [1, 4, 9, 16]\nplt.plot(x, y)\nplt.xlabel('x')\nplt.ylabel('y')\nplt.title('Line plot')\nplt.show()\n```")

add("Make a scatter plot of two columns from a DataFrame.",
    "```python\nimport matplotlib.pyplot as plt\n\nplt.scatter(df['height'], df['weight'])\nplt.xlabel('Height')\nplt.ylabel('Weight')\nplt.show()\n```")

add("Plot a histogram of a numpy array with 20 bins.",
    "```python\nimport matplotlib.pyplot as plt\nimport numpy as np\n\ndata = np.random.randn(1000)\nplt.hist(data, bins=20)\nplt.xlabel('Value')\nplt.ylabel('Frequency')\nplt.show()\n```")

add("Make a bar chart from a pandas value_counts.",
    "```python\nimport matplotlib.pyplot as plt\n\ncounts = df['category'].value_counts()\ncounts.plot(kind='bar')\nplt.ylabel('Count')\nplt.show()\n```")

add("Create a horizontal bar chart.",
    "```python\nimport matplotlib.pyplot as plt\n\ncategories = ['A', 'B', 'C']\nvalues = [5, 7, 3]\nplt.barh(categories, values)\nplt.show()\n```")

add("Add a legend to a matplotlib plot with two lines.",
    "Pass `label=` to each plot call, then call `plt.legend()`.\n\n```python\nimport matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [1, 2, 3], label='line 1')\nplt.plot([1, 2, 3], [3, 2, 1], label='line 2')\nplt.legend()\nplt.show()\n```")

add("Create a figure with two subplots side by side.",
    "```python\nimport matplotlib.pyplot as plt\n\nfig, axes = plt.subplots(1, 2, figsize=(10, 4))\naxes[0].plot([1, 2, 3], [1, 4, 9])\naxes[0].set_title('Left')\naxes[1].scatter([1, 2, 3], [3, 2, 1])\naxes[1].set_title('Right')\nplt.show()\n```")

add("Make a 2x2 grid of subplots.",
    "```python\nimport matplotlib.pyplot as plt\n\nfig, axes = plt.subplots(2, 2, figsize=(8, 8))\naxes[0, 0].plot([1, 2, 3])\naxes[0, 1].hist([1, 1, 2, 3])\naxes[1, 0].bar(['a', 'b'], [3, 5])\naxes[1, 1].scatter([1, 2], [2, 1])\nplt.tight_layout()\nplt.show()\n```")

add("Save a matplotlib figure to a PNG file.",
    "```python\nimport matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [1, 4, 9])\nplt.savefig('plot.png', dpi=300, bbox_inches='tight')\n```")

add("Set the figure size in matplotlib.",
    "```python\nimport matplotlib.pyplot as plt\n\nplt.figure(figsize=(12, 6))\nplt.plot([1, 2, 3], [1, 4, 9])\nplt.show()\n```")

add("Plot a pie chart of category proportions.",
    "```python\nimport matplotlib.pyplot as plt\n\nsizes = [40, 30, 20, 10]\nlabels = ['A', 'B', 'C', 'D']\nplt.pie(sizes, labels=labels, autopct='%1.1f%%')\nplt.show()\n```")

add("Plot a box plot of a numeric column grouped by category.",
    "```python\nimport matplotlib.pyplot as plt\n\ndf.boxplot(column='value', by='group')\nplt.show()\n```")

add("Add gridlines to a matplotlib plot.",
    "```python\nimport matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [1, 4, 9])\nplt.grid(True)\nplt.show()\n```")

add("Rotate the x-axis tick labels by 45 degrees.",
    "```python\nimport matplotlib.pyplot as plt\n\nplt.bar(['Jan', 'Feb', 'Mar'], [3, 5, 2])\nplt.xticks(rotation=45)\nplt.show()\n```")

add("Plot two lines with different colors and markers.",
    "```python\nimport matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [1, 2, 3], 'r-o', label='red')\nplt.plot([1, 2, 3], [3, 2, 1], 'b--s', label='blue')\nplt.legend()\nplt.show()\n```")

add("Plot a histogram directly from a pandas column.",
    "```python\nimport matplotlib.pyplot as plt\n\ndf['age'].plot(kind='hist', bins=15)\nplt.xlabel('Age')\nplt.show()\n```")

add("Set x and y axis limits in matplotlib.",
    "```python\nimport matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [1, 4, 9])\nplt.xlim(0, 5)\nplt.ylim(0, 10)\nplt.show()\n```")

add("Plot a line chart of a time series DataFrame.",
    "```python\nimport matplotlib.pyplot as plt\n\ndf.set_index('date')['value'].plot()\nplt.ylabel('Value')\nplt.show()\n```")

# ---------------------------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------------------------
add("How do I compute the mode of a list of numbers in Python?",
    "```python\nimport statistics\n\ndata = [1, 2, 2, 3, 3, 3, 4]\nprint(statistics.mode(data))  # 3\n```")

add("Compute mean, median and standard deviation of a list.",
    "```python\nimport statistics\n\ndata = [4, 8, 15, 16, 23, 42]\nprint(statistics.mean(data))\nprint(statistics.median(data))\nprint(statistics.stdev(data))\n```")

add("What's the difference between population and sample standard deviation in numpy?",
    "By default numpy computes population std (ddof=0). Set `ddof=1` for the sample standard deviation.\n\n```python\nimport numpy as np\n\ndata = np.array([2, 4, 4, 4, 5, 5, 7, 9])\nprint(data.std())          # population, ddof=0\nprint(data.std(ddof=1))    # sample, ddof=1\n```")

add("Compute the variance of a dataset.",
    "```python\nimport numpy as np\n\ndata = np.array([10, 12, 23, 23, 16, 23, 21, 16])\nprint(np.var(data))\n```")

add("Compute the covariance matrix of two variables.",
    "```python\nimport numpy as np\n\nx = np.array([1, 2, 3, 4, 5])\ny = np.array([2, 4, 6, 8, 10])\nprint(np.cov(x, y))\n```")

add("How do I compute a z-score for a value?",
    "```python\nimport numpy as np\n\ndata = np.array([10, 20, 30, 40, 50])\nvalue = 35\nz = (value - data.mean()) / data.std()\nprint(z)\n```")

add("Compute quartiles of a dataset.",
    "```python\nimport numpy as np\n\ndata = np.array([1, 2, 3, 4, 5, 6, 7, 8])\nq1, q2, q3 = np.percentile(data, [25, 50, 75])\nprint(q1, q2, q3)\n```")

add("Find the interquartile range (IQR) of an array.",
    "```python\nimport numpy as np\n\ndata = np.array([1, 3, 5, 7, 9, 11, 13])\nq1, q3 = np.percentile(data, [25, 75])\niqr = q3 - q1\nprint(iqr)\n```")

# ---------------------------------------------------------------------------
# SCIKIT-LEARN
# ---------------------------------------------------------------------------
add("How do I split data into training and test sets with scikit-learn?",
    "```python\nfrom sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42)\nprint(X_train.shape, X_test.shape)\n```")

add("Train a linear regression model with scikit-learn.",
    "```python\nfrom sklearn.linear_model import LinearRegression\n\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\nprint(model.coef_, model.intercept_)\n```")

add("Make predictions with a trained model and evaluate with R^2.",
    "```python\nfrom sklearn.metrics import r2_score\n\ny_pred = model.predict(X_test)\nprint(r2_score(y_test, y_pred))\n```")

add("Compute the mean squared error of predictions.",
    "```python\nfrom sklearn.metrics import mean_squared_error\n\nmse = mean_squared_error(y_test, y_pred)\nprint(mse)\n```")

add("Train a logistic regression classifier.",
    "```python\nfrom sklearn.linear_model import LogisticRegression\n\nclf = LogisticRegression(max_iter=1000)\nclf.fit(X_train, y_train)\nprint(clf.score(X_test, y_test))\n```")

add("Compute the accuracy of a classifier.",
    "```python\nfrom sklearn.metrics import accuracy_score\n\ny_pred = clf.predict(X_test)\nprint(accuracy_score(y_test, y_pred))\n```")

add("Standardize features with StandardScaler.",
    "Fit the scaler on the training data only, then transform both splits.\n\n```python\nfrom sklearn.preprocessing import StandardScaler\n\nscaler = StandardScaler()\nX_train_scaled = scaler.fit_transform(X_train)\nX_test_scaled = scaler.transform(X_test)\n```")

add("Train a k-nearest neighbors classifier.",
    "```python\nfrom sklearn.neighbors import KNeighborsClassifier\n\nclf = KNeighborsClassifier(n_neighbors=5)\nclf.fit(X_train, y_train)\nprint(clf.score(X_test, y_test))\n```")

add("Train a decision tree classifier.",
    "```python\nfrom sklearn.tree import DecisionTreeClassifier\n\nclf = DecisionTreeClassifier(max_depth=4, random_state=0)\nclf.fit(X_train, y_train)\nprint(clf.score(X_test, y_test))\n```")

add("Train a random forest classifier.",
    "```python\nfrom sklearn.ensemble import RandomForestClassifier\n\nclf = RandomForestClassifier(n_estimators=100, random_state=0)\nclf.fit(X_train, y_train)\nprint(clf.score(X_test, y_test))\n```")

add("Show a confusion matrix for classification results.",
    "```python\nfrom sklearn.metrics import confusion_matrix\n\ny_pred = clf.predict(X_test)\nprint(confusion_matrix(y_test, y_pred))\n```")

add("Print a full classification report.",
    "```python\nfrom sklearn.metrics import classification_report\n\ny_pred = clf.predict(X_test)\nprint(classification_report(y_test, y_pred))\n```")

add("Do K-means clustering with scikit-learn.",
    "```python\nfrom sklearn.cluster import KMeans\n\nkmeans = KMeans(n_clusters=3, random_state=0, n_init=10)\nlabels = kmeans.fit_predict(X)\nprint(labels[:10])\n```")

add("Run cross-validation on a model.",
    "```python\nfrom sklearn.model_selection import cross_val_score\n\nscores = cross_val_score(model, X, y, cv=5)\nprint(scores.mean(), scores.std())\n```")

add("Use PCA to reduce data to 2 dimensions.",
    "```python\nfrom sklearn.decomposition import PCA\n\npca = PCA(n_components=2)\nX_2d = pca.fit_transform(X)\nprint(X_2d.shape)\nprint(pca.explained_variance_ratio_)\n```")

add("Encode categorical labels as integers.",
    "```python\nfrom sklearn.preprocessing import LabelEncoder\n\nle = LabelEncoder()\ny_encoded = le.fit_transform(y)\nprint(y_encoded[:10])\n```")

add("Predict on new data with a fitted linear regression.",
    "```python\nimport numpy as np\nfrom sklearn.linear_model import LinearRegression\n\nmodel = LinearRegression().fit(X_train, y_train)\nnew = np.array([[5.0, 2.0]])\nprint(model.predict(new))\n```")

# More numpy / pandas variety
add("How do I count nonzero elements in a numpy array?",
    "```python\nimport numpy as np\n\narr = np.array([0, 1, 0, 3, 0, 5])\nprint(np.count_nonzero(arr))  # 3\n```")

add("Check whether any / all elements of a boolean array are True.",
    "```python\nimport numpy as np\n\narr = np.array([True, False, True])\nprint(arr.any())  # True\nprint(arr.all())  # False\n```")

add("Compute element-wise maximum of two numpy arrays.",
    "```python\nimport numpy as np\n\na = np.array([1, 5, 3])\nb = np.array([4, 2, 6])\nprint(np.maximum(a, b))  # [4 5 6]\n```")

add("Tile a numpy array 3 times.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2])\nprint(np.tile(arr, 3))  # [1 2 1 2 1 2]\n```")

add("Repeat each element of a numpy array twice.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3])\nprint(np.repeat(arr, 2))  # [1 1 2 2 3 3]\n```")

add("Compute the outer product of two vectors.",
    "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([4, 5])\nprint(np.outer(a, b))\n```")

add("Get the diagonal of a matrix.",
    "```python\nimport numpy as np\n\nA = np.array([[1, 2], [3, 4]])\nprint(np.diag(A))  # [1 4]\n```")

add("Compute the trace of a matrix.",
    "```python\nimport numpy as np\n\nA = np.array([[1, 2], [3, 4]])\nprint(np.trace(A))  # 5\n```")

add("Find rows in a DataFrame where any value is null.",
    "```python\nimport pandas as pd\n\nrows = df[df.isnull().any(axis=1)]\nprint(rows)\n```")

add("Count the total number of missing cells in a DataFrame.",
    "```python\nimport pandas as pd\n\nprint(df.isnull().sum().sum())\n```")

add("Replace a specific value in a column with another.",
    "```python\nimport pandas as pd\n\ndf['status'] = df['status'].replace('old', 'new')\nprint(df['status'].value_counts())\n```")

add("Get the row with the maximum value of a column.",
    "```python\nimport pandas as pd\n\nrow = df.loc[df['sales'].idxmax()]\nprint(row)\n```")

add("Compute the difference between consecutive rows of a column.",
    "```python\nimport pandas as pd\n\ndf['change'] = df['value'].diff()\nprint(df.head())\n```")

add("Compute the percent change of a column.",
    "```python\nimport pandas as pd\n\ndf['pct_change'] = df['price'].pct_change()\nprint(df.head())\n```")

add("Rank rows by a column value.",
    "```python\nimport pandas as pd\n\ndf['rank'] = df['score'].rank(ascending=False)\nprint(df.sort_values('rank').head())\n```")

add("Compute a cumulative max of a column.",
    "```python\nimport pandas as pd\n\ndf['running_max'] = df['value'].cummax()\nprint(df.head())\n```")

add("Group by a column and get the first row of each group.",
    "```python\nimport pandas as pd\n\nprint(df.groupby('user_id').first())\n```")

add("Group and compute the size of each group sorted descending.",
    "```python\nimport pandas as pd\n\nprint(df.groupby('city').size().sort_values(ascending=False))\n```")

add("Filter a DataFrame to rows where a string column starts with 'A'.",
    "```python\nimport pandas as pd\n\nresult = df[df['name'].str.startswith('A')]\nprint(result)\n```")

add("Extract the length of strings in a column into a new column.",
    "```python\nimport pandas as pd\n\ndf['name_len'] = df['name'].str.len()\nprint(df.head())\n```")

add("Split a string column on a comma into multiple columns.",
    "```python\nimport pandas as pd\n\ndf[['first', 'last']] = df['full_name'].str.split(',', expand=True)\nprint(df.head())\n```")

add("Replace substrings in a column using regex.",
    "```python\nimport pandas as pd\n\ndf['phone'] = df['phone'].str.replace(r'\\D', '', regex=True)\nprint(df.head())\n```")

add("Convert a column of strings to numeric, coercing errors to NaN.",
    "```python\nimport pandas as pd\n\ndf['amount'] = pd.to_numeric(df['amount'], errors='coerce')\nprint(df['amount'].dtype)\n```")

add("Get the memory usage of a DataFrame.",
    "```python\nimport pandas as pd\n\nprint(df.memory_usage(deep=True).sum())\n```")

add("Iterate over the rows of a DataFrame.",
    "`iterrows` yields `(index, row)` pairs, though vectorized ops are preferred for speed.\n\n```python\nimport pandas as pd\n\nfor idx, row in df.iterrows():\n    print(idx, row['name'])\n```")

add("Apply different aggregations to different columns in a groupby.",
    "```python\nimport pandas as pd\n\nresult = df.groupby('region').agg({'sales': 'sum', 'profit': 'mean'})\nprint(result)\n```")

add("Find duplicate rows in a DataFrame.",
    "```python\nimport pandas as pd\n\nprint(df[df.duplicated()])\n```")

add("Get value counts including NaN values.",
    "```python\nimport pandas as pd\n\nprint(df['category'].value_counts(dropna=False))\n```")

add("Create a one-hot encoding of a categorical column.",
    "```python\nimport pandas as pd\n\nencoded = pd.get_dummies(df, columns=['category'])\nprint(encoded.head())\n```")

add("Compute a weighted average of a column.",
    "```python\nimport numpy as np\n\nvalues = np.array([10, 20, 30])\nweights = np.array([1, 2, 3])\nwavg = np.average(values, weights=weights)\nprint(wavg)\n```")

add("Smooth a numpy array with a moving average of window 3.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3, 4, 5, 6])\nkernel = np.ones(3) / 3\nsmoothed = np.convolve(arr, kernel, mode='valid')\nprint(smoothed)\n```")

add("Generate a 2D grid of coordinates with meshgrid.",
    "```python\nimport numpy as np\n\nx = np.arange(3)\ny = np.arange(2)\nxx, yy = np.meshgrid(x, y)\nprint(xx)\nprint(yy)\n```")

add("Compute pairwise euclidean distance between two points.",
    "```python\nimport numpy as np\n\na = np.array([1, 2])\nb = np.array([4, 6])\ndist = np.linalg.norm(a - b)\nprint(dist)  # 5.0\n```")

add("Normalize each row of a matrix to sum to 1.",
    "```python\nimport numpy as np\n\nmat = np.array([[1, 1, 2], [2, 2, 0]], dtype=float)\nnorm = mat / mat.sum(axis=1, keepdims=True)\nprint(norm)\n```")

add("Apply a softmax to a numpy vector.",
    "Subtracting the max first keeps the exponentials numerically stable.\n\n```python\nimport numpy as np\n\ndef softmax(x):\n    e = np.exp(x - x.max())\n    return e / e.sum()\n\nprint(softmax(np.array([1.0, 2.0, 3.0])))\n```")

add("Create a boolean mask for even numbers in an array.",
    "```python\nimport numpy as np\n\narr = np.arange(10)\nmask = arr % 2 == 0\nprint(arr[mask])  # [0 2 4 6 8]\n```")

add("Find the index of the value closest to a target in an array.",
    "```python\nimport numpy as np\n\narr = np.array([1.0, 2.5, 3.8, 5.0])\ntarget = 3.0\nidx = np.argmin(np.abs(arr - target))\nprint(idx)  # 1\n```")

add("Replace NaN values in a numpy array with 0.",
    "```python\nimport numpy as np\n\narr = np.array([1.0, np.nan, 3.0])\nclean = np.nan_to_num(arr, nan=0.0)\nprint(clean)  # [1. 0. 3.]\n```")

add("Compute the mean of a numpy array ignoring NaNs.",
    "```python\nimport numpy as np\n\narr = np.array([1.0, np.nan, 3.0])\nprint(np.nanmean(arr))  # 2.0\n```")

add("Stack a list of arrays into a single 2D array.",
    "```python\nimport numpy as np\n\nrows = [np.array([1, 2]), np.array([3, 4]), np.array([5, 6])]\nmat = np.array(rows)\nprint(mat.shape)  # (3, 2)\n```")

add("Get a DataFrame summarizing missing-value percentages per column.",
    "```python\nimport pandas as pd\n\nmissing_pct = df.isnull().mean() * 100\nprint(missing_pct.sort_values(ascending=False))\n```")

add("Create a column of cumulative counts within each group.",
    "```python\nimport pandas as pd\n\ndf['occurrence'] = df.groupby('user_id').cumcount() + 1\nprint(df.head())\n```")

add("Filter a DataFrame to rows in the top 10% of a column.",
    "```python\nimport pandas as pd\n\nthreshold = df['income'].quantile(0.9)\ntop = df[df['income'] >= threshold]\nprint(top)\n```")

add("Compute group-wise z-scores within each category.",
    "```python\nimport pandas as pd\n\ndf['z'] = df.groupby('category')['value'].transform(\n    lambda x: (x - x.mean()) / x.std())\nprint(df.head())\n```")

add("Replace outliers beyond 3 standard deviations with the mean.",
    "```python\nimport numpy as np\n\narr = np.array([1, 2, 3, 100, 4, 5])\nmean, std = arr.mean(), arr.std()\narr = np.where(np.abs(arr - mean) > 3 * std, mean, arr)\nprint(arr)\n```")

# ---------------------------------------------------------------------------
# MULTI-TURN CONVERSATIONS
# ---------------------------------------------------------------------------
add_multi([
    ("user", "Load sales.csv into a DataFrame."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = pd.read_csv('sales.csv')\nprint(df.head())\n```"),
    ("user", "Now show only rows where revenue is above 1000."),
    ("silicat", "```python\nhigh = df[df['revenue'] > 1000]\nprint(high)\n```"),
    ("user", "Group those by region and sum the revenue."),
    ("silicat", "```python\nresult = high.groupby('region')['revenue'].sum()\nprint(result)\n```"),
])

add_multi([
    ("user", "Read employees.csv."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = pd.read_csv('employees.csv')\nprint(df.head())\n```"),
    ("user", "Show only rows where age > 30."),
    ("silicat", "```python\nolder = df[df['age'] > 30]\nprint(older)\n```"),
    ("user", "Now group by city and average the salary."),
    ("silicat", "```python\nresult = older.groupby('city')['salary'].mean()\nprint(result)\n```"),
])

add_multi([
    ("user", "Create a numpy array from 1 to 10."),
    ("silicat", "```python\nimport numpy as np\n\narr = np.arange(1, 11)\nprint(arr)\n```"),
    ("user", "Reshape it into a 2x5 matrix."),
    ("silicat", "```python\nmat = arr.reshape(2, 5)\nprint(mat)\n```"),
    ("user", "Now compute the sum of each column."),
    ("silicat", "```python\nprint(mat.sum(axis=0))\n```"),
])

add_multi([
    ("user", "I have a DataFrame df with columns name, score. Sort it by score descending."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = df.sort_values('score', ascending=False)\nprint(df.head())\n```"),
    ("user", "Just give me the top 3."),
    ("silicat", "```python\nprint(df.head(3))\n```"),
    ("user", "Save those top 3 to top3.csv without the index."),
    ("silicat", "```python\ndf.head(3).to_csv('top3.csv', index=False)\n```"),
])

add_multi([
    ("user", "Make a random numpy array of shape (4, 4)."),
    ("silicat", "```python\nimport numpy as np\n\nnp.random.seed(0)\narr = np.random.rand(4, 4)\nprint(arr)\n```"),
    ("user", "Find the maximum value."),
    ("silicat", "```python\nprint(arr.max())\n```"),
    ("user", "And which position has it?"),
    ("silicat", "Use `argmax` with `unravel_index` to convert the flat index to row/column.\n\n```python\nimport numpy as np\n\npos = np.unravel_index(arr.argmax(), arr.shape)\nprint(pos)\n```"),
])

add_multi([
    ("user", "Load data.csv and tell me the shape."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = pd.read_csv('data.csv')\nprint(df.shape)\n```"),
    ("user", "How many missing values are in each column?"),
    ("silicat", "```python\nprint(df.isnull().sum())\n```"),
    ("user", "Drop all rows with any missing values."),
    ("silicat", "```python\ndf = df.dropna()\nprint(df.shape)\n```"),
])

add_multi([
    ("user", "I want to plot a histogram of the 'age' column in df."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\ndf['age'].plot(kind='hist', bins=20)\nplt.xlabel('Age')\nplt.show()\n```"),
    ("user", "Add a title and save it as ages.png."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\ndf['age'].plot(kind='hist', bins=20)\nplt.xlabel('Age')\nplt.title('Age distribution')\nplt.savefig('ages.png', dpi=300, bbox_inches='tight')\n```"),
])

add_multi([
    ("user", "Merge orders and customers on customer_id."),
    ("silicat", "```python\nimport pandas as pd\n\nmerged = pd.merge(orders, customers, on='customer_id')\nprint(merged.head())\n```"),
    ("user", "Now total the order amount per customer name."),
    ("silicat", "```python\nresult = merged.groupby('name')['amount'].sum()\nprint(result)\n```"),
    ("user", "Sort that from highest to lowest."),
    ("silicat", "```python\nprint(result.sort_values(ascending=False))\n```"),
])

add_multi([
    ("user", "Split X and y into train and test sets."),
    ("silicat", "```python\nfrom sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.25, random_state=42)\n```"),
    ("user", "Fit a linear regression on the training data."),
    ("silicat", "```python\nfrom sklearn.linear_model import LinearRegression\n\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\n```"),
    ("user", "Evaluate it on the test set with R squared."),
    ("silicat", "```python\nfrom sklearn.metrics import r2_score\n\ny_pred = model.predict(X_test)\nprint(r2_score(y_test, y_pred))\n```"),
])

add_multi([
    ("user", "Create a DataFrame with columns x and y, each 5 numbers."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 4, 5, 4, 6]})\nprint(df)\n```"),
    ("user", "What's the correlation between x and y?"),
    ("silicat", "```python\nprint(df['x'].corr(df['y']))\n```"),
    ("user", "Make a scatter plot of them."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\nplt.scatter(df['x'], df['y'])\nplt.xlabel('x')\nplt.ylabel('y')\nplt.show()\n```"),
])

add_multi([
    ("user", "Read transactions.csv with the date column parsed as dates."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = pd.read_csv('transactions.csv', parse_dates=['date'])\nprint(df.dtypes)\n```"),
    ("user", "Add a month column."),
    ("silicat", "```python\ndf['month'] = df['date'].dt.month\nprint(df.head())\n```"),
    ("user", "Now sum the amount per month."),
    ("silicat", "```python\nresult = df.groupby('month')['amount'].sum()\nprint(result)\n```"),
])

add_multi([
    ("user", "Make a 1D numpy array of 100 random normal values."),
    ("silicat", "```python\nimport numpy as np\n\nnp.random.seed(1)\narr = np.random.randn(100)\nprint(arr[:5])\n```"),
    ("user", "Standardize it to zero mean and unit std."),
    ("silicat", "```python\nstd = (arr - arr.mean()) / arr.std()\nprint(std.mean(), std.std())\n```"),
    ("user", "Plot a histogram of the standardized values."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\nplt.hist(std, bins=20)\nplt.show()\n```"),
])

add_multi([
    ("user", "I have df with a 'category' column. Show me the value counts."),
    ("silicat", "```python\nprint(df['category'].value_counts())\n```"),
    ("user", "Turn that into a bar chart."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\ndf['category'].value_counts().plot(kind='bar')\nplt.ylabel('Count')\nplt.show()\n```"),
    ("user", "Only show the top 5 categories."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\ndf['category'].value_counts().head(5).plot(kind='bar')\nplt.ylabel('Count')\nplt.show()\n```"),
])

add_multi([
    ("user", "Filter df where status == 'active'."),
    ("silicat", "```python\nactive = df[df['status'] == 'active']\nprint(active.shape)\n```"),
    ("user", "From those, keep only the email and signup_date columns."),
    ("silicat", "```python\nsubset = active[['email', 'signup_date']]\nprint(subset.head())\n```"),
    ("user", "Drop any rows where email is missing."),
    ("silicat", "```python\nsubset = subset.dropna(subset=['email'])\nprint(subset.shape)\n```"),
])

add_multi([
    ("user", "Compute the column means of a DataFrame df."),
    ("silicat", "```python\nprint(df.mean(numeric_only=True))\n```"),
    ("user", "Now the standard deviation per column too."),
    ("silicat", "```python\nprint(df.std(numeric_only=True))\n```"),
    ("user", "Combine both into one summary DataFrame."),
    ("silicat", "```python\nimport pandas as pd\n\nsummary = pd.DataFrame({\n    'mean': df.mean(numeric_only=True),\n    'std': df.std(numeric_only=True),\n})\nprint(summary)\n```"),
])

add_multi([
    ("user", "Create two numpy arrays a=[1,2,3] and b=[4,5,6]."),
    ("silicat", "```python\nimport numpy as np\n\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\n```"),
    ("user", "Compute their dot product."),
    ("silicat", "```python\nprint(np.dot(a, b))  # 32\n```"),
    ("user", "Now stack them into a 2x3 matrix."),
    ("silicat", "```python\nmat = np.vstack([a, b])\nprint(mat)\n```"),
])

add_multi([
    ("user", "Load iris.csv into pandas."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = pd.read_csv('iris.csv')\nprint(df.head())\n```"),
    ("user", "Get describe() grouped by species."),
    ("silicat", "```python\nprint(df.groupby('species').describe())\n```"),
    ("user", "Just the mean petal_length per species."),
    ("silicat", "```python\nprint(df.groupby('species')['petal_length'].mean())\n```"),
])

add_multi([
    ("user", "Build a DataFrame of monthly sales for 12 months."),
    ("silicat", "```python\nimport pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'month': range(1, 13),\n    'sales': np.random.randint(100, 500, 12),\n})\nprint(df)\n```"),
    ("user", "Plot sales as a line chart."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\nplt.plot(df['month'], df['sales'], marker='o')\nplt.xlabel('Month')\nplt.ylabel('Sales')\nplt.show()\n```"),
    ("user", "Add a 3-month rolling average line to the same plot."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\ndf['rolling'] = df['sales'].rolling(3).mean()\nplt.plot(df['month'], df['sales'], marker='o', label='sales')\nplt.plot(df['month'], df['rolling'], label='3-mo avg')\nplt.legend()\nplt.show()\n```"),
])

add_multi([
    ("user", "I have a numpy matrix M. Get its shape."),
    ("silicat", "```python\nprint(M.shape)\n```"),
    ("user", "Transpose it."),
    ("silicat", "```python\nprint(M.T)\n```"),
    ("user", "Multiply M by its transpose."),
    ("silicat", "```python\nprint(M @ M.T)\n```"),
])

add_multi([
    ("user", "Filter df to age between 20 and 40."),
    ("silicat", "```python\nsubset = df[df['age'].between(20, 40)]\nprint(subset.shape)\n```"),
    ("user", "Count how many are in each gender."),
    ("silicat", "```python\nprint(subset['gender'].value_counts())\n```"),
    ("user", "Average income by gender for this group."),
    ("silicat", "```python\nprint(subset.groupby('gender')['income'].mean())\n```"),
])

add_multi([
    ("user", "Read scores.csv."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = pd.read_csv('scores.csv')\nprint(df.head())\n```"),
    ("user", "Add a pass/fail column: pass if score >= 50."),
    ("silicat", "```python\nimport numpy as np\n\ndf['result'] = np.where(df['score'] >= 50, 'pass', 'fail')\nprint(df.head())\n```"),
    ("user", "What fraction passed?"),
    ("silicat", "```python\nprint((df['result'] == 'pass').mean())\n```"),
])

add_multi([
    ("user", "Generate X with 100 samples and 3 features, plus a target y."),
    ("silicat", "```python\nimport numpy as np\n\nnp.random.seed(0)\nX = np.random.rand(100, 3)\ny = X @ np.array([1.5, -2.0, 0.5]) + np.random.randn(100) * 0.1\n```"),
    ("user", "Fit a linear regression and show the coefficients."),
    ("silicat", "```python\nfrom sklearn.linear_model import LinearRegression\n\nmodel = LinearRegression().fit(X, y)\nprint(model.coef_)\n```"),
    ("user", "How good is the fit?"),
    ("silicat", "```python\nprint(model.score(X, y))  # R^2 on training data\n```"),
])

add_multi([
    ("user", "Make a pivot table of average price by product and region."),
    ("silicat", "```python\nimport pandas as pd\n\npivot = df.pivot_table(index='product', columns='region',\n                       values='price', aggfunc='mean')\nprint(pivot)\n```"),
    ("user", "Fill any missing cells with 0."),
    ("silicat", "```python\npivot = pivot.fillna(0)\nprint(pivot)\n```"),
])

add_multi([
    ("user", "Concatenate df_jan and df_feb into one DataFrame."),
    ("silicat", "```python\nimport pandas as pd\n\ndf = pd.concat([df_jan, df_feb], ignore_index=True)\nprint(df.shape)\n```"),
    ("user", "Drop any exact duplicate rows."),
    ("silicat", "```python\ndf = df.drop_duplicates()\nprint(df.shape)\n```"),
    ("user", "Now total the amount column."),
    ("silicat", "```python\nprint(df['amount'].sum())\n```"),
])

add_multi([
    ("user", "Create a numpy array of 20 evenly spaced points from 0 to 2*pi."),
    ("silicat", "```python\nimport numpy as np\n\nx = np.linspace(0, 2 * np.pi, 20)\nprint(x)\n```"),
    ("user", "Compute the sine of each."),
    ("silicat", "```python\ny = np.sin(x)\nprint(y)\n```"),
    ("user", "Plot x against y."),
    ("silicat", "```python\nimport matplotlib.pyplot as plt\n\nplt.plot(x, y)\nplt.xlabel('x')\nplt.ylabel('sin(x)')\nplt.show()\n```"),
])

# Write JSONL
import os
out_path = '/home/user/Silicat/data/synth/datasci.jsonl'
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w') as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + '\n')

print(f"Wrote {len(examples)} examples to {out_path}")
