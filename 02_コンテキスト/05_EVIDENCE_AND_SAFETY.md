# 05_EVIDENCE_AND_SAFETY.md
この文書は元Repositoryの必要な規則・契約を原文のまま集約したものです。章見出しは元のファイルパスです。


---

## SOURCE: Knowledge/evidence/evidence_codes.json

```json
{
  "registry_name": "EVIDENCE_CODE_REGISTRY",
  "version": "1.0",
  "items": [
    {
      "code": "CTR_BELOW_POSITION_EXPECTATION",
      "source": "SEARCH_CONSOLE",
      "description": "掲載順位帯に対してCTRが期待値を下回る",
      "required_inputs": [
        "position",
        "ctr",
        "impressions"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "POSITION_DECLINE_OBSERVED",
      "source": "SEARCH_CONSOLE",
      "description": "比較期間において平均順位の下落が観察された",
      "required_inputs": [
        "baseline_position",
        "current_position"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "VISIBILITY_DECLINE_OBSERVED",
      "source": "SEARCH_CONSOLE",
      "description": "比較期間において表示回数の減少が観察された",
      "required_inputs": [
        "baseline_impressions",
        "current_impressions"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "LONG_TIME_SINCE_UPDATE",
      "source": "METADATA",
      "description": "最終更新から長期間経過している",
      "required_inputs": [
        "last_modified_at",
        "observed_at"
      ],
      "minimum_sample_policy": "NOT_APPLICABLE"
    },
    {
      "code": "QUERY_DISTRIBUTION_CHANGED",
      "source": "SEARCH_CONSOLE",
      "description": "流入クエリ構成が過去期間から変化した",
      "required_inputs": [
        "baseline_queries",
        "current_queries"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "SERP_INTENT_CHANGED",
      "source": "SERP",
      "description": "検索結果上位の主要検索意図が以前から変化した",
      "required_inputs": [
        "baseline_intent",
        "current_intent"
      ],
      "minimum_sample_policy": "NOT_APPLICABLE"
    },
    {
      "code": "INTERNAL_LINK_SUPPORT_WEAK",
      "source": "INTERNAL_LINKS",
      "description": "記事への内部リンク支援が弱い",
      "required_inputs": [
        "incoming"
      ],
      "minimum_sample_policy": "NOT_APPLICABLE"
    },
    {
      "code": "LONG_TERM_VISIBILITY_DECLINE",
      "source": "LONG_TERM",
      "description": "複数期間で表示回数の長期低下が観察された",
      "required_inputs": [
        "windows",
        "trend.visibility_change_ratio"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "LONG_TERM_CTR_DECAY",
      "source": "LONG_TERM",
      "description": "長期的なCTR低下が観察された",
      "required_inputs": [
        "windows",
        "trend.ctr_change_ratio"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "LONG_TERM_POSITION_DECAY",
      "source": "LONG_TERM",
      "description": "長期的な順位低下が観察された",
      "required_inputs": [
        "windows",
        "trend.position_change"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "SEASONAL_PATTERN_OBSERVED",
      "source": "LONG_TERM",
      "description": "季節性が疑われる周期パターンが観察された",
      "required_inputs": [
        "windows",
        "trend.seasonality_score"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "LONG_TERM_RECOVERY_OBSERVED",
      "source": "LONG_TERM",
      "description": "長期回復傾向が観察された",
      "required_inputs": [
        "windows",
        "trend.visibility_change_ratio"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "TREATMENT_EFFECT_POSITIVE",
      "source": "TREATMENT_HISTORY",
      "description": "改善後に総合的な改善効果が観察された",
      "required_inputs": [
        "assessment.effect_score"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "TREATMENT_NO_EFFECT",
      "source": "TREATMENT_HISTORY",
      "description": "改善後に有意な効果が観察されない",
      "required_inputs": [
        "assessment.effect_score"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "POST_TREATMENT_WORSENING",
      "source": "TREATMENT_HISTORY",
      "description": "改善後に主要指標の悪化が観察された",
      "required_inputs": [
        "assessment.effect_score",
        "assessment.metric_changes"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "TREATMENT_MIXED_RESPONSE",
      "source": "TREATMENT_HISTORY",
      "description": "改善後の指標が改善と悪化に分かれた",
      "required_inputs": [
        "assessment.metric_changes"
      ],
      "minimum_sample_policy": "REQUIRED"
    },
    {
      "code": "TREATMENT_FOLLOW_UP_INSUFFICIENT",
      "source": "TREATMENT_HISTORY",
      "description": "改善後の測定期間またはデータ量が不足している",
      "required_inputs": [
        "assessment.selected_checkpoint_days"
      ],
      "minimum_sample_policy": "ALWAYS"
    }
  ]
}

```


---

## SOURCE: Knowledge/evidence/rules/evidence_rules_v1.json

```json
{
  "rule_set": "SIMS_DOCTOR_EVIDENCE_RULES_V1",
  "version": "1.0",
  "status": "INITIAL_UNCALIBRATED",
  "sample_policy": {
    "minimum_impressions_for_ctr": 100,
    "minimum_impressions_for_trend": 100,
    "minimum_clicks_for_ctr_support": 1,
    "low_sample_behavior": "RECORD_EVIDENCE_WITH_LOW_SAMPLE_FLAG"
  },
  "rules": [
    {
      "evidence_code": "CTR_BELOW_POSITION_EXPECTATION",
      "rule_version": "1.0",
      "inputs": [
        "days_28.ctr",
        "days_28.position",
        "days_28.impressions"
      ],
      "parameters": {
        "position_bands": [
          {
            "min_position": 1.0,
            "max_position": 3.0,
            "minimum_expected_ctr": 0.08
          },
          {
            "min_position": 3.01,
            "max_position": 5.0,
            "minimum_expected_ctr": 0.04
          },
          {
            "min_position": 5.01,
            "max_position": 10.0,
            "minimum_expected_ctr": 0.015
          },
          {
            "min_position": 10.01,
            "max_position": 20.0,
            "minimum_expected_ctr": 0.005
          }
        ]
      },
      "notes": "Initial conservative bands. Calibration required with real cases."
    },
    {
      "evidence_code": "POSITION_DECLINE_OBSERVED",
      "rule_version": "1.0",
      "inputs": [
        "baseline.position",
        "current.position"
      ],
      "parameters": {
        "minimum_absolute_decline": 1.0,
        "minimum_relative_decline_ratio": 0.1
      }
    },
    {
      "evidence_code": "VISIBILITY_DECLINE_OBSERVED",
      "rule_version": "1.0",
      "inputs": [
        "baseline.impressions",
        "current.impressions"
      ],
      "parameters": {
        "minimum_decline_ratio": 0.2
      }
    },
    {
      "evidence_code": "LONG_TIME_SINCE_UPDATE",
      "rule_version": "1.0",
      "inputs": [
        "last_modified_at",
        "observed_at"
      ],
      "parameters": {
        "minimum_days_since_update": 365
      }
    }
  ]
}

```


---

## SOURCE: Knowledge/explainability/explainability_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_EXPLAINABILITY_POLICY_V1",
  "version": "1.0",
  "audiences": [
    "USER",
    "SYSTEM"
  ],
  "decision_step_order": [
    "DATA_SUFFICIENCY",
    "RECENT_CHANGE",
    "WINNER_QUERY",
    "MERGE",
    "ROLE_SEPARATION",
    "SEVERE_DAMAGE",
    "OPPORTUNITY",
    "FINAL_DIAGNOSIS"
  ],
  "user_explanation": {
    "maximum_steps": 8,
    "hide_rule_ids": true,
    "hide_raw_evidence": true,
    "hide_internal_scores": false,
    "plain_language": true
  },
  "system_explanation": {
    "include_rule_ids": true,
    "include_assessment_ids": true,
    "include_safety_flags": true,
    "include_score_trace": true
  },
  "safety": {
    "never_invent_missing_evidence": true,
    "mark_inference_as_inference": true,
    "do_not_expose_secrets": true
  }
}

```


---

## SOURCE: shared/ALGORITHM_EVIDENCE_V1.md

```markdown
# Algorithm Evidence v1

## Purpose

Google検索アルゴリズム更新や検索結果環境の変化を、SIMS Article Doctorが診断へ統合するためのPlatform共通境界を定義する。

## Core rule

**Algorithm information is Evidence, not Diagnosis.**

アップデート期間との時間的一致だけで、順位・クリック・表示変動の原因をGoogleアップデートと断定してはならない。

Doctorは少なくとも利用可能な次のEvidenceを統合して判断する。

- Search Console performance and query evidence
- SERP composition and intent evidence
- Article content quality, factual accuracy, freshness, and alignment
- Site-wide or segment-wide performance evidence
- Treatment and monitoring history
- Officially confirmed Google Search update information

## Source boundary

Google Search updateの存在・名称・rollout期間は、可能な限りGoogle公式情報をPRIMARY/OFFICIAL evidenceとして扱う。第三者の変動観測だけで公式アップデートを確定しない。

## Causation boundary

Algorithm Evidenceは次のような役割評価を取り得る。

- `PRIMARY_FACTOR`
- `CONTRIBUTING_FACTOR`
- `POSSIBLE_FACTOR`
- `UNLIKELY_FACTOR`
- `NOT_SUPPORTED`

ただし、これらは因果関係の数学的証明を意味しない。Evidence不足時は確信度を下げ、断定表現を避ける。

## Treatment boundary

アップデート中または直後で変動が不安定な場合、Doctorは`WAIT`を選択できる。`WAIT`は放置ではなく、観察対象・再診時期・避けるべき変更を伴う経過観察である。

重大な事実誤認、危険情報、検索意図の明確な不一致など、待つことで利用者・読者リスクが増える問題がある場合は、Algorithm Evidenceのみを理由に必要な治療を延期してはならない。

## Product responsibility

- SBM: GSC、記事、履歴、site impact等のEvidenceを収集・集計・保存・配送する。
- Doctor: Algorithm Evidenceを外部環境Evidenceとして評価し、他Evidenceと統合して診断・Treatment Strategyを決定する。
- Writer / Creator / Merge: SBMから発行された紹介状・依頼だけを処置する。Algorithm Evidenceを理由に独自Routingしない。

## Prohibited shortcuts

- 「アップデート期間と重なった = アップデートが原因」
- 「サイトが下落した = 全記事を全面リライト」
- 「アップデート中 = 何も確認せず待つ」
- 非公式情報だけで公式Update名や期間を確定する

```


---

## SOURCE: shared/SBM_DOCTOR_SAFETY_BOUNDARY.md

```markdown
# SBM Safety Boundary

1. Doctor does not invoke SBM daily-processing functions.
2. SBM may reject Doctor request generation or treatment start while daily processing is active.
3. Doctor does not directly update SBM's article master, improvement history, Case state, or monitoring records.
4. SBM changes state only after validating an accepted platform message or a user action.
5. Doctor-specific time triggers and Properties keys use the `Doctor` prefix.
6. Doctor failure does not change SBM daily-processing state.
7. Doctor does not invoke Writer, Creator, or Merge directly.
8. Specialist treatment results return to SBM, not to Doctor.
9. Doctor cannot release or bypass an SBM Workflow Lock.
10. Re-examination is initiated by a new SBM request containing the relevant Case evidence.

```


---

## SOURCE: Knowledge/integration/production_security_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_PRODUCTION_SECURITY_POLICY_V1",
  "version": "1.0",
  "persistent_security_state": {
    "nonce_store": "SQLITE",
    "idempotency_store": "SQLITE",
    "audit_log": "SQLITE"
  },
  "configuration": {
    "client_secrets_source": "ENVIRONMENT",
    "required_environment": [
      "SIMS_DOCTOR_QUEUE_DB",
      "SIMS_DOCTOR_SECURITY_DB",
      "SIMS_DOCTOR_CLIENT_SECRETS_JSON"
    ],
    "forbid_default_secret": true
  },
  "health": {
    "liveness_path": "/health/live",
    "readiness_path": "/health/ready",
    "readiness_checks": [
      "QUEUE_DATABASE",
      "SECURITY_DATABASE",
      "CLIENT_SECRET_CONFIGURATION"
    ]
  },
  "deployment": {
    "application_factory": "src.doctor.deployment.app_factory:create_application",
    "recommended_workers": 1,
    "reason": "SQLite-backed queue and security state require serialized deployment until external database adapters are added."
  }
}

```
