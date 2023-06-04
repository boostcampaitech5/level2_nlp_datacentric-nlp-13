from cleanlab.filter import find_label_issues
from cleanlab.dataset import health_summary


def scaling(predicion_probabilities):
    arr = predicion_probabilities
    # min max 스케일링 (0 ~ 1)
    scaled_arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

    # softmax 함수 취하기
    sum_value = np.sum(scaled_arr, axis=1).reshape(-1,1)
    normalized_arr = np.divide(scaled_arr, sum_value)

    return normalized_arr


def cleanlab(y_true, predicion_probabilities, class_names, train_dataset):
    normalized_arr = scaling(predicion_probabilities)
    
    ordered_label_issue_indices = find_label_issues(labels=y_true, # 정답 라벨     
                                         pred_probs=normalized_arr, # 정답 예측 확률    
                                         return_indices_ranked_by='self_confidence')
    label_error_report = health_summary(y_true, normalized_arr, class_names=class_names)
    
    return ordered_label_issue_indices, label_error_report

