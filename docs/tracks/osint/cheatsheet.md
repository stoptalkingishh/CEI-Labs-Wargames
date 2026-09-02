# OSINT Instructor Checklist

Before release:

1. Install the pinned CTFGenerator host and the reviewed `ctfgen-family-osint` package.
2. Run the adapter tests and build the pilot in `hidden` state.
3. Verify the manifest lists three unique reviewed public bundles.
4. Confirm every downloadable file appears in its evidence manifest with the same SHA-256 and size.
5. Confirm no private path is present under any generated `files/` directory.
6. Review provenance, licensing, safety/privacy approval, and playtest timing in the plugin.
7. Rebuild with `CEI_OSINT_RELEASE_STATE=visible` only after approval.

Do not hand-edit generated flags, briefings, evidence, or writeups. Correct the canonical dossier in the plugin and rebuild.
