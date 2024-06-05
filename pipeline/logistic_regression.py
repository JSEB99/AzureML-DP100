import os
import glob
import argparse
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path


def main(args):
    # Cargar datos de entrenamiento
    # Utiliza glob para encontrar los archivos train.csv y test.csv en el directorio de entrada
    print(f"Directorio de entrada: {args.input_dir}")

    train_files = glob.glob(os.path.join(args.input_dir, "train.csv"))
    test_files = glob.glob(os.path.join(args.input_dir, "test.csv"))

    # Lee los archivos train.csv y test.csv si existen
    if train_files:
        data = pd.read_csv(train_files[0])
    else:
        raise FileNotFoundError(
            "No se encontró el archivo train.csv en el directorio de entrada.")

    if test_files:
        test = pd.read_csv(test_files[0])
    else:
        raise FileNotFoundError(
            "No se encontró el archivo test.csv en el directorio de entrada.")
    print(len(data), len(test))
    print(data.columns)
    print(data.head(2))
    print(test.columns)
    print(test.head(2))

    # Dividir en características (X) y etiqueta (y)
    X = data.drop(columns=['default.payment.next.month'])
    y = data['default.payment.next.month']

    # Crear y entrenar el modelo de regresión logística
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    X_test = test.drop(columns=['default.payment.next.month'])

    # Predecir los valores del conjunto de prueba
    y_pred = model.predict(X_test)
    predictions_df = pd.DataFrame(y_pred, columns=['predicciones'])

    # Guardar el modelo entrenado
    joblib_file = os.path.join(
        Path(args.output_dir)/"credit_model_logisticR.pkl")
    joblib.dump(model, joblib_file)

    # Guardar las predicciones
    predictions = predictions_df.to_csv(
        (Path(args.output_dir)/"predictions.csv"), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str,
                        help='Ruta al archivo de datos')
    parser.add_argument('--output_dir', type=str,
                        help='Directorio de salida para el modelo y predicciones')
    args = parser.parse_args()
    main(args)
