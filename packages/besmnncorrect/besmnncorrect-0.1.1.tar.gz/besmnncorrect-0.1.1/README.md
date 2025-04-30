if __name__ == "__main__":
    # 示例用法
    dataA = pd.read_csv('./dataA.csv', header=None).values
    dataB = pd.read_csv('./dataB.csv', header=None).values

    aligner = BatchAlignerAdvanced(
        pca_components=0.99,
        init_strategy='mi_based',
        noise_scale='auto',
        max_iter=30,
        verbose_changes=True
    )

    batch1 = dataA[:, :-1].astype(np.float64)
    batch2 = dataB[:, :-1].astype(np.float64)
    final_weights, final_pairs = aligner.fit(batch1, batch2)
    adjusted_B, used_pairs = aligner.adjust_batch(batch1, batch2)

    print("\n=== 最终结果 ===")
    print(f"匹配对数: {len(final_pairs)}")
    print(f"权重范围: {np.min(final_weights):.2f}-{np.max(final_weights):.2f}")
    print(f"权重中位数: {np.median(final_weights):.2f}")
    print("前10个特征权重:", np.round(final_weights[:10], 2))
    print(final_pairs)
    pd.DataFrame(adjusted_B).to_csv('corrected_B02.csv', index=False, header=False)