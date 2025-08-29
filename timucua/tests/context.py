# -*- coding: utf-8 -*-

from collections import Counter, defaultdict
from copy import deepcopy
import gzip
import sys, json
import os, re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import timucua as mv

# verbs_to_test = ['vyetv',
#                  'tvcetv',
#                  "letketv",
#                  "vpeletv",
#                  "vpoketv",
#                  "hvlketv",
#                  "hompetv",
#                  "vfvnketv",
#                  "hvoketv",
#                  "hueretv",
#                  "hvkihketv",
#                  "akkvretv",
#                  "folothoketv",
#                  "enlopicetv",
#                  "etepvkocetv",
#                  "hvkvnceropotketv",
#                  "vwvnayetv",
#                  "ak-vpoketv",
#                  "opunvyetv",
#                  "etekelketv"


#                 #  'mēcetv',
#                 #  'fēketv',
#                 #  'wvnvyetv',
#                  ]
verbs_to_test = [
    "vyetv",
    "vwvnayetv",
    "vwvnvyetv",
    "hayetv",
    "vpoketv",
    "fēketv",
    "esketv",
    "letketv",
    "hompetv",
    "vfvnketv",
    "tvmketv",
    "yefolketv",
    "hvkihketv",
    "akketv",
    "wakketv",
    "akhottetv",
    "fekhonnetv",
    "kerretv",
    "lentappetv",
    "liketv",
    "lvoketv",
    "cvpkuecetv",
    "hueretv",
]


def test_lgrade():
    print("L-grade test:")
    for word in verbs_to_test:
        verb = mv.Verb(word)
        print(f"\t{verb} -> {verb.l()}")


def test_hgrade():
    print("H-grade test:")
    for word in verbs_to_test:
        verb = mv.Verb(word)
        print(f"\t{verb} -> {verb.h()}")


with open(
    os.path.join(os.path.dirname(__file__), "../mvskoke/mvskoke_dic.json"),
    "r",
    encoding="utf-8",
) as f:
    mvskoke_dict = json.load(f)

active_verbs = [
    x for x in mvskoke_dict if x["headword"].endswith("etv")
]  # and True in [True for y in x["senses"] if "verb" in y["graminfoname"].split(" ")]
three_or_more = [
    x
    for x in active_verbs
    if len(x["senses"]) > 0
    and "three or more" in " ".join([y["definition"] for y in x["senses"]])
]
two = [
    x
    for x in active_verbs
    if len(x["senses"]) > 0
    and "of two" in " ".join([y["definition"] for y in x["senses"]])
    and "two or more" not in " ".join([y["definition"] for y in x["senses"]])
]
two_or_more = [
    x
    for x in active_verbs
    if len(x["senses"]) > 0
    and "two or more" in " ".join([y["definition"] for y in x["senses"]])
]


two_set = {x["headword"] for x in two}
two_or_more_set = {x["headword"] for x in two_or_more}
three_or_more_set = {x["headword"] for x in three_or_more}

one = [
    x
    for x in active_verbs
    if x["headword"] not in three_or_more_set
    and x["headword"] not in two_set
    and x["headword"] not in two_or_more_set
]

one_set = {x["headword"] for x in one}

print(f"Active Verbs: {len(active_verbs)}")
v_objs = [mv.Verb(x["headword"], x["pronunciations"]) for x in active_verbs]

# test_lgrade()
# for word in verbs_to_test:
#     mv.Verb(word).show_all_grades()
test_hgrade()


verb_clusters = dict()
for verb in three_or_more:
    print(verb["headword"])
    if "see" in verb.keys():
        related_words = verb["see"]
        verb_clusters[verb["headword"]] = {x["headword"] for x in related_words}

defective_3 = {x: y for x, y in verb_clusters.items() if len(y) < 2}
verb_clusters = dict()
for verb in two:
    print(verb["headword"])
    if "see" in verb.keys():
        related_words = verb["see"]
        verb_clusters[verb["headword"]] = {x["headword"] for x in related_words}
defective_2 = {x: y for x, y in verb_clusters.items() if len(y) < 2}
verb_clusters = dict()
for verb in two_or_more:
    print(verb["headword"])
    if "see" in verb.keys():
        related_words = verb["see"]
        verb_clusters[verb["headword"]] = {x["headword"] for x in related_words}
defective_2_or_more = {x: y for x, y in verb_clusters.items() if len(y) < 1}

print("one entries: ", len(one))
print("two entries: ", len(two))
print("two or more entries: ", len(two_or_more))
print("three_or_more entries: ", len(three_or_more))
print("defective_2 entries: ", len(defective_2))
print("defective_2 or more entries: ", len(defective_2_or_more))
print("defective_3 entries: ", len(defective_3))
sample_obj = {"one": "", "two": "", "two_or_more": "", "three_or_more": ""}
# make a defaultdict that return sample_obj if key is not found
combined = defaultdict(lambda: deepcopy(sample_obj))
for current_set in [one, two, two_or_more, three_or_more]:
    for verb in current_set:
        word = verb["headword"]
        if word in one_set:
            combined[word] = combined[word]
            combined[word]["one"] = word
        if "see" in verb.keys():
            related_words = verb["see"]
            for related_word in related_words:
                combined[word]["one"] = (
                    related_word["headword"]
                    if related_word["headword"] in one_set and word not in one_set
                    else combined[word]["one"]
                )
                combined[word]["two"] = (
                    related_word["headword"]
                    if related_word["headword"] in two_set and word not in two_set
                    else combined[word]["two"]
                )
                combined[word]["two_or_more"] = (
                    related_word["headword"]
                    if related_word["headword"] in two_or_more_set
                    and word not in two_or_more_set
                    else combined[word]["two_or_more"]
                )
                combined[word]["three_or_more"] = (
                    related_word["headword"]
                    if related_word["headword"] in three_or_more_set
                    and word not in three_or_more_set
                    else combined[word]["three_or_more"]
                )
all_pluriform = set(combined.keys())
one_full = {x: y for x, y in combined.items() if x in one_set}
active_verbs_dict = defaultdict(lambda: deepcopy(sample_obj))
for verb in active_verbs:
    word = verb["headword"]
    if word in one_set or word not in all_pluriform:
        active_verbs_dict[word] = combined[word]
        if active_verbs_dict[word]["one"] == "":
            active_verbs_dict[word]["one"] = word
        active_verbs_dict[word]["raw_entry"] = verb

rest = [x for x in active_verbs if x["headword"] not in all_pluriform]
# assert len(rest) + len(all_pluriform) == len(active_verbs)


def conjugate_verb(verb):
    if type(verb) == str:
        verb = active_verbs_dict[verb]
    conjugations = defaultdict(lambda: "")
    conjugations["raw_entry"] = verb["raw_entry"]
    conjugations["1p"] = mv.Verb(verb["one"])
    conjugations["2p"] = mv.Verb(verb["one"])
    conjugations["3p"] = mv.Verb(verb["one"])
    if verb["two"]:
        conjugations["2p"] = mv.Verb(verb["two"])
    if verb["two_or_more"]:
        conjugations["2p"] = mv.Verb(verb["two_or_more"])
        conjugations["3p"] = mv.Verb(verb["two_or_more"])
    if verb["three_or_more"]:
        conjugations["3p"] = mv.Verb(verb["three_or_more"])
    try:
        # First Person Singular
        conjugations["1ps_pres_basic"] = conjugations["1p"].l().stem + "is"
        conjugations["-1ps_pres_basic"] = conjugations["1p"].l().stem + "vkos"  # neg
        conjugations["1ps_pres_tos"] = conjugations["1p"].l().stem + "iyē tos"
        conjugations["1ps_pres_ometv"] = conjugations["1p"].stem + "e towis"

        # Second Person Singular
        basic2ps = ["esk", "eck", "ecc", "etc"]
        conjugations["2ps_pres_basic"] = [
            conjugations["1p"].l().stem + suffix + "es" for suffix in basic2ps
        ]
        conjugations["-2ps_pres_basic"] = [
            conjugations["1p"].l().stem + suffix + "ekos" for suffix in basic2ps
        ]
        conjugations["2ps_pres_tos"] = [
            conjugations["1p"].l().stem + suffix + "ē tos" for suffix in basic2ps
        ]
        conjugations["2ps_pres_ometv"] = [
            conjugations["1p"].stem + "e to" + suffix
            for suffix in ["wetskes", "weckes", "wecces", "ntces", "nckes"]
        ]

        # Third Person Singular
        conjugations["3ps_pres_basic"] = conjugations["1p"].l().stem + "es"
        conjugations["-3ps_pres_basic"] = conjugations["1p"].l().stem + "ekos"  # neg
        conjugations["3ps_pres_tos"] = conjugations["1p"].l().stem + "ē tos"
        conjugations["3ps_pres_ometv"] = conjugations["1p"].stem + "e tos"

        # First Person Plural 2
        conjugations["1pp_pres_basic"] = conjugations["2p"].l().stem + "ēs"
        conjugations["-1pp_pres_basic"] = conjugations["2p"].l().stem + "ēkos"  # neg
        conjugations["1pp_pres_tos"] = conjugations["2p"].l().stem + "eyē tos"
        conjugations["1pp_pres_ometv"] = conjugations["2p"].stem + "e towēs"

        # First Person Plural more
        conjugations["1pp+_pres_basic"] = conjugations["3p"].l().stem + "ēs"
        conjugations["-1pp+_pres_basic"] = conjugations["3p"].l().stem + "ēkos"
        conjugations["1pp+_pres_tos"] = conjugations["3p"].l().stem + "eyē tos"
        conjugations["1pp+_pres_ometv"] = conjugations["3p"].stem + "e towēs"

        # Second Person Plural 2
        conjugations["2pp_pres_basic"] = [
            conjugations["2p"].l().stem + suffix for suffix in ["atskes", "ackes"]
        ]
        conjugations["-2pp_pres_basic"] = [
            conjugations["2p"].l().stem + suffix for suffix in ["atskekos", "ackekos"]
        ]
        conjugations["2pp_pres_tos"] = [
            conjugations["2p"].l().stem + suffix + " tos"
            for suffix in ["atskē", "ackē"]
        ]
        conjugations["2pp_pres_ometv"] = [
            conjugations["2p"].stem + "e towa" + suffix for suffix in ["tskes", "ckes"]
        ]
        # Second Person Plural more
        conjugations["2pp+_pres_basic"] = [
            conjugations["3p"].l().stem + suffix for suffix in ["atskes", "ackes"]
        ]
        conjugations["-2pp+_pres_basic"] = [
            conjugations["3p"].l().stem + suffix for suffix in ["atskekos", "ackekos"]
        ]
        conjugations["2pp+_pres_tos"] = [
            conjugations["3p"].l().stem + suffix + " tos"
            for suffix in ["atskē", "ackē"]
        ]
        conjugations["2pp+_pres_ometv"] = [
            conjugations["3p"].stem + "e towa" + suffix for suffix in ["tskes", "ckes"]
        ]

        # Third Person Plural 2
        conjugations["3pp_pres_basic"] = conjugations["2p"].l().stem + "akes"
        conjugations["-3pp_pres_basic"] = conjugations["2p"].l().stem + "akekos"
        conjugations["3pp_pres_tos"] = conjugations["2p"].l().stem + "akē tos"
        conjugations["3pp_pres_ometv"] = conjugations["2p"].stem + "e towakes"
        # Third Person Plural more
        conjugations["3pp+_pres_basic"] = conjugations["3p"].l().stem + "akes"
        conjugations["-3pp+_pres_basic"] = conjugations["3p"].l().stem + "akekos"
        conjugations["3pp+_pres_tos"] = conjugations["3p"].l().stem + "akē tos"
        conjugations["3pp+_pres_ometv"] = conjugations["3p"].stem + "e towakes"
    except Exception as e:
        print(e)
        breakpoint()
    return conjugations


# lik = [(verb, conjugate_verb(verb)) for verb in active_verbs_dict.values() if verb["raw_entry"]["first_word"] == "liketv"][0]
all_conjugations = [(verb, conjugate_verb(verb)) for verb in active_verbs_dict.values()]
hompetv = conjugate_verb("hompetv")
pvpetv = conjugate_verb("pvpetv")
# breakpoint()

# make the quiz format
quiz = []
# make dictionary format
for root, verb in all_conjugations:
    q_obj = dict()
    con_list = []
    if "raw_entry" in verb.keys():
        sound_url = (
            verb["raw_entry"]["pronunciations_audio"][0]["server_url"]
            if len(verb["raw_entry"]["pronunciations_audio"]) > 0
            else None
        )
        show1 = True
        show2 = True
        show3 = True
        if verb["1p"].stem == verb["2p"].stem and verb["1p"].stem == verb["3p"].stem:
            show2 = False
            show3 = False
        # If 1p and 3p are the same but 2p is different
        elif verb["2p"].stem == verb["3p"].stem and verb["1p"].stem != verb["2p"].stem:
            show3 = False
        # breakpoint()
        d = (
            verb["raw_entry"]["senses"][0]["definition"]
            if len(verb["raw_entry"]["senses"]) > 0
            else "Data not loaded..."
        )
        definition = f"{verb['1p'].root} - {d}"
        # { f: "Data not loaded...", m: "circunstancial", s: "ixé", o: "xé" },
        # if verb["1p"].stem == "lik":
        # breakpoint()
        for key, value in [
            x
            for x in verb.items()
            if ("pp" not in x[0])
            or (not show3 and show2 and "+" not in x[0])
            or ("+" in x[0] and show3)
            or ("pp_" in x[0] and show1)
        ]:
            if key in ["1p", "2p", "3p", "raw_entry"]:
                continue
            values = value if type(value) == list else [value]
            neg_val = None
            if f"-{key}" in verb.keys():
                neg_val = verb[f"-{key}"]
            neg_values = neg_val if type(neg_val) == list else [neg_val] * len(values)
            for v, n in zip(values, neg_values):
                q_obj = {
                    "surl": sound_url,
                    "f": v,
                    "m": key.split("_")[1],
                    "s": key.split("_")[0],
                    "t": key.split("_")[2],
                    "o": None,
                    "n": n,
                    "r": verb["1p"].root,
                    "d": definition,
                }
                con_list.append(q_obj)
                quiz.append(q_obj)
        for i, val in enumerate(mvskoke_dict):
            if val == root["raw_entry"]:
                mvskoke_dict[i]["c"] = con_list

# mvskoke_dict with conjugations; go through each

with gzip.open(
    os.path.join(os.path.dirname(__file__), "../../quiz/quiz.json.gz"),
    "wt",
    encoding="utf-8",
) as f:
    json.dump(quiz, f, cls=mv.VerbEncoder, ensure_ascii=False)
with gzip.open(
    os.path.join(os.path.dirname(__file__), "../../quiz/all_conjugations.json.gz"),
    "wt",
    encoding="utf-8",
) as f:
    json.dump(
        [x[1] for x in all_conjugations], f, cls=mv.VerbEncoder, ensure_ascii=False
    )

with gzip.open(
    os.path.join(os.path.dirname(__file__), "../../dict_w_conjugations.json.gz"),
    "wt",
    encoding="utf-8",
) as f:
    json.dump(mvskoke_dict, f, cls=mv.VerbEncoder, ensure_ascii=False)

with open(
    os.path.join(os.path.dirname(__file__), "../../dict_w_conjugations.json"),
    "w",
    encoding="utf-8",
) as f:
    json.dump(mvskoke_dict, f, cls=mv.VerbEncoder, ensure_ascii=False)


restricted = [
    x
    for x in active_verbs
    if "senses" in x.keys() and len(x["senses"]) > 0 and x["senses"][0]["restrictions"]
]

tl = Counter([x["senses"][0]["restrictions"] for x in restricted])
print(tl)

# # print histogram of tl using matplotlib
# import matplotlib.pyplot as plt
# import numpy as np

# # Sort the Counter by value
# sorted_tl = dict(sorted(tl.items(), key=lambda item: item[1], reverse=True))

# fig, ax = plt.subplots(
#     figsize=(10, 6)
# )  # Increase the figure size for better readability
# ax.bar(sorted_tl.keys(), sorted_tl.values())
# ax.set_xticklabels(sorted_tl.keys(), rotation=45, ha="right")
# plt.tight_layout()  # Adjust layout to make room for the rotated labels
# plt.show()
