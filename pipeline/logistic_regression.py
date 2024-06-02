import os
import argparse
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib


def main(args):
    # Cargar datos de entrenamiento
    data = pd.read_csv(f"{args.input_dir}/train.csv")

    # Dividir en características (X) y etiqueta (y)
    X = data.drop(columns=['default.payment.next.month'])
    y = data['default.payment.next.month']

    # Crear y entrenar el modelo de regresión logística
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    # Cargar datos de prueba
    test = pd.read_csv(f"{args.input_dir}/test.csv")
    X_test = test.drop(columns=['default.payment.next.month'])
    y_test = test['default.payment.next.month']

    # Predecir los valores del conjunto de prueba
    y_pred = model.predict(X_test)

    # Crear el directorio de salida si no existe
    os.makedirs(args.output_dir, exist_ok=True)

    # Guardar el modelo entrenado
    joblib_file = os.path.join(args.output_dir, "credit_model_logisticR.pkl")
    joblib.dump(model, joblib_file)

    # Guardar las predicciones
    predictions_file = os.path.join(args.output_dir, 'logistic_preds.csv')
    pd.DataFrame(y_pred, columns=['Predictions']).to_csv(
        predictions_file, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str,
                        help='Ruta al archivo de datos')
    parser.add_argument('--output_dir', type=str,
                        help='Directorio de salida para el modelo y predicciones')
    args = parser.parse_args()
    main(args)
