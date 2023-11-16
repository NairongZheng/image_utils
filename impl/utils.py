import numpy as np


def _generate_matrix(gt_image, pre_image, num_class=7):
    """
    混淆矩阵:
    行: 实际,每一行之和表示该类别的真实样本数量;
    列: 预测,每一列之和表示被预测为该类别的样本数量;
    """
    mask = (gt_image >= 0) & (
        gt_image < num_class
    )  # ground truth中所有正确(值在[0, classe_num])的像素label的mask
    label = num_class * gt_image[mask].astype("int") + pre_image[mask]
    # np.bincount计算了从0到n**2-1这n**2个数中每个数出现的次数，返回值形状(n, n)
    count = np.bincount(label, minlength=num_class**2)
    confusion_matrix = count.reshape(num_class, num_class)  # 21 * 21(for pascal)
    return confusion_matrix


def _Class_IOU(confusion_matrix):
    MIoU = np.diag(confusion_matrix) / (
        np.sum(confusion_matrix, axis=1)
        + np.sum(confusion_matrix, axis=0)
        - np.diag(confusion_matrix)
    )
    return MIoU


def meanIntersectionOverUnion(confusion_matrix):
    # Intersection = TP Union = TP + FP + FN
    # IoU = TP / (TP + FP + FN)
    intersection = np.diag(confusion_matrix)  # 交集: 混淆矩阵对角线
    union = (
        np.sum(confusion_matrix, axis=1)
        + np.sum(confusion_matrix, axis=0)
        - np.diag(confusion_matrix)
    )  # 并集
    IoU = intersection / union
    mIoU = np.nanmean(IoU)
    # return mIoU
    return mIoU, IoU


# def Frequency_Weighted_Intersection_over_Union(confusion_matrix):
#     # FWIOU =     [(TP+FN)/(TP+FP+TN+FN)] *[TP / (TP + FP + FN)]
#     freq = np.sum(confusion_matrix, axis=1) / np.sum(confusion_matrix)          # 真实样本分别占整张图的比例
#     iu = np.diag(confusion_matrix) / (
#             np.sum(confusion_matrix, axis=1) + np.sum(confusion_matrix, axis=0) -
#             np.diag(confusion_matrix))
#     FWIoU = (freq[freq > 0] * iu[freq > 0]).sum()       # 有没有大于0其实无所谓,反正0乘了啥也是0,这么写是为了防止nan？
#     return FWIoU


def Frequency_Weighted_Intersection_over_Union(confusion_matrix):
    # FWIOU =     [(TP+FN)/(TP+FP+TN+FN)] *[TP / (TP + FP + FN)]
    freq = np.sum(confusion_matrix, axis=1) / np.sum(confusion_matrix)  # 真实样本分别占整张图的比例
    iu = np.diag(confusion_matrix) / (
        np.sum(confusion_matrix, axis=1)
        + np.sum(confusion_matrix, axis=0)
        - np.diag(confusion_matrix)
        + 1e-7
    )
    FWIoU = (freq[freq > 0] * iu[freq > 0]).sum()  # 有没有大于0其实无所谓,反正0乘了啥也是0,这么写是为了防止nan？
    return FWIoU


def Kappa(confusion_matrix):
    pe_rows = np.sum(confusion_matrix, axis=0)
    pe_cols = np.sum(confusion_matrix, axis=1)
    sum_total = sum(pe_cols)
    pe = np.dot(pe_rows, pe_cols) / float(sum_total**2)
    po = np.trace(confusion_matrix) / float(sum_total)  # np.trace:对对角线求和
    return (po - pe) / (1 - pe)
