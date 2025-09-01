import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
import joblib
from training.train_utils import MODEL_PATH, MODEL_DIR, DATA_FILE_PATH


df = (
    pd.read_csv(DATA_FILE_PATH)
    .drop(columns=["name", "model", "edition"])
    .drop_duplicates()
)
X = df.drop(columns=["selling_price"])
y = df.selling_price.copy()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

num_cols = X_train.select_dtypes(include="number").columns.tolist()
cat_cols = [col for col in X_train.columns if col not in num_cols]

num_pipe = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
)

cat_pipe = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[("num", num_pipe, num_cols), ("cat", cat_pipe, cat_cols)]
)
preprocessor.fit_transform(X_train)

regressor = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)

rf_model = Pipeline(steps=[("pre", preprocessor), ("reg", regressor)])

rf_model.fit(X_train, y_train)

os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(rf_model, MODEL_PATH)
