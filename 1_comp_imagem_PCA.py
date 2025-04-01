"""
numpy: Para operações matemáticas e manipulação de arrays

cv2 (OpenCV): Para processamento de imagens

os: Para operações com sistema de arquivos

matplotlib.pyplot: Para visualização dos resultados

"""

import numpy as np
import cv2
import os
import matplotlib.pyplot as plt


def pca_compress(image_path, k_components=30, output_dir='output'):
    """Compressão de imagem com PCA e salvamento dos resultados"""

    # Criar diretório de saída
    os.makedirs(output_dir, exist_ok=True)

    # 1. Carregar a imagem
    #
    """
    IMREAD_GRAYSCALE converte a imagem para um único canal (intensidade de brilho), eliminando cores.

    O PCA trabalha com matrizes 2D, e imagens coloridas (RGB) teriam 3 canais (R, G, B), exigindo tratamento mais complexo.

    Compressão mais eficiente, já que escala de cinza reduz a dimensionalidade (1 canal vs. 3 do RGB).
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Imagem não encontrada em {image_path}")

    original_size = os.path.getsize(image_path)
    img_float = img.astype(np.float32) / 255.0  # Converte a imagem para float32 e normaliza os pixels para [0, 1]

    # 2. Calcular PCA (Análise de componente principal(PCA) )

    mean = np.mean(img_float, axis=0)  # Calcula a média de intensidade para cada coluna de pixels na imagem

    centered = img_float - mean  # Centraliza os dados subtraindo a média de cada coluna (preparação para PCA)

    cov = np.cov(centered,rowvar=False)  # Calcula matriz de covariância entre colunas (mostra como pixels variam conjuntamente)

    eigenvalues, eigenvectors = np.linalg.eig(cov)  # Obtém autovalores (importância) e autovetores (direções principais) da covariância

    eigenvectors = np.real(eigenvectors[:, np.argsort(-np.real(eigenvalues))])  # Ordena autovetores do mais para o menos importante

    components = eigenvectors[:,:k_components]  # Seleciona apenas os k autovetores mais significativos (componentes principais)

    scores = np.dot(centered,components)  # Transforma os dados originais para o novo espaço dimensional reduzido (projeção PCA)

    # 3. Salvar dados comprimidos
    compressed_path = os.path.join(output_dir, 'compressed_data.npz')
    np.savez_compressed(
        compressed_path,
        mean=mean.astype(np.float32),
        components=components.astype(np.float32),
        scores=scores.astype(np.float32),
        original_shape=img.shape
    )
    compressed_size = os.path.getsize(compressed_path)

    # 4. Reconstruir imagem
    reconstructed = np.dot(scores, components.T) + mean
    reconstructed = np.clip(reconstructed, 0, 1)
    reconstructed_img = (reconstructed * 255).astype(np.uint8)

    # 5. Salvar imagens para comparação
    reconstructed_path = os.path.join(output_dir, 'reconstructed_PCA.jpg')
    cv2.imwrite(reconstructed_path, reconstructed_img)

    original_path = os.path.join(output_dir, 'original.jpg')
    cv2.imwrite(original_path, img)

    # 6. Mostrar resultados
    print(f"\n{' RESULTADOS ':=^40}")
    print(f"Original: {original_size / 1024:.1f} KB")
    print(f"Comprimido: {compressed_size / 1024:.1f} KB")
    print(f"Taxa de compressão: {original_size / compressed_size:.1f}x")

    # 7. Plotar comparação
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(reconstructed, cmap='gray')
    plt.title(f'Comprimida (k={k_components})')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    explained_variance = np.cumsum(np.real(eigenvalues)) / np.sum(np.real(eigenvalues))
    plt.plot(explained_variance)
    plt.axvline(k_components, color='r', linestyle='--')
    plt.title('Variância Explicada')
    plt.xlabel('Componentes Principais')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison.png'))
    plt.show()

    return {
        'original': original_path,
        'compressed': compressed_path,
        'reconstructed': reconstructed_path
    }


# Exemplo de uso
if __name__ == "__main__":
    # Configurações
    input_image = 'imgs/img_P.jpg'
    components = 100  # Número de componentes principais

    # Executar compressão
    results = pca_compress(input_image, k_components=components)

    print("\nArquivos salvos em:")
    print(f"- Original: {results['original']}")
    print(f"- Dados comprimidos: {results['compressed']}")
    print(f"- Reconstruída: {results['reconstructed']}")