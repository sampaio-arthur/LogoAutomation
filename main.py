from PIL import Image, ImageDraw
import os

def add_watermark(input_image_path, output_image_path, watermark, position='bottom_right', displacement=(0, 0)):
    try:
        # Abrir a imagem base e a logo
        base_image = Image.open(input_image_path).convert("RGBA")
        watermark_image = Image.open(watermark).convert("RGBA")
        
        # Redimensionar a logo (ajuste conforme necessário)
        width_ratio = base_image.size[0] / watermark_image.size[0]
        watermark_image = watermark_image.resize(
            (int(watermark_image.size[0] * width_ratio / 2), 
             int(watermark_image.size[1] * width_ratio / 2)), 
            Image.Resampling.LANCZOS
        )

        # Cria uma nova imagem transparente para combinar a logo
        transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
        transparent.paste(base_image, (0, 0))
        
        # Definir posição da marca d'água
        watermark_width, watermark_height = watermark_image.size
        base_width, base_height = base_image.size
        
        if position == 'top_left':
            position = (10 + displacement[0], 10 + displacement[1])
        elif position == 'top_right':
            position = (base_width - watermark_width - 10 + displacement[0], 50 + displacement[1])
        elif position == 'bottom_left':
            position = (10 + displacement[0], base_height - watermark_height - 10 + displacement[1])
        elif position == 'bottom_right':
            position = (base_width - watermark_width + displacement[0], base_height - watermark_height + displacement[1])
        elif position == 'center':
            position = ((base_width - watermark_width) // 2 + displacement[0], 
                        (base_height - watermark_height) // 2 + displacement[1])
        else:
            raise ValueError(f"Posição inválida: {position}")

        # Adicionar a marca d'água na posição calculada
        transparent.paste(watermark_image, position, mask=watermark_image)
        
        # Converter para RGB antes de salvar
        transparent = transparent.convert("RGB")

        # Salvar a imagem com a marca d'água
        transparent.save(output_image_path)
        print(f"Imagem salva com sucesso em: {output_image_path}")
    except Exception as e:
        print(f"Erro ao processar a imagem {input_image_path}: {e}")

# Definir pastas e caminho das marcas d'água
input_folder = r"H:/Meu Drive/MATERIAIS SAMPAIO/Fotos/zFotosParaEnviar/Entrada"
output_folder = r"H:/Meu Drive/MATERIAIS SAMPAIO/Fotos/zFotosParaEnviar/Saida"

watermark_image_1 = r'H:/Meu Drive/MATERIAIS SAMPAIO/LogosVinhetas/Teste2.png'
watermark_image_2 = r'H:/Meu Drive/MATERIAIS SAMPAIO/LogosVinhetas/V.png'

# Criar a pasta de saída se não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Processar todas as imagens na pasta de entrada
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename)
        
        # Aplicar a primeira marca d'água (ajustar deslocamento conforme necessário)
        add_watermark(input_image_path, output_image_path, watermark_image_1, position='bottom_right', displacement=(300, 800))
        
        # Aplicar a segunda marca d'água (ajustar deslocamento conforme necessário)
        add_watermark(output_image_path, output_image_path, watermark_image_2, position='bottom_right', displacement=(-2600, -1800))
    else:
        print(f"Formato de arquivo não suportado: {filename}")

print("Processamento concluído!")
