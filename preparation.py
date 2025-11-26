
import pandas as pd
import io
file_path = r'C:\Users\thant_6ntwleo\Downloads\vgsales (original).csv'
# df = pd.read_csv(io.BytesIO(uploaded['vgsales (original).csv']))

# --- Quick overview ---
print(df.shape)                          # (rows, cols)
print(df.columns.tolist())               # column names
display(df.head(3))                      # first rows
df.info()                                # dtypes + nulls
display(df.isna().sum())                 # missing per column

# --- Minimal cleaning ---
for c in df.columns:
    if df[c].dtype.kind in "if":         # numeric
        df[c] = df[c].fillna(df[c].median())
    else:                                # categorical
        if df[c].isna().any():
            df[c] = df[c].fillna(df[c].mode().iloc[0])

# --- Pick columns automatically ---
num_cols = df.select_dtypes("number").columns.tolist()
cat_cols = df.select_dtypes("object").columns.tolist()

# --- Three dead-simple charts (matplotlib only) ---

# 1) Histogram
if num_cols:
    plt.figure()
    df[num_cols[0]].plot(kind="hist", bins=30)
    plt.title(f"Distribution of {num_cols[0]}")
    plt.xlabel(num_cols[0])
    plt.ylabel("Count")
    plt.show()

# 2) Bar chart
if cat_cols:
    plt.figure()
    df[cat_cols[0]].value_counts().head(10).plot(kind="bar")
    plt.title(f"Top {cat_cols[0]} categories")
    plt.xlabel(cat_cols[0])
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.show()

# 3) Scatter
if len(num_cols) >= 2:
    plt.figure()
    plt.scatter(df[num_cols[0]], df[num_cols[1]], s=10)
    plt.title(f"{num_cols[0]} vs {num_cols[1]}")
    plt.xlabel(num_cols[0])
    plt.ylabel(num_cols[1])
    plt.show()
