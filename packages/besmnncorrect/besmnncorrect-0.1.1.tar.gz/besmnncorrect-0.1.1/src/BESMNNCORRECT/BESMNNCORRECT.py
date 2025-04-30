import numpy as np
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
import pandas as pd
import os
import random

os.environ["LOKY_MAX_CPU_COUNT"] = "10"


class BatchAlignerAdvanced:
    def __init__(self,
                 pca_components=0.95,
                 init_strategy='mi_based',
                 max_iter=30,
                 init_lr=0.8,
                 momentum=0.85,
                 noise_scale='auto',
                 anneal_rate=0.93,
                 l2_penalty=0.1,
                 random_ratio=0.1,h=3.5, k=5,
                 verbose_changes=True):

        self.pca_components = pca_components
        self.init_strategy = init_strategy
        self.max_iter = max_iter
        self.init_lr = init_lr
        self.momentum = momentum
        self.noise_scale = noise_scale
        self.anneal_rate = anneal_rate
        self.l2_penalty = l2_penalty
        self.random_ratio = random_ratio
        self.verbose_changes = verbose_changes
        self.k = k
        self.h = h

        # 运行时的中间状态
        self.scaler = None
        self.weights = None
        self.best = None
        self.velocity = None
        self.prev_pairs = None
        self.noise_history = []
        self.last_low1 = None
        self.last_low2 = None

    def fit(self, batch1_raw, batch2_raw):
        # ========== 初始化阶段 ==========
        self.scaler = StandardScaler().fit(np.vstack([batch1_raw, batch2_raw]))
        batch1 = self.scaler.transform(batch1_raw)
        batch2 = self.scaler.transform(batch2_raw)
        n_samples = len(batch1) + len(batch2)

        # === 智能权重初始化 ===
        n_features = batch1.shape[1]
        self.weights = self._initialize_weights(batch1_raw, batch2_raw, n_features)

        # === 优化状态初始化 ===
        self.best = {
            'weights': self.weights.copy(),
            'pairs': np.empty((0, 2), dtype=int),
            'score': -np.inf
        }
        self.velocity = np.zeros(n_features)
        self.prev_pairs = None
        self.noise_history = []

        # === 自动噪声参数 ===
        self.noise_params = {
            'min_noise': 0.05,
            'max_noise': 0.3,
            'adjust_rate': 0.15,
            'stability_threshold': 0.75
        }
        self.base_noise = self._get_base_noise(n_samples)

        # ========== 迭代优化 ==========
        stability_rounds = int(0.8 * self.max_iter)
        for iter in range(self.max_iter):
            current_noise = self._self_adapt_noise(iter, self.best['score'],
                                                   len(self.prev_pairs) if self.prev_pairs is not None else 0)

            # 应用噪声和降维
            noisy_weights = self._apply_noise(current_noise)
            low1, low2, explained_var = self._dimension_reduction(batch1, batch2, noisy_weights)

            # 进行匹配
            pairs = self._diversified_mnn(low1, low2, iter)

            # 更新最佳状态
            current_score = self._update_best_state(pairs, noisy_weights)

            # 动量更新权重
            self._momentum_update(batch1, batch2, pairs, iter)

            # 收敛检查
            if iter > stability_rounds and self._check_convergence(pairs):
                if self.verbose_changes:
                    print(f"提前终止于迭代 {iter + 1}，稳定性 {self._check_convergence(pairs):.2f}")
                break

            # 日志输出
            self._log_iteration(iter, pairs, current_noise, explained_var, current_score)
        self.last_low1, self.last_low2, _ = self._dimension_reduction(
            batch1, batch2, self.best['weights'])
        return self.best['weights'], self.best['pairs']

    # ========== 内部方法 ==========
    def _initialize_weights(self, batch1_raw, batch2_raw, n_features):
        if self.init_strategy == 'fixed':
            return np.random.uniform(0.5, 1.5, n_features)
        elif self.init_strategy == 'adaptive':
            return self._adaptive_init(batch1_raw, batch2_raw)
        elif self.init_strategy == 'mi_based':
            return self._mi_based_init(batch1_raw, batch2_raw)
        else:
            raise ValueError(f"无效初始化策略: {self.init_strategy}")

    def _adaptive_init(self, batch1_raw, batch2_raw):
        raw_combined = np.vstack([batch1_raw, batch2_raw])
        feature_std = np.std(raw_combined, axis=0)
        q = np.quantile(feature_std, [0.2, 0.8])
        ranges = []
        for std in feature_std:
            if std < q[0]:
                ranges.append((0.8, 1.2))
            elif std > q[1]:
                ranges.append((0.2, 2.0))
            else:
                ranges.append((0.5, 1.5))
        return np.array([np.random.uniform(low, high) for (low, high) in ranges])

    def _mi_based_init(self, batch1_raw, batch2_raw):
        mi_scores = self._mutual_info_analysis(batch1_raw, batch2_raw)
        quantiles = np.quantile(mi_scores, [0.25, 0.75])
        ranges = []
        for score in mi_scores:
            if score < quantiles[0]:
                ranges.append((0.9, 1.1))
            elif score > quantiles[1]:
                ranges.append((0.1, 3.0))
            else:
                ranges.append((0.6, 1.4))
        return np.array([np.random.uniform(low, high) for (low, high) in ranges])

    def _get_base_noise(self, n_samples):
        if self.noise_scale == 'auto':
            return 0.2 * np.log(n_samples / 1000 + 1) + 0.5
        else:
            self.noise_params.update({
                'min_noise': self.noise_scale * 0.3,
                'max_noise': self.noise_scale * 1.7
            })
            return self.noise_scale

    def _self_adapt_noise(self, iter, best_score, current_pairs):
        noise = self.base_noise * (0.6 ** iter)
        if self.noise_scale != 'auto':
            return np.clip(noise, self.noise_params['min_noise'], self.noise_params['max_noise'])

        if iter > 0 and best_score > 0:
            if current_pairs < best_score * 0.8:
                noise = min(noise * (1 + self.noise_params['adjust_rate'] * 2),
                            self.noise_params['max_noise'])
            elif current_pairs > best_score * self.noise_params['stability_threshold']:
                noise = max(noise * (1 - self.noise_params['adjust_rate']),
                            self.noise_params['min_noise'])

        if iter > self.max_iter // 2:
            decay = 1 - (iter / self.max_iter) ** 2
            noise *= decay

        return np.clip(noise, self.noise_params['min_noise'], self.noise_params['max_noise'])

    def _apply_noise(self, current_noise):
        noise = np.exp(current_noise * np.random.randn(len(self.weights)))
        return np.clip(self.weights * noise, 0.2, 2.0)

    def _dimension_reduction(self, batch1, batch2, weights):
        w_batch1 = batch1 * weights
        w_batch2 = batch2 * weights
        pca = PCA(n_components=self.pca_components).fit(np.vstack([w_batch1, w_batch2]))
        return (
            pca.transform(w_batch1),
            pca.transform(w_batch2),
            np.sum(pca.explained_variance_ratio_)
        )

    def _diversified_mnn(self, low1, low2, iter):
        base_pairs = self._find_mutual_nn(low1, low2)
        return self._diversify_pairs(base_pairs, low1, low2, iter)

    def _update_best_state(self, pairs, noisy_weights):
        stability = self._check_stability(self.best['pairs'], pairs) if self.best['pairs'].size > 0 else 0.0
        current_score = len(pairs) * (1 + stability)

        if current_score > self.best['score']:
            self.best['weights'] = noisy_weights.copy()
            self.best['pairs'] = pairs.copy()
            self.best['score'] = current_score
        return current_score

    def _momentum_update(self, batch1, batch2, pairs, iter):
        bes = self._compute_bes(batch1, batch2, pairs)
        gradient = bes / (np.abs(bes).max() + 1e-6)
        gradient -= self.l2_penalty * self.weights
        self.velocity = self.momentum * self.velocity + (1 - self.momentum) * gradient
        self.weights += self.init_lr * (self.anneal_rate ** iter) * self.velocity

    def _check_convergence(self, pairs):
        if self.best['pairs'].size == 0:
            return False
        stability = self._check_stability(self.best['pairs'], pairs)
        return stability > 0.8

    def adjust_batch(self, batch1_raw, batch2_raw, k=None, h=None):
        """ 执行批次调整的后处理步骤 """
        # 参数处理
        k = k if k is not None else self.k
        h = h if h is not None else self.h

        # 数据标准化
        batch1 = self.scaler.transform(batch1_raw)
        batch2 = self.scaler.transform(batch2_raw)
        pairb = self.best['pairs']

        if len(pairb) == 0:
            raise ValueError("无互为最近邻对，无法调整。")

        # === 特征差异计算 ===
        batch2_paired_indices = pairb[:, 1]
        paired_batch1 = batch1[pairb[:, 0]]
        paired_batch2 = batch2[batch2_paired_indices]
        deltas = paired_batch1 - paired_batch2

        # === 经验贝叶斯估计 ===
        m_j = deltas.mean(axis=0)
        s_j_sq = deltas.var(axis=0, ddof=1)
        mu_prior = m_j.mean()
        tau_sq = max(m_j.var() - s_j_sq.mean() / len(pairb), 1e-6)  # 防止负值

        n = len(pairb)
        mu_post = (m_j * n / s_j_sq + mu_prior / tau_sq) / (n / s_j_sq + 1 / tau_sq)
        adjusted_deltas = deltas - m_j.reshape(1, -1) + mu_post.reshape(1, -1)

        # === 批次调整 ===
        adjusted_batch2 = batch2.copy()

        # 处理已匹配样本
        unique_indices, counts = np.unique(batch2_paired_indices, return_counts=True)
        for idx, count in zip(unique_indices, counts):
            mask = (batch2_paired_indices == idx)
            avg_delta = adjusted_deltas[mask].mean(axis=0)
            adjusted_batch2[idx] += avg_delta

        # 处理未匹配样本（需要降维后的数据）
        non_paired = np.setdiff1d(np.arange(len(batch2)), batch2_paired_indices)
        if len(non_paired) > 0 and self.last_low2 is not None:
            paired_low = self.last_low2[batch2_paired_indices]
            k_actual = min(k, len(paired_low))
            if k_actual > 0:
                nbrs = NearestNeighbors(n_neighbors=k_actual).fit(paired_low)

                for j in non_paired:
                    current = self.last_low2[j].reshape(1, -1)
                    dists, indices = nbrs.kneighbors(current)
                    selected = adjusted_deltas[indices.flatten()]

                    weights = np.exp(-dists.flatten() ** 2 / (2 * h ** 2))
                    weighted = np.average(selected, axis=0, weights=weights)
                    adjusted_batch2[j] += weighted

        # 逆标准化
        adjusted_batch2_original = self.scaler.inverse_transform(adjusted_batch2)
        return adjusted_batch2_original, pairb

    def _log_iteration(self, iter, pairs, current_noise, explained_var, current_score):
        if not self.verbose_changes:
            return

        change_info = ""
        if self.prev_pairs is not None and len(self.prev_pairs) > 0:
            prev_set = {tuple(pair) for pair in self.prev_pairs}
            current_set = {tuple(pair) for pair in pairs}
            added = sorted(current_set - prev_set, key=lambda x: (x[0], x[1]))
            removed = sorted(prev_set - current_set, key=lambda x: (x[0], x[1]))
            change_info = f"Δ+{len(added)}/Δ-{len(removed)}"
        else:
            change_info = "Δ+0/Δ-0"

        print(f"Iter {iter + 1}: pairs={len(pairs)} ({change_info}) "
              f"best={len(self.best['pairs'])}, noise={current_noise:.3f}, "
              f"lr={self.init_lr * (self.anneal_rate ** iter):.3f}, "
              f"explained_var={explained_var:.1%}, score={current_score:.1f}")

    # ========== 静态方法 ==========
    @staticmethod
    def _mutual_info_analysis(batch1, batch2):
        combined = np.vstack([batch1, batch2])
        labels = np.concatenate([np.zeros(len(batch1)), np.ones(len(batch2))])
        mi_scores = []
        for g in range(combined.shape[1]):
            mi = mutual_info_classif(combined[:, g].reshape(-1, 1), labels,
                                     discrete_features=False, n_neighbors=5)[0]
            mi_scores.append(mi)
        return np.array(mi_scores)

    @staticmethod
    def _diversify_pairs(base_pairs, low1, low2, iter):
        # 原始diversified_mnn的具体实现
        base_ratio = 1
        random_ratio = 0.1 * (1 - iter / 30)
        n_base = int(base_ratio * len(base_pairs))
        base_selected = base_pairs[:n_base]
        used_i = set(base_selected[:, 0])
        used_j = set(base_selected[:, 1])
        available_i = [i for i in range(len(low1)) if i not in used_i]
        available_j = [j for j in range(len(low2)) if j not in used_j]

        n_random = int(random_ratio * len(base_pairs))
        rand_i = np.random.choice(available_i, min(n_random, len(available_i)), replace=False)
        rand_j = np.random.choice(available_j, min(n_random, len(available_j)), replace=False)
        rand_pairs = np.stack([rand_i, rand_j], axis=1)

        all_pairs = np.vstack([base_pairs[:n_base], rand_pairs])
        paired_i, paired_j = set(), set()
        final_pairs = []
        for pair in all_pairs:
            i, j = pair
            if i not in paired_i and j not in paired_j:
                final_pairs.append([i, j])
                paired_i.add(i)
                paired_j.add(j)
        return np.array(final_pairs)

    @staticmethod
    def _compute_bes(batch1, batch2, pairs):
        n_features = batch1.shape[1]
        mi_cross = np.zeros(n_features)
        if len(pairs) > 0:
            idx1, idx2 = pairs[:, 0], pairs[:, 1]
            for g in range(n_features):
                mi_cross[g] = mutual_info_regression(
                    batch1[idx1, g].reshape(-1, 1),
                    batch2[idx2, g]
                )[0]
        var_term = 1 / (0.5 * (batch1.var(axis=0, ddof=1) + batch2.var(axis=0, ddof=1)) + 1e-6)
        return mi_cross * var_term

    @staticmethod
    def _find_mutual_nn(batch1, batch2, metric='cosine'):
        nbrs_batch2 = NearestNeighbors(n_neighbors=1, metric=metric).fit(batch2)
        _, indices1 = nbrs_batch2.kneighbors(batch1)
        nbrs_batch1 = NearestNeighbors(n_neighbors=1, metric=metric).fit(batch1)
        _, indices2 = nbrs_batch1.kneighbors(batch2)
        candidates = []
        for i in range(len(batch1)):
            j = indices1[i][0]
            if indices2[j][0] == i:
                candidates.append((i, j))
        paired_i, paired_j = set(), set()
        final_pairs = []
        for i, j in candidates:
            if i not in paired_i and j not in paired_j:
                final_pairs.append([i, j])
                paired_i.add(i)
                paired_j.add(j)
        return np.array(final_pairs)

    @staticmethod
    def _check_stability(old_pairs, new_pairs):
        set_old = {tuple(pair) for pair in old_pairs}
        set_new = {tuple(pair) for pair in new_pairs}
        intersection = len(set_old & set_new)
        union = len(set_old | set_new)
        return intersection / union if union > 0 else 0.0


