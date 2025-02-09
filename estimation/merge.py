import numpy as np

def merge(subset, min_num_body_parts=4, min_score=0.4):
    """
    合併和過濾骨架
    :param subset: 輸入的骨架數據
    :param min_num_body_parts: 骨架的最小部位數量
    :param min_score: 骨架的最低平均得分
    :return: 合併和過濾後的骨架集合
    """
    num_skeletons = len(subset)

    # Step 1: 合併重疊的骨架
    for i in range(num_skeletons):
        if subset[i, -1] == -1:  # 已刪除的骨架不處理
            continue
        for j in range(i + 1, num_skeletons):
            if subset[j, -1] == -1:  # 已刪除的骨架不處理
                continue

            # 檢查是否有重疊的部位（相同ID）
            common_parts = np.where(
                (subset[i, :-2] >= 0) & (subset[i, :-2] == subset[j, :-2])
            )[0]

            # 如果存在重疊部位，合併兩個骨架
            if len(common_parts) > 0:
                subset[i, :-2] = np.maximum(subset[i, :-2], subset[j, :-2])
                subset[i, -2] += subset[j, -2]  # 更新總分數
                subset[i, -1] += subset[j, -1]  # 更新部位數量
                subset[j, -1] = -1  # 標記為刪除

    # 刪除標記為 -1 的骨架
    subset = subset[subset[:, -1] != -1]

    # Step 2: 刪除不符合要求的骨架
    delete_idx = []
    for i in range(len(subset)):
        parts_num = subset[i, -1]   # 骨架中的部位數量
        total_score = subset[i, -2]  # 骨架的總分數
        
        # 計算每個部位的平均得分
        avg_score = total_score / parts_num if parts_num > 0 else 0

        # 刪除不符合最低部位數量或最低平均得分的骨架
        if parts_num < min_num_body_parts or avg_score < min_score:
            delete_idx.append(i)

    subset = np.delete(subset, delete_idx, axis=0)

    # Print the final subset
    print("最終的 subset:")
    for i, skeleton in enumerate(subset):
        print(f"骨架 {i}:", skeleton)

    return subset
