"""
author: Josef Baloun
"""
import json
import numpy as np
from sklearn.metrics import confusion_matrix
from functools import cmp_to_key


def evaluate_main_diag(gt, pred, set_invalid_value_to_zero=False):
    """
    Same as evaluate_multiclass_singlelabel
    - prev. version compatibility
    """
    return evaluate_multiclass_singlelabel(gt, pred, set_invalid_value_to_zero)


def evaluate_multiclass_singlelabel(gt, pred, set_invalid_value_to_zero=False):
    """
    Evaluates multiclass singlelabel scenario.
    Based on confusion matrix.
    Evaluation is done only for the labels presented in gt or pred. Other labels are not considered.

    :param list gt:     1D list of shape (numOfSamples). Contains GT str or indices. E.g. ["H305", "H309"] or [0, 3]
    :param list pred:   1D list of shape (numOfSamples). List of predictions or indices. E.g. ["H305", "H309"] or [0, 3]
                        Has to be same format as gt.
    :param bool set_invalid_value_to_zero: If the metrics that can not be computed should be set to 0. (eg precision if there is no prediction) If false these are ignored.
                                           True to reproduce scikit-learn method results.

    :return:    dict with results, labels and confusion matrix
    """
    alllabels = list(set(gt + pred))
    alllabels.sort()
    cm = confusion_matrix(gt, pred, labels=alllabels)
    results = _eval_conf_mat(cm, set_invalid_value_to_zero)
    results["labels"] = alllabels
    results["confusion_matrix"] = cm
    # log.info(f"Multiclass singlelabel evaluation results for {len(alllabels)} labels: {results}")
    #print(f"Multiclass singlelabel evaluation results for {len(alllabels)} labels: {results}")
    return results


def evaluate_all_diag(gt, pred, set_invalid_value_to_zero=False, ignore_code_occurences=True):
    """
    :param bool ignore_code_occurences: If the number of code occurences should be ignored. eg for ["H203", "H204"] there are ["H", "H"] as first letters, then if ignore_code_occurences=True, it becomes list of unique values ["H"] ignoring the number of their occurences.

    Same as evaluate_multiclass_multilabel
    - prev. version compatibility
    """
    if ignore_code_occurences:  # make codes unique
        gt = [list(set(cl)) for cl in gt]
        pred = [list(set(cl)) for cl in pred]

    return evaluate_multiclass_multilabel(gt, pred, set_invalid_value_to_zero)


def evaluate_multiclass_multilabel(gt, pred, set_invalid_value_to_zero=False):
    """
    Evaluates multiclass multilabel scenario.
    Evaluation is done only for the labels presented in gt or pred. Other labels are not considered.

    Prediction-wise and class-wise scenarios are used.
        Prediction-wise:
            - each prediction is evaluated separately (as micro)
            - mean values are provided as a result
            - corresponds to scikit-learn with average='samples'
        Class-wise:
            - TPs, FPs and FNs are collected for each class (label) across all predictions
            - classwise, macro and micro results are then provided
            - corresponds to scikit-learn with average='micro'/'macro'

    :param list gt:     2D list of shape (numOfSamples, variableLenListOfGT). List of lists with GT codes or indices. E.g. [["H305", "H309"], ...] or [[0, 3, 4], ...]
    :param list pred:   2D list of shape (numOfSamples, variableLenListOfPredictions). List of lists with predicted codes or indices. E.g. [["H305", "H309"], ...] or [[0, 3, 4], ...]
                        Has to be same format as gt.
    :param bool set_invalid_value_to_zero: If the metrics that could not be computed should be set to 0. (eg precision if there is no prediction) If false these are ignored.

    :return:    dict with results
    """
    alllabels = _get_unique_labels_from_2d(gt + pred)
    results = _eval_multiclass_multilabel(gt, pred, labels=alllabels, set_invalid_value_to_zero=set_invalid_value_to_zero)
    results["labels"] = alllabels
    # log.info(f"Multiclass multilabel evaluation results for {len(alllabels)} labels: {results}")
    #print(f"Multiclass multilabel evaluation results for {len(alllabels)} labels: {results}")
    return results


def show_confusion_matrix(cm, labels, title=None):
    from sklearn.metrics import ConfusionMatrixDisplay
    import matplotlib.pyplot as plt
    if not isinstance(cm, np.ndarray):
        cm = np.asarray(cm)
    cmd = ConfusionMatrixDisplay(cm, display_labels=labels)
    cmd.plot()
    plt.title(title)
    plt.show()


def save_eval(data, file_path, comment=""):
    d = _cvt_ndarray_to_list(data)
    d = {
        "comment": comment,
        "data": d
    }
    with open(file_path, 'w', encoding='utf8') as json_file:
        json.dump(d, json_file, indent=None, separators=(',', ':'))


def load_eval(file_path):
    with open(file_path, 'r', encoding='utf8') as json_file:
        data = json.load(json_file)
    return data["data"]


# HELPER FUNCTIONS
def _cvt_ndarray_to_list(val):
    if isinstance(val, np.ndarray):
        return val.tolist()
    elif isinstance(val, dict):
        d = {}
        for k, v in val.items():
            v = _cvt_ndarray_to_list(v)
            d[k] = v
        return d
    elif isinstance(val, list):
        l = []
        for x in val:
            l.append(_cvt_ndarray_to_list(x))
        return l
    else:
        return val


def _eval_conf_mat(cm, set_invalid_value_to_zero):
    # log.debug(f"Confusion matrix evaluation.")
    # label wise
    TPs = np.diag(cm)
    FPs = np.sum(cm, axis=0) - TPs  # as column
    FNs = np.sum(cm, axis=1) - TPs  # as row

    # total - micro eval
    TP = np.sum(TPs)
    FP = np.sum(FPs)
    FN = FP  # = np.sum(FNs)

    pred_total = TP + FP  # equals to np.sum(cm)
    total_accuracy = TP / pred_total

    results = {
        "accuracy": total_accuracy,
        "hamming_loss": 1 - total_accuracy
    }
    results.update(_eval_classwise_macro(TPs=TPs, FPs=FPs, FNs=FNs, set_invalid_value_to_zero=set_invalid_value_to_zero))
    results.update(_eval_micro(TP=TP, FP=FP, FN=FN, set_invalid_value_to_zero=set_invalid_value_to_zero))
    return results


def __sort_unique_vals_cmp(a, b):
    ta = type(a)
    tb = type(b)
    if ta == tb:
        return -1 if a < b else 1
    return -1 if str(ta) < str(tb) else 1


def _get_unique_labels_from_2d(listcodelist):
    lbls = []
    for cl in listcodelist:
        lbls.extend(cl)
    lbls = list(set(lbls))
    lbls.sort(key=cmp_to_key(__sort_unique_vals_cmp))
    return lbls


def _eval_multiclass_multilabel(all_gt, all_pred, labels, set_invalid_value_to_zero):
    # s prefix - samplewise results
    # c prefix - classwise evaluation - based on labels not predictions
    cli = {}  # label indices
    for i in range(len(labels)):
        cli[labels[i]] = i

    # classwise results TP, FP, FN for each label
    cTPs = np.zeros((len(labels)), dtype=np.int64)
    cFPs = np.zeros((len(labels)), dtype=np.int64)
    cFNs = np.zeros((len(labels)), dtype=np.int64)

    # samplewise results for each prediction
    sTPs = np.zeros((len(all_pred)), dtype=np.int64)
    sFPs = np.zeros((len(all_pred)), dtype=np.int64)
    sFNs = np.zeros((len(all_pred)), dtype=np.int64)

    for i in range(len(all_gt)):
        gts = all_gt[i]
        preds = all_pred[i].copy()  # will be edited, thus copy (the set is speed comparable for +- 500 labels)
        for gtcode in gts:
            if gtcode in preds:
                cTPs[cli[gtcode]] += 1  # TP for GT (and pred) class
                sTPs[i] += 1
                preds.remove(gtcode)
            else:
                cFNs[cli[gtcode]] += 1  # FN for GT class
                sFNs[i] += 1
        for predcode in preds:  # only the predictions that were not in GT
            cFPs[cli[predcode]] += 1  # FP for pred class
        sFPs[i] += len(preds)  # only the FPs are left

    # output results
    results = {}
    totalTP = np.sum(cTPs)
    totalFP = np.sum(cFPs)
    totalFN = np.sum(cFNs)

    swrong = sFPs + sFNs
    results["exact_match"] = np.sum((swrong) == 0) / len(sFPs)  # percentage of predictions where all is TP
    results["hamming_loss"] = np.mean(swrong) / len(
        labels)  # the fraction of the wrong labels to the total number of labels
    results["total_mistakes"] = int(np.sum(swrong))  # total sum of FNs and FPs

    results.update(_eval_micro(TP=totalTP, FP=totalFP, FN=totalFN, set_invalid_value_to_zero=set_invalid_value_to_zero))
    results.update(_eval_classwise_macro(TPs=cTPs, FPs=cFPs, FNs=cFNs, set_invalid_value_to_zero=set_invalid_value_to_zero))

    # samplewise results
    microkeys = list(_eval_micro(TP=0, FP=1, FN=1, set_invalid_value_to_zero=set_invalid_value_to_zero).keys())
    sw_results = {
        "TPs": sTPs,
        "FPs": sFPs,
        "FNs": sFNs
    }
    for k in microkeys:
        sw_results[k] = []

    for i in range(len(sTPs)):
        sres = _eval_micro(TP=sTPs[i], FP=sFPs[i], FN=sFNs[i], set_invalid_value_to_zero=set_invalid_value_to_zero)
        for k in microkeys:
            sw_results[k].append(sres[k])

    for mk in microkeys:
        v = np.nanmean(sw_results[mk])
        k = "mean_samplewise_" + mk
        results[k] = v  # add to results

    results["samplewise_results"] = sw_results

    return results


def _eval_classwise_macro(TPs, FPs, FNs, set_invalid_value_to_zero):
    with np.errstate(invalid='ignore'):  # ignore the warning - 0/0 is set to nan
        classwise_jaccard = TPs / (TPs + FPs + FNs)
        classwise_f1 = TPs / (TPs + (FPs + FNs) / 2)
        classwise_precision = TPs / (TPs + FPs)
        classwise_recall = TPs / (TPs + FNs)

    if set_invalid_value_to_zero:
        classwise_jaccard = np.nan_to_num(classwise_jaccard, nan=0.0)
        classwise_f1 = np.nan_to_num(classwise_f1, nan=0.0)
        classwise_precision = np.nan_to_num(classwise_precision, nan=0.0)
        classwise_recall = np.nan_to_num(classwise_recall, nan=0.0)

    cw_results = {
        "TPs": TPs,
        "FPs": FPs,
        "FNs": FNs,
        "jaccard": classwise_jaccard,
        "f1": classwise_f1,
        "precision": classwise_precision,
        "recall": classwise_recall,
    }

    results = {
        "macro_jaccard": np.nanmean(classwise_jaccard),  # if nan occur it is ignored - eg:
        "macro_precision": np.nanmean(classwise_precision),  # precision if there is no prediction for the class
        "macro_recall": np.nanmean(classwise_recall),  # recall if there is no gt for the class
        "macro_f1": np.nanmean(classwise_f1),

        # if different num of labels can occur in multiple models, the mean is not comparable
        "macro_jaccard_sum": np.nansum(classwise_jaccard),
        "macro_precision_sum": np.nansum(classwise_precision),
        "macro_recall_sum": np.nansum(classwise_recall),
        "macro_f1_sum": np.nansum(classwise_f1),

        "classwise_results": cw_results
    }
    return results


def _eval_micro(TP, FP, FN, set_invalid_value_to_zero):
    if set_invalid_value_to_zero:
        nanval = 0.0
    else:
        nanval = float("nan")

    if (TP + FN + FP) == 0:
        micro_jaccard = nanval
        micro_f1 = nanval
    else:
        micro_jaccard = TP / (TP + FN + FP)
        micro_f1 = TP / (TP + (FP + FN) / 2)

    if (TP + FP) == 0:
        micro_precision = nanval
    else:
        micro_precision = TP / (TP + FP)

    if (TP + FN) == 0:
        micro_recall = nanval
    else:
        micro_recall = TP / (TP + FN)

    results = {
        "micro_jaccard": micro_jaccard,
        "micro_precision": micro_precision,
        "micro_recall": micro_recall,
        "micro_f1": micro_f1,
    }
    return results








