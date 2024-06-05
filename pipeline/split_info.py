import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from azureml.core import Run
from pathlib import Path


def main(args):

    # Iniciar la ejecución de Azure ML
    run = Run.get_context()
    # Cargar datos
    data = pd.read_csv(args.input_data)

    # Dividir datos en entrenamiento y prueba
    train, test = train_test_split(data, test_size=0.2, random_state=42)

    train_df = train.to_csv((Path(args.output_path)/"train.csv"), index=False)
    test_df = test.to_csv((Path(args.output_path)/"test.csv"), index=False)

    # Registrar métricas
    run.log("Train Dataset Size", len(train))
    run.log("Test Dataset Size", len(test))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data', type=str,
                        help='Ruta al archivo de datos de entrada')
    parser.add_argument('--output_path', type=str,
                        help='Directorio de salida para el conjunto de datos')
    # parser.add_argument('--output_test', type=str,
    #                    help='Directorio de salida para el conjunto de datos')
    args = parser.parse_args()
    main(args)
