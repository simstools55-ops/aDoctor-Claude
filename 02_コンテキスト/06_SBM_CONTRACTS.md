# 06_SBM_CONTRACTS.md
この文書は元Repositoryの必要な規則・契約を原文のまま集約したものです。章見出しは元のファイルパスです。


---

## SOURCE: Runtime/OUTPUT_RUNTIME.md

```markdown
# aDoctor Claude Output Runtime v1.1.3

通常回答は治療計画書として次の順序で出力する。

1. Doctorコメント
2. 総合診断（診断名、確信度、治療区分、次の担当候補）
3. 今回やること（今日・SBM登録後・次回）
4. 今回はやらないこと
5. この方針にした理由
6. 利用者へのアドバイス
7. SBM登録用診断結果JSON
8. 次回診察予定

Doctorから専門製品への直接依頼文は表示しない。回答末尾には、SBM 5.9.8以降が読み取れる完全な `SIMS_DOCTOR_CASE_RESULT_V2` JSONを独立したjsonコードブロックで必ず表示する。

JSON直前の固定案内:

> 下のJSONをすべてコピーし、SBMの精密診断ダイアログにある「② Doctorの診断結果を受け取る」欄へ貼り付けてください。登録すると、SBMが次の担当への完全な紹介状を自動表示します。

## 次担当
`workflow_handoff.next_action`を必ず出力します。


## Personal Knowledge v1.4.0
診断結果JSONには `knowledge_candidates` を配列で返す。再利用価値がない場合は空配列。現在の指標やSERPスナップショットは入れない。SITE候補はSBMからの `personal_knowledge_site_id` を使い、`confirmation_event_id` は `case_id` とする。

```


---

## SOURCE: Knowledge/workflow/output_policy_v1.json

```json
{
  "policy_name": "SIMS_DOCTOR_OUTPUT_POLICY_V1",
  "version": "1.0",
  "user_display": {
    "language": "ja",
    "show_internal_ids": false,
    "show_raw_rule_names": false,
    "show_confidence": true,
    "show_severity": true,
    "show_review_date": true,
    "show_supporting_reasons_limit": 5
  },
  "system_output": {
    "include_trace_ids": true,
    "include_evidence_ids": true,
    "include_finding_ids": true,
    "include_contract_version": true
  },
  "writer_referral": {
    "allowed_diagnoses": [
      "CTR_PROBLEM",
      "POSITION_DECLINE",
      "CONTENT_STALE",
      "UPDATE_FAILURE"
    ],
    "deferred_behavior": "DO_NOT_CREATE_WRITER_REQUEST"
  }
}

```


---

## SOURCE: Knowledge/workflow/diagnosis_report.md

```markdown
# Diagnosis Report and Referral Output

Doctor produces three distinct outputs.

1. Medical Record: the diagnostic source of truth
2. Diagnosis Report: a user-facing explanation
3. Referral Request: a system-facing instruction for a treatment product

The user-facing report must not expose internal rule names or require the user to
understand SEO diagnosis logic.

```


---

## SOURCE: contracts/platform/SIMS_DOCTOR_DIAGNOSIS_REQUEST_V1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "envelope",
    "payload"
  ],
  "properties": {
    "envelope": {
      "type": "object",
      "required": [
        "platform",
        "platform_version",
        "contract_name",
        "contract_version",
        "message_type",
        "message_id",
        "correlation_id",
        "created_at",
        "source_product",
        "target_product",
        "shared_version"
      ],
      "properties": {
        "platform": {
          "const": "SIMS_EDITORIAL_PLATFORM"
        },
        "platform_version": {
          "type": "string"
        },
        "contract_name": {
          "const": "SIMS_DOCTOR_DIAGNOSIS_REQUEST_V1"
        },
        "contract_version": {
          "type": "string"
        },
        "message_type": {
          "enum": [
            "REQUEST",
            "RESULT",
            "EVENT",
            "ERROR",
            "ACKNOWLEDGEMENT"
          ]
        },
        "message_id": {
          "type": "string",
          "minLength": 1
        },
        "correlation_id": {
          "type": "string",
          "minLength": 1
        },
        "causation_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "created_at": {
          "type": "string"
        },
        "source_product": {
          "type": "object"
        },
        "target_product": {
          "type": "object"
        },
        "shared_version": {
          "type": "string"
        },
        "locale": {
          "type": "string"
        },
        "timezone": {
          "type": "string"
        }
      }
    },
    "payload": {
      "type": "object",
      "required": [
        "case",
        "objective",
        "workflow_context",
        "evidence"
      ],
      "additionalProperties": true,
      "properties": {
        "case": {},
        "objective": {},
        "workflow_context": {},
        "evidence": {}
      }
    }
  },
  "title": "SIMS_DOCTOR_DIAGNOSIS_REQUEST_V1"
}

```


---

## SOURCE: contracts/platform/SIMS_DOCTOR_DIAGNOSIS_RESULT_V1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "envelope",
    "payload"
  ],
  "properties": {
    "envelope": {
      "type": "object",
      "required": [
        "platform",
        "platform_version",
        "contract_name",
        "contract_version",
        "message_type",
        "message_id",
        "correlation_id",
        "created_at",
        "source_product",
        "target_product",
        "shared_version"
      ],
      "properties": {
        "platform": {
          "const": "SIMS_EDITORIAL_PLATFORM"
        },
        "platform_version": {
          "type": "string"
        },
        "contract_name": {
          "const": "SIMS_DOCTOR_DIAGNOSIS_RESULT_V1"
        },
        "contract_version": {
          "type": "string"
        },
        "message_type": {
          "enum": [
            "REQUEST",
            "RESULT",
            "EVENT",
            "ERROR",
            "ACKNOWLEDGEMENT"
          ]
        },
        "message_id": {
          "type": "string",
          "minLength": 1
        },
        "correlation_id": {
          "type": "string",
          "minLength": 1
        },
        "causation_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "created_at": {
          "type": "string"
        },
        "source_product": {
          "type": "object"
        },
        "target_product": {
          "type": "object"
        },
        "shared_version": {
          "type": "string"
        },
        "locale": {
          "type": "string"
        },
        "timezone": {
          "type": "string"
        }
      }
    },
    "payload": {
      "type": "object",
      "required": [
        "case_id",
        "diagnosis_id",
        "result_status",
        "diagnosis",
        "treatment_required",
        "referrals"
      ],
      "additionalProperties": true,
      "properties": {
        "case_id": {},
        "diagnosis_id": {},
        "result_status": {},
        "diagnosis": {},
        "treatment_required": {},
        "referrals": {}
      }
    }
  },
  "title": "SIMS_DOCTOR_DIAGNOSIS_RESULT_V1"
}

```


---

## SOURCE: contracts/registry/COMPATIBILITY_POLICY.md

```markdown
# Compatibility Policy v0.1.0

- `contract_version`: breaking contract generation, `MAJOR.MINOR`.
- `schema_version`: structural revision, `MAJOR.MINOR.PATCH`.
- Optional field additions are backward compatible.
- Required field additions, type changes, removals, and semantic changes require a new major contract version.
- Receivers must ignore unknown optional fields.
- Receivers must reject unsupported contract versions explicitly.
- Duplicate `message_id` must not create duplicate records or locks.

```


---

## SOURCE: contracts/registry/DATA_OWNERSHIP_MATRIX.md

```markdown
# Data Ownership Matrix v0.1.0

| Data | System of record |
|---|---|
| SiteID / ArticleID / URL / title / publish date | SIMS-Blog-Manager |
| Search Console long-term history | SIMS Article Doctor Collector |
| Diagnosis Case | SIMS Article Doctor |
| Treatment plan | SIMS Article Doctor |
| Writer detailed changes | SIMS Writer |
| Creator detailed article output | SIMS Article Creator |
| Merge detailed integration output | SIMS Merge |
| Publication confirmation | SBM / user input |
| Monitoring measurements | SBM |
| Case aggregate state | SIMS Article Doctor |

```


---

## SOURCE: contracts/registry/ENUM_REGISTRY.md

```markdown
# Enum Registry v0.1.0

## Systems
SIMS_BLOG_MANAGER / SIMS_DOCTOR / SIMS_DOCTOR_COLLECTOR /
SIMS_DOCTOR_DIAGNOSIS_ENGINE / SIMS_WRITER / SIMS_ARTICLE_CREATOR /
SIMS_MERGE / USER

## Case status
NEW / DIAGNOSING / DIAGNOSED / PLAN_CREATED / TREATMENT_PENDING /
TREATING / PUBLICATION_PENDING / MONITORING / REASSESSMENT_REQUIRED /
CLOSED / CANCELLED / FAILED

## Treatment status
PENDING / ACCEPTED / IN_PROGRESS / COMPLETED / PARTIALLY_COMPLETED /
BLOCKED / REJECTED / FAILED / CANCELLED

## Article workflow status
AVAILABLE / SBM_IMPROVEMENT_PENDING / SBM_IMPROVEMENT_IN_PROGRESS /
SBM_MONITORING / DOCTOR_DIAGNOSING / DOCTOR_TREATMENT_PENDING /
DOCTOR_TREATMENT_IN_PROGRESS / DOCTOR_PUBLICATION_PENDING /
DOCTOR_MONITORING / MANUAL_HOLD / ARCHIVED / DELETED

```


---

## SOURCE: contracts/registry/ERROR_WARNING_REGISTRY.md

```markdown
# Error and Warning Registry v0.1.0

## Error categories
VALIDATION / AUTHENTICATION / AUTHORIZATION / VERSION_MISMATCH /
RESOURCE_NOT_FOUND / CONFLICT / TEMPORARY_FAILURE / RATE_LIMIT /
SYSTEM_FAILURE

## Warning severity
INFO / WARNING / HIGH

Errors use:
```json
{
  "success": false,
  "error": {
    "code": "ACTIVE_TREATMENT_CONFLICT",
    "category": "CONFLICT",
    "message": "対象記事では別の処置が進行中です。",
    "retryable": false,
    "details": {}
  }
}
```

```


---

## SOURCE: contracts/registry/IDENTIFIER_REGISTRY.md

```markdown
# Identifier Registry v0.1.0

| Identifier | Issuer |
|---|---|
| site_id | SBM |
| article_id | SBM |
| catalog_id | SBM |
| collector_job_id | Doctor Collector |
| snapshot_id | Doctor Collector |
| diagnosis_run_id | Doctor |
| case_id | Doctor |
| treatment_id | Doctor |
| message_id | Each sender |
| temporary_content_id | Creator / Doctor |
| redirect_id | Doctor / Merge |
| action_id | Doctor |

```


---

## SOURCE: contracts/registry/INTERFACE_CONTRACT_REGISTRY.md

```markdown
# SIMS Article Doctor Interface Contract Registry v0.1.0

## Contracts

| Contract | Source | Target | Responsibility |
|---|---|---|---|
| SIMS_DOCTOR_ARTICLE_CATALOG_V1 | SIMS_BLOG_MANAGER | SIMS_DOCTOR | 記事マスタと運用状態 |
| SIMS_DOCTOR_LONG_TERM_SNAPSHOT_V1 | SIMS_DOCTOR_COLLECTOR | SIMS_DOCTOR_DIAGNOSIS_ENGINE | 長期集計とデータ品質 |
| SIMS_DOCTOR_CASE_DIAGNOSIS_V1 | SIMS_DOCTOR | SIMS_BLOG_MANAGER | 診断Case・治療案・ロック要求 |
| SIMS_DOCTOR_WRITER_REQUEST_V1 | SIMS_DOCTOR | SIMS_WRITER | Writer向け個別Treatment |
| SIMS_TREATMENT_RESULT_V1 | 専門システム | SIMS_DOCTOR | 個別Treatment結果 |
| SIMS_DOCTOR_CASE_RESULT_V1 | SIMS_DOCTOR | SIMS_BLOG_MANAGER | Case全体の集約結果 |

## Core rules

- `site_id` と `article_id` の正本は SBM。
- `case_id` と `treatment_id` の発行主体は Doctor。
- `message_id` は送信元内で一意。
- 同一 `message_id` は冪等に無視。
- Case状態 `TREATING` と Treatment状態 `IN_PROGRESS` を混同しない。
- 公開判断と公開状態を分離する。
- 未知の任意フィールドは無視できる。
- 未知の列挙値は既知値へ自動変換しない。

```


---

## SOURCE: contracts/registry/STATE_TRANSITION_MATRIX.md

```markdown
# State Transition Matrix v0.1.0

## Case
NEW → DIAGNOSING → DIAGNOSED → PLAN_CREATED → TREATMENT_PENDING →
TREATING → PUBLICATION_PENDING → MONITORING → CLOSED

Alternative transitions:
- DIAGNOSED → MONITORING
- DIAGNOSED → CLOSED
- TREATING → REASSESSMENT_REQUIRED
- Any active state → CANCELLED / FAILED where valid

## Treatment
PENDING → ACCEPTED → IN_PROGRESS → COMPLETED

Alternative outcomes:
PARTIALLY_COMPLETED / BLOCKED / REJECTED / FAILED / CANCELLED

```


---

## SOURCE: contracts/SIMS_DOCTOR_CASE_RESULT_V2.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "SIMS_DOCTOR_CASE_RESULT_V2.schema.json",
  "title": "SIMS Article Doctor Case Result V2",
  "type": "object",
  "required": [
    "format",
    "contract_version",
    "case_id",
    "article_id",
    "diagnosis",
    "treatment_plan",
    "referral",
    "workflow",
    "reexamination"
  ],
  "properties": {
    "format": {
      "const": "SIMS_DOCTOR_CASE_RESULT_V2"
    },
    "contract_version": {
      "const": "2.0"
    },
    "case_id": {
      "type": "string",
      "minLength": 1
    },
    "diagnosis_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "medical_record_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "site_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "article_id": {
      "type": "string",
      "minLength": 1
    },
    "completed_at": {
      "type": "string"
    },
    "diagnosis": {
      "type": "object"
    },
    "treatment_plan": {
      "type": "object"
    },
    "referral": {
      "type": "object",
      "required": [
        "required",
        "destination",
        "allowed_scope",
        "blocked_scope"
      ]
    },
    "workflow": {
      "type": "object",
      "required": [
        "workflow_locked",
        "return_to"
      ],
      "properties": {
        "return_to": {
          "const": "SIMS_BLOG_MANAGER"
        }
      }
    },
    "reexamination": {
      "type": "object"
    },
    "presentation": {
      "type": "object",
      "required": [
        "standard",
        "summary",
        "do_now",
        "do_not",
        "next_step"
      ],
      "properties": {
        "standard": {
          "const": "SIMS_PRESENTATION_STANDARD_V1"
        },
        "summary": {
          "type": [
            "string",
            "null"
          ]
        },
        "do_now": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "do_not": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "next_step": {
          "type": [
            "string",
            "null"
          ]
        },
        "review_after_days": {
          "type": [
            "integer",
            "null"
          ]
        },
        "note": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "additionalProperties": true
    },
    "personal_knowledge_site_id": {
      "type": [
        "string",
        "null"
      ]
    },
    "knowledge_candidates": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/knowledge_candidate"
      }
    }
  },
  "additionalProperties": true,
  "$defs": {
    "knowledge_candidate": {
      "type": "object",
      "required": [
        "scope",
        "knowledge_type",
        "statement",
        "confidence",
        "source_product",
        "source_type",
        "confirmation_event_id"
      ],
      "properties": {
        "candidate_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "scope": {
          "enum": [
            "OWNER",
            "SITE",
            "CROSS_SITE"
          ]
        },
        "site_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "knowledge_type": {
          "enum": [
            "ARTICLE_ROLE",
            "ARTICLE_RELATIONSHIP",
            "INTENT_BOUNDARY",
            "CANNIBALIZATION_BOUNDARY",
            "SITE_SPECIFIC_TREATMENT_LEARNING",
            "CONTENT_FRESHNESS_RISK"
          ]
        },
        "statement": {
          "type": "string",
          "minLength": 1
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "source_product": {
          "const": "SIMS Article Doctor"
        },
        "source_type": {
          "const": "DIAGNOSIS_INFERENCE"
        },
        "evidence_refs": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "confirmation_event_id": {
          "type": "string",
          "minLength": 1
        },
        "explicit_user_confirmation": {
          "type": "boolean"
        },
        "deterministic_state": {
          "type": "boolean"
        }
      }
    }
  }
}

```


---

## SOURCE: contracts/SIMS_DOCTOR_WRITER_REQUEST_V1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://sims.local/contracts/SIMS_DOCTOR_WRITER_REQUEST_V1.schema.json",
  "title": "SIMS_DOCTOR_WRITER_REQUEST_V1",
  "type": "object",
  "required": [
    "contract_name",
    "contract_version",
    "request_id",
    "case_id",
    "article",
    "diagnosis",
    "treatment"
  ],
  "properties": {
    "contract_name": {
      "const": "SIMS_DOCTOR_WRITER_REQUEST_V1"
    },
    "contract_version": {
      "const": "1.0"
    },
    "request_id": {
      "type": "string"
    },
    "case_id": {
      "type": "string"
    },
    "article": {
      "type": "object"
    },
    "diagnosis": {
      "type": "object"
    },
    "treatment": {
      "type": "object"
    }
  }
}

```


---

## SOURCE: contracts/SIMS_DOCTOR_SINGLE_CASE_REQUEST_V1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://sims.local/contracts/SIMS_DOCTOR_SINGLE_CASE_REQUEST_V1.schema.json",
  "title": "SIMS_DOCTOR_SINGLE_CASE_REQUEST_V1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "contract_name",
    "contract_version",
    "requested_at",
    "request_source",
    "request_type",
    "site",
    "article",
    "trigger"
  ],
  "properties": {
    "contract_name": {
      "const": "SIMS_DOCTOR_SINGLE_CASE_REQUEST_V1"
    },
    "contract_version": {
      "const": "1.0"
    },
    "requested_at": {
      "type": "string",
      "format": "date-time"
    },
    "request_source": {
      "const": "SIMS_BLOG_MANAGER"
    },
    "request_type": {
      "const": "SINGLE_CASE_DIAGNOSIS"
    },
    "site": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "site_id",
        "site_name",
        "blog_url"
      ],
      "properties": {
        "site_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 100
        },
        "site_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 300
        },
        "blog_url": {
          "type": "string",
          "format": "uri",
          "maxLength": 2048
        }
      }
    },
    "article": {
      "type": "object",
      "additionalProperties": true,
      "required": [
        "article_id",
        "url",
        "title"
      ],
      "properties": {
        "article_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 100
        },
        "url": {
          "type": "string",
          "format": "uri",
          "maxLength": 2048
        },
        "title": {
          "type": "string",
          "minLength": 1,
          "maxLength": 1000
        },
        "main_query": {
          "type": [
            "string",
            "null"
          ],
          "maxLength": 500
        },
        "current_metrics": {
          "type": [
            "object",
            "null"
          ],
          "additionalProperties": true
        }
      }
    },
    "trigger": {
      "type": "object",
      "additionalProperties": true,
      "required": [
        "source_screen",
        "reason"
      ],
      "properties": {
        "source_screen": {
          "type": "string",
          "enum": [
            "ARTICLE_LIST",
            "IMPROVEMENT_TREND"
          ]
        },
        "reason": {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        }
      }
    }
  }
}

```


---

## SOURCE: contracts/SIMS_DOCTOR_SINGLE_CASE_RESULT_V1.1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SIMS Article Doctor Single Case Result v1.1 Claude Extension",
  "type": "object",
  "properties": {
    "contract_name": {"const": "SIMS_DOCTOR_SINGLE_CASE_RESULT_V1"},
    "contract_version": {"enum": ["1.0", "1.1"]},
    "clinical_review": {"type": "object"},
    "evidence_quality": {"type": "array", "items": {"type": "object"}},
    "external_factors": {"type": "array", "items": {"type": "object"}},
    "confidence_factors": {"type": "object"},
    "treatment_tracks": {"type": "object"}
  },
  "additionalProperties": true
}

```


---

## SOURCE: contracts/SIMS_DOCTOR_REPORT_V1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SIMS_DOCTOR_REPORT_V1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "contract_name",
    "contract_version",
    "report_id",
    "case_id",
    "medical_record_id",
    "generated_at",
    "audience",
    "article",
    "summary",
    "diagnosis",
    "recommendation",
    "monitoring",
    "sections",
    "trace"
  ],
  "properties": {
    "contract_name": {
      "const": "SIMS_DOCTOR_REPORT_V1"
    },
    "contract_version": {
      "const": "1.0"
    },
    "report_id": {
      "type": "string"
    },
    "case_id": {
      "type": "string"
    },
    "medical_record_id": {
      "type": "string"
    },
    "generated_at": {
      "type": "string",
      "format": "date-time"
    },
    "audience": {
      "type": "string",
      "enum": [
        "USER",
        "SYSTEM"
      ]
    },
    "article": {
      "type": "object"
    },
    "summary": {
      "type": "string"
    },
    "diagnosis": {
      "type": "object"
    },
    "recommendation": {
      "type": "object"
    },
    "monitoring": {
      "type": "object"
    },
    "sections": {
      "type": "array",
      "items": {
        "type": "object"
      }
    },
    "trace": {
      "type": "object"
    }
  }
}

```


---

## SOURCE: contracts/SIMS_DOCTOR_REFERRAL_V1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://sims.local/contracts/SIMS_DOCTOR_REFERRAL_V1.schema.json",
  "title": "SIMS_DOCTOR_REFERRAL_V1",
  "type": "object",
  "required": [
    "referral_id",
    "case_id",
    "medical_record_id",
    "diagnosis_id",
    "treatment_recommendation_id",
    "target",
    "priority",
    "article",
    "clinical_summary",
    "issued_at",
    "contract_version",
    "fingerprint"
  ],
  "properties": {
    "referral_id": {
      "type": "string"
    },
    "case_id": {
      "type": "string"
    },
    "medical_record_id": {
      "type": "string"
    },
    "diagnosis_id": {
      "type": "string"
    },
    "treatment_recommendation_id": {
      "type": "string"
    },
    "target": {
      "type": "string",
      "enum": [
        "WRITER",
        "CREATOR",
        "MERGE",
        "OBSERVATION",
        "NOINDEX_REVIEW",
        "DELETE_REVIEW"
      ]
    },
    "priority": {
      "type": "string",
      "enum": [
        "LOW",
        "MEDIUM",
        "HIGH"
      ]
    },
    "article": {
      "type": "object"
    },
    "clinical_summary": {
      "type": "object"
    },
    "issued_at": {
      "type": "string",
      "format": "date-time"
    },
    "contract_version": {
      "const": "1.0"
    },
    "fingerprint": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    }
  }
}

```


---

## SOURCE: shared/contracts/doctor/doctor-diagnosis-request-v1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "envelope",
    "payload"
  ],
  "properties": {
    "envelope": {
      "type": "object",
      "required": [
        "platform",
        "platform_version",
        "contract_name",
        "contract_version",
        "message_type",
        "message_id",
        "correlation_id",
        "created_at",
        "source_product",
        "target_product",
        "shared_version"
      ],
      "properties": {
        "platform": {
          "const": "SIMS_EDITORIAL_PLATFORM"
        },
        "platform_version": {
          "type": "string"
        },
        "contract_name": {
          "const": "SIMS_DOCTOR_DIAGNOSIS_REQUEST_V1"
        },
        "contract_version": {
          "type": "string"
        },
        "message_type": {
          "enum": [
            "REQUEST",
            "RESULT",
            "EVENT",
            "ERROR",
            "ACKNOWLEDGEMENT"
          ]
        },
        "message_id": {
          "type": "string",
          "minLength": 1
        },
        "correlation_id": {
          "type": "string",
          "minLength": 1
        },
        "causation_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "created_at": {
          "type": "string"
        },
        "source_product": {
          "type": "object"
        },
        "target_product": {
          "type": "object"
        },
        "shared_version": {
          "type": "string"
        },
        "locale": {
          "type": "string"
        },
        "timezone": {
          "type": "string"
        }
      }
    },
    "payload": {
      "type": "object",
      "required": [
        "case",
        "objective",
        "workflow_context",
        "evidence"
      ],
      "additionalProperties": true,
      "properties": {
        "case": {},
        "objective": {},
        "workflow_context": {},
        "evidence": {}
      }
    }
  },
  "title": "SIMS_DOCTOR_DIAGNOSIS_REQUEST_V1"
}

```


---

## SOURCE: shared/contracts/doctor/doctor-diagnosis-result-v1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "envelope",
    "payload"
  ],
  "properties": {
    "envelope": {
      "type": "object",
      "required": [
        "platform",
        "platform_version",
        "contract_name",
        "contract_version",
        "message_type",
        "message_id",
        "correlation_id",
        "created_at",
        "source_product",
        "target_product",
        "shared_version"
      ],
      "properties": {
        "platform": {
          "const": "SIMS_EDITORIAL_PLATFORM"
        },
        "platform_version": {
          "type": "string"
        },
        "contract_name": {
          "const": "SIMS_DOCTOR_DIAGNOSIS_RESULT_V1"
        },
        "contract_version": {
          "type": "string"
        },
        "message_type": {
          "enum": [
            "REQUEST",
            "RESULT",
            "EVENT",
            "ERROR",
            "ACKNOWLEDGEMENT"
          ]
        },
        "message_id": {
          "type": "string",
          "minLength": 1
        },
        "correlation_id": {
          "type": "string",
          "minLength": 1
        },
        "causation_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "created_at": {
          "type": "string"
        },
        "source_product": {
          "type": "object"
        },
        "target_product": {
          "type": "object"
        },
        "shared_version": {
          "type": "string"
        },
        "locale": {
          "type": "string"
        },
        "timezone": {
          "type": "string"
        }
      }
    },
    "payload": {
      "type": "object",
      "required": [
        "case_id",
        "diagnosis_id",
        "result_status",
        "diagnosis",
        "treatment_required",
        "referrals"
      ],
      "additionalProperties": true,
      "properties": {
        "case_id": {},
        "diagnosis_id": {},
        "result_status": {},
        "diagnosis": {},
        "treatment_required": {},
        "referrals": {}
      }
    }
  },
  "title": "SIMS_DOCTOR_DIAGNOSIS_RESULT_V1"
}

```


---

## SOURCE: shared/enums/diagnosis-code.json

```json
{
  "name": "diagnosis-code",
  "version": "1.0",
  "values": [
    "POSITION_OPPORTUNITY",
    "CTR_UNDERPERFORMANCE",
    "INTENT_MISMATCH",
    "INTENT_DRIFT",
    "LOW_SAMPLE",
    "EVIDENCE_INSUFFICIENT",
    "THIN_CONTENT",
    "INCOMPLETE_ANSWER",
    "CANNIBALIZATION_CONFIRMED",
    "CANNIBALIZATION_SUSPECTED",
    "LONG_TERM_DECLINE",
    "POST_TREATMENT_DECLINE",
    "WINNER_QUERY_LOSS",
    "TREATMENT_NO_EFFECT",
    "NEW_ARTICLE_REQUIRED",
    "TOPIC_GAP",
    "INTENT_SPLIT_REQUIRED",
    "MERGE_REQUIRED",
    "REDIRECT_CANDIDATE",
    "NOINDEX_CANDIDATE",
    "DELETE_CANDIDATE",
    "ROLE_SEPARATION_REQUIRED",
    "HEALTHY",
    "TREATMENT_NOT_REQUIRED"
  ]
}

```


---

## SOURCE: shared/enums/result-status.json

```json
{
  "name": "result-status",
  "version": "1.0",
  "values": [
    "SUCCESS",
    "PARTIAL_SUCCESS",
    "NO_ACTION",
    "USER_DECISION_REQUIRED",
    "EVIDENCE_INSUFFICIENT",
    "NOT_APPLICABLE",
    "VALIDATION_FAILED",
    "FAILED"
  ]
}

```


---

## SOURCE: shared/enums/treatment-type.json

```json
{
  "name": "treatment-type",
  "version": "1.0",
  "values": [
    "WRITER_PARTIAL_REWRITE",
    "WRITER_FULL_REWRITE",
    "WRITER_CTR_OPTIMIZATION",
    "WRITER_CONTENT_UPDATE",
    "WRITER_INTENT_ALIGNMENT",
    "WRITER_INTERNAL_LINK",
    "CREATOR_NEW_ARTICLE",
    "CREATOR_INTENT_SPLIT",
    "CREATOR_TOPIC_GAP",
    "CREATOR_SUPPORTING_ARTICLE",
    "MERGE_CONTENT_CONSOLIDATION",
    "MERGE_CANNIBALIZATION_RESOLUTION",
    "MERGE_ROLE_SEPARATION",
    "MERGE_REDIRECT_PLAN",
    "MERGE_NOINDEX_PLAN",
    "MERGE_DELETE_PLAN",
    "MONITOR_ONLY",
    "NO_ACTION",
    "USER_DECISION"
  ]
}

```


## Optional keyword strategy metadata (v2.0.5)
The top-level `keyword_strategy_assessment` is optional in `SIMS_DOCTOR_CASE_RESULT_V2`; it does not replace diagnosis, treatment_plan, referral, workflow or workflow_handoff and does not authorize a change to GSC observations. Unknown optional fields may be retained in Manager Doctor result JSON, but downstream specialist interpretation must not be assumed without its own contract audit.


## V2 JSON contract guard — v2.0.5
- Managerへ登録する通常診断の最終JSONは `SIMS_DOCTOR_CASE_RESULT_V2.schema.json` に従い、少なくとも `format`, `contract_version`, `case_id`, `article_id`, `diagnosis`, `treatment_plan`, `referral`, `workflow`, `reexamination` を必ず含める。`referral` は `required`, `destination`, `allowed_scope`, `blocked_scope` を含み、`workflow` は `workflow_locked` と `return_to: SIMS_BLOG_MANAGER` を含める。
- `keyword_strategy_assessment` は任意で、存在する場合は **次の7項目を必須**とする: `decision` (MAINTAIN / RETARGET / ROLE_SEPARATION / DEFER), `original_target_query` (文字列またはnull), `observed_main_query` (文字列またはnull), `improvement_target_query` (文字列またはnull), `article_role` (文字列またはnull), `reason` (空でない文字列), `confidence` (CONFIRMED / PROVISIONAL / INSUFFICIENT)。任意で `evidence_gaps` (文字列配列) を付けられる。
- **禁止**: このオブジェクト内で `confidence: 0.8` のような数値、`original_target` や `gsc_observed_main_query` や `doctor_improvement_target` の入れ子オブジェクト、`role_assignments` 等の未定義キーを出さない。数値確信度や詳細根拠は従来の `diagnosis` や説明文に置く。
- GSC観測値を推測した当初狙い語で置き換えない。観測クエリの出典が曖昧なら `observed_main_query: null` とし `evidence_gaps` に記す。記事の役割から戦略を確定できる場合、当初狙い語がnullでもROLE_SEPARATIONを許容する。
- **検証専用モード**: 既存Caseの判定確認を求められ、Managerへ登録しない場合、通常診断JSONの代わりに `keyword_strategy_assessment` 単独のJSONを「検証用・登録不可」と明記して出す。既存の `workflow_handoff.next_action` をコピーした登録可能そうなV2 JSONを作らない。既存の処置を再実行・再登録しない。
- 通常診断と情報更新専用受付の契約は従来どおり維持し、情報更新専用受付にはこの戦略評価を適用しない。
