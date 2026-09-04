# SIMS aDoctor Claude v1.5.1

Release status: repository-ready / test-showcase baseline.

- LOW_SAMPLE + structurally hard SERP now triggers `CLUSTER_OPPORTUNITY_CHECK` before low-priority closure.
- Added existing-content support and aCreator opportunity routes.
- New articles must have independent search intent/user value and pass cannibalization/SERP checks; thin link-only satellites are prohibited.
- Enforced workflow consistency: normal-close outcomes cannot simultaneously request WAIT/MONITOR.
- Distribution metadata and release-facing documentation synchronized to v1.5.1.
- No Personal Knowledge user data is bundled.
