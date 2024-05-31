import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from azureml.core import Run
import tempfile


def main(args):

    # Iniciar la ejecución de Azure ML
    run = Run.get_context()
    # Cargar datos
    data = pd.read_csv(args.input_data)
    # Obtener el directorio de salida específico para esta ejecución
    output_directory = os.path.join(
        run.get_output_data_reference().get_datastore().path, "outputs")

    # Dividir datos en entrenamiento y prueba
    train, test = train_test_split(data, test_size=0.2, random_state=42)

    # Crear directorios de salida si no existen
    # os.makedirs(args.output_train, exist_ok=True)
    # os.makedirs(args.output_test, exist_ok=True)

    # Crear un directorio temporal dentro del directorio de salida de entrenamiento
    # temp_dir = tempfile.mkdtemp(dir=args.output_dir)

    # Guardar los conjuntos de datos en el directorio temporal
    # train.to_csv(os.path.join(temp_dir, 'train.csv'), index=False)
    # test.to_csv(os.path.join(temp_dir, 'test.csv'), index=False)
    # Guardar los conjuntos de datos en Azure Blob Storage
    train_blob = run.upload_file(
        name=f'{output_directory}/train.csv', data=train.to_csv(index=False), overwrite=True)
    test_blob = run.upload_file(
        name=f'{output_directory}/test.csv', data=test.to_csv(index=False), overwrite=True)

    # Registrar métricas
    run.log("Train Dataset Size", len(train))
    run.log("Test Dataset Size", len(test))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_data', type=str,
                        help='Ruta al archivo de datos de entrada')
    # parser.add_argument('--output_train', type=str,
    #                    help='Directorio de salida para el conjunto de datos')
    # parser.add_argument('--output_test', type=str,
    #                    help='Directorio de salida para el conjunto de datos')
    args = parser.parse_args()
    main(args)
