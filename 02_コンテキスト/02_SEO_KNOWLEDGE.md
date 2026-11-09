# 02_SEO_KNOWLEDGE.md
この文書は元Repositoryの必要な規則・契約を原文のまま集約したものです。章見出しは元のファイルパスです。


---

## SOURCE: Knowledge/ctr_opportunity/ctr_opportunity_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_CTR_OPPORTUNITY_POLICY_V1",
  "version": "1.0",
  "thresholds": {
    "minimum_impressions": 200,
    "minimum_clicks": 1,
    "position_opportunity_min": 1.0,
    "position_opportunity_max": 10.0,
    "strong_position_max": 5.0,
    "ctr_gap_ratio": -0.25,
    "critical_ctr_gap_ratio": -0.5,
    "winner_query_click_share": 0.4,
    "recent_title_change_days": 28
  },
  "expected_ctr_by_position": [
    {
      "position_max": 1.0,
      "expected_ctr": 0.28
    },
    {
      "position_max": 2.0,
      "expected_ctr": 0.15
    },
    {
      "position_max": 3.0,
      "expected_ctr": 0.1
    },
    {
      "position_max": 5.0,
      "expected_ctr": 0.06
    },
    {
      "position_max": 10.0,
      "expected_ctr": 0.03
    },
    {
      "position_max": 20.0,
      "expected_ctr": 0.015
    },
    {
      "position_max": 100.0,
      "expected_ctr": 0.005
    }
  ],
  "classifications": [
    "CTR_OPPORTUNITY",
    "HIGH_CTR_OPPORTUNITY",
    "WINNER_QUERY_PROTECTED",
    "RECENT_CHANGE_OBSERVATION",
    "HEALTHY_CTR",
    "INSUFFICIENT_DATA"
  ],
  "safety": {
    "low_sample_blocks_opportunity": true,
    "winner_query_requires_protection": true,
    "recent_title_change_requires_observation": true,
    "do_not_rewrite_body_for_ctr_only": true
  }
}

```


---

## SOURCE: Knowledge/position_opportunity/position_opportunity_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_POSITION_OPPORTUNITY_POLICY_V1",
  "version": "1.0",
  "thresholds": {
    "minimum_impressions": 100,
    "low_sample_impressions": 50,
    "near_page_one_min": 8.0,
    "near_page_one_max": 20.0,
    "strong_opportunity_min": 10.0,
    "strong_opportunity_max": 15.0,
    "weak_visibility_position": 30.0,
    "query_concentration_ratio": 0.5,
    "winner_query_click_share": 0.4,
    "competition_resilience_min": 45,
    "content_integrity_min": 55
  },
  "classifications": [
    "POSITION_OPPORTUNITY",
    "HIGH_POSITION_OPPORTUNITY",
    "QUERY_FOCUSED_OPPORTUNITY",
    "WINNER_QUERY_PROTECTED",
    "LOW_VISIBILITY_OR_MISALIGNMENT",
    "HEALTHY_POSITION",
    "INSUFFICIENT_DATA"
  ],
  "safety": {
    "low_sample_blocks_opportunity": true,
    "winner_query_requires_protection": true,
    "low_content_integrity_blocks_aggressive_rewrite": true,
    "position_only_does_not_authorize_new_article": true
  }
}

```


---

## SOURCE: Knowledge/cannibalization/cannibalization_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_CANNIBALIZATION_POLICY_V1",
  "version": "1.0",
  "thresholds": {
    "minimum_shared_queries": 3,
    "possible_query_overlap": 0.4,
    "confirmed_query_overlap": 0.65,
    "merge_query_overlap": 0.75,
    "confirmed_serp_overlap": 0.5,
    "merge_serp_overlap": 0.65,
    "same_intent_min": 0.7,
    "role_separation_intent_max": 0.55,
    "weak_article_traffic_ratio": 0.3,
    "winner_query_click_share": 0.4,
    "minimum_candidate_impressions": 50
  },
  "classifications": [
    "NO_CANNIBALIZATION",
    "POSSIBLE_CANNIBALIZATION",
    "CONFIRMED_CANNIBALIZATION",
    "ROLE_SEPARATION_RECOMMENDED",
    "MERGE_CANDIDATE",
    "FOLLOW_UP_REQUIRED"
  ],
  "safety": {
    "merge_allowed": false,
    "delete_allowed": false,
    "redirect_allowed": false,
    "noindex_allowed": false,
    "winner_query_requires_protection": true,
    "single_candidate_does_not_authorize_action": true
  }
}

```


---

## SOURCE: Knowledge/freshness_decay/freshness_decay_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_FRESHNESS_DECAY_POLICY_V1",
  "version": "1.0",
  "thresholds": {
    "stale_days": 365,
    "severe_stale_days": 730,
    "recent_update_days": 60,
    "minimum_freshness_score": 55,
    "severe_freshness_score": 35,
    "outdated_signal_count": 2,
    "critical_outdated_signal_count": 4,
    "winner_query_click_share": 0.4,
    "minimum_impressions": 100
  },
  "outdated_signal_codes": [
    "OUTDATED_YEAR",
    "OUTDATED_PRICE",
    "OUTDATED_SPECIFICATION",
    "OUTDATED_PROCEDURE",
    "OUTDATED_POLICY",
    "BROKEN_EXTERNAL_REFERENCE",
    "STALE_SCREENSHOT",
    "OBSOLETE_PRODUCT_OR_SERVICE"
  ],
  "classifications": [
    "FRESH",
    "PARTIAL_FRESHNESS_DECAY",
    "SEVERE_FRESHNESS_DECAY",
    "RECENT_UPDATE_OBSERVATION",
    "WINNER_QUERY_PROTECTED",
    "INSUFFICIENT_DATA"
  ],
  "safety": {
    "recent_update_requires_observation": true,
    "winner_query_blocks_aggressive_title_change": true,
    "freshness_only_does_not_authorize_deletion": true,
    "partial_decay_prefers_local_update": true
  }
}

```


---

## SOURCE: Knowledge/intent_drift/intent_drift_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_INTENT_DRIFT_POLICY_V1",
  "version": "1.0",
  "thresholds": {
    "minimum_impressions": 100,
    "minimum_queries": 3,
    "primary_intent_share_min": 0.55,
    "secondary_intent_share_warning": 0.3,
    "intent_entropy_high": 0.75,
    "query_title_overlap_min": 0.35,
    "winner_query_click_share": 0.4,
    "emerging_intent_growth_ratio": 0.5
  },
  "classifications": [
    "ALIGNED",
    "INTENT_DRIFT",
    "TOPIC_DISPERSION",
    "EMERGING_INTENT_TRANSITION",
    "WINNER_QUERY_PROTECTED",
    "INSUFFICIENT_DATA"
  ],
  "safety": {
    "winner_query_blocks_aggressive_retargeting": true,
    "intent_drift_does_not_authorize_new_article_alone": true,
    "low_sample_blocks_confirmation": true,
    "article_title_and_query_overlap_is_supporting_evidence_only": true
  }
}

```


---

## SOURCE: Knowledge/long_term_degradation/long_term_degradation_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_LONG_TERM_DEGRADATION_POLICY_V1",
  "version": "1.0",
  "thresholds": {
    "chronic_visibility_decline": -0.25,
    "sharp_visibility_decline": -0.4,
    "ctr_decline": -0.25,
    "position_decline": 2.0,
    "vital_score_decline": -10,
    "recurrence_count": 2,
    "seasonality_score": 0.75,
    "recovery_visibility_growth": 0.2,
    "minimum_windows": 6
  },
  "classifications": [
    "STABLE",
    "CHRONIC_DEGRADATION",
    "SHARP_DEGRADATION",
    "CTR_DEGRADATION",
    "POSITION_DEGRADATION",
    "SEASONAL_VARIATION",
    "RECOVERY_IN_PROGRESS",
    "INSUFFICIENT_HISTORY"
  ],
  "safety": {
    "seasonality_blocks_chronic_diagnosis_when_strong": true,
    "recovery_blocks_degradation_when_current": true,
    "low_sample_reduces_confidence": true
  }
}

```


---

## SOURCE: Knowledge/algorithm_impact/algorithm_impact_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_ALGORITHM_IMPACT_POLICY_V1",
  "version": "1.0",
  "principles": {
    "algorithm_update_is_evidence_not_diagnosis": true,
    "temporal_overlap_alone_is_insufficient": true,
    "official_google_source_preferred": true,
    "site_and_serp_corroboration_required_for_high_confidence": true
  },
  "weights": {
    "temporal": 25,
    "site_wide": 30,
    "segment": 10,
    "article": 15,
    "serp": 20
  },
  "thresholds": {
    "low": 20,
    "possible": 40,
    "likely": 60,
    "high": 80
  },
  "wait_policy": {
    "eligible_statuses": ["LIKELY", "HIGH"],
    "eligible_rollout_statuses": ["IN_PROGRESS"],
    "minimum_wait_days": 7,
    "recommended_review_days": 14,
    "block_wait_when_severe_content_integrity_problem": true
  }
}

```


---

## SOURCE: Knowledge/external_factors/external_demand_policy_v1.json

```json
{
  "policy_name": "external_demand_policy_v1",
  "version": "1.0.0",
  "demand_health": ["GROWING", "STABLE", "SHRINKING", "COLLAPSED", "UNKNOWN"],
  "evidence_types": [
    "SEARCH_CONSOLE",
    "SERP_SNAPSHOT",
    "OFFICIAL_ANNOUNCEMENT",
    "NEWS",
    "SEASONALITY",
    "MANUAL_WEB_VERIFICATION"
  ],
  "improvement_failure_exclusion": {
    "minimum_external_factor_confidence": 80,
    "excluded_when_demand_health": ["SHRINKING", "COLLAPSED"]
  }
}

```


---

## SOURCE: Knowledge/external_demand.md

```markdown
# External Demand Knowledge RC4

記事の検索流入減少は、記事品質だけでなく外部需要の変化でも起こる。

評価区分：
- 成長中
- 安定
- 縮小中
- ほぼ消失
- 判定不能

公式発表や制度終了が検索需要縮小を高い確度で説明する場合、改善失敗を確定しない。
手動Web確認はSBM取得SERPと区別し、source_typeを記録する。

```


---

## SOURCE: Knowledge/internal_link_referral_policy_v1.md

```markdown
# Internal Link Referral Policy V1

Doctor may recommend internal-link destinations as part of a treatment plan, but does not write the final insertion copy.

Each recommendation should identify:
- `url`
- `title` when known
- `reason`: why this destination is relevant
- `relationship`: how it relates to the treated article/readers
- `suggested_context`: where/when the link is useful
- `suggested_anchor_hint`: optional hint only

Writer owns final placement, surrounding sentence, and anchor wording after reading the source article and referral context. Doctor must not force title-only link lists.

SBM remains the orchestration hub and preserves the recommendation metadata when generating Writer referrals.

```


---

## SOURCE: Knowledge/url_identity_diagnostic_rule.md

```markdown
# URL Identity Diagnostic Rule v1.0

## Purpose
Prevent false indexing diagnoses when the user-supplied URL and the indexed URL differ only by a trailing slash.

## Required order
1. Read the requested article URL.
2. Read Search Console `matched_url` when supplied.
3. Compare canonical URL, Google-selected canonical, and redirect target when available.
4. Test both trailing-slash variants before concluding that the page is not indexed.
5. Separate technical indexing failure from ranking/evaluation loss.

## Decision rules
- `/1238` and `/1238/` are not automatically different articles.
- If the indexed or matched URL is the trailing-slash variant, treat it as the same resource unless evidence shows otherwise.
- A non-indexed alias must not be described as an indexing failure when the canonical variant is indexed.
- When the canonical variant is indexed but impressions collapse, prioritize ranking loss, site-wide evaluation change, algorithm update, demand change, or SERP competition.
- Ask the user only for the Google-selected canonical when supplied evidence cannot resolve the identity.

## User-facing language
Do not ask the user to choose whether a trailing slash should exist. WordPress, Hatena, the web server, redirects, and canonical settings normally determine it.

```
