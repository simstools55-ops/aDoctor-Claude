# 04_INFORMATION_UPDATE.md
この文書は元Repositoryの必要な規則・契約を原文のまま集約したものです。章見出しは元のファイルパスです。

一次情報を調査し、未検証事項を断定しない。証拠不足ではNEEDS_EVIDENCE等の正規状態を返す。利用者に資料の提出を標準必須条件として強制しない。


---

## SOURCE: contracts/SIMS_INFO_CHANGE_DOCTOR_RESPONSE_V1.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SIMS_INFO_CHANGE_DOCTOR_RESPONSE_V1",
  "type": "object",
  "required": [
    "format",
    "request_id",
    "article_id",
    "article_url",
    "diagnosis_status",
    "findings"
  ],
  "properties": {
    "format": {
      "const": "SIMS_INFO_CHANGE_DOCTOR_RESPONSE_V1"
    },
    "request_id": {
      "type": "string",
      "minLength": 1
    },
    "article_id": {
      "type": "string",
      "minLength": 1
    },
    "article_url": {
      "type": "string",
      "format": "uri",
      "pattern": "^https://"
    },
    "diagnosis_status": {
      "enum": [
        "READY",
        "NO_CHANGE_NEEDED",
        "NEEDS_EVIDENCE"
      ]
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "current_text",
          "proposed_change",
          "evidence_url"
        ],
        "properties": {
          "current_text": {
            "type": "string",
            "minLength": 1
          },
          "proposed_change": {
            "type": "string",
            "minLength": 1
          },
          "evidence_url": {
            "type": "string",
            "pattern": "^https://"
          }
        },
        "additionalProperties": true
      }
    }
  },
  "additionalProperties": true
}
```
