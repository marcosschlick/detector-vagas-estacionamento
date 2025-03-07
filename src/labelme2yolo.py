import json
import os

# Caminhos
annotation_dir = "dataset/annotations_resized"
output_yolo_dir = "dataset/labels_yolo"

# Cria o diretório de saída se não existir
os.makedirs(output_yolo_dir, exist_ok=True)

# Tamanho das imagens redimensionadas (use o mesmo valor do primeiro script)
new_size = (640, 853)  # ou (480, 640)

# Função para converter JSON (LabelMe) para YOLO
def convert_labelme_to_yolo(annotation_dir, output_yolo_dir):
    for annotation_name in os.listdir(annotation_dir):
        if annotation_name.endswith(".json"):
            annotation_path = os.path.join(annotation_dir, annotation_name)
            with open(annotation_path, "r") as f:
                annotation = json.load(f)

            # Cria o arquivo YOLO
            yolo_file_path = os.path.join(output_yolo_dir, annotation_name.replace(".json", ".txt"))
            with open(yolo_file_path, "w") as f:
                for shape in annotation["shapes"]:
                    label = shape["label"]
                    points = shape["points"]

                    # Converte pontos para formato YOLO (x_center, y_center, width, height)
                    x_min = min(p[0] for p in points)
                    x_max = max(p[0] for p in points)
                    y_min = min(p[1] for p in points)
                    y_max = max(p[1] for p in points)

                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2
                    width = x_max - x_min
                    height = y_max - y_min

                    # Normaliza as coordenadas (0 a 1)
                    x_center /= new_size[0]
                    y_center /= new_size[1]
                    width /= new_size[0]
                    height /= new_size[1]

                    # Escreve no arquivo YOLO
                    f.write(f"{0 if label == 'vaga_livre' else 1} {x_center} {y_center} {width} {height}\n")

# Executa a função
convert_labelme_to_yolo(annotation_dir, output_yolo_dir)
print("Conversão para YOLO concluída!")