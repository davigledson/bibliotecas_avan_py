
""""tem que baixar o CUDA da NVIDIA"""
  # Importa a biblioteca PyTorch para computação tensorial com suporte a GPU

import torch  # Importa a biblioteca PyTorch para computação tensorial com suporte a GPU
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np


def pca_gpu_compress(image_path, k_components=30, output_dir='output_gpu'):
    """Compressão de imagem com PCA acelerado por GPU"""

    # Criar diretório de saída
    os.makedirs(output_dir, exist_ok=True)

    # 1. Carregar a imagem
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Imagem não encontrada em {image_path}")

    original_size = os.path.getsize(image_path)

    # 2. Converter para tensor GPU e normalizar
    img_tensor = torch.from_numpy(img.astype(np.float32)).cuda() / 255.0

    # 3. Calcular PCA na GPU
    mean = torch.mean(img_tensor, dim=0)
    centered = img_tensor - mean

    # PCA via SVD (otimizado para GPU)
    _, _, V = torch.pca_lowrank(centered, q=k_components)
    components = V[:, :k_components]
    scores = torch.matmul(centered, components)

    # 4. Salvar dados comprimidos (convertendo para CPU/numpy)
    compressed_path = os.path.join(output_dir, 'compressed_data.npz')
    np.savez_compressed(
        compressed_path,
        mean=mean.cpu().numpy().astype(np.float32),
        components=components.cpu().numpy().astype(np.float32),
        scores=scores.cpu().numpy().astype(np.float32),
        original_shape=img.shape
    )
    compressed_size = os.path.getsize(compressed_path)

    # 5. Reconstruir imagem
    reconstructed = torch.matmul(scores, components.T) + mean
    reconstructed = torch.clamp(reconstructed, 0, 1)
    reconstructed_img = (reconstructed.cpu().numpy() * 255).astype(np.uint8)

    # 6. Salvar imagens
    reconstructed_path = os.path.join(output_dir, 'reconstructed_PCA_GPU.jpg')
    cv2.imwrite(reconstructed_path, reconstructed_img)

    original_path = os.path.join(output_dir, 'original.jpg')
    cv2.imwrite(original_path, img)

    # 7. Mostrar resultados
    print(f"\n{' RESULTADOS GPU ':=^40}")
    print(f"Original: {original_size / 1024:.1f} KB")
    print(f"Comprimido: {compressed_size / 1024:.1f} KB")
    print(f"Taxa de compressão: {original_size / compressed_size:.1f}x")

    # 8. Plotar comparação
    eigenvalues = torch.sum(scores ** 2, dim=0) / (scores.shape[0] - 1)  # Autovalores aproximados

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(reconstructed_img, cmap='gray')
    plt.title(f'GPU Comprimida (k={k_components})')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    explained_variance = torch.cumsum(eigenvalues, dim=0) / torch.sum(eigenvalues)
    plt.plot(explained_variance.cpu().numpy())
    plt.axvline(k_components, color='r', linestyle='--')
    plt.title('Variância Explicada (GPU)')
    plt.xlabel('Componentes Principais')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_gpu.png'))
    plt.show()

    return {
        'original': original_path,
        'compressed': compressed_path,
        'reconstructed': reconstructed_path
    }


# Exemplo de uso
if __name__ == "__main__":
    # Verificar se GPU está disponível
    print(f"GPU disponível: {torch.cuda.is_available()}")

    # Configurações
    input_image = 'imgs/img_P.jpg'  # Substitua pelo seu caminho
    components = 100  # Número de componentes principais

    # Executar compressão
    results = pca_gpu_compress(input_image, k_components=components)

    print("\nArquivos salvos em:")
    print(f"- Original: {results['original']}")
    print(f"- Dados comprimidos: {results['compressed']}")
    print(f"- Reconstruída: {results['reconstructed']}")