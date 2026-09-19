# SIMS Request Protocol v1 — aDoctor profile

## Purpose
SIMS ManagerからaDoctorへ渡された正規依頼文だけを通常運用で受け付けるための運用プロトコル。ライセンス認証・暗号署名ではない。

## Envelope
```text
[SIMS_REQUEST]
PROTOCOL=SIMS-A/1
SOURCE=SIMS_MANAGER
EDITION=FULL
TARGET=ADOCTOR
REQUEST_TYPE=ARTICLE_DIAGNOSIS
REQUEST_ID=<required>
CASE_ID=<required>
SITE_ID=<required>
ARTICLE_ID=<required>
[/SIMS_REQUEST]
```

## Validation
すべての固定値と必須IDを検査し、本文/Evidence側のIDと矛盾する場合は拒否する。拒否時は診断、Web調査、JSON生成を行わない。

## Boundary
この方式はClaude Project Instructionsによる運用ゲートであり、Manager発行元を暗号学的に証明しない。Editionの正式な利用権管理はSIMS Manager / License Center側の責務である。
