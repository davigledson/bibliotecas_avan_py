import numpy as np
import cv2
import os
import time
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim


def print_stats(image, title, original_size=None):
    """
    Exibe estatísticas detalhadas da imagem no terminal
    :param image: imagem numpy array (pode ser original ou comprimida)
    :param title: título para identificar a imagem
    :param original_size: tamanho do arquivo original em KB (opcional)
    """
    # Cabeçalho com borda decorativa
    print(f"\n{'=' * 50}")
    print(f"{title.upper():^50}")
    print(f"{'=' * 50}")

    # Estatísticas básicas
    print(f"\n{' DADOS GERAIS ':-^50}")
    print(f"| {'Dimensões (HxW):':<25} | {str(image.shape):>20} |")
    print(f"| {'Tipo de dados:':<25} | {str(image.dtype):>20} |")

    mem_size = image.nbytes / 1024
    if original_size:
        ratio = original_size / mem_size if mem_size > 0 else 0
        print(f"| {'Tamanho do arquivo:':<25} | {original_size:>18.2f} KB |")
        print(f"| {'Tamanho na memória:':<25} | {mem_size:>18.2f} KB |")
        print(f"| {'Razão memória/arquivo:':<25} | {ratio:>18.2f}x |")
    else:
        print(f"| {'Tamanho na memória:':<25} | {mem_size:>18.2f} KB |")

    # Estatísticas de intensidade dos pixels
    print(f"\n{' DISTRIBUIÇÃO DE PIXELS ':-^50}")
    print(f"| {'Mínimo:':<25} | {np.min(image):>18.4f} |")
    print(f"| {'Máximo:':<25} | {np.max(image):>18.4f} |")
    print(f"| {'Média:':<25} | {np.mean(image):>18.4f} |")
    print(f"| {'Mediana:':<25} | {np.median(image):>18.4f} |")
    print(f"| {'Desvio padrão:':<25} | {np.std(image):>18.4f} |")

    # Histograma simplificado no terminal
    if len(image.shape) == 2:  # Apenas para imagens em tons de cinza
        hist, bins = np.histogram(image, bins=5)
        print(f"\n{' HISTOGRAMA (SIMPLIFICADO) ':-^50}")
        for i in range(len(hist)):
            bin_range = f"{bins[i]:.2f}-{bins[i + 1]:.2f}"
            bar = '■' * int(hist[i] / max(hist) * 30) if max(hist) > 0 else ''
            print(f"| {bin_range:<15} | {hist[i]:>8} pixels | {bar:<20} |")

    print(f"\n{'=' * 50}\n")


def dct_compress(image_path, quality=50, block_size=8, show_stats=True):
    """
    Implementa compressão de imagem usando DCT similar ao JPEG
    :param image_path: caminho para a imagem original
    :param quality: qualidade da compressão (1-100)
    :param block_size: tamanho do bloco para DCT (tipicamente 8)
    :param show_stats: mostra estatísticas detalhadas no terminal
    :return: imagem comprimida, razão de compressão, métricas de qualidade
    """
    start_time = time.time()

    # 1. Carregar imagem
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original_image is None:
        raise FileNotFoundError(f"Imagem não encontrada em {image_path}")

    original_size = os.path.getsize(image_path) / 1024  # Tamanho em KB
    original_image = original_image.astype(np.float32)
    height, width = original_image.shape

    if show_stats:
        print_stats(original_image, "Imagem Original", original_size)

    # 2. Definir matriz de quantização (standard JPEG luminance quantization table)
    Q = np.array([
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ], dtype=np.float32)

    # Ajustar qualidade (1-100)
    if quality < 1:
        quality = 1
    elif quality > 100:
        quality = 100

    if quality < 50:
        scaling_factor = 5000 / quality
    else:
        scaling_factor = 200 - 2 * quality

    Q = np.floor((Q * scaling_factor + 50) / 100)
    Q[Q < 1] = 1

    # 3. Processar a imagem em blocos
    compressed_image = np.zeros_like(original_image)

    for y in range(0, height - block_size + 1, block_size):
        for x in range(0, width - block_size + 1, block_size):
            # Extrair bloco
            block = original_image[y:y + block_size, x:x + block_size]

            # Subtrair 128 para centralizar em zero
            block -= 128

            # Aplicar DCT
            dct_block = cv2.dct(block)

            # Quantização
            quantized_block = np.round(dct_block / Q)

            # Reconstrução (inversa)
            reconstructed_block = quantized_block * Q
            idct_block = cv2.idct(reconstructed_block)

            # Adicionar 128 de volta
            compressed_image[y:y + block_size, x:x + block_size] = idct_block + 128

    # 4. Calcular métricas
    compressed_image = np.clip(compressed_image, 0, 255).astype(np.uint8)
    original_image_uint8 = np.clip(original_image, 0, 255).astype(np.uint8)

    # Calcular PSNR e SSIM
    psnr_value = psnr(original_image_uint8, compressed_image)
    ssim_value = ssim(original_image_uint8, compressed_image)
    compression_time = time.time() - start_time

    # 5. Mostrar estatísticas da imagem comprimida
    if show_stats:
        print_stats(compressed_image, "Imagem Comprimida", original_size)

        # Métricas adicionais
        print(f"{' MÉTRICAS DE QUALIDADE ':=^50}")
        print(f"| {'PSNR:':<25} | {psnr_value:>18.2f} dB |")
        print(f"| {'SSIM:':<25} | {ssim_value:>18.4f} |")
        print(f"| {'Tempo de compressão:':<25} | {compression_time:>18.2f} s |")

        # Cálculo da taxa de compressão
        compressed_size = os.path.getsize('compressed_dct.jpg') / 1024 if os.path.exists('compressed_dct.jpg') else 0
        if compressed_size > 0:
            print(f"| {'Taxa de compressão:':<25} | {(original_size / compressed_size):>18.2f}x |")
            print(f"| {'Redução de tamanho:':<25} | {(1 - (compressed_size / original_size)) * 100:>17.2f}% |")
        print(f"{'=' * 50}\n")

    # 6. Visualização
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(original_image_uint8, cmap='gray')
    plt.title('Original')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(compressed_image, cmap='gray')
    plt.title(f'Comprimida (Qualidade: {quality})')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # 7. Retornar resultados
    return {
        'compressed_image': compressed_image,
        'quality': quality,
        'psnr': psnr_value,
        'ssim': ssim_value,
        'block_size': block_size,
        'quantization_matrix': Q,
        'compression_time': compression_time,
        'original_size': original_size,
        'compressed_size': os.path.getsize('compressed_dct.jpg') / 1024 if os.path.exists('compressed_dct.jpg') else 0
    }



if __name__ == "__main__":
    # Configurações
    IMAGE_PATH = 'imgs/kelry.jpeg'  # caminho da sua imagem
    QUALITY = 10  # Qualidade desejada (1-100)

    # Executar compressão
    results = dct_compress(IMAGE_PATH, quality=QUALITY)

    # Salvar imagem comprimida
    cv2.imwrite('output/compressed_dct.jpg', results['compressed_image'])
    print("\nRESUMO FINAL:")
    print(f"- Qualidade configurada: {results['quality']}")
    print(f"- PSNR: {results['psnr']:.2f} dB (maior é melhor)")
    print(f"- SSIM: {results['ssim']:.4f} (1.0 = perfeito)")
    print(f"- Tempo de compressão: {results['compression_time']:.2f} segundos")
    if results['compressed_size'] > 0:
        print(f"- Tamanho original: {results['original_size']:.2f} KB")
        print(f"- Tamanho comprimido: {results['compressed_size']:.2f} KB")
        print(f"- Taxa de compressão: {results['original_size'] / results['compressed_size']:.2f}x")
        print(f"- Redução: {(1 - (results['compressed_size'] / results['original_size'])) * 100:.2f}%")
    print("\nProcesso concluído. Imagem comprimida salva como 'compressed_dct.jpg'")