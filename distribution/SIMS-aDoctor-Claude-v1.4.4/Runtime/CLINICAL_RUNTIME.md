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
