import pandas as pd
import scipy as sp

# Create a simple pandas DataFrame
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6]
}
df = pd.DataFrame(data)

# Print the DataFrame
print("DataFrame:")
print(df)

# Perform a simple operation using scipy
x = sp.linspace(0, 10, 5)
print("Linspace using scipy:")
print(x)
