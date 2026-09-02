# Natas 12/13 RCE Isolation Audit

`scripts/audit_natas_rce_isolation.py` is an authorized local-container audit
for the intentional Natas 12 and 13 upload RCE lessons. It builds the target,
starts one disposable container with generated `AUDIT_ONLY_*` secrets, and
uses each level's real upload vulnerability to execute a minimal PHP proof in
the assigned Apache/MPM-ITK request context.

Run it only on an authorized Docker host:

```bash
python3 scripts/audit_natas_rce_isolation.py
```

The proof returns booleans only. It does not emit secret values, database
credentials, capability masks, process environments, or host information. The
container is removed whether the audit passes or fails.

The audit fails if either RCE context can access:

- a nonadjacent webpass file;
- a nonadjacent runtime-written secret include or the scrubbed
  `LEVEL_SECRETS` environment variable;
- MariaDB with the level-14 application credentials;
- Apache `CAP_SETUID` or `CAP_SETGID`, which could cross per-vhost identities;
- a Docker socket, or common orchestrator secret material.

An `NATAS_RCE_ISOLATION_FAILED` result identifies only the level and failed
boundary. Do not extend the proof into interactive shells, data collection, or
host-control attempts. Preserve the result for the orchestrator: target
hardening or curriculum changes are deliberately outside this audit.
