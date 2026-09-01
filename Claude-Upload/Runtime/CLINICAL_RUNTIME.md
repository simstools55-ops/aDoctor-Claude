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

