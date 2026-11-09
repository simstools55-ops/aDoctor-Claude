# 03_TREATMENT_AND_FOLLOWUP.md
この文書は元Repositoryの必要な規則・契約を原文のまま集約したものです。章見出しは元のファイルパスです。


---

## SOURCE: Knowledge/treatment/rules/treatment_rules_v1.json

```json
{
  "rule_set": "SIMS_DOCTOR_TREATMENT_RULES_V1",
  "version": "1.0",
  "rules": [
    {
      "diagnosis_code": "CTR_PROBLEM",
      "treatment_code": "REWRITE_SNIPPET_AND_INTENT_ALIGNMENT",
      "target": "WRITER",
      "priority": "HIGH",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "POSITION_DECLINE",
      "treatment_code": "REWRITE_CONTENT_RECOVERY",
      "target": "WRITER",
      "priority": "HIGH",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "CONTENT_STALE",
      "treatment_code": "REFRESH_OUTDATED_CONTENT",
      "target": "WRITER",
      "priority": "MEDIUM",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "UPDATE_FAILURE",
      "treatment_code": "REASSESS_FAILED_TREATMENT",
      "target": "WRITER",
      "priority": "HIGH",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "CANNIBALIZATION",
      "treatment_code": "REVIEW_QUERY_CONFLICT",
      "target": "MERGE",
      "priority": "HIGH",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "ARTICLE_MERGE_REQUIRED",
      "treatment_code": "MERGE_OVERLAPPING_ARTICLES",
      "target": "MERGE",
      "priority": "HIGH",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "NEW_ARTICLE_NEEDED",
      "treatment_code": "CREATE_DISTINCT_INTENT_ARTICLE",
      "target": "CREATOR",
      "priority": "MEDIUM",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "LONG_TERM_DECAY",
      "treatment_code": "REWRITE_LONG_TERM_RECOVERY",
      "target": "WRITER",
      "priority": "HIGH",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "SEASONAL_DECLINE",
      "treatment_code": "SEASONAL_OBSERVATION",
      "target": "OBSERVATION",
      "priority": "LOW",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "RECOVERY_IN_PROGRESS",
      "treatment_code": "CONTINUE_OBSERVATION",
      "target": "OBSERVATION",
      "priority": "LOW",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "TREATMENT_SUCCESS",
      "treatment_code": "CONTINUE_EFFECT_MONITORING",
      "target": "OBSERVATION",
      "priority": "LOW",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "IMPROVEMENT_FAILURE",
      "treatment_code": "REASSESS_INEFFECTIVE_IMPROVEMENT",
      "target": "WRITER",
      "priority": "HIGH",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "POST_IMPROVEMENT_WORSENING",
      "treatment_code": "REVIEW_AND_ROLLBACK_WORSENING",
      "target": "WRITER",
      "priority": "HIGH",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "MIXED_TREATMENT_RESPONSE",
      "treatment_code": "ADDITIONAL_EFFECT_MEASUREMENT",
      "target": "OBSERVATION",
      "priority": "MEDIUM",
      "required_status": "CONFIRMED"
    },
    {
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "treatment_code": "WAIT_FOR_EFFECT_MEASUREMENT",
      "target": "OBSERVATION",
      "priority": "LOW",
      "required_status": "CONFIRMED"
    }
  ],
  "deferred_rules": [
    {
      "defer_reason": "LOW_SAMPLE_ONLY",
      "treatment_code": "OBSERVATION_ONLY",
      "target": "OBSERVATION",
      "priority": "LOW"
    },
    {
      "defer_reason": "CLOSE_CANDIDATES",
      "treatment_code": "ADDITIONAL_OBSERVATION",
      "target": "OBSERVATION",
      "priority": "MEDIUM"
    },
    {
      "defer_reason": "MISSING_EVIDENCE",
      "treatment_code": "COLLECT_MISSING_EVIDENCE",
      "target": "OBSERVATION",
      "priority": "MEDIUM"
    },
    {
      "defer_reason": "MISSING_FINDINGS",
      "treatment_code": "COLLECT_MISSING_EVIDENCE",
      "target": "OBSERVATION",
      "priority": "MEDIUM"
    },
    {
      "defer_reason": "MISSING_CONTEXT",
      "treatment_code": "COLLECT_TREATMENT_HISTORY",
      "target": "OBSERVATION",
      "priority": "MEDIUM"
    },
    {
      "defer_reason": "CONTRADICTION",
      "treatment_code": "MANUAL_REVIEW",
      "target": "OBSERVATION",
      "priority": "MEDIUM"
    },
    {
      "defer_reason": "NO_CANDIDATE",
      "treatment_code": "OBSERVATION_ONLY",
      "target": "OBSERVATION",
      "priority": "LOW"
    },
    {
      "defer_reason": "INSUFFICIENT_DATA",
      "treatment_code": "OBSERVATION_ONLY",
      "target": "OBSERVATION",
      "priority": "LOW"
    },
    {
      "defer_reason": "LOW_CONFIDENCE",
      "treatment_code": "ADDITIONAL_OBSERVATION",
      "target": "OBSERVATION",
      "priority": "MEDIUM"
    }
  ]
}

```


---

## SOURCE: Knowledge/treatment_recommendation/treatment_recommendation_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_TREATMENT_RECOMMENDATION_POLICY_V1",
  "version": "1.0",
  "referral_targets": [
    "SIMS_WRITER",
    "SIMS_CREATOR",
    "SIMS_MERGE",
    "OBSERVE",
    "FOLLOW_UP",
    "NONE"
  ],
  "mapping": {
    "HEALTHY": {
      "target": "NONE",
      "treatment_mode": "NO_TREATMENT",
      "scope": []
    },
    "MINOR_REFRESH": {
      "target": "SIMS_WRITER",
      "treatment_mode": "LOCAL_REFRESH",
      "scope": [
        "FACTS",
        "YEAR",
        "PRICE",
        "SPECIFICATION",
        "FAQ"
      ]
    },
    "LOCAL_OPTIMIZATION": {
      "target": "SIMS_WRITER",
      "treatment_mode": "LOCAL_OPTIMIZATION",
      "scope": [
        "SEO_TITLE",
        "META_DESCRIPTION",
        "INTRODUCTION",
        "HEADINGS",
        "FAQ",
        "INTERNAL_LINKS"
      ]
    },
    "FULL_REWRITE_RECOMMENDED": {
      "target": "SIMS_WRITER",
      "treatment_mode": "FULL_REWRITE",
      "scope": [
        "SEO_TITLE",
        "META_DESCRIPTION",
        "INTRODUCTION",
        "STRUCTURE",
        "BODY",
        "FAQ",
        "INTERNAL_LINKS"
      ]
    },
    "NEW_ARTICLE_RECOMMENDED": {
      "target": "SIMS_CREATOR",
      "treatment_mode": "NEW_ARTICLE",
      "scope": [
        "NEW_ARTICLE_BRIEF"
      ]
    },
    "MERGE_RECOMMENDED": {
      "target": "SIMS_MERGE",
      "treatment_mode": "MERGE_REVIEW",
      "scope": [
        "SOURCE_ARTICLES",
        "PRIMARY_ARTICLE",
        "REDIRECT_PLAN",
        "ROLE_CONSOLIDATION"
      ]
    },
    "OBSERVE_ONLY": {
      "target": "OBSERVE",
      "treatment_mode": "OBSERVATION",
      "scope": [
        "MONITORING"
      ]
    },
    "FOLLOW_UP_REQUIRED": {
      "target": "FOLLOW_UP",
      "treatment_mode": "FOLLOW_UP",
      "scope": [
        "ADDITIONAL_DATA",
        "REASSESSMENT"
      ]
    }
  },
  "safety": {
    "doctor_never_executes_treatment": true,
    "winner_query_blocks_full_rewrite": true,
    "merge_requires_merge_target": true,
    "creator_requires_new_article_allowed": true,
    "full_rewrite_requires_full_rewrite_allowed": true,
    "no_delete_noindex_redirect_execution": true
  },
  "wait_policy": {
    "minimum_wait_days": 7,
    "recommended_review_days": 14
  }
}

```


---

## SOURCE: Knowledge/clinical_review/clinical_review_policy_v1.json

```json
{
  "policy_name": "clinical_review_policy_v1",
  "version": "1.0.0",
  "diagnostic_order": [
    "EVIDENCE_VALIDATION",
    "CLINICAL_REVIEW",
    "SEO_PERFORMANCE_REVIEW",
    "SERP_REVIEW",
    "COMPOSITE_DIAGNOSIS",
    "TREATMENT_RECOMMENDATION"
  ],
  "checks": [
    "INTERNAL_CONTRADICTION",
    "FACTUAL_ACCURACY",
    "FRESHNESS",
    "TITLE_BODY_ALIGNMENT",
    "INTERNAL_LINK_RELEVANCE"
  ],
  "low_sample_rule": {
    "block_broad_seo_rewrite": true,
    "allow_factual_correction": true,
    "allow_internal_contradiction_repair": true,
    "allow_freshness_verification": true,
    "allow_low_relevance_link_removal": true
  },
  "user_language": "ja"
}

```


---

## SOURCE: Knowledge/clinical_review.md

```markdown
# Clinical Review Knowledge RC4

## 検査対象
- 同一記事内の相反する説明
- 公式情報と一致しない可能性がある記述
- 名称、料金、対応機器、制度、サービス仕様の鮮度
- SEOタイトル・H1・本文の約束の一致
- FAQと本文の矛盾
- 内部リンク候補の意味的関連性

## 処置
- FACTUAL_CORRECTION_REQUIRED
- LIMITED_CONTENT_REPAIR
- FRESHNESS_VERIFICATION_REQUIRED
- LOW_RELEVANCE_INTERNAL_LINKS

本文修正は必要箇所だけに限定し、LOW_SAMPLEを理由に明確な誤りを放置しない。

```


---

## SOURCE: Knowledge/case_lifecycle.md

```markdown
# Case Lifecycle v1

## Sprint2-1 active states

| State | Meaning | Next state |
|---|---|---|
| OPEN | Case ID has been reserved | REQUEST_VALIDATED or ERROR |
| REQUEST_VALIDATED | External request passed validation | RECORD_CREATED or ERROR |
| RECORD_CREATED | Medical record was created | READY_FOR_OBSERVATION or ERROR |
| READY_FOR_OBSERVATION | Observation Engine may begin | OBSERVING |
| ERROR | Reception transaction failed | retry or manual review |

## Future states

`OBSERVING → DIAGNOSING → DIAGNOSED → REFERRED → UNDER_TREATMENT → FOLLOW_UP → CLOSED`

## Invariants

1. A case has exactly one medical record.
2. A medical record ID never changes.
3. An active case is identified primarily by `site_id + article_id`.
4. A second request for an active case is appended to the same medical record.
5. A closed case creates a new case in Doctor v1.0.
6. Registry commit and medical-record creation are one transaction.
7. Observation and diagnosis never read the raw SBM request directly.

```


---

## SOURCE: Knowledge/improvement_failure/improvement_failure_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_IMPROVEMENT_FAILURE_POLICY_V1",
  "version": "1.0",
  "minimum_follow_up_days": 7,
  "preferred_confirm_days": 28,
  "thresholds": {
    "no_effect_absolute_effect_score": 0.05,
    "worsening_effect_score": -0.15,
    "wrong_direction_effect_score": -0.05,
    "vital_score_decline": -8,
    "ctr_decline_ratio": -0.2,
    "position_decline_ratio": -0.15,
    "impression_decline_ratio": -0.2,
    "recurrence_count": 2,
    "minimum_impressions": 100
  },
  "classifications": [
    "TREATMENT_EFFECTIVE",
    "NO_MEASURABLE_EFFECT",
    "POST_TREATMENT_WORSENING",
    "POSSIBLE_WRONG_TREATMENT_DIRECTION",
    "RECURRENT_FAILURE",
    "INSUFFICIENT_FOLLOW_UP"
  ],
  "safety": {
    "low_sample_cannot_confirm_failure": true,
    "automatic_rollback_forbidden": true,
    "writer_review_required_for_wrong_direction": true
  }
}

```


---

## SOURCE: Knowledge/observation/article_snapshot/article_snapshot_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_ARTICLE_SNAPSHOT_POLICY_V1",
  "version": "1.0",
  "limits": {
    "maximum_headings": 300,
    "maximum_internal_links": 1000,
    "maximum_faq_items": 100,
    "maximum_title_length": 1000,
    "maximum_text_length": 1000000
  },
  "content_integrity": {
    "weights": {
      "title_presence": 0.1,
      "heading_structure": 0.2,
      "faq_coverage": 0.15,
      "internal_link_support": 0.15,
      "intent_alignment": 0.25,
      "freshness_markers": 0.15
    },
    "minimum_heading_count": 3,
    "minimum_internal_links": 2,
    "minimum_faq_items": 1
  },
  "comparison": {
    "track_title_change": true,
    "track_heading_change": true,
    "track_faq_change": true,
    "track_internal_link_change": true
  }
}

```


---

## SOURCE: Knowledge/observation/cross_article/cross_article_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_CROSS_ARTICLE_POLICY_V1",
  "version": "1.0",
  "thresholds": {
    "minimum_shared_queries": 3,
    "minimum_query_overlap_ratio": 0.35,
    "minimum_title_similarity": 0.55,
    "minimum_intent_similarity": 0.7,
    "dominance_ratio_for_primary_article": 1.5,
    "minimum_candidate_impressions": 100
  },
  "classifications": [
    "NO_CONFLICT",
    "POSSIBLE_CANNIBALIZATION",
    "MERGE_CANDIDATE",
    "SEPARATE_INTENT",
    "NEW_ARTICLE_OPPORTUNITY"
  ],
  "safety": {
    "never_auto_merge": true,
    "never_auto_delete": true,
    "creator_requires_distinct_intent": true
  }
}

```


---

## SOURCE: Knowledge/observation/long_term/long_term_analysis_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_LONG_TERM_ANALYSIS_POLICY_V1",
  "version": "1.0",
  "window_days": 28,
  "minimum_windows": 6,
  "trend_thresholds": {
    "gradual_decline_ratio": 0.25,
    "sharp_decline_ratio": 0.4,
    "ctr_decline_ratio": 0.25,
    "position_decline_absolute": 2.0,
    "recovery_ratio": 0.2,
    "seasonality_similarity_threshold": 0.75
  },
  "minimum_sample": {
    "impressions_per_window": 100,
    "clicks_per_window": 1
  },
  "classification": [
    "STABLE",
    "GRADUAL_DECLINE",
    "SHARP_DECLINE",
    "CTR_DECAY",
    "POSITION_DECAY",
    "SEASONAL_PATTERN",
    "RECOVERY"
  ]
}

```


---

## SOURCE: Knowledge/observation/observation_types.json

```json
{
  "registry_name": "OBSERVATION_TYPE_REGISTRY",
  "version": "1.0",
  "items": [
    {
      "code": "SEARCH_CONSOLE",
      "description": "Search Consoleの期間別・クエリ別実測値",
      "required_fields": [
        "periods",
        "queries"
      ],
      "evaluation_allowed": false
    },
    {
      "code": "SERP",
      "description": "検索結果面、競合、検索意図、SERP機能の観察",
      "required_fields": [
        "query",
        "observed_at",
        "results"
      ],
      "evaluation_allowed": false
    },
    {
      "code": "ARTICLE_SNAPSHOT",
      "description": "記事タイトル、見出し、本文構造、FAQ、更新情報のスナップショット",
      "required_fields": [
        "captured_at",
        "title",
        "headings"
      ],
      "evaluation_allowed": false
    },
    {
      "code": "INTERNAL_LINKS",
      "description": "受信・発信内部リンクの観察",
      "required_fields": [
        "captured_at",
        "incoming",
        "outgoing"
      ],
      "evaluation_allowed": false
    },
    {
      "code": "HISTORY",
      "description": "改善、診断、紹介、治療結果の履歴",
      "required_fields": [
        "events"
      ],
      "evaluation_allowed": false
    },
    {
      "code": "METADATA",
      "description": "公開日、更新日、カテゴリ、タグなどのメタデータ",
      "required_fields": [
        "captured_at"
      ],
      "evaluation_allowed": false
    },
    {
      "code": "TREATMENT_HISTORY",
      "description": "改善前後の効果測定履歴",
      "source": "SBM_IMPROVEMENT_HISTORY"
    }
  ]
}

```


---

## SOURCE: Knowledge/observation/search_console/acquisition_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_SEARCH_CONSOLE_ACQUISITION_POLICY_V1",
  "version": "1.0",
  "coverage_days": 365,
  "periods": {
    "days_28": 28,
    "days_90": 90,
    "days_365": 365
  },
  "query_rows": {
    "page_size": 25000,
    "maximum_rows": 200000,
    "sort": "CLICKS_DESC"
  },
  "retry": {
    "maximum_attempts": 3,
    "retryable_errors": [
      "RATE_LIMIT",
      "TEMPORARY_UNAVAILABLE",
      "TIMEOUT"
    ]
  },
  "status_policy": {
    "all_requests_successful": "COMPLETE",
    "some_requests_failed": "PARTIAL",
    "all_requests_failed": "FAILED",
    "successful_with_zero_rows": "NO_DATA"
  },
  "date_policy": {
    "end_date_lag_days": 3,
    "timezone": "SITE_DEFAULT"
  }
}

```


---

## SOURCE: Knowledge/observation/serp/serp_observation_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_SERP_OBSERVATION_POLICY_V1",
  "version": "1.0",
  "result_limit": 10,
  "comparison_depth": 10,
  "features": [
    "AI_OVERVIEW",
    "FEATURED_SNIPPET",
    "PEOPLE_ALSO_ASK",
    "VIDEO",
    "IMAGE_PACK",
    "LOCAL_PACK",
    "SHOPPING",
    "NEWS"
  ],
  "intent_labels": [
    "INFORMATIONAL",
    "HOW_TO",
    "COMPARISON",
    "TRANSACTIONAL",
    "NAVIGATIONAL",
    "LOCAL",
    "MIXED",
    "UNKNOWN"
  ],
  "competition": {
    "authority_weight": 0.35,
    "exact_intent_match_weight": 0.3,
    "freshness_weight": 0.2,
    "serp_feature_weight": 0.15,
    "score_min": 0,
    "score_max": 100
  },
  "retry": {
    "maximum_attempts": 3,
    "retryable_errors": [
      "RATE_LIMIT",
      "TEMPORARY_UNAVAILABLE",
      "TIMEOUT"
    ]
  },
  "privacy": {
    "store_snippets": true,
    "maximum_snippet_length": 500
  }
}

```


---

## SOURCE: Knowledge/observation/treatment_history/treatment_history_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_TREATMENT_HISTORY_POLICY_V1",
  "version": "1.0",
  "minimum_follow_up_days": 7,
  "preferred_checkpoints_days": [
    7,
    14,
    28
  ],
  "metric_weights": {
    "clicks": 0.35,
    "impressions": 0.2,
    "ctr": 0.25,
    "position": 0.2
  },
  "thresholds": {
    "improved_score": 0.15,
    "partial_improvement_score": 0.05,
    "worsened_score": -0.15,
    "no_effect_absolute_score": 0.05,
    "single_metric_guardrail_decline": -0.3,
    "minimum_baseline_impressions": 100
  },
  "classifications": [
    "IMPROVED",
    "PARTIAL_IMPROVEMENT",
    "NO_EFFECT",
    "WORSENED",
    "MIXED_RESPONSE",
    "INSUFFICIENT_FOLLOW_UP"
  ],
  "safety": {
    "never_auto_rollback": true,
    "rollback_is_writer_review_only": true,
    "low_sample_cannot_confirm_worsening": true
  }
}

```


---

## SOURCE: Knowledge/longitudinal/longitudinal_profile_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_LONGITUDINAL_PROFILE_POLICY_V1",
  "version": "1.0",
  "minimum_completed_diagnoses": 2,
  "thresholds": {
    "recurrence_count": 2,
    "chronic_case_count": 3,
    "treatment_success_ratio_good": 0.6,
    "treatment_failure_ratio_high": 0.5,
    "recent_window_cases": 3,
    "urgent_recurrence_days": 60
  },
  "profile_statuses": [
    "INSUFFICIENT_HISTORY",
    "STABLE",
    "RECURRENT",
    "CHRONIC",
    "TREATMENT_RESPONSIVE",
    "TREATMENT_RESISTANT",
    "RECOVERING"
  ],
  "priority_levels": [
    "LOW",
    "MEDIUM",
    "HIGH",
    "URGENT"
  ],
  "safety": {
    "profile_is_not_final_diagnosis": true,
    "no_automatic_treatment": true,
    "no_automatic_deletion": true
  }
}

```


---

## SOURCE: Knowledge/referral/rules/referral_rules_v1.json

```json
{
  "rule_set": "SIMS_DOCTOR_REFERRAL_RULES_V1",
  "version": "1.0",
  "targets": [
    "WRITER",
    "CREATOR",
    "MERGE",
    "OBSERVATION",
    "NOINDEX_REVIEW",
    "DELETE_REVIEW"
  ],
  "policies": {
    "diagnosis_and_referral_are_separate": true,
    "doctor_does_not_execute_treatment": true,
    "deferred_diagnosis_cannot_route_to_writer_creator_merge": true,
    "unsupported_target_behavior": "REJECT"
  }
}

```


---

## SOURCE: Knowledge/reporting/DIRECT_SPECIALIST_HANDOFF_V1_0_3.md

```markdown
# Direct Specialist Handoff v1.0.3

## 正式フロー

SBM → Doctor → Writer / Creator / Merge → SBM

Doctorは診断後、対象製品への依頼文を利用者向け本文に必ず表示する。利用者はその依頼文を直接対象製品へ渡す。Doctor診断結果をSBMへ登録して同じ依頼文を再生成する運用は行わない。

## SBMの役割

- Doctor依頼の作成
- CaseIDの発行と保持
- Writer / Creator / Mergeの処置結果の登録
- 公開後の効果測定
- 再診予定の管理

Doctor診断JSONは監査・保管用の任意情報であり、通常運用では利用者が登録する必要はない。

## Doctor出力

1. 優先順位チェックリスト
2. 今回やること
3. 利用者が確認すること（結果別の次の行動を含む）
4. 対象製品へのコピー可能な依頼文
5. 診断結果と根拠
6. 再診条件
7. 診断記録JSON（通常操作不要）

Writer等への依頼文にはCaseID、ArticleID、実施範囲、禁止範囲、依存条件、および「処置結果をSBMへ登録する」指示を含める。

```


---

## SOURCE: Knowledge/reporting/SBM_ORCHESTRATED_HANDOFF_V1_1_2.md

```markdown
# SBM Orchestrated Specialist Handoff v1.1.2

## 正式ワークフロー

`SBM → Doctor → SBM → Writer / Creator / Merge → SBM`

Doctorは診断と治療方針決定を担当し、専門製品への最終紹介状は作成しない。DoctorはSBM登録用の機械可読診断結果を返す。SBMは最初の診断依頼時に保持した記事本文、検索クエリ、内部リンク候補、改善履歴とDoctor診断を統合し、次の担当製品へ渡す完全な紹介状を生成する。

## 理由

Doctorから専門製品へ直接渡す短い依頼文だけでは、WriterがBeforeを確定するための記事本文や、判断に必要なクエリ・履歴が不足する可能性がある。カルテを保持するSBMが紹介状を生成することで、責務分離と情報完全性を両立する。

## 利用者操作

1. SBMの精密診断ダイアログ上段からDoctor依頼JSONをコピーする。
2. Doctorへ貼り付ける。
3. Doctor回答末尾のSBM登録用診断結果JSONだけをコピーする。
4. 同じダイアログ下段へ貼り付けて登録する。
5. SBMが即時表示するWriter / Creator / Merge紹介状をコピーする。

```


---

## SOURCE: Knowledge/reporting/TREATMENT_PLAN_UX_V1_1_0.md

```markdown
# SIMS Article Doctor v1.1.0 Treatment Plan UX Standard

## Purpose
Doctorの回答はSEOレポートではなく、利用者が安心して次の行動へ進むための治療計画書です。

## Required order
1. Doctorコメント
2. 総合診断（診断、確信度、治療区分、次の担当）
3. 今回やること
4. 今回はやらないこと
5. この方針にした理由
6. 利用者へのアドバイス
7. Writer / Creator / Mergeへのコピー専用依頼文
8. SBMで行うこと
9. 次回診察予定

## Confidence policy
- 95%以上: ほぼ確定。Doctorが方針を決定する。
- 80〜94%: 可能性が高い。利用者へ分析を委ねず、Doctorが方針を決定する。
- 60〜79%: 有力な推定。低リスク処置を優先し、必要最小限の確認だけ依頼できる。
- 40〜59%: 追加証拠が望ましい。大規模処置を止める。
- 40%未満: 診断保留。

## Reassurance
安心コメントは根拠のない楽観ではありません。重大な問題がない場合、慌てて全面リライト、URL変更、削除を行う必要がないことを明確にします。

## User workload
SEO分析、サイト横断比較、原因切り分けを利用者へ丸投げしません。Doctorが利用可能な証拠から判断します。利用者確認は、Search Console URL検査などDoctorが実行できない検査で、かつ治療分岐に不可欠な場合だけです。

## Copy-ready handoff
担当製品への依頼文は独立したプレーンテキストコードブロックとして表示します。説明文、診断JSON、コピー対象外の注記を混在させません。

## JSON
通常利用者向け回答にDoctor診断JSONを表示しません。SBMへ登録するのはWriter / Creator / Mergeが処置完了後に返す結果JSONだけです。

```


---

## SOURCE: Knowledge/reporting/USER_ACTION_FIRST_OUTPUT.md

```markdown
# SIMS Article Doctor User Action First Output Standard v1.0.1

## 目的
Doctorの利用者向け回答は、診断説明より先に「利用者が次に行う作業」を示す。Doctorは治療を実行せず、SBMへ診断結果と紹介内容を返す。

## 必須表示順
1. 今回やること
2. そのまま使える依頼文
3. 診断結果
4. 診断の根拠
5. 今回行わないこと
6. 再診時期・未評価項目
7. 機械連携用JSON

## 「今回やること」の必須項目
- 利用者またはSBMで確認すること
- Writerへ依頼するか
- Creatorへ依頼するか
- Mergeへ依頼するか
- 大規模リライトの可否
- 再診時期

対象外の製品も省略せず「今回は不要」と明記する。

## 依頼文
治療が必要な場合は、SBMが後続製品へ渡せる依頼文を生成する。依頼文には担当製品、実施範囲、保護範囲、禁止範囲、前提条件を含める。
DoctorからWriter、Creator、Mergeを直接起動してはならない。正式な返却先はSBMとする。

## 利用者向け表現
英語の内部コードは利用者向け本文へ表示しない。
- LONG_TERM_DECLINE: 長期間にわたり検索表示やクリックが減っています
- CLIFF_DROP: ある時点から検索表示が急激に落ちています
- LOW_SAMPLE: 直近のデータが少なく、この期間だけでは判断できません
- INDEXED: Google検索には登録されています
- NOT_ASSESSABLE: 判断に必要なデータが不足しています

内部コードは機械連携用JSON、Trace、QAにのみ保持する。

## 禁止表現
- 記事IDだけを使った過去事例参照
- 説明のない略語、記号、星評価
- 利用者が次の作業を判断しなければならない曖昧な結論
- 「利用者の判断で回してよい」だけで終わる表現

```


---

## SOURCE: Knowledge/reporting/USER_FACING_JSON_HIDDEN_V1_0_4.md

```markdown
# 利用者向けJSON非表示とコピー用依頼文 v1.0.4

## 正式フロー

`SBM → Doctor → Writer / Creator / Merge → SBM`

Article Doctorの診断結果JSONは内部監査用に保持し、通常の利用者向け回答には表示しない。
利用者がSBMへ登録するのは、Writer・Creator・Mergeが処置完了後に返す結果だけである。

## 利用者向け回答の必須順序

1. 優先順位チェックリスト
2. 今回やること
3. 利用者が確認すること（必要な場合のみ）
4. 担当製品へそのまま渡す依頼文
5. 診断結果
6. 診断の根拠
7. 今回行わないこと
8. 再診時期と未評価項目

## 依頼文の表示規則

担当製品への依頼がある場合は、直前に次の案内を明記する。

> 下の枠内をすべてコピーし、SIMS Writerへそのまま貼り付けてください。

依頼文は単独のプレーンテキストコードブロックに入れる。コードブロック内には説明、前置き、JSON、診断詳細を混在させない。
Writer、Creator、Mergeが複数必要な場合は、それぞれ別のコードブロックにする。

依頼文には最低限、CaseID、ArticleID、記事タイトル、治療区分、実施範囲、変更禁止範囲、前提条件、処置完了後にSBMへ結果を登録する指示を含める。

## 利用者確認の分岐

利用者による確認が必要な場合は、「確認してください」で終わらせない。
正常・異常・判断不能など、確認結果ごとの次の行動を明記する。

## JSON

利用者向け回答にDoctor結果JSONを表示しない。
内部Contract、テスト、監査ログでは従来の機械可読結果を維持してよい。
利用者から開発者向けJSONを明示的に求められた場合だけ、通常回答と分離して提示する。

```


---

## SOURCE: Knowledge/reporting/WORKFLOW_HANDOFF_V1_0_2.md

```markdown
# SIMS Article Doctor Workflow Handoff Standard v1.0.2

## 目的
Doctorは診断結果を説明するだけでなく、利用者とSBMが次の工程へ迷わず進めるための治療指示と依頼文を返す。
DoctorはWriter、Creator、Mergeを直接起動せず、正式な返却先はSBMとする。

## 必須表示順
1. 今回やること
2. 優先順位付きチェックリスト
3. そのまま使える依頼文
4. 診断結果
5. 診断の根拠
6. 今回行わないこと
7. 再診時期と未評価項目
8. JSON（機械連携用）

## 利用者向けの担当表現
- 「SBMへ渡す依頼」は使用しない。
- 利用者自身の確認作業は「利用者が確認すること」と表示する。
- Writer、Creator、Mergeは「実施」「今回は不要」「保留」を明示する。
- 対象外の製品も省略しない。

## 治療区分
Doctorは後続工程へ次のいずれかを返す。
- 軽微修正: 事実・表記・内部リンクなど、構成を変えない小さな修正
- 限定修正: 指定箇所だけを直し、記事全体は維持する修正
- 通常リライト: 検索意図に合わせて複数箇所を改善する修正
- 全面リライト: 構成から見直す大規模修正
- 新規記事作成: Creatorによる別記事作成
- 記事統合: Mergeによる統合または役割分担
- 経過観察: 治療を行わず再測定

## 優先順位付きチェックリスト
利用者が実行する順番を1、2、3の番号で示す。星や記号だけで優先度を表さない。
各項目には担当、作業内容、実施時期、前提条件を含める。

## JSON引き渡し
機械連携用JSONには `workflow_handoff` を追加する。

必須項目:
- `treatment_class`
- `action_checklist`
- `user_confirmation_text`
- `writer_request_text`
- `creator_request_text`
- `merge_request_text`
- `dependencies`

不要な依頼文は空文字ではなく `null` とする。
既存の診断、referral、workflow項目は削除せず、後方互換を維持する。

## 利用者向け表現
英語の内部コードは本文へ表示しない。内部コードはJSON、Trace、QAにのみ保持する。
記事IDだけを用いた過去事例参照、説明のない略語、曖昧な判断委任は禁止する。

```


---

## SOURCE: Knowledge/reporting/doctor_report_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_REPORT_POLICY_V1",
  "version": "1.0",
  "audiences": [
    "USER",
    "SYSTEM"
  ],
  "labels": {
    "HEALTHY": "治療不要",
    "MINOR_REFRESH": "部分更新",
    "LOCAL_OPTIMIZATION": "局所改善",
    "FULL_REWRITE_RECOMMENDED": "大規模リライト推奨",
    "NEW_ARTICLE_RECOMMENDED": "新記事作成推奨",
    "MERGE_RECOMMENDED": "記事統合推奨",
    "OBSERVE_ONLY": "経過観察",
    "FOLLOW_UP_REQUIRED": "再診・追加データ"
  },
  "safety": {
    "hide_internal_rule_ids_from_user_report": true,
    "hide_raw_evidence_from_user_report": true,
    "hide_stack_traces": true,
    "do_not_claim_treatment_executed": true,
    "do_not_expose_secrets": true
  }
}

```
