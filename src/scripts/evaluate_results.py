# Cell 2: The "Chief Editor" Reranking and Evaluation Script
# TODO there are sentence transformers and other things

import torch
import spacy
import re
from collections import Counter
from fuzzywuzzy import process, fuzz
from transformers import pipeline
import pandas as pd
import evaluate  # Using the evaluate library for ROUGE is more robust

# ==============================================================================
# --- ⚙️ YOUR CONTROL PANEL ⚙️ ---
# ==============================================================================

# @markdown ### 1. The Original Article Text
# @markdown Paste the source article that the summaries were generated from.
SOURCE_TEXT = """
    Turkish Foreign Minister Hakan Fidan said Wednesday that the latest talks between Russia and Ukraine in Istanbul marked another step toward ending the war, emphasizing that “every new achievement brings the sides one step closer to peace.”

In a statement following the third round of direct negotiations hosted by Türkiye, Fidan noted that the two parties agreed on the mutual exchange of at least 1,200 prisoners of war, along with new steps for the return of civilians, including children.

“We observed with satisfaction that the negotiations are moving in a more constructive and result-oriented direction,” he said, underlining Türkiye’s role as a facilitator.

Fidan said the delegations discussed concrete measures to advance technical consultations on a ceasefire and agreed to work toward forming joint working groups on political, humanitarian and military matters.

“Another brick has been laid in the construction of a joint will toward a solution,” he said. “Negotiations must be conducted with patience. The support and interest shown by the international community to the Istanbul meetings also reflect the global yearning for peace.”

The head of the Ukrainian delegation, Rustem Umerov, said Kyiv proposed organizing a presidential-level meeting by late August and thanked Türkiye for its facilitation.

Ukraine also signaled its readiness for a ceasefire without preconditions.

On the Russian side, negotiator Vladimir Medinsky confirmed the prisoner exchange and proposed short-term ceasefires to evacuate the wounded and retrieve fallen soldiers.

He said Moscow had reviewed a list of Ukrainian children for repatriation and was open to a fourth round of talks.

    """

# @markdown ### 2. The Candidate Summaries
# @markdown Paste your list of "good" summaries here.
CANDIDATE_SUMMARIES = [
    "‘Another brick has been laid in the construction of a joint will toward a solution,’ says Hakan Fidan after 3rd round of direct talks in Istanbul",
    "‘Another brick has been laid in the construction of a joint will toward a solution,’ says Turkish foreign minister",
    "‘We observed with satisfaction that the negotiations are moving in a more constructive and result-oriented direction,’ says Turkish Foreign Minister Hakan Fidan",
    "‘Another brick has been laid in the construction of a joint will toward a solution,’ says Hakan Fidan after 3rd round of direct talks",
    "‘Another brick has been laid in the construction of a joint will toward a solution,’ Hakan Fidan says after 3rd round of direct talks in Istanbul",
    "Turkish Foreign Minister Hakan Fidan says ‘every new achievement brings the sides one step closer to peace’ after 3rd round of direct talks",
    "Turkish Foreign Minister Hakan Fidan says ‘every new achievement brings the sides one step closer to peace’ after 3rd round of direct talks in Istanbul",
    "‘Another brick has been laid in the construction of a joint will toward a solution,’ Hakan Fidan says after 3rd round of direct talks between Russia, Ukraine",
]

# ==============================================================================


def chief_editor_reranker(candidates, source_text, nlp_ner, rouge_metric):
    """
    Analyzes a list of candidate summaries and ranks them based on a
    multi-factor scoring system.
    """
    print("\n--- Starting Chief Editor Reranking Process ---")

    # --- Metric A: Calculate Keyword Relevance Weights from Source Text ---
    doc = nlp_ner(source_text)
    target_labels = ["ORG", "PERSON", "PRODUCT", "EVENT", "GPE"]
    all_entities = [ent.text.lower() for ent in doc.ents if ent.label_ in target_labels]
    keyword_weights = Counter(all_entities)
    source_words = set(re.findall(r"\b\w+\b", source_text.lower()))
    print(f"   - Calculated Keyword Weights: {keyword_weights}")

    ranked_candidates = []
    for candidate in candidates:
        # --- Score 1: Weighted Keyword Relevance ---
        relevance_score = 0
        found_keywords = set()
        for keyword, weight in keyword_weights.items():
            if keyword in candidate.lower() and keyword not in found_keywords:
                relevance_score += weight
                found_keywords.add(keyword)

        # --- Score 2: Hallucination Penalty ---
        hallucination_penalty = 0
        doc_cand = nlp_ner(candidate)
        for ent in doc_cand.ents:
            if ent.label_ in target_labels:
                individual_words = re.findall(r"\b\w+\b", ent.text.lower())
                is_grounded = True
                if not individual_words:
                    continue
                for word in individual_words:
                    match = process.extractOne(word, source_words, scorer=fuzz.ratio)
                    if not match or match[1] < 85:
                        is_grounded = False
                        break
                if not is_grounded:
                    hallucination_penalty += (
                        1  # Add 1 penalty point per hallucinated entity
                    )

        # --- Score 3: Abstraction Bonus ---
        rouge_score = rouge_metric.compute(
            predictions=[candidate], references=[source_text]
        )
        rouge_l = rouge_score["rougeL"]
        abstraction_bonus = 0
        # Give a bonus if the ROUGE-L score is in the "sweet spot" for abstraction
        if 0.3 <= rouge_l <= 0.5:
            abstraction_bonus = 1

        # --- Final Weighted Score ---
        # We prioritize relevance and heavily penalize hallucinations.
        final_score = (
            (relevance_score * 1.5)
            - (hallucination_penalty * 5.0)
            + (abstraction_bonus * 1.0)
        )

        ranked_candidates.append(
            {
                "summary": candidate,
                "final_score": final_score,
                "relevance_score": relevance_score,
                "hallucination_penalty": hallucination_penalty,
                "abstraction_bonus": abstraction_bonus,
            }
        )

    # Sort the candidates by their final score, descending
    ranked_candidates.sort(key=lambda x: x["final_score"], reverse=True)
    return ranked_candidates


def main():
    print("--- Starting Evaluation of the 'Chief Editor' ---")
    try:
        print("\nStep 1: Loading scoring models...")
        nlp_ner = spacy.load("en_core_web_sm")
        rouge_metric = evaluate.load("rouge")
        print("✅ Scoring models loaded.")

        # --- Run the Reranking ---
        ranked_results = chief_editor_reranker(
            CANDIDATE_SUMMARIES, SOURCE_TEXT, nlp_ner, rouge_metric
        )

        # --- Display the Final Report ---
        print("\n" + "=" * 60)
        print("      CHIEF EDITOR RANKING REPORT")
        print("=" * 60)

        if not ranked_results:
            print("No summaries were provided to rank.")
        else:
            print("\n--- 🏆 The Winning Summary 🏆 ---")
            print(f"   - Final Score: {ranked_results[0]['final_score']:.2f}")
            print(f"   - Summary: {ranked_results[0]['summary']}")

            print("\n" + "-" * 60)
            print("      Full Score Breakdown (Ranked)")
            print("-" * 60)

            for i, item in enumerate(ranked_results):
                print(f"\nRank #{i + 1}:")
                print(f"  Summary: {item['summary']}")
                print(f"  - Final Score: {item['final_score']:.2f}")
                print(
                    f"    (Relevance: {item['relevance_score']} | Hallucinations: {item['hallucination_penalty']} | Abstraction Bonus: {item['abstraction_bonus']})"
                )

    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

    print("\n--- Script Finished ---")


if __name__ == "__main__":
    main()
