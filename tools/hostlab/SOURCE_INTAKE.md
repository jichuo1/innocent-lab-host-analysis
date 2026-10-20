# Source intake: preparatory validation only

Status: **no AppShare discovery, login, link request, download, or schedule is
implemented or enabled**. This change adds the independent local admission gate
and makes existing SDK identity inspection usable on POSIX runners. It does not
claim that unattended AppShare downloads have been verified. Do not use this
code to bypass an environment's download restrictions.

## Contract

An AppShare adapter, once a supported and authorized integration is established,
must supply a local APK and a receipt containing exactly:

```json
{"schema":1,"source":"appshare","channel":"official","version_code":9160200,"version_name":"9.16.0"}
```

The values above illustrate the observed listing, not a validated APK identity.
The channel label is an assertion, not proof that the file is official.
No URL, cookie, password, token, page body or arbitrary metadata is accepted in
this receipt. Never put such data in public CI logs, artifacts or the repository.

A separately provisioned policy contains exactly `schema` (1), `package`
(`tv.danmaku.bili`), `channel`, and `signer_sets` (nonempty list of allowed complete
sets of lowercase SHA-256 certificate fingerprints). Derive this policy from an
independently trusted APK; **never trust a certificate merely because it appears
in the incoming sample**. No production signer fingerprints are supplied here.
Signer rotation needs a reviewed policy update, not automatic enrollment.

Offline check, with Android build-tools available via ANDROID_HOME,
ANDROID_SDK_ROOT or PATH:

```sh
python tools/hostlab/source_intake.py input.apk --receipt receipt.json --policy trusted-policy.json --output admission.json
```

The output must not already exist. Validation checks SDK signature validity,
package, exact version code/name and exact signer set, and records ABI metadata
and a content hash. Unit tests mock SDK execution: they are not real APK evidence.

Once upload credentials and destination are separately authorized and configured,
the existing private-library upload can enforce the same gate:

```sh
python tools/hostlab/hostlab.py upload input.apk --source-receipt receipt.json --trust-policy trusted-policy.json
```

Both options are required together. Gate failure occurs before private-library
access. The existing content-hash deduplication, private-repository check,
parent-commit CAS and manifest readback are retained. The original unqualified
manual upload command remains backward compatible; it is not a source-intake
security gate. Automatic source ingestion must use both policy arguments.

## Still required before live enablement

- Verified AppShare version/discovery and acquisition contract; no guessed API.
- Separately approved credential provisioning. Do not export an existing browser
  session or put credentials in source control.
- A durable acquisition state machine: discovered / requesting / uncertain /
  acquired / validated / registered. An uncertain paid request must not be
  blindly repeated. SHA deduplication alone does not prevent repeat point charges.
- A deployment environment expressly permitted to acquire these inputs.
- End-to-end file, channel, signer, private-library and analysis-trigger validation.
- No new recurring job, external upload, points spending, or repository secret was
  configured by this preparatory change.
