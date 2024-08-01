import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Carregando os dados
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Explorando os dados
print(train_data.head())
print(train_data.info())
print(train_data.describe())

# Limpeza e pré-processamento dos dados de treinamento
train_data['Age'].fillna(train_data['Age'].median(), inplace=True)
train_data['Embarked'].fillna(train_data['Embarked'].mode()[0], inplace=True)
train_data['Fare'].fillna(train_data['Fare'].median(), inplace=True)

# Transformando variáveis categóricas em numéricas
train_data = pd.get_dummies(train_data, columns=['Sex', 'Embarked'], drop_first=True)

# Selecionando recursos e alvo
X = train_data.drop(['Survived', 'Name', 'Ticket', 'Cabin', 'PassengerId'], axis=1)
y = train_data['Survived']

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Padronizando os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)

# Construindo o modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Avaliando o modelo
y_pred = model.predict(X_valid)
print(f'Acurácia: {accuracy_score(y_valid, y_pred)}')
print(f'Matriz de Confusão: \n{confusion_matrix(y_valid, y_pred)}')
print(f'Relatório de Classificação: \n{classification_report(y_valid, y_pred)}')

# Limpeza e pré-processamento dos dados de teste
test_data['Age'].fillna(test_data['Age'].median(), inplace=True)
test_data['Embarked'].fillna(test_data['Embarked'].mode()[0], inplace=True)
test_data['Fare'].fillna(test_data['Fare'].median(), inplace=True)

# Transformando variáveis categóricas em numéricas nos dados de teste
test_data = pd.get_dummies(test_data, columns=['Sex', 'Embarked'], drop_first=True)

# Selecionando os mesmos recursos utilizados no treinamento
X_submission = test_data.drop(['Name', 'Ticket', 'Cabin', 'PassengerId'], axis=1)
X_submission = scaler.transform(X_submission)

# Realizando previsões nos dados de teste
submission_predictions = model.predict(X_submission)

# Criando o arquivo de submissão
submission = pd.DataFrame({'PassengerId': test_data['PassengerId'], 'Survived': submission_predictions})
submission.to_csv('submission.csv', index=False)

print("Previsões salvas no arquivo submission.csv")
