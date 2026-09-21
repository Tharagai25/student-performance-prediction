import os
import pandas as pd
import tensorflow as tf
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# 1. LOAD DATASET
# ============================================================

data = pd.read_csv("dataset/StudentPerformanceFactors.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)

print("\nColumns:")
print(data.columns.tolist())


# ============================================================
# 2. REMOVE UNNECESSARY COLUMNS
# ============================================================

# G3 is our target (final grade)
# G1 and G2 are previous/following grades and can cause data leakage
X = data.drop(["G3", "G1", "G2"], axis=1)

y = data["G3"]


print("\nTarget column: G3")
print("Input shape:", X.shape)
print("Target shape:", y.shape)


# ============================================================
# 3. FIND NUMERICAL AND CATEGORICAL COLUMNS
# ============================================================

numerical_columns = X.select_dtypes(
    include=["int64", "float64"]
).columns

categorical_columns = X.select_dtypes(
    include=["object"]
).columns


print("\nNumerical columns:")
print(list(numerical_columns))

print("\nCategorical columns:")
print(list(categorical_columns))


# ============================================================
# 4. DATA PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_columns
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_columns
        )
    ]
)


# ============================================================
# 5. TRANSFORM DATA
# ============================================================

X_processed = preprocessor.fit_transform(X)

print("\nPreprocessing completed!")
print("Processed data shape:", X_processed.shape)


# ============================================================
# 6. TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_processed,
    y,
    test_size=0.2,
    random_state=42
)


print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# ============================================================
# 7. BUILD DEEP LEARNING MODEL
# ============================================================

model = tf.keras.Sequential([

    tf.keras.layers.Input(
        shape=(X_train.shape[1],)
    ),

    tf.keras.layers.Dense(
        128,
        activation="relu"
    ),

    tf.keras.layers.Dense(
        64,
        activation="relu"
    ),

    tf.keras.layers.Dense(
        32,
        activation="relu"
    ),

    tf.keras.layers.Dense(
        1
    )
])


# ============================================================
# 8. COMPILE MODEL
# ============================================================

model.compile(
    optimizer="adam",
    loss="mse",
    metrics=["mae"]
)


print("\nDeep Learning model created successfully!")

model.summary()


# ============================================================
# 9. TRAIN MODEL
# ============================================================

print("\nTraining started...\n")

history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=50,
    batch_size=32,
    verbose=1
)


# ============================================================
# 10. PREDICTION
# ============================================================

y_pred = model.predict(X_test)

y_pred = y_pred.flatten()


# ============================================================
# 11. MODEL EVALUATION
# ============================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)


print("\n===================================")
print("MODEL EVALUATION")
print("===================================")

print("MAE  :", mae)
print("MSE  :", mse)
print("RMSE :", rmse)
print("R2   :", r2)


# ============================================================
# 12. CREATE MODEL FOLDER
# ============================================================

os.makedirs(
    "model",
    exist_ok=True
)


# ============================================================
# 13. SAVE DEEP LEARNING MODEL
# ============================================================

model.save(
    "model/student_model.keras"
)


# ============================================================
# 14. SAVE PREPROCESSOR
# ============================================================

joblib.dump(
    preprocessor,
    "model/preprocessor.pkl"
)


# ============================================================
# 15. FINAL MESSAGE
# ============================================================

print("\n===================================")
print("TRAINING COMPLETED SUCCESSFULLY!")
print("===================================")

print("\nSaved files:")

print("1. model/student_model.keras")
print("2. model/preprocessor.pkl")

print("\nStudent Performance Prediction model is ready!")