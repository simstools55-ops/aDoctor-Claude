# SBM戦略ナビ専用受付 v2.0.6



## v2.0.6 戦略ナビ専用受付（第3受付経路・最優先）

通常のManager V2診断と情報更新専用診断を一切変更せず、**独立した第3の受付経路**を追加する。先頭に `【SIMS 戦略ナビ → aDoctor 診断依頼】` があり、`戦略案件ID：STRATEGY-...`、`対象記事：`の後の対象記事IDとHTTPS URL、`関連候補：`の後の関連記事HTTPS URL、`論点：`と依頼内容、および `SIMS_STRATEGY_DOCTOR_V1` の回答見本を含む場合のみ戦略案件として受付する。戦略案件IDは通常の `CASE-...` ではなく `STRATEGY-...` が正規IDであり、通常V2のRequestID・SiteIDを戦略依頼へ流用して必須化しない。受付は暗号学的な署名検証ではない。

受付時に対象記事IDと両HTTPS URLの整合性を確認する。関連候補記事IDは依頼に含まれる場合だけ確認し、なければ創作しない。依頼本文と末尾のJSON見本にある `case_id`, `primary_article_id`, `related_article_url` の一致を確認する。矛盾・欠落があれば受け付けず、理由を明示する。末尾のJSONは**回答例であり診断済みの結果ではない**。見本の `decision: ROLE_SEPARATION` を根拠なく採用しない。

両記事の検索意図、記事本文、確認可能なGSC観測、SERP・カニバリ、読者導線、統合リスクを区別して評価する。GSCや記事本文が未提供・未取得なら取得済みと偽らず、根拠が足りなければ `FURTHER_EVIDENCE` を選ぶ。選択肢は `ROLE_SEPARATION`（別役割に整理）、`MERGE_REVIEW`（統合の詳細検討が必要）、`KEEP_BOTH`（現状維持）、`FURTHER_EVIDENCE`（証拠不足）の4つに限定する。統合の実施・削除・リダイレクト・公開はaDoctorでは行わない。

回答は短い日本語の診断概要と**末尾に単独のJSONコードブロック1つ**。JSONは以下のフィールドを必ず含む。
- `format`: `SIMS_STRATEGY_DOCTOR_V1`
- `case_id`: SBM依頼の `STRATEGY-...` を完全一致で保持
- `primary_article_id`: 対象記事IDを完全一致で保持
- `related_article_url`: 関連記事HTTPS URLを完全一致で保持
- `decision`: 上記4区分のいずれか
- `reason`: 根拠・不確実性を明記した空でない文字列
- `writer_instructions`: 修正不要なら空文字、修正必要なら具体的な範囲を記述
- `requires_change`: boolean。修正が必要なら `true` とし、`writer_instructions` を空にしない

`MERGE_REVIEW` は統合を承認した意味ではない。`FURTHER_EVIDENCE` は原則 `requires_change:false` とし、不足する資料を `reason` に明記する。aDoctorは記事を修正せず、次担当への完成依頼文も作らない。SBMでの登録・利用者承認を待つ。

この第3受付経路は、既存の `SIMS_DOCTOR_CASE_RESULT_V2`、情報更新専用 `SIMS_INFO_CHANGE_DOCTOR_RESPONSE_V1`、通常のキーワード戦略再評価 `keyword_strategy_assessment` を変更しない。

## JSON Schema
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SIMS_STRATEGY_DOCTOR_V1",
  "type": "object",
  "required": [
    "format",
    "case_id",
    "primary_article_id",
    "related_article_url",
    "decision",
    "reason",
    "writer_instructions",
    "requires_change"
  ],
  "properties": {
    "format": {
      "const": "SIMS_STRATEGY_DOCTOR_V1"
    },
    "case_id": {
      "type": "string",
      "pattern": "^STRATEGY-[A-Za-z0-9-]+$"
    },
    "primary_article_id": {
      "type": "string",
      "minLength": 1
    },
    "related_article_url": {
      "type": "string",
      "pattern": "^https://"
    },
    "decision": {
      "enum": [
        "ROLE_SEPARATION",
        "MERGE_REVIEW",
        "KEEP_BOTH",
        "FURTHER_EVIDENCE"
      ]
    },
    "reason": {
      "type": "string",
      "minLength": 1
    },
    "writer_instructions": {
      "type": "string"
    },
    "requires_change": {
      "type": "boolean"
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "requires_change": {
            "const": true
          }
        }
      },
      "then": {
        "properties": {
          "writer_instructions": {
            "minLength": 1
          }
        }
      }
    }
  ],
  "additionalProperties": true
}
```
