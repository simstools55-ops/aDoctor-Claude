# 07_SHARED_KNOWLEDGE.md
この文書は元Repositoryの必要な規則・契約を原文のまま集約したものです。章見出しは元のファイルパスです。


---

## SOURCE: shared/CASE_LIFECYCLE_V1.md

```markdown
# SIMS Editorial Platform Case Lifecycle v1.0

## Principle

A Case represents one diagnosis-treatment-measurement-re-examination cycle. An article may have multiple Cases over time.

## Identifier format

```text
CASE-YYYYMMDD-ARTICLEID-NNN
```

Example:

```text
CASE-20260805-A999999-001
```

SBM issues the CaseID before sending a Doctor request.

## Records linked to a Case

- SiteID and ArticleID
- Doctor diagnosis request
- Doctor diagnosis result
- Treatment Plan and Referral
- Writer treatment request
- Writer treatment result
- User publication decision
- Publication confirmation
- Improvement History ID
- 7/14/21/28-day measurements
- Doctor re-examination result
- Completion or cancellation reason

## Standard transitions

### Monitor only

```text
DOCTOR_DIAGNOSIS_PENDING
-> DOCTOR_DIAGNOSED
-> MONITORING
-> REEXAMINATION_PENDING
-> COMPLETED
```

### Writer treatment

```text
DOCTOR_DIAGNOSIS_PENDING
-> DOCTOR_DIAGNOSED
-> TREATMENT_REVIEW_PENDING
-> WRITER_REQUEST_READY
-> WRITER_IN_PROGRESS
-> TREATMENT_RESULT_RECEIVED
-> PUBLICATION_PENDING
-> MONITORING
-> REEXAMINATION_PENDING
-> COMPLETED
```

### Existing SBM monitoring lock

```text
DOCTOR_DIAGNOSIS_PENDING
-> DOCTOR_DIAGNOSED
-> WORKFLOW_LOCKED
-> TREATMENT_REVIEW_PENDING
```

The transition out of `WORKFLOW_LOCKED` is performed by SBM after the active monitoring condition ends or the user explicitly resolves it.

## State ownership

- SBM stores and changes authoritative Case state.
- Doctor recommends actions and re-examination conditions.
- Writer reports treatment progress and result status.
- User approval and publication events are recorded by SBM.

## Idempotency

A repeated message with the same `message_id`, `diagnosis_id`, or `treatment_result_id` must not create a duplicate Case event.

```


---

## SOURCE: shared/CASE_TREATMENT_TERMINOLOGY.md

```markdown
# Case and Treatment Terminology

- **Case**: One diagnosis-treatment-measurement-re-examination cycle concerning one article or an explicitly defined article group.
- **Treatment**: One concrete editorial action performed within a Case.
- **Referral**: Doctor's structured recommendation returned to SBM describing the destination, objective, allowed scope, blocked scope, and review conditions.
- **Treatment Plan**: Doctor's recommendation about whether treatment is needed, its level, priority, expected impact, risk, and review timing.
- **CaseID**: Issued and owned by SBM before diagnosis is requested.
- **DiagnosisID**: Issued by Doctor for each diagnosis result and stored under the SBM Case.
- **Treatment Request ID**: Issued by SBM when a treatment request is created.
- **Treatment Result ID**: Issued by Writer, Creator, or Merge for the returned result and stored by SBM.

## Product roles

- SBM owns Case state, routing, records, publication management, measurement, and re-examination scheduling.
- Doctor diagnoses, prepares the Treatment Plan and Referral, and performs re-examination when requested.
- Writer treats existing articles.
- Creator creates new articles.
- Merge will perform article consolidation when implemented.

Doctor does not directly dispatch a Treatment to a specialist product. SBM converts an accepted Referral into a specialist request.

`DELETE`, `NOINDEX`, `ARCHIVE`, and `MERGE` are Treatments or disposition options, not diagnoses.

```


---

## SOURCE: shared/INTERFACE_CONTRACTS_V2.md

```markdown
# SIMS Editorial Platform Interface Contract Registry v2.0.0

## 1. Purpose

This registry defines the canonical minimum workflow connecting SIMS-Blog-Manager, SIMS Article Doctor, and SIMS Writer.

The platform orchestration rule is:

```text
SBM -> Doctor -> SBM -> Writer -> SBM -> measurement -> Doctor re-examination
```

SIMS-Blog-Manager is the system of record for Case state, workflow history, requests, results, publication status, and performance measurement.

## 2. Canonical contracts

| Contract | Source | Target | Responsibility |
|---|---|---|---|
| `SIMS_DOCTOR_SINGLE_CASE_REQUEST_V2` | SBM | Doctor | Individual diagnosis request and Evidence Package |
| `SIMS_DOCTOR_CASE_RESULT_V2` | Doctor | SBM | Diagnosis, Treatment Plan, Referral, and re-examination conditions |
| `SIMS_WRITER_TREATMENT_REQUEST_V1` | SBM | Writer | Doctor-referred treatment request with allowed and blocked scope |
| `SIMS_WRITER_TREATMENT_RESULT_V1` | Writer | SBM | Treatment result, referral compliance, and publication readiness |
| `SIMS_DOCTOR_REEXAMINATION_REQUEST_V1` | SBM | Doctor | Post-treatment re-examination evidence |

## 3. Ownership rules

- `site_id` and `article_id` are issued and owned by SBM.
- `case_id` is issued and owned by SBM.
- `diagnosis_id` is issued by Doctor and stored by SBM.
- `treatment_request_id` is issued by SBM.
- `treatment_result_id` is issued by the treatment product and stored by SBM.
- `improvement_history_id` remains owned by SBM.
- Every sender issues a unique `message_id`; duplicate messages are handled idempotently.

## 4. Routing rules

- Doctor never directly invokes Writer, Creator, or Merge.
- Doctor returns a diagnosis, Treatment Plan, and Referral to SBM.
- SBM validates the Referral, checks Workflow Lock, and creates the treatment request.
- Writer returns the treatment result to SBM, not to Doctor.
- Doctor receives a new request only when SBM requests diagnosis or re-examination.
- Creator and Merge will use the same SBM-mediated routing model when connected.

## 5. Case lifecycle source of truth

SBM is the only source of truth for Case lifecycle state.

Canonical minimum states:

```text
DOCTOR_DIAGNOSIS_PENDING
DOCTOR_DIAGNOSED
TREATMENT_REVIEW_PENDING
WRITER_REQUEST_READY
WRITER_IN_PROGRESS
TREATMENT_RESULT_RECEIVED
PUBLICATION_PENDING
MONITORING
REEXAMINATION_PENDING
COMPLETED
```

Exception states:

```text
WORKFLOW_LOCKED
USER_DECISION_REQUIRED
EVIDENCE_INSUFFICIENT
TREATMENT_FAILED
PUBLICATION_VERIFICATION_REQUIRED
CANCELLED
```

Doctor and Writer may report facts relevant to state transitions, but they do not authoritatively change the Case state.

## 6. Treatment scope rules

A Doctor Referral may define:

- `allowed_scope`
- `blocked_scope`
- `treatment_level`
- `objective`
- `reason_codes`
- `priority`
- `review_after_days`

Writer must not modify a blocked scope. A scope conflict or violation is returned to SBM as `USER_DECISION_REQUIRED` or `BLOCKED` and must not be silently normalized.


## 6A. Algorithm and Treatment Strategy extensions

Doctor case results may include additive, backward-compatible fields for:

- Algorithm Impact Assessment
- Evidence Confidence metadata
- Treatment Strategy: `WAIT`, `LIGHT_FIX`, `NORMAL_REWRITE`, `FULL_REWRITE`
- WAIT observation/re-examination plan
- User-facing ToDo
- Evidence-based guidance / reassurance

Algorithm information is Evidence, not a standalone diagnosis. Doctor must not route treatment directly from an update-date match. Site-wide impact evidence may be supplied by SBM as an aggregated Evidence Package component.

These extensions do not change the canonical routing path: `Doctor -> SBM -> specialist`.

## 7. Workflow Lock

- Doctor may diagnose while an SBM monitoring lock exists.
- Doctor cannot release, replace, or bypass an SBM lock.
- SBM decides whether a treatment request may be generated.
- A Referral received during a lock is stored and held until SBM permits the next transition.

## 8. Compatibility

`doctor/INTERFACE_CONTRACTS_V1.md` is retained only for historical compatibility.

The following V1 routing is deprecated:

```text
Doctor -> Writer
Writer -> Doctor
Doctor-owned case_id
```

New implementations must use this V2 registry. Existing V1 messages may be read by adapters, but must not be emitted as the preferred platform path.

```


---

## SOURCE: shared/PLATFORM_INTEGRATION_POLICY.md

```markdown
# Integration Policy

## Source of truth and snapshots

This repository is the source of truth for shared editorial knowledge and cross-product platform contracts. Each product includes a validated snapshot of a specific released version.

## Platform orchestration

- SIMS-Blog-Manager is the workflow orchestrator and system of record.
- SBM issues CaseID and routes diagnosis and treatment requests.
- Doctor returns diagnosis, Treatment Plan, and Referral to SBM.
- Writer, Creator, and Merge return results to SBM.
- Specialist products do not directly mutate another product's records.

## Update procedure

1. Change shared knowledge or platform contracts in this repository.
2. Run shared repository tests.
3. Update VERSION, CHANGELOG, registries, and release notes.
4. Create a release tag.
5. Import a scoped snapshot into each affected product.
6. Run product-specific regression tests.
7. Release the affected products in dependency order.

For the minimum treatment loop, the preferred release order is:

```text
Shared -> Doctor -> SBM -> Writer -> integration test
```

## Prohibited practices

- Editing the same shared rule independently in Writer and Article Creator
- Automatically tracking unreleased Shared content from a product
- Skipping product regression tests after a Shared change
- Doctor directly dispatching Writer/Creator/Merge work
- Writer/Creator/Merge returning the official treatment result only to Doctor
- A specialist product authoritatively changing SBM Case state

```


---

## SOURCE: shared/TREATMENT_ROUTING_V1.md

```markdown
# Doctor Treatment Routing v1

- Existing single-article change: Writer.
- Independent new intent or topic gap: Creator.
- Multi-URL competition, duplication, consolidation, redirect/noindex/delete planning: Merge.
- Low sample, recent publication/treatment, unresolved seasonality, or indexing transition: Monitor.
- Healthy, aligned, or risk-exceeds-benefit: No Action.
- Post-treatment decline requires Doctor re-examination before another Writer treatment.
- Referrals are recommendations; SBM validates Workflow Lock, evidence, dependencies, user approval, and compatibility before issuing a request.

## Treatment Strategy layer

Doctor may attach one platform-visible Treatment Strategy above the existing treatment level/scope.

- `WAIT`: do not initiate material treatment yet; define observation targets and re-examination timing.
- `LIGHT_FIX`: limited, low-risk correction such as factual freshness, title/meta/FAQ or narrowly scoped alignment.
- `NORMAL_REWRITE`: ordinary Writer-level treatment within an SBM-issued allowed scope.
- `FULL_REWRITE`: broad restructuring or extensive rewrite is justified by integrated evidence.

Treatment Strategy does not bypass Routing. Doctor returns it to SBM; SBM decides whether and when to issue Writer, Creator, or Merge work.

`WAIT` is an active monitoring strategy, not a synonym for no evidence review or indefinite inaction.


```


---

## SOURCE: shared/presentation/HUMAN_EXPERIENCE_ARCHITECTURE_V1.md

```markdown
# SIMS Human Experience Architecture v1

## Purpose
SIMS Editorial Platformは、機械が判断するための情報と、利用者が作業するための情報を分離する。

## Three layers
1. Machine Layer: Contract、Evidence、Confidence、Routing、Scope、Internal Flags、JSONを保持する。
2. Presentation Layer: Machine Layerの情報から利用者に必要な内容だけを選択・整形する。
3. Human Layer: 利用者が迷わず作業できる完成形を提示する。

## Platform scope
本ArchitectureはSBM、Doctor、Writer、Creator、Mergeおよび各Claude実装の共通方針である。

## Adoption policy
- RC3先行適用: Doctor / SBM / Writer
- Specification-only adoption: Creator / Merge
- Creator / Mergeは後続フェーズでPresentation実装を追加する。今回のShared更新だけを理由に既存出力を壊してはならない。

## Core rule
機械向け情報をそのままHuman Layerへ露出してはならない。Human Layerは「利用者が次の操作を実行できること」を最優先する。

```


---

## SOURCE: shared/presentation/HUMAN_OUTPUT_POLICY_V1.md

```markdown
# SIMS Human Output Policy v1

## Show to users
利用者向け出力は、作業に必要な情報を優先する。
- 公開可否 / 実行可否
- 今回やること
- Before / After（変更作業がある場合）
- 理由
- 期待効果
- 注意事項
- 次の作業
- 再診・測定予定（必要な場合）

## Do not expose by default
次の情報はMachine Layerに保持し、利用者への通常説明には出さない。
- Contract名・schema詳細
- allowed_scope / blocked_scope等の内部フィールド名
- Routing / handoff_mode
- Internal Flags
- Evidence IDの羅列
- Confidenceの内部計算過程
- Adapterのフォールバック処理
- 「空配列なので別フィールドを正本とみなす」等の内部整合処理

必要な意味は自然な日本語へ変換する。
例: `FULL_REWRITE`をそのまま説明するのではなく「今回は全面リライトを行いません」と提示する。

## Human usability requirement
正しいMachine JSONが存在するだけでは品質合格としない。利用者がHuman Outputだけで次の作業を開始できることを必要条件とする。

```


---

## SOURCE: shared/presentation/HUMAN_USABILITY_GATE_V1.md

```markdown
# SIMS Human Usability Gate v1

リリース候補のHuman Outputは次を満たすこと。

1. 利用者が出力を読んで次の作業を開始できる。
2. 既存記事の変更はBefore / Afterで特定できる。
3. Afterは原則コピー可能な完成形である。
4. 理由と期待効果が確認できる。
5. Contract / Routing / Scope等の内部用語が通常表示されない。
6. 「今回やること」と「今回やらないこと」が混同されない。
7. JSONが必要な場合は人間向け説明の後に置く。

Doctor Referral経路も通常Writer経路と同じGateを通過しなければならない。

```


---

## SOURCE: shared/presentation/MACHINE_OUTPUT_POLICY_V1.md

```markdown
# SIMS Machine Output Policy v1

## Preserve machine data
AI・製品間通信では以下を保持する。
- Contract / Version
- Evidence / Evidence Confidence
- Treatment Strategy
- allowed_scope / blocked_scope
- actions_permitted / actions_prohibited
- Routing / Case correlation
- Internal validation results

Presentationの簡素化を理由にMachine情報を削除してはならない。

## Adapter responsibility
Machine Contractのフィールドが製品間で異なる場合、Adapterが明示的に正規化する。
利用者向けPresentationで補完することでContract不整合を隠してはならない。

## Doctor to SBM to specialist
Doctorの結果はSBMへ返す。SBMは専門家向け依頼へ正規化し、Writer / Creator / Mergeへ渡す。
専門家はMachine情報を守りつつHuman OutputをPresentation Standardに従って生成する。

```


---

## SOURCE: shared/presentation/PRESENTATION_STANDARD_V1.md

```markdown
# SIMS Presentation Standard v1

## Standard order
利用者向けの主要出力は、原則として次の順序で提示する。

1. 公開可否または実行可否
2. 今回やること
3. 変更内容または成果物
4. 理由と期待効果
5. 今回やらないこと / 注意事項（必要な場合のみ）
6. 次の作業
7. Machine JSON（利用者の運用上必要な場合のみ、最後に配置）

## Existing article treatment
Writerが変更を提示する場合、各変更は以下を満たす。
- target
- Before
- After
- reason
- expected_effect

Afterは、利用者が原則そのままコピーして記事へ反映できる完成形とする。
新規追加でBeforeが存在しない場合も省略せず「（該当箇所なし・新規追加）」等と明示する。

## No simplification for referral mode
DOCTOR_REFERRAL_TREATMENT等の経路であっても、通常Writerより利用者向け表示品質を下げてはならない。
治療範囲が狭いことは、Before/Afterや理由の省略理由にならない。

## Product-specific projection
- Doctor: 診断要約 / 今回やること / 今回やらないこと / 再診
- Writer: 公開可否 / Before / After / 理由 / 期待効果
- Creator: 記事作成結果 / 公開前確認 / 完成記事
- Merge: 統合判断 / Primary / Preservation / 作業順序 / 注意事項
- SBM: 次に実行すべき操作と状態を人間向けに表示

```
