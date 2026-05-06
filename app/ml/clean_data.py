import pandas as pd

# Load raw dataset
df = pd.read_csv("data.csv")

# -----------------------------
# 1. Basic cleaning
# -----------------------------
df["title"] = df["title"].fillna("").astype(str).str.lower().str.strip()
df["category"] = df["category"].fillna("").astype(str).str.strip()

# -----------------------------
# 2. Remove empty rows
# -----------------------------
df = df[df["title"] != ""]
df = df[df["category"] != ""]

# -----------------------------
# 3. Remove noise (very important)
# -----------------------------
noise_words = [
    "adjust balance", "init", "something", "help",
    "transfer", "withdraw", "change"
]

df = df[~df["title"].isin(noise_words)]

# -----------------------------
# 4. Fix wrong categories (domain knowledge)
# -----------------------------
category_corrections = {
    "petrol": "Transport",
    "bus": "Transport",
    "auto": "Transport",
    "uber": "Transport",
    "ola": "Transport",
    "snack": "Food & Drinks",
    "snacks": "Food & Drinks",
    "juice": "Food & Drinks",
    "biryani": "Food & Drinks",
}

df["category"] = df.apply(
    lambda row: category_corrections.get(row["title"], row["category"]),
    axis=1
)

# -----------------------------
# 5. Remove duplicates
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# 6. Save cleaned data
# -----------------------------
df.to_csv("cleaned_data.csv", index=False)

print("✅ Cleaned data saved as cleaned_data.csv")
print(df.head())