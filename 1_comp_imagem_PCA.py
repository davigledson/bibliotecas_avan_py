import numpy as np
import cv2
import os
import time
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as ssim


def print_stats(image, title):
    """Exibe estatísticas da imagem"""
    print(f"\n{title}:")
    print(f"- Dimensões: {image.shape}")
    print(f"- Tamanho na memória: {image.nbytes / 1024:.2f} KB")
    print(f"- Valor mínimo: {np.min(image):.4f}, máximo: {np.max(image):.4f}")
    print(f"- Média: {np.mean(image):.4f}, Desvio padrão: {np.std(image):.4f}")


def pca_compress(image_path, k_components=50):
    """Pipeline completo de compressão por PCA com métricas"""

    # Inicia contagem de tempo total
    start_time = time.time()

    # Passo 1: Carregamento e pré-processamento
    load_time = time.time()
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Imagem não encontrada em {image_path}")

    original_size = os.path.getsize(image_path) / 1024  # KB
    original_shape = image.shape

    # Normaliza para [0, 1]
    image = image.astype(np.float32) / 255.0
    load_time = time.time() - load_time

    print_stats(image, "IMAGEM ORIGINAL")
    print(f"- Tamanho do arquivo: {original_size:.2f} KB")
    print(f"- Tempo de carregamento: {load_time:.4f} segundos")

    # Passo 2: Cálculo da matriz de covariância
    cov_time = time.time()
    mean = np.mean(image, axis=0)
    centered_image = image - mean
    cov_matrix = np.cov(centered_image, rowvar=False)
    cov_time = time.time() - cov_time

    print(f"\nMatriz de covariância calculada em {cov_time:.4f} segundos")
    print(f"- Dimensões da matriz: {cov_matrix.shape}")

    # Passo 3: Decomposição em autovalores/autovetores
    eigen_time = time.time()
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # Converter para números reais (ignorando parte imaginária se existir)
    eigenvalues = np.real(eigenvalues)
    eigenvectors = np.real(eigenvectors)

    sorted_idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_idx]
    eigenvectors = eigenvectors[:, sorted_idx]
    eigen_time = time.time() - eigen_time

    print(f"\nDecomposição eigen concluída em {eigen_time:.4f} segundos")
    print(f"- Autovalor máximo: {eigenvalues[0]:.2f}, mínimo: {eigenvalues[-1]:.2f}")

    # Passo 4: Seleção de componentes principais
    select_time = time.time()
    components = eigenvectors[:, :k_components]

    # Calcula variância explicada
    explained_variance = np.sum(eigenvalues[:k_components]) / np.sum(eigenvalues)
    select_time = time.time() - select_time

    print(f"\nSelecionados {k_components} componentes em {select_time:.4f} segundos")
    print(f"- Variância explicada: {explained_variance * 100:.2f}%")

    # Passo 5: Reconstrução da imagem
    recon_time = time.time()
    projected = np.dot(centered_image, components)
    reconstructed = np.dot(projected, components.T) + mean
    reconstructed = np.clip(reconstructed, 0, 1)
    recon_time = time.time() - recon_time

    # Garante que a imagem reconstruída é real
    reconstructed = np.real(reconstructed)

    # Calcula tamanho teórico comprimido (em KB)
    compressed_size = (components.size + projected.size) * 4 / 1024  # float32 = 4 bytes

    print_stats(reconstructed, "IMAGEM COMPRIMIDA")
    print(f"- Tamanho teórico comprimido: {compressed_size:.2f} KB")
    print(f"- Razão de compressão: {original_size / compressed_size:.2f}x")
    print(f"- Tempo de reconstrução: {recon_time:.4f} segundos")

    # Cálculo de métricas de qualidade
    quality_time = time.time()
    mse = np.mean((image - reconstructed) ** 2)
    psnr = 10 * np.log10(1.0 / mse) if mse != 0 else float('inf')
    ssim_val = ssim(image, reconstructed, data_range=1.0)
    quality_time = time.time() - quality_time

    print(f"\nMÉTRICAS DE QUALIDADE (calculadas em {quality_time:.4f} segundos):")
    print(f"- MSE: {mse:.6f}")
    print(f"- PSNR: {psnr:.2f} dB")
    print(f"- SSIM: {ssim_val:.4f}")

    # Visualização
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title(f'Original\n{original_shape} | {original_size:.2f} KB')

    plt.subplot(1, 3, 2)
    plt.imshow(reconstructed, cmap='gray')
    plt.title(f'Comprimida (k={k_components})\n{compressed_size:.2f} KB | {explained_variance * 100:.1f}% var.')

    plt.subplot(1, 3, 3)
    plt.plot(np.cumsum(eigenvalues) / np.sum(eigenvalues))
    plt.axvline(k_components, color='r', linestyle='--')
    plt.title('Variância Explicada Cumulativa')
    plt.xlabel('Nº Componentes')
    plt.ylabel('Variância Explicada')

    plt.tight_layout()
    plt.show()

    total_time = time.time() - start_time
    print(f"\nPROCESSO CONCLUÍDO EM {total_time:.2f} SEGUNDOS")

    return reconstructed


# Execução principal
if __name__ == "__main__":
    # Configurações
    IMAGE_PATH = 'imgs/kelry.jpeg'  # Substitua pelo seu caminho
    K_COMPONENTS = 100  # Componentes principais

    # Executa a compressão
    compressed_image = pca_compress(IMAGE_PATH, K_COMPONENTS)

    # Salva a imagem reconstruída
    cv2.imwrite('imgs_comp/compressed_PCA.jpg', (compressed_image * 255).astype(np.uint8))