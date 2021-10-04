import argparse
import json
import math
from collections import Counter

def load_gold_stardard(gold_path):
    gold_answers = dict()
    with open(gold_path) as json_file:
        data = json.load(json_file)
    for ques in data:
        gold_answers[ques['id']] = ques['relations']
    print(f"\tgold answers: loaded {len(data)} questions!")
    return gold_answers


def load_system_answers(system_path):
    system_answers = dict()
    with open(system_path) as json_file:
        data = json.load(json_file)
    for ques in data:
        if 'relations' in ques:
            system_answers[ques['id']] = ques['relations']
        else:
            print(f"Missing relations: {ques['id']}")
    print(f"\tsystem answers: loaded {len(data)} questions!")
    return system_answers


def calculate_f1(precision, recall):
    if precision + recall == 0:
        return 0
    else:
        return 2 * ((precision * recall) / (precision + recall))


def evaluate_dbpedia(gold_answers, system_answers):
    count, total_p, total_r, total_f1 = 0, 0, 0, 0
    for ques_id in gold_answers:
        count += 1
        # if an answer is not provided to a question, we just move on
        if ques_id not in system_answers:
            continue

        gold_answer_list = gold_answers[ques_id]
        system_relations = system_answers[ques_id].copy()
        sys_rel_count, gold_rel_count, found_count, correct_count = len(system_relations), 0, 0, 0

        # collect all gold relations
        all_gold_rels = set()
        for gold_rel_set in gold_answer_list:
            all_gold_rels.update(gold_rel_set)

        # mark all correct answers from system answers
        for rel in system_relations:
            if rel in all_gold_rels:
                correct_count += 1

        # check how many relation sets are covered in system answers. In ground truth, we have multiple correct
        # relations for a given slot.
        # For example, {"dbo:locatedInArea", "dbo:city", "dbo:isPartOf", "dbo:location", "dbo:region"}
        for gold_rel_set in gold_answer_list:
            gold_rel_count += 1
            found_rel = False
            for rel in gold_rel_set:
                if rel in system_relations:
                    found_rel = True
                    system_relations.remove(rel)
                    break
            if found_rel:
                found_count += 1

        # precision, recall and F1 calculation
        precision = correct_count / sys_rel_count
        recall = found_count / gold_rel_count
        total_p += precision
        total_r += recall
        total_f1 += calculate_f1(precision, recall)

    return total_p/count, total_r/count, total_f1/count


def evaluate_wikidata(gold_answers, system_answers):
    count, total_p, total_r, total_f1 = 0, 0, 0, 0
    for ques_id in gold_answers:
        count += 1
        # if an answer is not provided to a question, we just move on
        if ques_id not in system_answers:
            continue

        gold_relations = gold_answers[ques_id]
        system_relations = system_answers[ques_id]
        if len(system_relations) == 0:
            continue
        precision = (sum((Counter(system_relations) & Counter(gold_relations)).values())) / len(system_relations)
        recall = (sum((Counter(system_relations) & Counter(gold_relations)).values())) / len(gold_relations)
        f1 = calculate_f1(precision, recall)
        total_p += precision
        total_r += recall
        total_f1 += f1

    return total_p/count, total_r/count, total_f1/count


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gt', type=str,
                        help='ground truth JSON file')
    parser.add_argument('--so', type=str,
                        help='system output JSON file')
    parser.add_argument('--kb', type=str,
                        help='Knowledge Base', default="dbpedia")
    args = parser.parse_args()
    return args


def main(args):
    system_path = args.so
    gt_path = args.gt
    kb = args.kb
    print(f"Config:\n\tGround truth: {gt_path}\n\tSystem path: {system_path}")
    gold_answers = load_gold_stardard(gt_path)
    system_answers = load_system_answers(system_path)
    if kb == "dbpedia":
        precision, recall, f1 = evaluate_dbpedia(gold_answers, system_answers)
    elif kb == "wikidata":
        precision, recall, f1 = evaluate_wikidata(gold_answers, system_answers)
    else:
        raise Exception(f"Invalid KB: {kb}")

    print(f"\nResults:\n\tPrecision: {round(precision, 5)}\n\tRecall: {round(recall, 5)}\n\tF1: {round(f1, 5)}")


if __name__ == "__main__":
    main(arg_parser())