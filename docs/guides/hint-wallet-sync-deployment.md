# Hint-wallet signed sync deployment

## Secret provisioning

The Wargames deployment client must receive `HINT_WALLET_SYNC_SECRET` from a protected deployment-secret source. Its value must exactly match the Engine platform secret mounted at `/run/secrets/hint_wallet_sync_secret`. It is a high-entropy shared signing secret, not a challenge value or participant secret.

Never commit, print, paste into tickets, store in challenge YAML, or enable shell tracing around it. Use the platform secret store or CI secret manager. An operator can create a Docker secret from stdin with a restrictive umask; this pipeline does not echo the generated value:

```bash
umask 077
openssl rand -base64 48 | docker secret create hint_wallet_sync_secret -
```

Inject the matching value only into the short-lived Wargames deploy job. Do not use a tracked `.env` file. Disable `set -x` and debug HTTP logging, and redact authorization headers/signatures from job logs.

## Revision and atomicity

Every release sets `HINT_WALLET_REVISION` to a positive decimal CI/release number, normally the monotonically increasing pipeline run number. The revision is signed with the catalog. Engine accepts a strictly higher revision. It may accept an exact retry only when the signed catalog digest is identical; this is idempotent. A lower revision is rejected and cannot roll back active policy. To correct a release, publish the desired catalog as a new higher revision.

One signed payload contains Bandit, Krypton, and Natas. Engine validates the signature, revision, schema, all three track counts, tier costs, and cross-track references before changing state, then commits all tracks in one database transaction. It must never leave a one- or two-track catalog active.

Expected fail-closed responses are `401 invalid_signature`, `400 invalid_schema`, `400 incomplete_tracks`, `409 stale_revision`, `409 revision_digest_conflict`, `422 catalog_validation_failed`, and `503 secret_or_database_unavailable`. Keep the last accepted catalog active, mark the release failed, and investigate; do not bypass validation or manually edit a single track.

## Coordinated rotation

Create a new versioned platform secret. Configure Engine to accept old and new secret identifiers for a short overlap, deploy Engine, update the protected Wargames CI secret, publish and verify one higher-revision three-track sync, then remove the old secret and verify it is rejected. Never rotate only one side without this overlap plan. Audit only secret IDs, revision, catalog digest, operator, timestamp, and result, never the secret/signature/payload secret data.

## TLS and offline behavior

Use the Engine internal HTTPS endpoint with hostname and certificate validation enabled. Trust or pin the internal CA through deployment configuration; do not use an insecure-TLS override for wallet sync. This is a controlled deployment-time call. Once accepted, hint rendering and unlocks use the local catalog: they have no runtime internet dependency and never fetch remote documentation.

## Release acceptance

1. Verify the Wargames job secret and Engine mounted secret match without printing either value; verify logs and CI artifacts contain neither.
2. Submit a valid higher revision and confirm all three tracks change together.
3. Retry the same payload and confirm idempotence; submit a lower revision and a same-revision/different-digest payload and confirm rejection with no state change.
4. Exercise each listed signature/schema/track/validation/secret failure and confirm the previous three-track catalog remains active.
5. During a coordinated rotation, verify old+new overlap acceptance, successful new-secret release, old-secret rejection after retirement, and TLS validation failure when the expected CA/hostname is absent.
