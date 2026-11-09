# 01_DOCTOR_DIAGNOSIS.md
この文書は元Repositoryの必要な規則・契約を原文のまま集約したものです。章見出しは元のファイルパスです。


---

## SOURCE: Runtime/CLINICAL_RUNTIME.md

```markdown
# aDoctor Claude Clinical Runtime v1.0.0 RC4

## 診断順序
1. Evidence ValidationとDoctor Readinessを確認する。
2. 記事本文を診察し、自己矛盾・誤情報・鮮度・タイトル本文整合・内部リンク関連性を確認する。
3. Search Consoleの長期・短期・クエリ推移を診断する。
4. 必要な場合だけSERP・公式情報・外部イベントを確認する。
5. SEO、本文、SERP、外部要因、Workflowを別々に判定する。
6. Composite DiagnosisとTreatmentを作る。

## LOW_SAMPLE保護
LOW_SAMPLEは大規模なSEOリライトを保留するためのルールである。次の処置は止めない。
- 明確な事実誤認の修正
- 本文内の自己矛盾の修正
- 古い制度・料金・サービス情報の確認
- 関連性の低い内部リンクの除去

## 複合処置
単一処置に丸めず、必要に応じて次を同時に返す。
- SEO：経過観察
- 本文：限定修正
- SERP：未評価
- 外部要因：需要縮小の可能性
- Workflow：SBMロックを尊重

## 診断状態
- 病態が未確定ならDEFERRED。
- 経過観察方針を決めただけでCONFIRMEDにしない。
- 明確な問題がない場合はNO_TREATMENT_REQUIREDを使用できる。

## Confidence
固定値を使わない。Evidence Scoreを基礎に、LOW_SAMPLE、SERP不足、横断記事不足、矛盾シグナル、データ品質警告を減点し、公式情報確認を加点する。

## 外部要因
公式発表、制度終了、サービス変更、季節性、キャンペーン終了などが高確度で検索需要減少を説明する場合、改善失敗の確定を保留または除外する。

## LOW_SAMPLE SERP競争力フォールバック（v1.5.1）
- GSCの母数不足だけを「悪化」「改善失敗」と判定しない。
- LOW_SAMPLEで通常の効果判定ができない場合、単純に待機期間を延長する前にターゲットクエリの信頼度を確認する。
- ターゲットクエリは、信頼できるGSC観測 → SBM保存ターゲット → 記事タイトル・H1・本文の検索意図、の順で評価する。疎なGSCだけを理由に保存済みターゲットを置換しない。
- ターゲットが未確定なら `TARGET_QUERY_REASSESSMENT` とし、無理にメインクエリを作らない。
- LOW_SAMPLEかつターゲットが評価可能なら、Web検索が利用できる場合はそのクエリの現在SERPを確認し、上位結果との競争力を診断する。
- 比較対象は検索意図、SERP構造、情報の具体性・鮮度、意思決定支援、独自価値、上位ページにのみ存在する有用なGap、公式/高権威サイト支配の有無。文字数や見出しを機械的に模倣しない。
- 判定は `SERP_GAP_ACTIONABLE` / `SERP_COMPETITIVENESS_SUFFICIENT` / `TARGET_QUERY_REASSESSMENT` / `LOW_DEMAND_MAINTAIN` / `ADDITIONAL_OBSERVATION` / `LOW_PRIORITY_SERP_STRUCTURE` を使う。
- `SERP_GAP_ACTIONABLE` の場合だけ、Gapを埋める必要最小限の処置範囲をSBMへ返す。LOW_SAMPLEだけを根拠に全面リライト・タイトル変更を指示しない。
- SERP競争力が十分なのに需要が小さい場合は `LOW_DEMAND_MAINTAIN` とし、改善失敗ではなく正常終了候補としてSBMへ返す。
- 公式サイト等が支配し追加投資の期待値が低い場合は `LOW_PRIORITY_SERP_STRUCTURE` として正常終了候補にできる。
- 現在SERPの順位・競合スナップショットはPersonal Knowledge候補へ保存しない。
- 診断JSONには可能な範囲で `low_sample_serp_assessment` を含め、`activated`, `target_query`, `target_query_confidence`, `serp_checked`, `outcome`, `actionable_gaps`, `serp_structure`, `reason` を構造化する。


## 強SERP時のクラスター戦略診断（v1.5.1）
- LOW_SAMPLEでターゲット記事自体に大きな品質問題がなく、対象クエリSERPが大手・公式・集約プラットフォーム等に構造的に支配されている場合、`LOW_PRIORITY_SERP_STRUCTURE` で即終了してはならない。まず `CLUSTER_OPPORTUNITY_CHECK` を実施する。
- クラスター診断では、既存関連記事からの内部リンク/既存記事改善、新しい独立検索意図の周辺記事、検索需要シグナル、SERP参入余地、カニバリ、対象記事への自然な導線、サイトテーマ適合、投資期待値を確認する。
- 既存記事で支援できる場合は `cluster_strategy_assessment.outcome=EXISTING_CONTENT_SUPPORT` とし、必要最小限のaWriter支援としてSIMS Managerへ返す。
- 新規記事に独立した検索価値があり、既存記事とカニバらず、その記事自身が流入を獲得でき、対象記事へ自然にリンクできる場合だけ `CREATOR_OPPORTUNITY` とし、aCreator向け紹介状を生成する。親記事を押し上げるだけの薄いサテライト記事は禁止する。
- 新規候補は実検索需要/SERP/既存記事との境界を確認してからaCreatorへ渡す。候補語を思いついただけで記事化決定しない。
- クラスターまで確認して勝ち筋がない場合のみ `NO_CLUSTER_OPPORTUNITY` → `LOW_PRIORITY_SERP_STRUCTURE` として正常終了できる。
- `LOW_PRIORITY_SERP_STRUCTURE` または `LOW_DEMAND_MAINTAIN` を出した場合、`treatment_plan.strategy=MAINTAIN`, `workflow_handoff.next_action=CLOSE_MONITORING`, `review_after_days=null` とし、WAIT/MONITORを同時に出さない。観察延長を許すのは原則 `ADDITIONAL_OBSERVATION`。
- 診断JSONには `cluster_strategy_assessment` を含め、少なくとも `activated`, `checked`, `outcome`, `existing_support`, `creator_candidates`, `cannibalization_checked`, `reason` を構造化する。aCreatorへ送る場合は `workflow_handoff.next_action=CREATOR_REQUEST_READY` とし、`creator_request_text` に検索意図・SERP Gap・既存記事との境界・対象記事への自然な内部リンク目的を含める。

```


---

## SOURCE: Knowledge/workflow/clinical_pipeline.md

```markdown
# Clinical Pipeline v1

The pipeline coordinates existing Doctor components without merging their responsibilities.

```text
Request Reception
→ Search Console Observation
→ SERP Observation
→ Article Snapshot Observation
→ Evidence
→ Vital Signs
→ Findings
→ Differential Diagnosis
→ Final Diagnosis
→ Treatment Recommendation
→ Referral
```

Every step remains independently testable and idempotent.
The pipeline only coordinates order, failure handling, resume, and final result generation.

```


---

## SOURCE: Knowledge/workflow/clinical_workflow.md

```markdown
# Clinical Workflow v1.0

```text
Request
  → Medical Record
  → Observation
  → Evidence
  → Vital Signs
  → Findings
  → Differential Diagnosis
  → Final Diagnosis
  → Treatment Recommendation
  → Referral
  → Follow-up
```

## Separation of duties

- SBM requests diagnosis and manages operations.
- Doctor owns observation, evidence, findings, diagnosis, the medical record, and referrals.
- Writer performs rewrite treatment.
- Creator creates a new article when referred.
- Merge performs article integration in the future.

```


---

## SOURCE: Knowledge/diagnostic_rules/core_diagnostic_rules_v1.json

```json
{
  "rule_set": "SIMS_DOCTOR_CORE_DIAGNOSTIC_RULES_V1",
  "version": "1.0",
  "rules": [
    {
      "rule_id": "DR-CTR-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 80,
      "diagnosis_code": "CTR_PROBLEM",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "FINDING",
          "code": "CTR_UNDERPERFORMING",
          "field": "finding_code",
          "operator": "EQ",
          "value": "CTR_UNDERPERFORMING"
        },
        {
          "source": "VITAL_SIGN",
          "code": "CTR_HEALTH",
          "field": "score",
          "operator": "LT",
          "value": 50
        }
      ],
      "base_confidence": 65,
      "severity": "MODERATE",
      "mutual_exclusion_group": null,
      "specificity": 80,
      "explanation_template": "CTR関連所見とCTR Health低下が一致しました。",
      "tags": [
        "CTR",
        "SINGLE_CASE"
      ]
    },
    {
      "rule_id": "DR-LONG-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 95,
      "diagnosis_code": "LONG_TERM_DECAY",
      "condition_logic": "ANY",
      "conditions": [
        {
          "source": "FINDING",
          "code": "LONG_TERM_VISIBILITY_DECAY",
          "field": "finding_code",
          "operator": "EQ",
          "value": "LONG_TERM_VISIBILITY_DECAY"
        },
        {
          "source": "FINDING",
          "code": "LONG_TERM_POSITION_DECAY",
          "field": "finding_code",
          "operator": "EQ",
          "value": "LONG_TERM_POSITION_DECAY"
        }
      ],
      "base_confidence": 70,
      "severity": "SEVERE",
      "mutual_exclusion_group": "LONG_TERM_STATE",
      "specificity": 90,
      "explanation_template": "長期推移に継続的な劣化所見が確認されました。",
      "tags": [
        "LONG_TERM",
        "DECLINE"
      ]
    },
    {
      "rule_id": "DR-RECOVERY-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 85,
      "diagnosis_code": "RECOVERY_IN_PROGRESS",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "FINDING",
          "code": "RECOVERY_TREND",
          "field": "finding_code",
          "operator": "EQ",
          "value": "RECOVERY_TREND"
        }
      ],
      "base_confidence": 70,
      "severity": "MILD",
      "mutual_exclusion_group": "LONG_TERM_STATE",
      "specificity": 85,
      "explanation_template": "直近データに回復傾向が確認されました。",
      "tags": [
        "LONG_TERM",
        "RECOVERY"
      ]
    },
    {
      "rule_id": "DR-IMPROVEMENT-FAILURE-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 96,
      "diagnosis_code": "IMPROVEMENT_FAILURE",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "IMPROVEMENT_FAILURE_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "NO_MEASURABLE_EFFECT"
        }
      ],
      "base_confidence": 78,
      "severity": "MODERATE",
      "mutual_exclusion_group": "IMPROVEMENT_OUTCOME",
      "specificity": 90,
      "explanation_template": "改善履歴の比較で明確な効果が確認できませんでした。",
      "tags": [
        "IMPROVEMENT",
        "FAILURE"
      ]
    },
    {
      "rule_id": "DR-IMPROVEMENT-WORSENING-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 99,
      "diagnosis_code": "POST_IMPROVEMENT_WORSENING",
      "condition_logic": "ANY",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "IMPROVEMENT_FAILURE_ASSESSMENT",
          "field": "facts.classification",
          "operator": "IN",
          "value": [
            "POST_TREATMENT_WORSENING",
            "POSSIBLE_WRONG_TREATMENT_DIRECTION",
            "RECURRENT_FAILURE"
          ]
        }
      ],
      "base_confidence": 85,
      "severity": "SEVERE",
      "mutual_exclusion_group": "IMPROVEMENT_OUTCOME",
      "specificity": 95,
      "explanation_template": "改善後の主要指標に悪化または再発が確認されました。",
      "tags": [
        "IMPROVEMENT",
        "WORSENING"
      ]
    },
    {
      "rule_id": "DR-IMPROVEMENT-FOLLOWUP-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 88,
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "IMPROVEMENT_FAILURE_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "INSUFFICIENT_FOLLOW_UP"
        }
      ],
      "base_confidence": 75,
      "severity": "INFO",
      "mutual_exclusion_group": "IMPROVEMENT_OUTCOME",
      "specificity": 85,
      "explanation_template": "改善効果を判断するための期間またはデータ量が不足しています。",
      "tags": [
        "IMPROVEMENT",
        "FOLLOW_UP"
      ]
    },
    {
      "rule_id": "DR-LONGTERM-CHRONIC-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 97,
      "diagnosis_code": "LONG_TERM_DECAY",
      "condition_logic": "ANY",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "LONG_TERM_DEGRADATION_ASSESSMENT",
          "field": "facts.classification",
          "operator": "IN",
          "value": [
            "CHRONIC_DEGRADATION",
            "SHARP_DEGRADATION"
          ]
        }
      ],
      "base_confidence": 84,
      "severity": "SEVERE",
      "mutual_exclusion_group": "LONG_TERM_STATE",
      "specificity": 95,
      "explanation_template": "365日推移に慢性的または急激な劣化が確認されました。",
      "tags": [
        "LONG_TERM",
        "DEGRADATION"
      ]
    },
    {
      "rule_id": "DR-LONGTERM-SEASONAL-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 89,
      "diagnosis_code": "SEASONAL_DECLINE",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "LONG_TERM_DEGRADATION_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "SEASONAL_VARIATION"
        }
      ],
      "base_confidence": 80,
      "severity": "INFO",
      "mutual_exclusion_group": "LONG_TERM_STATE",
      "specificity": 90,
      "explanation_template": "過去期間と類似した季節変動が確認されました。",
      "tags": [
        "LONG_TERM",
        "SEASONAL"
      ]
    },
    {
      "rule_id": "DR-LONGTERM-RECOVERY-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 91,
      "diagnosis_code": "RECOVERY_IN_PROGRESS",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "LONG_TERM_DEGRADATION_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "RECOVERY_IN_PROGRESS"
        }
      ],
      "base_confidence": 82,
      "severity": "MILD",
      "mutual_exclusion_group": "LONG_TERM_STATE",
      "specificity": 92,
      "explanation_template": "長期推移に回復傾向が確認されました。",
      "tags": [
        "LONG_TERM",
        "RECOVERY"
      ]
    },
    {
      "rule_id": "DR-LONGTERM-FOLLOWUP-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 82,
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "LONG_TERM_DEGRADATION_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "INSUFFICIENT_HISTORY"
        }
      ],
      "base_confidence": 72,
      "severity": "INFO",
      "mutual_exclusion_group": "LONG_TERM_STATE",
      "specificity": 82,
      "explanation_template": "長期診断に必要な観察期間が不足しています。",
      "tags": [
        "LONG_TERM",
        "FOLLOW_UP"
      ]
    },
    {
      "rule_id": "DR-CTR-OPPORTUNITY-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 93,
      "diagnosis_code": "CTR_OPPORTUNITY",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "CTR_OPPORTUNITY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "IN",
          "value": [
            "CTR_OPPORTUNITY",
            "HIGH_CTR_OPPORTUNITY"
          ]
        }
      ],
      "base_confidence": 84,
      "severity": "MODERATE",
      "mutual_exclusion_group": "CTR_STATE",
      "specificity": 94,
      "explanation_template": "現在順位に対してCTRが期待値を下回っています。",
      "tags": [
        "CTR",
        "OPPORTUNITY"
      ]
    },
    {
      "rule_id": "DR-CTR-WINNER-PROTECT-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 96,
      "diagnosis_code": "CTR_WINNER_QUERY_PROTECTED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "CTR_OPPORTUNITY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "WINNER_QUERY_PROTECTED"
        }
      ],
      "base_confidence": 88,
      "severity": "MILD",
      "mutual_exclusion_group": "CTR_STATE",
      "specificity": 96,
      "explanation_template": "主要流入クエリを保護しながら限定的なCTR改善を検討します。",
      "tags": [
        "CTR",
        "WINNER_QUERY"
      ]
    },
    {
      "rule_id": "DR-CTR-FOLLOWUP-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 86,
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "CTR_OPPORTUNITY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "IN",
          "value": [
            "RECENT_CHANGE_OBSERVATION",
            "INSUFFICIENT_DATA"
          ]
        }
      ],
      "base_confidence": 74,
      "severity": "INFO",
      "mutual_exclusion_group": "CTR_STATE",
      "specificity": 84,
      "explanation_template": "CTR改善判断には追加測定が必要です。",
      "tags": [
        "CTR",
        "FOLLOW_UP"
      ]
    },
    {
      "rule_id": "DR-POSITION-OPPORTUNITY-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 92,
      "diagnosis_code": "POSITION_OPPORTUNITY",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "POSITION_OPPORTUNITY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "IN",
          "value": [
            "POSITION_OPPORTUNITY",
            "HIGH_POSITION_OPPORTUNITY",
            "QUERY_FOCUSED_OPPORTUNITY"
          ]
        }
      ],
      "base_confidence": 84,
      "severity": "MODERATE",
      "mutual_exclusion_group": "POSITION_STATE",
      "specificity": 94,
      "explanation_template": "表示回数があり、上位表示へ改善できる余地があります。",
      "tags": [
        "POSITION",
        "OPPORTUNITY"
      ]
    },
    {
      "rule_id": "DR-POSITION-WINNER-PROTECT-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 95,
      "diagnosis_code": "POSITION_WINNER_QUERY_PROTECTED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "POSITION_OPPORTUNITY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "WINNER_QUERY_PROTECTED"
        }
      ],
      "base_confidence": 88,
      "severity": "MILD",
      "mutual_exclusion_group": "POSITION_STATE",
      "specificity": 96,
      "explanation_template": "主要流入クエリを維持しながら限定的な順位改善を検討します。",
      "tags": [
        "POSITION",
        "WINNER_QUERY"
      ]
    },
    {
      "rule_id": "DR-POSITION-MISALIGNMENT-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 94,
      "diagnosis_code": "LOW_VISIBILITY_OR_MISALIGNMENT",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "POSITION_OPPORTUNITY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "LOW_VISIBILITY_OR_MISALIGNMENT"
        }
      ],
      "base_confidence": 82,
      "severity": "SEVERE",
      "mutual_exclusion_group": "POSITION_STATE",
      "specificity": 92,
      "explanation_template": "順位が低く、検索意図または記事役割のずれが疑われます。",
      "tags": [
        "POSITION",
        "MISALIGNMENT"
      ]
    },
    {
      "rule_id": "DR-POSITION-FOLLOWUP-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 84,
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "POSITION_OPPORTUNITY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "INSUFFICIENT_DATA"
        }
      ],
      "base_confidence": 72,
      "severity": "INFO",
      "mutual_exclusion_group": "POSITION_STATE",
      "specificity": 82,
      "explanation_template": "順位改善判断には追加データが必要です。",
      "tags": [
        "POSITION",
        "FOLLOW_UP"
      ]
    },
    {
      "rule_id": "DR-INTENT-DRIFT-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 96,
      "diagnosis_code": "INTENT_DRIFT",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "INTENT_DRIFT_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "INTENT_DRIFT"
        }
      ],
      "base_confidence": 86,
      "severity": "SEVERE",
      "mutual_exclusion_group": "INTENT_STATE",
      "specificity": 96,
      "explanation_template": "主要検索意図と記事テーマのずれが確認されました。",
      "tags": [
        "INTENT",
        "DRIFT"
      ]
    },
    {
      "rule_id": "DR-INTENT-DISPERSION-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 95,
      "diagnosis_code": "TOPIC_DISPERSION",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "INTENT_DRIFT_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "TOPIC_DISPERSION"
        }
      ],
      "base_confidence": 85,
      "severity": "SEVERE",
      "mutual_exclusion_group": "INTENT_STATE",
      "specificity": 95,
      "explanation_template": "流入クエリが複数の検索意図へ分散しています。",
      "tags": [
        "INTENT",
        "DISPERSION"
      ]
    },
    {
      "rule_id": "DR-INTENT-EMERGING-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 94,
      "diagnosis_code": "EMERGING_INTENT_TRANSITION",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "INTENT_DRIFT_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "EMERGING_INTENT_TRANSITION"
        }
      ],
      "base_confidence": 84,
      "severity": "MODERATE",
      "mutual_exclusion_group": "INTENT_STATE",
      "specificity": 94,
      "explanation_template": "新しい検索意図への流入遷移が確認されました。",
      "tags": [
        "INTENT",
        "EMERGING"
      ]
    },
    {
      "rule_id": "DR-INTENT-WINNER-PROTECT-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 97,
      "diagnosis_code": "INTENT_WINNER_QUERY_PROTECTED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "INTENT_DRIFT_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "WINNER_QUERY_PROTECTED"
        }
      ],
      "base_confidence": 88,
      "severity": "MILD",
      "mutual_exclusion_group": "INTENT_STATE",
      "specificity": 97,
      "explanation_template": "主要流入クエリを保護しながら意図調整を検討します。",
      "tags": [
        "INTENT",
        "WINNER_QUERY"
      ]
    },
    {
      "rule_id": "DR-INTENT-FOLLOWUP-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 84,
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "INTENT_DRIFT_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "INSUFFICIENT_DATA"
        }
      ],
      "base_confidence": 72,
      "severity": "INFO",
      "mutual_exclusion_group": "INTENT_STATE",
      "specificity": 82,
      "explanation_template": "検索意図診断には追加データが必要です。",
      "tags": [
        "INTENT",
        "FOLLOW_UP"
      ]
    },
    {
      "rule_id": "DR-FRESHNESS-PARTIAL-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 90,
      "diagnosis_code": "FRESHNESS_DECAY",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "FRESHNESS_DECAY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "PARTIAL_FRESHNESS_DECAY"
        }
      ],
      "base_confidence": 82,
      "severity": "MODERATE",
      "mutual_exclusion_group": "FRESHNESS_STATE",
      "specificity": 92,
      "explanation_template": "一部情報に鮮度劣化があり、局所更新が必要です。",
      "tags": [
        "FRESHNESS",
        "PARTIAL"
      ]
    },
    {
      "rule_id": "DR-FRESHNESS-SEVERE-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 97,
      "diagnosis_code": "SEVERE_FRESHNESS_DECAY",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "FRESHNESS_DECAY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "SEVERE_FRESHNESS_DECAY"
        }
      ],
      "base_confidence": 88,
      "severity": "SEVERE",
      "mutual_exclusion_group": "FRESHNESS_STATE",
      "specificity": 97,
      "explanation_template": "記事全体に重大な情報鮮度劣化が確認されました。",
      "tags": [
        "FRESHNESS",
        "SEVERE"
      ]
    },
    {
      "rule_id": "DR-FRESHNESS-WINNER-PROTECT-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 96,
      "diagnosis_code": "FRESHNESS_WINNER_QUERY_PROTECTED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "FRESHNESS_DECAY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "WINNER_QUERY_PROTECTED"
        }
      ],
      "base_confidence": 88,
      "severity": "MILD",
      "mutual_exclusion_group": "FRESHNESS_STATE",
      "specificity": 96,
      "explanation_template": "主要流入クエリを維持しながら事実情報を更新します。",
      "tags": [
        "FRESHNESS",
        "WINNER_QUERY"
      ]
    },
    {
      "rule_id": "DR-FRESHNESS-FOLLOWUP-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 84,
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "FRESHNESS_DECAY_ASSESSMENT",
          "field": "facts.classification",
          "operator": "IN",
          "value": [
            "RECENT_UPDATE_OBSERVATION",
            "INSUFFICIENT_DATA"
          ]
        }
      ],
      "base_confidence": 72,
      "severity": "INFO",
      "mutual_exclusion_group": "FRESHNESS_STATE",
      "specificity": 84,
      "explanation_template": "鮮度劣化判断には追加観察が必要です。",
      "tags": [
        "FRESHNESS",
        "FOLLOW_UP"
      ]
    },
    {
      "rule_id": "DR-CANNIBAL-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 97,
      "diagnosis_code": "CANNIBALIZATION",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "CANNIBALIZATION_ASSESSMENT",
          "field": "facts.classification",
          "operator": "IN",
          "value": [
            "POSSIBLE_CANNIBALIZATION",
            "CONFIRMED_CANNIBALIZATION"
          ]
        }
      ],
      "base_confidence": 86,
      "severity": "SEVERE",
      "mutual_exclusion_group": "CANNIBAL_STATE",
      "specificity": 96,
      "explanation_template": "サイト内の記事間競合が確認されました。",
      "tags": [
        "CANNIBALIZATION"
      ]
    },
    {
      "rule_id": "DR-MERGE-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 100,
      "diagnosis_code": "MERGE_CANDIDATE",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "CANNIBALIZATION_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "MERGE_CANDIDATE"
        }
      ],
      "base_confidence": 90,
      "severity": "SEVERE",
      "mutual_exclusion_group": "CANNIBAL_STATE",
      "specificity": 100,
      "explanation_template": "同一意図の記事を統合候補としてMergeへ紹介します。",
      "tags": [
        "CANNIBALIZATION",
        "MERGE"
      ]
    },
    {
      "rule_id": "DR-ROLE-SEPARATION-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 98,
      "diagnosis_code": "ROLE_SEPARATION",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "CANNIBALIZATION_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "ROLE_SEPARATION_RECOMMENDED"
        }
      ],
      "base_confidence": 88,
      "severity": "MODERATE",
      "mutual_exclusion_group": "CANNIBAL_STATE",
      "specificity": 98,
      "explanation_template": "記事統合ではなく役割分担が適切です。",
      "tags": [
        "CANNIBALIZATION",
        "ROLE"
      ]
    },
    {
      "rule_id": "DR-CANNIBAL-FOLLOWUP-001",
      "rule_version": "1.0",
      "enabled": true,
      "priority": 84,
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "condition_logic": "ALL",
      "conditions": [
        {
          "source": "OBSERVATION",
          "code": "CANNIBALIZATION_ASSESSMENT",
          "field": "facts.classification",
          "operator": "EQ",
          "value": "FOLLOW_UP_REQUIRED"
        }
      ],
      "base_confidence": 72,
      "severity": "INFO",
      "mutual_exclusion_group": "CANNIBAL_STATE",
      "specificity": 84,
      "explanation_template": "記事間競合の判断には追加データが必要です。",
      "tags": [
        "CANNIBALIZATION",
        "FOLLOW_UP"
      ]
    }
  ]
}

```


---

## SOURCE: Knowledge/diagnostic_rules/diagnostic_rule_engine_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_DIAGNOSTIC_RULE_ENGINE_POLICY_V1",
  "version": "1.0",
  "evaluation": {
    "condition_logic": [
      "ALL",
      "ANY"
    ],
    "unknown_value_behavior": "CONDITION_NOT_MET",
    "maximum_rules_per_evaluation": 500,
    "deterministic_order": [
      "priority_desc",
      "specificity_desc",
      "rule_id_asc"
    ]
  },
  "confidence": {
    "base_range": [
      0,
      100
    ],
    "evidence_bonus_per_item": 3,
    "finding_bonus_per_item": 4,
    "low_sample_penalty": 20,
    "maximum_bonus": 20
  },
  "conflict_resolution": {
    "same_diagnosis": "KEEP_HIGHEST_SCORE",
    "mutually_exclusive": "KEEP_HIGHEST_PRIORITY_THEN_SCORE",
    "allow_multiple_non_exclusive": true
  },
  "safety": {
    "rules_cannot_modify_article": true,
    "rules_cannot_create_referral_directly": true,
    "rules_must_explain_match": true,
    "rules_must_reference_registered_codes": true
  }
}

```


---

## SOURCE: Knowledge/diagnosis/diagnosis_codes.json

```json
{
  "registry_name": "DIAGNOSIS_CODE_REGISTRY",
  "version": "1.0",
  "items": [
    {
      "code": "LOW_CTR_WITH_STRONG_POSITION",
      "category": "CTR"
    },
    {
      "code": "LONG_TERM_DECLINE",
      "category": "DECLINE"
    },
    {
      "code": "CONTENT_STALE",
      "category": "FRESHNESS"
    },
    {
      "code": "UPDATE_FAILURE",
      "category": "TREATMENT_RESPONSE"
    },
    {
      "code": "INSUFFICIENT_DATA",
      "category": "QUALITY"
    },
    {
      "code": "CTR_PROBLEM",
      "category": "FINAL_CTR"
    },
    {
      "code": "POSITION_DECLINE",
      "category": "FINAL_DECLINE"
    },
    {
      "code": "CANNIBALIZATION",
      "category": "CROSS_ARTICLE"
    },
    {
      "code": "ARTICLE_MERGE_REQUIRED",
      "category": "MERGE"
    },
    {
      "code": "NEW_ARTICLE_NEEDED",
      "category": "CREATOR"
    },
    {
      "code": "LONG_TERM_DECAY",
      "category": "LONG_TERM"
    },
    {
      "code": "SEASONAL_DECLINE",
      "category": "SEASONAL"
    },
    {
      "code": "RECOVERY_IN_PROGRESS",
      "category": "RECOVERY"
    },
    {
      "code": "TREATMENT_SUCCESS",
      "category": "TREATMENT_RESPONSE"
    },
    {
      "code": "IMPROVEMENT_FAILURE",
      "category": "TREATMENT_RESPONSE"
    },
    {
      "code": "POST_IMPROVEMENT_WORSENING",
      "category": "TREATMENT_RESPONSE"
    },
    {
      "code": "MIXED_TREATMENT_RESPONSE",
      "category": "TREATMENT_RESPONSE"
    },
    {
      "code": "FOLLOW_UP_REQUIRED",
      "category": "TREATMENT_RESPONSE"
    },
    {
      "code": "POSITION_OPPORTUNITY",
      "category": "RANKING"
    },
    {
      "code": "POSITION_WINNER_QUERY_PROTECTED",
      "category": "RANKING"
    },
    {
      "code": "LOW_VISIBILITY_OR_MISALIGNMENT",
      "category": "RANKING"
    },
    {
      "code": "INTENT_DRIFT",
      "category": "INTENT"
    },
    {
      "code": "TOPIC_DISPERSION",
      "category": "INTENT"
    },
    {
      "code": "EMERGING_INTENT_TRANSITION",
      "category": "INTENT"
    },
    {
      "code": "INTENT_WINNER_QUERY_PROTECTED",
      "category": "INTENT"
    },
    {
      "code": "FRESHNESS_DECAY",
      "category": "FRESHNESS"
    },
    {
      "code": "SEVERE_FRESHNESS_DECAY",
      "category": "FRESHNESS"
    },
    {
      "code": "FRESHNESS_WINNER_QUERY_PROTECTED",
      "category": "FRESHNESS"
    },
    {
      "code": "MERGE_CANDIDATE",
      "category": "CROSS_ARTICLE"
    },
    {
      "code": "ROLE_SEPARATION",
      "category": "CROSS_ARTICLE"
    }
  ]
}

```


---

## SOURCE: Knowledge/diagnosis/rules/final_diagnosis_rules_v1.json

```json
{
  "rule_set": "SIMS_DOCTOR_FINAL_DIAGNOSIS_RULES_V1",
  "version": "1.0",
  "status": "INITIAL_UNCALIBRATED",
  "global_policy": {
    "minimum_confirmation_confidence": 70,
    "minimum_margin_to_second_candidate": 15,
    "low_sample_only_behavior": "DEFER",
    "contradiction_behavior": "DEFER_IF_PRESENT_AND_TOP_CONFIDENCE_BELOW_90",
    "no_candidate_behavior": "DEFER",
    "review_days": {
      "CONFIRMED_DEFAULT": 28,
      "DEFERRED_LOW_SAMPLE": 14,
      "DEFERRED_CLOSE_CANDIDATES": 14,
      "DEFERRED_LOW_CONFIDENCE": 28,
      "DEFERRED_MISSING_EVIDENCE": 14,
      "DEFERRED_CONTRADICTION": 14,
      "DEFERRED_NO_CANDIDATE": 30
    }
  },
  "diagnoses": [
    {
      "candidate_code": "LOW_CTR_WITH_STRONG_POSITION",
      "final_diagnosis_code": "CTR_PROBLEM",
      "required_evidence": [
        "CTR_BELOW_POSITION_EXPECTATION"
      ],
      "required_findings": [
        "CTR_UNDERPERFORMING"
      ],
      "severity_source": [
        "HIGH_VISIBILITY_LOW_CLICK",
        "CTR_UNDERPERFORMING"
      ]
    },
    {
      "candidate_code": "LONG_TERM_DECLINE",
      "final_diagnosis_code": "POSITION_DECLINE",
      "required_evidence": [
        "POSITION_DECLINE_OBSERVED",
        "VISIBILITY_DECLINE_OBSERVED"
      ],
      "required_findings": [
        "POSITION_DECLINING",
        "LOW_VISIBILITY"
      ],
      "severity_source": [
        "POSITION_DECLINING",
        "LOW_VISIBILITY"
      ]
    },
    {
      "candidate_code": "CONTENT_STALE",
      "final_diagnosis_code": "CONTENT_STALE",
      "required_evidence": [
        "LONG_TIME_SINCE_UPDATE"
      ],
      "required_findings": [
        "CONTENT_OUTDATED"
      ],
      "severity_source": [
        "CONTENT_OUTDATED"
      ]
    },
    {
      "candidate_code": "UPDATE_FAILURE",
      "final_diagnosis_code": "UPDATE_FAILURE",
      "required_evidence": [
        "POSITION_DECLINE_OBSERVED"
      ],
      "required_findings": [
        "POSITION_DECLINING"
      ],
      "required_context": [
        "history.improvement_event_exists"
      ],
      "severity_source": [
        "POSITION_DECLINING",
        "LOW_VISIBILITY",
        "CTR_UNDERPERFORMING"
      ]
    },
    {
      "candidate_code": "INSUFFICIENT_DATA",
      "final_diagnosis_code": "INSUFFICIENT_DATA",
      "required_evidence": [],
      "required_findings": [
        "INSUFFICIENT_EVIDENCE"
      ],
      "force_status": "DEFERRED"
    },
    {
      "candidate_code": "CANNIBALIZATION",
      "final_diagnosis_code": "CANNIBALIZATION",
      "required_evidence": [],
      "required_findings": [
        "QUERY_OVERLAP_HIGH"
      ],
      "severity_source": [
        "QUERY_OVERLAP_HIGH"
      ]
    },
    {
      "candidate_code": "ARTICLE_MERGE_REQUIRED",
      "final_diagnosis_code": "ARTICLE_MERGE_REQUIRED",
      "required_evidence": [],
      "required_findings": [
        "MERGE_SUITABILITY_HIGH"
      ],
      "severity_source": [
        "MERGE_SUITABILITY_HIGH"
      ]
    },
    {
      "candidate_code": "NEW_ARTICLE_NEEDED",
      "final_diagnosis_code": "NEW_ARTICLE_NEEDED",
      "required_evidence": [],
      "required_findings": [
        "DISTINCT_INTENT_OPPORTUNITY"
      ],
      "severity_source": [
        "DISTINCT_INTENT_OPPORTUNITY"
      ]
    },
    {
      "candidate_code": "LONG_TERM_DECAY",
      "final_diagnosis_code": "LONG_TERM_DECAY",
      "required_evidence": [],
      "required_findings": [
        "LONG_TERM_VISIBILITY_DECAY"
      ],
      "severity_source": [
        "LONG_TERM_VISIBILITY_DECAY",
        "LONG_TERM_CTR_DECAY",
        "LONG_TERM_POSITION_DECAY"
      ]
    },
    {
      "candidate_code": "SEASONAL_DECLINE",
      "final_diagnosis_code": "SEASONAL_DECLINE",
      "required_evidence": [],
      "required_findings": [
        "SEASONALITY_DETECTED"
      ],
      "severity_source": [
        "SEASONALITY_DETECTED"
      ]
    },
    {
      "candidate_code": "RECOVERY_IN_PROGRESS",
      "final_diagnosis_code": "RECOVERY_IN_PROGRESS",
      "required_evidence": [],
      "required_findings": [
        "RECOVERY_TREND"
      ],
      "severity_source": [
        "RECOVERY_TREND"
      ]
    },
    {
      "candidate_code": "TREATMENT_SUCCESS",
      "final_diagnosis_code": "TREATMENT_SUCCESS",
      "required_evidence": [],
      "required_findings": [
        "IMPROVEMENT_CONFIRMED"
      ],
      "severity_source": [
        "IMPROVEMENT_CONFIRMED"
      ]
    },
    {
      "candidate_code": "IMPROVEMENT_FAILURE",
      "final_diagnosis_code": "IMPROVEMENT_FAILURE",
      "required_evidence": [],
      "required_findings": [
        "TREATMENT_INEFFECTIVE"
      ],
      "severity_source": [
        "TREATMENT_INEFFECTIVE"
      ]
    },
    {
      "candidate_code": "POST_IMPROVEMENT_WORSENING",
      "final_diagnosis_code": "POST_IMPROVEMENT_WORSENING",
      "required_evidence": [],
      "required_findings": [
        "POST_TREATMENT_WORSENING"
      ],
      "severity_source": [
        "POST_TREATMENT_WORSENING"
      ]
    },
    {
      "candidate_code": "MIXED_TREATMENT_RESPONSE",
      "final_diagnosis_code": "MIXED_TREATMENT_RESPONSE",
      "required_evidence": [],
      "required_findings": [
        "MIXED_TREATMENT_RESPONSE"
      ],
      "severity_source": [
        "MIXED_TREATMENT_RESPONSE"
      ]
    },
    {
      "candidate_code": "FOLLOW_UP_REQUIRED",
      "final_diagnosis_code": "FOLLOW_UP_REQUIRED",
      "required_evidence": [],
      "required_findings": [
        "FOLLOW_UP_INSUFFICIENT"
      ],
      "severity_source": [
        "FOLLOW_UP_INSUFFICIENT"
      ]
    }
  ]
}

```


---

## SOURCE: Knowledge/findings/finding_codes.json

```json
{
  "registry_name": "FINDING_CODE_REGISTRY",
  "version": "1.0",
  "severity_levels": [
    "INFO",
    "MILD",
    "MODERATE",
    "SEVERE",
    "CRITICAL"
  ],
  "items": [
    {
      "code": "CTR_UNDERPERFORMING",
      "category": "CTR",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "TITLE_ATTRACTION_LOW",
      "category": "SNIPPET",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "POSITION_DECLINING",
      "category": "RANKING",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE",
        "CRITICAL"
      ]
    },
    {
      "code": "POSITION_STABLE",
      "category": "RANKING",
      "allowed_severity": [
        "INFO"
      ]
    },
    {
      "code": "LOW_VISIBILITY",
      "category": "VISIBILITY",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "HIGH_VISIBILITY_LOW_CLICK",
      "category": "CTR",
      "allowed_severity": [
        "MODERATE",
        "SEVERE",
        "CRITICAL"
      ]
    },
    {
      "code": "QUERY_SHIFT",
      "category": "QUERY",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "INTENT_DRIFT",
      "category": "INTENT",
      "allowed_severity": [
        "MODERATE",
        "SEVERE",
        "CRITICAL"
      ]
    },
    {
      "code": "CONTENT_OUTDATED",
      "category": "FRESHNESS",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "SERP_COMPETITION_HIGH",
      "category": "COMPETITION",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "INTERNAL_LINKS_WEAK",
      "category": "LINKS",
      "allowed_severity": [
        "MILD",
        "MODERATE"
      ]
    },
    {
      "code": "FAQ_COVERAGE_WEAK",
      "category": "CONTENT",
      "allowed_severity": [
        "MILD",
        "MODERATE"
      ]
    },
    {
      "code": "INSUFFICIENT_EVIDENCE",
      "category": "QUALITY",
      "allowed_severity": [
        "INFO"
      ]
    },
    {
      "code": "QUERY_OVERLAP_HIGH",
      "category": "CANNIBALIZATION",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "ARTICLE_INTENT_OVERLAP",
      "category": "CANNIBALIZATION",
      "allowed_severity": [
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "MERGE_SUITABILITY_HIGH",
      "category": "MERGE",
      "allowed_severity": [
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "DISTINCT_INTENT_OPPORTUNITY",
      "category": "CREATOR",
      "allowed_severity": [
        "INFO",
        "MILD"
      ]
    },
    {
      "code": "LONG_TERM_VISIBILITY_DECAY",
      "category": "LONG_TERM",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE",
        "CRITICAL"
      ]
    },
    {
      "code": "LONG_TERM_CTR_DECAY",
      "category": "LONG_TERM",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "LONG_TERM_POSITION_DECAY",
      "category": "LONG_TERM",
      "allowed_severity": [
        "MILD",
        "MODERATE",
        "SEVERE"
      ]
    },
    {
      "code": "SEASONALITY_DETECTED",
      "category": "LONG_TERM",
      "allowed_severity": [
        "INFO"
      ]
    },
    {
      "code": "RECOVERY_TREND",
      "category": "LONG_TERM",
      "allowed_severity": [
        "INFO",
        "MILD"
      ]
    },
    {
      "code": "IMPROVEMENT_CONFIRMED",
      "category": "TREATMENT_RESPONSE",
      "allowed_severity": [
        "INFO"
      ]
    },
    {
      "code": "TREATMENT_INEFFECTIVE",
      "category": "TREATMENT_RESPONSE",
      "allowed_severity": [
        "MODERATE"
      ]
    },
    {
      "code": "POST_TREATMENT_WORSENING",
      "category": "TREATMENT_RESPONSE",
      "allowed_severity": [
        "SEVERE",
        "CRITICAL"
      ]
    },
    {
      "code": "MIXED_TREATMENT_RESPONSE",
      "category": "TREATMENT_RESPONSE",
      "allowed_severity": [
        "MILD"
      ]
    },
    {
      "code": "FOLLOW_UP_INSUFFICIENT",
      "category": "TREATMENT_RESPONSE",
      "allowed_severity": [
        "INFO"
      ]
    }
  ]
}

```


---

## SOURCE: Knowledge/findings/rules/cross_article_finding_rules_v1.json

```json
{
  "rule_set": "SIMS_DOCTOR_CROSS_ARTICLE_FINDING_RULES_V1",
  "version": "1.0",
  "rules": [
    {
      "classification": "POSSIBLE_CANNIBALIZATION",
      "finding_code": "QUERY_OVERLAP_HIGH",
      "severity": "MODERATE",
      "base_confidence": 80
    },
    {
      "classification": "MERGE_CANDIDATE",
      "finding_code": "MERGE_SUITABILITY_HIGH",
      "severity": "SEVERE",
      "base_confidence": 85
    },
    {
      "classification": "SEPARATE_INTENT",
      "finding_code": "DISTINCT_INTENT_OPPORTUNITY",
      "severity": "INFO",
      "base_confidence": 75
    },
    {
      "classification": "NEW_ARTICLE_OPPORTUNITY",
      "finding_code": "DISTINCT_INTENT_OPPORTUNITY",
      "severity": "MILD",
      "base_confidence": 80
    }
  ]
}

```


---

## SOURCE: Knowledge/findings/rules/finding_rules_v1.json

```json
{
  "rule_set": "SIMS_DOCTOR_FINDING_RULES_V1",
  "version": "1.0",
  "status": "INITIAL_UNCALIBRATED",
  "global_policy": {
    "confidence_min": 0,
    "confidence_max": 100,
    "low_sample_confidence_penalty": 25,
    "duplicate_behavior": "SKIP_IDENTICAL_FINGERPRINT",
    "missing_input_behavior": "DO_NOT_GENERATE"
  },
  "rules": [
    {
      "finding_code": "CTR_UNDERPERFORMING",
      "rule_version": "1.0",
      "required_evidence": [
        "CTR_BELOW_POSITION_EXPECTATION"
      ],
      "required_vital_sign": "CTR_HEALTH",
      "severity_by_score": [
        {
          "min": 0,
          "max": 29,
          "severity": "SEVERE"
        },
        {
          "min": 30,
          "max": 49,
          "severity": "MODERATE"
        },
        {
          "min": 50,
          "max": 69,
          "severity": "MILD"
        }
      ],
      "base_confidence": 85
    },
    {
      "finding_code": "POSITION_DECLINING",
      "rule_version": "1.0",
      "required_evidence": [
        "POSITION_DECLINE_OBSERVED"
      ],
      "required_vital_sign": "RANKING_STABILITY",
      "severity_by_score": [
        {
          "min": 0,
          "max": 29,
          "severity": "CRITICAL"
        },
        {
          "min": 30,
          "max": 49,
          "severity": "SEVERE"
        },
        {
          "min": 50,
          "max": 69,
          "severity": "MODERATE"
        },
        {
          "min": 70,
          "max": 89,
          "severity": "MILD"
        }
      ],
      "base_confidence": 90
    },
    {
      "finding_code": "LOW_VISIBILITY",
      "rule_version": "1.0",
      "required_evidence": [
        "VISIBILITY_DECLINE_OBSERVED"
      ],
      "required_vital_sign": "VISIBILITY",
      "severity_by_score": [
        {
          "min": 0,
          "max": 29,
          "severity": "SEVERE"
        },
        {
          "min": 30,
          "max": 49,
          "severity": "MODERATE"
        },
        {
          "min": 50,
          "max": 69,
          "severity": "MILD"
        }
      ],
      "base_confidence": 85
    },
    {
      "finding_code": "CONTENT_OUTDATED",
      "rule_version": "1.0",
      "required_evidence": [
        "LONG_TIME_SINCE_UPDATE"
      ],
      "required_vital_sign": "FRESHNESS",
      "severity_by_score": [
        {
          "min": 0,
          "max": 29,
          "severity": "SEVERE"
        },
        {
          "min": 30,
          "max": 49,
          "severity": "MODERATE"
        },
        {
          "min": 50,
          "max": 69,
          "severity": "MILD"
        }
      ],
      "base_confidence": 80
    },
    {
      "finding_code": "HIGH_VISIBILITY_LOW_CLICK",
      "rule_version": "1.0",
      "required_evidence": [
        "CTR_BELOW_POSITION_EXPECTATION"
      ],
      "required_vital_sign": "CTR_HEALTH",
      "additional_conditions": {
        "visibility_min_score": 70
      },
      "severity_by_score": [
        {
          "min": 0,
          "max": 29,
          "severity": "CRITICAL"
        },
        {
          "min": 30,
          "max": 49,
          "severity": "SEVERE"
        },
        {
          "min": 50,
          "max": 69,
          "severity": "MODERATE"
        }
      ],
      "base_confidence": 90
    },
    {
      "finding_code": "INSUFFICIENT_EVIDENCE",
      "rule_version": "1.0",
      "trigger": "LOW_SAMPLE_ONLY",
      "severity": "INFO",
      "base_confidence": 100
    }
  ]
}

```


---

## SOURCE: Knowledge/differential/rules/differential_rules_v1.json

```json
{
  "rule_set": "SIMS_DOCTOR_DIFFERENTIAL_RULES_V1",
  "version": "1.0",
  "status": "INITIAL_UNCALIBRATED",
  "global_policy": {
    "candidate_limit": 5,
    "minimum_candidate_confidence": 20,
    "low_sample_penalty": 20,
    "contradiction_penalty": 15,
    "duplicate_behavior": "SKIP_IDENTICAL_FINGERPRINT",
    "ranking": "CONFIDENCE_DESC_THEN_PRIORITY_DESC"
  },
  "candidates": [
    {
      "diagnosis_code": "LOW_CTR_WITH_STRONG_POSITION",
      "priority": 90,
      "supporting_findings": [
        {
          "code": "CTR_UNDERPERFORMING",
          "weight": 45
        },
        {
          "code": "HIGH_VISIBILITY_LOW_CLICK",
          "weight": 40
        }
      ],
      "contradicting_findings": [
        {
          "code": "LOW_VISIBILITY",
          "weight": 20
        }
      ],
      "base_confidence": 20,
      "minimum_support_count": 1,
      "notes": "Strong when CTR is weak while visibility remains healthy."
    },
    {
      "diagnosis_code": "LONG_TERM_DECLINE",
      "priority": 80,
      "supporting_findings": [
        {
          "code": "POSITION_DECLINING",
          "weight": 40
        },
        {
          "code": "LOW_VISIBILITY",
          "weight": 35
        },
        {
          "code": "CONTENT_OUTDATED",
          "weight": 20
        }
      ],
      "contradicting_findings": [
        {
          "code": "POSITION_STABLE",
          "weight": 30
        }
      ],
      "base_confidence": 15,
      "minimum_support_count": 2
    },
    {
      "diagnosis_code": "CONTENT_STALE",
      "priority": 70,
      "supporting_findings": [
        {
          "code": "CONTENT_OUTDATED",
          "weight": 60
        },
        {
          "code": "LOW_VISIBILITY",
          "weight": 20
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "UPDATE_FAILURE",
      "priority": 75,
      "supporting_findings": [
        {
          "code": "POSITION_DECLINING",
          "weight": 35
        },
        {
          "code": "LOW_VISIBILITY",
          "weight": 30
        },
        {
          "code": "CTR_UNDERPERFORMING",
          "weight": 15
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 10,
      "minimum_support_count": 2,
      "required_context": [
        "history.improvement_event_exists"
      ]
    },
    {
      "diagnosis_code": "INSUFFICIENT_DATA",
      "priority": 100,
      "supporting_findings": [
        {
          "code": "INSUFFICIENT_EVIDENCE",
          "weight": 80
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "CANNIBALIZATION",
      "priority": 95,
      "supporting_findings": [
        {
          "code": "QUERY_OVERLAP_HIGH",
          "weight": 70
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "ARTICLE_MERGE_REQUIRED",
      "priority": 98,
      "supporting_findings": [
        {
          "code": "MERGE_SUITABILITY_HIGH",
          "weight": 75
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "NEW_ARTICLE_NEEDED",
      "priority": 70,
      "supporting_findings": [
        {
          "code": "DISTINCT_INTENT_OPPORTUNITY",
          "weight": 60
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "LONG_TERM_DECAY",
      "priority": 92,
      "supporting_findings": [
        {
          "code": "LONG_TERM_VISIBILITY_DECAY",
          "weight": 50
        },
        {
          "code": "LONG_TERM_CTR_DECAY",
          "weight": 25
        },
        {
          "code": "LONG_TERM_POSITION_DECAY",
          "weight": 30
        }
      ],
      "contradicting_findings": [
        {
          "code": "RECOVERY_TREND",
          "weight": 40
        }
      ],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "SEASONAL_DECLINE",
      "priority": 65,
      "supporting_findings": [
        {
          "code": "SEASONALITY_DETECTED",
          "weight": 65
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "RECOVERY_IN_PROGRESS",
      "priority": 85,
      "supporting_findings": [
        {
          "code": "RECOVERY_TREND",
          "weight": 70
        }
      ],
      "contradicting_findings": [
        {
          "code": "LONG_TERM_VISIBILITY_DECAY",
          "weight": 30
        }
      ],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "TREATMENT_SUCCESS",
      "priority": 75,
      "supporting_findings": [
        {
          "code": "IMPROVEMENT_CONFIRMED",
          "weight": 75
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "IMPROVEMENT_FAILURE",
      "priority": 94,
      "supporting_findings": [
        {
          "code": "TREATMENT_INEFFECTIVE",
          "weight": 60
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "POST_IMPROVEMENT_WORSENING",
      "priority": 99,
      "supporting_findings": [
        {
          "code": "POST_TREATMENT_WORSENING",
          "weight": 75
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "MIXED_TREATMENT_RESPONSE",
      "priority": 80,
      "supporting_findings": [
        {
          "code": "MIXED_TREATMENT_RESPONSE",
          "weight": 60
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    },
    {
      "diagnosis_code": "FOLLOW_UP_REQUIRED",
      "priority": 90,
      "supporting_findings": [
        {
          "code": "FOLLOW_UP_INSUFFICIENT",
          "weight": 70
        }
      ],
      "contradicting_findings": [],
      "base_confidence": 20,
      "minimum_support_count": 1
    }
  ]
}

```


---

## SOURCE: Knowledge/composite_diagnosis/composite_diagnosis_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_COMPOSITE_DIAGNOSIS_POLICY_V1",
  "version": "1.0",
  "weights": {
    "competition": 0.1,
    "content_integrity": 0.2,
    "ctr_opportunity": 0.15,
    "position_opportunity": 0.15,
    "intent_drift": 0.15,
    "freshness_decay": 0.1,
    "cannibalization": 0.15
  },
  "diagnoses": [
    "HEALTHY",
    "MINOR_REFRESH",
    "LOCAL_OPTIMIZATION",
    "FULL_REWRITE_RECOMMENDED",
    "NEW_ARTICLE_RECOMMENDED",
    "MERGE_RECOMMENDED",
    "OBSERVE_ONLY",
    "FOLLOW_UP_REQUIRED"
  ],
  "safety_precedence": [
    "LOW_SAMPLE_OR_INSUFFICIENT_DATA",
    "RECENT_CHANGE_OR_RECENT_UPDATE",
    "WINNER_QUERY_PROTECTION",
    "MERGE_CANDIDATE",
    "ROLE_SEPARATION",
    "SEVERE_COMPOSITE_DAMAGE"
  ],
  "thresholds": {
    "healthy_vital_score": 75,
    "local_optimization_score": 45,
    "full_rewrite_score": 65,
    "severe_content_integrity_max": 45,
    "new_article_intent_confidence": 85,
    "minimum_composite_confidence": 60,
    "minimum_completed_assessments": 3
  },
  "safety": {
    "winner_query_blocks_full_rewrite": true,
    "recent_change_forces_observation": true,
    "low_sample_forces_follow_up": true,
    "merge_requires_cannibalization_merge_candidate": true,
    "new_article_requires_intent_signal_and_no_merge_candidate": true,
    "doctor_does_not_execute_treatment": true
  }
}

```


---

## SOURCE: Knowledge/vital_score/vital_score_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_VITAL_SCORE_POLICY_V1",
  "version": "1.0",
  "weights": {
    "VISIBILITY": 0.18,
    "TRAFFIC": 0.16,
    "CTR_HEALTH": 0.16,
    "RANKING_STABILITY": 0.16,
    "FRESHNESS": 0.12,
    "COMPETITION_RESILIENCE": 0.12,
    "CONTENT_INTEGRITY": 0.1
  },
  "missing_value": {
    "strategy": "REWEIGHT_AVAILABLE_SIGNS",
    "minimum_available_signs": 3,
    "insufficient_profile_score": null
  },
  "adjustments": {
    "low_sample_penalty": 8,
    "critical_finding_penalty": 12,
    "severe_finding_penalty": 6,
    "recovery_bonus": 5,
    "maximum_total_penalty": 25,
    "maximum_total_bonus": 10
  },
  "health_bands": [
    {
      "minimum": 85,
      "code": "EXCELLENT"
    },
    {
      "minimum": 70,
      "code": "GOOD"
    },
    {
      "minimum": 55,
      "code": "WATCH"
    },
    {
      "minimum": 40,
      "code": "UNHEALTHY"
    },
    {
      "minimum": 0,
      "code": "CRITICAL"
    }
  ],
  "explanation": {
    "top_negative_factors": 3,
    "top_positive_factors": 3
  }
}

```


---

## SOURCE: Knowledge/vital_signs/formulas/vital_sign_formulas_v1.json

```json
{
  "formula_set": "SIMS_DOCTOR_VITAL_SIGN_FORMULAS_V1",
  "version": "1.0",
  "status": "INITIAL_UNCALIBRATED",
  "global_policy": {
    "score_min": 0,
    "score_max": 100,
    "higher_is_healthier": true,
    "low_sample_penalty": 15,
    "missing_input_behavior": "MARK_UNAVAILABLE",
    "rounding": "NEAREST_INTEGER"
  },
  "formulas": [
    {
      "code": "VISIBILITY",
      "version": "1.0",
      "inputs": [
        "days_28.impressions",
        "days_90.impressions",
        "days_365.impressions"
      ],
      "method": "TREND_AND_COVERAGE",
      "weights": {
        "current_level": 0.4,
        "trend": 0.4,
        "historical_presence": 0.2
      }
    },
    {
      "code": "TRAFFIC",
      "version": "1.0",
      "inputs": [
        "days_28.clicks",
        "days_90.clicks",
        "days_365.clicks"
      ],
      "method": "TREND_AND_CURRENT_SHARE",
      "weights": {
        "current_level": 0.5,
        "trend": 0.5
      }
    },
    {
      "code": "CTR_HEALTH",
      "version": "1.0",
      "inputs": [
        "days_28.ctr",
        "days_28.position",
        "evidence.CTR_BELOW_POSITION_EXPECTATION"
      ],
      "method": "POSITION_ADJUSTED_CTR",
      "weights": {
        "position_adjusted": 0.8,
        "evidence_penalty": 0.2
      }
    },
    {
      "code": "RANKING_STABILITY",
      "version": "1.0",
      "inputs": [
        "days_28.position",
        "days_90.position",
        "days_365.position",
        "evidence.POSITION_DECLINE_OBSERVED"
      ],
      "method": "POSITION_VARIANCE",
      "weights": {
        "trend": 0.7,
        "evidence_penalty": 0.3
      }
    },
    {
      "code": "FRESHNESS",
      "version": "1.0",
      "inputs": [
        "metadata.last_modified_at",
        "evidence.LONG_TIME_SINCE_UPDATE"
      ],
      "method": "DAYS_SINCE_UPDATE",
      "parameters": {
        "full_score_days": 90,
        "zero_score_days": 730
      }
    },
    {
      "code": "COMPETITION_RESILIENCE",
      "version": "1.0",
      "inputs": [
        "serp.strength",
        "serp.intent_match",
        "serp.content_gap"
      ],
      "method": "SERP_COMPETITION_INVERSION",
      "notes": "Calculated from normalized SERP competition strength and intent match.",
      "status": "INITIAL_UNCALIBRATED"
    },
    {
      "code": "CONTENT_INTEGRITY",
      "version": "1.0",
      "inputs": [
        "article_snapshot",
        "internal_links",
        "serp.intent_match"
      ],
      "method": "ARTICLE_STRUCTURE_AND_INTENT",
      "notes": "Calculated from Article Snapshot structure and intent-alignment data.",
      "status": "INITIAL_UNCALIBRATED"
    }
  ]
}

```


---

## SOURCE: Knowledge/vital_signs/vital_signs.json

```json
{
  "registry_name": "VITAL_SIGN_REGISTRY",
  "version": "1.0",
  "score_range": {
    "minimum": 0,
    "maximum": 100
  },
  "normal_ranges": [
    {
      "minimum": 90,
      "maximum": 100,
      "classification": "NORMAL"
    },
    {
      "minimum": 70,
      "maximum": 89,
      "classification": "MILD_ATTENTION"
    },
    {
      "minimum": 50,
      "maximum": 69,
      "classification": "OBSERVATION_REQUIRED"
    },
    {
      "minimum": 30,
      "maximum": 49,
      "classification": "TREATMENT_REQUIRED"
    },
    {
      "minimum": 0,
      "maximum": 29,
      "classification": "SEVERE"
    }
  ],
  "items": [
    {
      "code": "VISIBILITY",
      "direction": "HIGHER_IS_HEALTHIER",
      "description": "検索結果上での露出状態",
      "inputs": [
        "impressions",
        "query_coverage",
        "historical_trend"
      ],
      "status": "FORMULA_PENDING_CALIBRATION"
    },
    {
      "code": "TRAFFIC",
      "direction": "HIGHER_IS_HEALTHIER",
      "description": "検索流入の獲得状態",
      "inputs": [
        "clicks",
        "historical_trend"
      ],
      "status": "FORMULA_PENDING_CALIBRATION"
    },
    {
      "code": "CTR_HEALTH",
      "direction": "HIGHER_IS_HEALTHIER",
      "description": "掲載順位を考慮したクリック率の健全性",
      "inputs": [
        "ctr",
        "position",
        "impressions"
      ],
      "status": "FORMULA_PENDING_CALIBRATION"
    },
    {
      "code": "RANKING_STABILITY",
      "direction": "HIGHER_IS_HEALTHIER",
      "description": "順位変動の安定性",
      "inputs": [
        "position_series"
      ],
      "status": "FORMULA_PENDING_CALIBRATION"
    },
    {
      "code": "FRESHNESS",
      "direction": "HIGHER_IS_HEALTHIER",
      "description": "記事情報の鮮度",
      "inputs": [
        "last_modified_at",
        "time_sensitive_markers"
      ],
      "status": "FORMULA_PENDING_CALIBRATION"
    },
    {
      "code": "COMPETITION_RESILIENCE",
      "direction": "HIGHER_IS_HEALTHIER",
      "description": "競合圧力に対する耐性。競合圧力そのものではなく健全度として表す",
      "inputs": [
        "serp_strength",
        "domain_mix",
        "content_gap"
      ],
      "status": "FORMULA_PENDING_CALIBRATION"
    },
    {
      "code": "CONTENT_INTEGRITY",
      "direction": "HIGHER_IS_HEALTHIER",
      "description": "検索意図、構造、内部リンク、FAQ、情報整合性の健全度",
      "inputs": [
        "article_snapshot",
        "internal_links",
        "serp_intent"
      ],
      "status": "FORMULA_PENDING_CALIBRATION"
    }
  ]
}

```


# Keyword Strategy Reassessment v1 — aDoctor v2.0.5

This policy applies ONLY after the existing SIMS Manager request gate and Evidence Validation succeed for a normal SEO diagnosis. It does not change the information-update dedicated reception or other contracts.

## Three distinct fields
- original_target_query: article creation intent, only when explicitly evidenced; otherwise null. Never infer it from current GSC.
- observed_main_query: Manager/GSC observation, read-only; do not overwrite or redefine it.
- improvement_target_query: Doctor's recommended next optimization focus; nullable when article-role separation or evidence insufficiency makes a single focus inappropriate.

## Four outcomes
- MAINTAIN: preserve original intent and article role when still appropriate.
- RETARGET: change the optimization focus only if repeated sufficient observations, SERP intent, article content and site portfolio support it; never rewrite GSC observations.
- ROLE_SEPARATION: preserve hub/specialist boundaries; route distinct search intents to existing specialist articles or recommend new ones only after verified independent demand and cannibalization checks.
- DEFER: insufficient or contradictory evidence; avoid irreversible title/URL/content changes and specify missing evidence.

## Evidence and risk controls
Reuse existing intent_drift, cannibalization, position and CTR policies and LOW_SAMPLE protection. Compare query impressions, clicks, CTR, position trend, observed periods, SERP intent, existing article roles, and monetization opportunity where evidence exists. Do not treat a top GSC query as the creation-time target. Revenue at query level is not observable from GSC; describe indirect opportunity as estimated, not measured. Do not fabricate original keyword, numerical confidence, rankings, revenue, or sibling article performance. Prefer reversible internal-link adjustments to broad rewrites when evidence is mixed.

## Output (optional, backward compatible)
When the SEO case involves a meaningful discrepancy between original intent and observed query, include a compact top-level keyword_strategy_assessment in SIMS_DOCTOR_CASE_RESULT_V2:
- decision: MAINTAIN | RETARGET | ROLE_SEPARATION | DEFER
- original_target_query: string|null
- observed_main_query: string|null
- improvement_target_query: string|null
- article_role: string|null
- reason: concise Japanese text grounded in evidence
- confidence: CONFIRMED | PROVISIONAL | INSUFFICIENT
- evidence_gaps: array of strings (optional)
Do not change workflow_handoff.next_action or treatment_plan strategy enumerations. This assessment is strategic metadata, not a new workflow state. Keep the JSON compact; Manager's Doctor result storage has a size limit. Never modify Manager article-management fields or GSC source data.

## Example A000185
Beginner hub, observed query 'notion 重い 開かない', links to three specialist pages already implemented: provisional ROLE_SEPARATION; original target and improvement target null until independently evidenced. Do not prescribe another edit merely because the assessment exists.
