import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from scipy.stats import randint

# Carregar os dados
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Função para criar novas features
def create_features(df):
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    df['Title'] = df['Name'].apply(lambda name: name.split(',')[1].split('.')[0].strip())
    df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    df['Title'] = df['Title'].replace('Mlle', 'Miss')
    df['Title'] = df['Title'].replace('Ms', 'Miss')
    df['Title'] = df['Title'].replace('Mme', 'Mrs')
    
    # Additional Features
    df['AgeClass'] = df['Age'] * df['Pclass']
    df['FarePerPerson'] = df['Fare'] / (df['FamilySize'] + 1)
    df['Embarked'] = df['Embarked'].fillna('S')  # Fill missing values with the most common value in 'Embarked'
    
    return df

# Criar novas features nos dados de treinamento e teste
train_data = create_features(train_data)
test_data = create_features(test_data)

# Selecionar colunas relevantes
cols_to_use = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'FamilySize', 'IsAlone', 'Title', 'AgeClass', 'FarePerPerson']

# Separar os dados em features e target
X = train_data[cols_to_use]
y = train_data['Survived']

# Definir colunas categóricas e numéricas
categorical_cols = ['Sex', 'Embarked', 'Title']
numerical_cols = ['Age', 'SibSp', 'Parch', 'Fare', 'FamilySize', 'IsAlone', 'AgeClass', 'FarePerPerson']

# Pré-processamento de dados
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numerical_cols),
        ('cat', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_cols)
    ])

# Pipeline com o modelo
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Tuning de Hiperparâmetros usando RandomizedSearchCV
param_dist = {
    'classifier__n_estimators': randint(100, 500),
    'classifier__max_depth': [None, 10, 20, 30, 40],
    'classifier__min_samples_split': randint(2, 10),
    'classifier__min_samples_leaf': randint(1, 10),
    'classifier__bootstrap': [True, False]
}

random_search = RandomizedSearchCV(pipeline, param_distributions=param_dist, n_iter=50, cv=5, n_jobs=-1, verbose=2, random_state=42)
random_search.fit(X, y)

# Melhor modelo encontrado pelo RandomizedSearch
best_model = random_search.best_estimator_

# Avaliação do modelo
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
y_pred = best_model.predict(X_valid)
print(f'Acurácia: {accuracy_score(y_valid, y_pred)}')
print(f'Matriz de Confusão: \n{confusion_matrix(y_valid, y_pred)}')
print(f'Relatório de Classificação: \n{classification_report(y_valid, y_pred)}')

# Preparar os dados de teste e realizar previsões
test_data_transformed = best_model.predict(test_data[cols_to_use])

# Criar o arquivo de submissão
submission = pd.DataFrame({'PassengerId': test_data['PassengerId'], 'Survived': test_data_transformed})
submission.to_csv('submission.csv', index=False)

print("Previsões salvas no arquivo submission.csv")
