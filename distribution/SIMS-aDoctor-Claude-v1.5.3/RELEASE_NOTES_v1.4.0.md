# SIMS Article Doctor Claude v1.4.0

- Manual Claude診断結果に `knowledge_candidates` を追加。
- SITE候補はSBMの `personal_knowledge_site_id` に束縛。
- `case_id` を `confirmation_event_id` として再貼付の二重確認を防止。
- 一時指標・SERPスナップショット・一般ルールはPersonal Knowledge候補にしない。
- 従来の手動コピー＆ペースト運用を維持し、API連携は追加しない。
