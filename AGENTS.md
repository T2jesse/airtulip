Cut taglines, helper text and secondary labels. If a screen needs them to make sense, fix the layout.

Make the best decision that will elevate all three: the user experience (UX), developer experience (DX), and agent experience (AX) always, without breaking anything

# AirTulip master agent guide

## Canonical instructions and precedence

This root `AGENTS.md` is the one master guide for this repository on Jesse's laptop and in cloud coding environments. Read it at every new or resumed session. Client adapters and linked project documents are supporting references, not competing guides. The user's latest explicit instructions take precedence. The workflow below supersedes conflicting Git, staging-branch, synchronization, startup, browser, and automatic authentication-recovery instructions elsewhere in this file, README, RULES, `.cursor/rules`, historical handoffs, or runbooks; unrelated project conventions remain applicable.

Work only in the repository and task the user identifies. Preserve unrelated changes, staged content, ignored files, assets, backups, and developer settings. Do not infer current tasks from old notes or dirty files. Do not copy personal context, client correspondence, customer data, private account records, or credentials into GitHub instructions.

## Session start and main-only Git workflow

1. Inspect the actual repository root, origin URL, actual branch or detached HEAD, local HEAD, upstream, staged/unstaged/untracked state, local and remote commits, and registered worktrees. Never assume a saved environment ref is the actual checkout branch. Use read-only commands with optional locks disabled where available.
2. Fetch the latest `origin/main` at every new or resumed session using existing authorized authentication. Fetch updates Git metadata only; do not pull or change working files during this inspection. If access is unavailable, stop synchronization and report that latest remote state could not be verified. Do not start login or change credentials/network settings to make fetch work.
3. Compare HEAD with fetched `origin/main` and check for concurrent writers. Jesse pushes laptop work to `main` before a phone/cloud handoff. Cloud work uses its own checkout and must not depend on laptop paths, running processes, browser profiles, or unpublished files.
4. Work only on `main`. A clean checkout already on `main` may fast-forward to fetched `origin/main` only after confirming no unpublished local work, divergence, conflicting worktree, or concurrent writer. Use a fast-forward-only operation; never merge divergent histories automatically.
5. A clean fresh cloud checkout on a branch literally named `work`, or on detached HEAD, may be normalized to `main` only after verifying HEAD has no commits absent from `origin/main`, the existing local `main` has no unique work, and no other worktree conflicts with checking out `main`. Do not delete branches or force branch refs. For any other branch, unique commits, dirty files, conflicting worktree, or unclear provenance, stop and report before changing branches.
6. Dirty, unpublished, diverged, or concurrently edited work requires a handoff decision before synchronization or new implementation. Preserve it. An explicit user instruction to edit named files on a known dirty baseline authorizes only those scoped edits, not synchronization or cleanup. Never reset, restore unrelated files, clean, automatically stash, overwrite changes, or resolve conflicts automatically.
7. After safe synchronization, re-read the current root `AGENTS.md` and relevant changed project instructions. Preserve latest user agreements and unpushed instruction edits; stop if remote and local instruction changes overlap or conflict. Do not replace newer instructions with a cached guide.

These instructions are not an automatic lock across machines. Verify handoff and concurrent work with the user when uncertain. Do not infer exclusivity from a clean checkout or a successful fetch.

## Shopify marketing and Customizer reconciliation

- Before reconciling marketing/Customizer edits, verify the exact Shopify store, theme ID, current theme role (live, draft, development), and GitHub repository/branch mapping using established authorized access. Historical IDs, names, ports, and saved mappings are hints only. Determine whether `main` is live-connected before any authorized push: a Git push can change the storefront through native Shopify sync.
- Fetch and inspect `origin/main` first to determine whether Shopify's native GitHub sync already included the marketing edits. If it did, reconcile through the safe Git workflow rather than pulling duplicate changes from a theme.
- If a theme pull is needed within the user's authorized reconciliation scope, use existing authorized access and the verified exact theme ID. Pull into a new empty temporary snapshot outside the working theme, then compare it with the synchronized repository and intended changes. Never run a blind pull into the working checkout.
- Apply only understood, nonconflicting differences within the requested scope. Preserve merchant settings, app blocks, template assignments, and unrelated work. Never blindly replace `config/settings_data.json`. Stop for overlapping changes, ambiguous theme identity/mapping, or unexplained differences; report the files and decision needed.
- Theme pulls retrieve theme files only. Products, collections, inventory, prices, customer records, and other Admin data require separate scoped Admin API work and authorization for mutations.

## Access, secrets, and release boundaries

- Reuse existing authorized access. New credentials, access grants, OAuth consent, scope expansion, security changes, and network changes require explicit user approval. Never print or commit tokens, passwords, filled environment files, cookies, customer exports, or private account configuration. Reference variable names or blank examples only.
- Agent-run Shopify commands must be noninteractive with child-only `CI=true`, `CLOUD_SHELL=true`, and `SHOPIFY_FLAG_OPEN=false`; use the existing project guard where available. Do not modify the environment of user-owned preview/watch processes.
- At the first authentication, access, scope, verification-code, or consent failure, stop that operation, report it once, and continue independent work. No automatic login/logout, credential reset, cache deletion, scope expansion, alternate CLI/store retries, or verification URLs. Theme access and backend API authorization are separate; a stale preview is not proof of failed authentication.
- Commits, staging changes for a commit, pushes, Shopify uploads, remote theme mutations, and live publication are explicit release steps requiring the user's authorization for the action and target. Do not treat these instructions or write-capable access as release approval. Preserve the existing theme identity and app configuration unless replacement is specifically requested. Review the changed-file manifest and verify the result.

## Platform-specific execution and verification

### Laptop

- Reuse the user's existing storefront preview and watchers. Do not start, stop, restart, replace, duplicate, or kill them unless explicitly asked. Discover the actual current preview URL rather than relying on a saved port or theme ID.
- For project browser work, use only the verified approved T2 Work Chrome account/profile. Discover profile and tab IDs each session through available tools; labels alone are not proof of the signed-in account. Preserve tabs and state. If that profile cannot be verified, stop laptop browser work and continue independent local reads. Never use Personal Chrome or the OS default browser as a fallback.

### Cloud

- Use the cloud checkout and advertised tools; never assume laptop filesystem, terminals, Windows recovery APIs, browser tabs, authentication caches, or local-only guides exist. Missing laptop-only resources are a limitation to report, not a reason to access the laptop automatically.
- An isolated cloud browser may inspect an authorized public storefront or verified preview. It cannot substitute for laptop Work Chrome on authenticated admin or account actions. Use only established authorized cloud access for protected resources; never import laptop cookies or secrets. Browser/account setup and preview startup require explicit user authorization where not already established.

### Completion and handoff

- Read affected files and nearby implementations before editing; keep changes scoped. Validate relevant syntax and behavior, and inspect representative desktop/mobile states for visual changes where an authorized preview is available. Distinguish source checks from rendered verification; report unavailable checks and baseline failures honestly.
- End each session with changed files, tests/checks and outcomes, actual branch, local HEAD, fetched `origin/main` SHA (or its verification blocker), and all remaining dirty, staged, untracked, or unpublished work. State whether changes were committed/pushed and whether a live-connected target was affected. Local instruction edits reach cloud checkouts only after an authorized commit/push and a fresh fetch.

## AirTulip technical conventions and public-repository privacy

- This is a Shopify Online Store Liquid theme based on RoarTheme Concept. Verify the current theme version in `config/settings_schema.json`; do not assume Dawn, Horizon, Hydrogen, or a React app.
- Extend existing section/snippet/schema patterns and theme color/spacing/typography variables. Preserve settings IDs, translations, app blocks, and saved merchant configuration.
- `assets/theme.css` is the vendor's compiled stylesheet; do not assume a local Tailwind source build exists. Inspect current `package.json` and nearby code before choosing commands or adding a build pipeline. Preserve dependent `vendor.js`/`theme.js` loading order.
- Title Case every word in newly written or edited storefront headings, preserving canonical brand names, acronyms, and numbers. Leave unrelated merchant headings alone; body copy uses sentence case.
- Retain the existing CLI compatibility patches that remove unsupported `visible_if` settings. Verify current official schema rules before copying vendor updates or restoring removed attributes. A failed section upload can leave product templates unavailable; source validation is not proof of a successful remote upload.
- Preserve selling-plan inputs and product-form/cart behavior. App scripts and embeds can affect behavior outside Git; verify the actual current integration rather than relying on a historical app inventory. Test add-to-cart, variants, subscriptions, and drawer behavior when touched.
- Verify current prices, warranties, shipping, subscription terms, and health/science claims before writing customer-facing copy. Do not invent clinical claims or reuse stale quantitative claims as approved facts.
- This repository is public. Keep Basecamp account/project configuration, SOW contents, meeting notes, client correspondence, credentials, and customer data out of this guide and new Git commits. Their availability on the laptop does not authorize publication.
- Laptop-only `.cursor/rules` may provide additional nonconflicting technical reference. Relevant portable rules are summarized here; cloud agents must not require ignored Cursor files. Do not copy those ignored files into Git. Private SOW/client context cannot safely be made portable through a public AGENTS file; request a separately authorized private source when needed.

## Historical theme references

Saved theme IDs and branch mappings in local documents are historical only. In particular, the older `staging` branch promotion workflow is superseded by the main-only workflow above. Verify whether remote `main` is live-connected before any authorized push; do not use historical theme names/IDs as a deployment target.

## Development preview URL

- Always inspect the Shopify development-preview URL printed by the user's current `npm run storefront` / `shopify theme dev` terminal. Read the terminal each session and after a restart; do not assume a previous theme ID is current.
- Use the storefront preview link containing `?preview_theme_id=...`, not localhost, `127.0.0.1`, a theme-info link, or the theme editor link.
- Last observed development-preview URL (2026-10-05): `https://airtulip.myshopify.com/?preview_theme_id=191444680994`. This is a reference, not a substitute for checking the running terminal.

## Laptop browser profile details

- For ANY browser work on this project, use only the user's signed-in Chrome **T2 Work / Work** profile for **the approved T2 work account**.
- This applies to local development previews, staging, the live storefront, Shopify admin, and all project research or QA.
- Never use Personal Chrome, another account/profile, an in-app browser, or a separate automated browser profile. If the required Work profile is unavailable, stop browser work and tell the user.

## Browser inspection tools and recovery

### Preferred workflow

- Prefer supported structured browser tools, such as Chrome DevTools/MCP or a documented browser debugging API, for preview inspection, DOM checks, console errors and screenshots. Discover the tools actually advertised in the current session and read their supported capabilities before using them; this preference does not establish that a particular integration or check is available.
- Discover the approved Work Chrome profile/account and the correct project tab each session. Verify identity and the actual preview URL using the guidance above; never hard-code browser, profile, tab or window IDs. Preserve unrelated tabs and reuse the verified binding during that session. If a tab closes, reacquire it within the same verified Work profile.
- Use DOM observations for structure and interaction, supported console tools for errors, and screenshots for visual checks. Report each check separately: a DOM snapshot does not prove visual correctness, and the absence of retrieved console errors does not prove a check ran successfully. Reset temporary viewport overrides after responsive inspection.
- Use desktop Computer Use only when the available structured tools cannot perform the required check or recovery. First identify exactly one returned native window belonging to the verified Work browser, inspect it, and use only advertised native APIs. Never guess a window ID, send input globally or use Personal Chrome. Refresh state after every native action and whenever user input invalidates the observation. Desktop recovery applies only on the laptop and does not establish cloud capabilities.
- An extension-blocker error does not by itself prove that an extension popup is open. Inspect the available evidence before acting. If structured recovery cannot dismiss a confirmed blocker, a supported native Escape action in the verified Work window may be used as the fallback above. Do not send Escape through a browser API already rejecting commands. Retry the same structured observation once after recovery and verify success with a DOM snapshot or screenshot; do not repeatedly retry the same blocker.
- If structured inspection remains unavailable, use the permitted desktop fallback only for checks it can actually perform, and report checks still unverified. If neither path is available or the Work target is ambiguous, stop browser work, report the blocker and continue independent local work.
- These instructions do not authorize enabling debugging ports, installing integrations, changing browser security settings or granting access. Such setup requires a separate explicit user request; reuse existing authorized tools and connections.

### Verified capability evidence and limits

- Observation, 2026-10-20: an "another extension UI is open" error occurred on screenshot capture even though no JavaScript dialog was reported. Creating a fresh tab in the same verified Work browser restored an initial DOM snapshot, but screenshot capture failed again. This is partial observation recovery, not a confirmed screenshot fix or proof of a visible popup.
- On this error, read the advertised browser troubleshooting guidance, retain the verified browser binding, and inspect available dialog/tab state. Do not repeatedly ask the user to dismiss an assumed popup. One fresh-tab attempt in the same profile may establish whether read-only observation still works; preserve user tabs.
- Test recovery with the capability actually needed. A successful DOM snapshot does not establish that screenshots or interactions recovered. If capture remains blocked, continue independent source checks and report visual QA as pending. Do not loop through new tabs, retry rejected commands, change extension permissions, or switch profiles.

- Historical observation, 2026-10-05: the browser-tab Escape call was blocked; native `sky.press_key` in the verified Work window succeeded, after which the same tab's screenshot API worked. This confirms that recovery in that session only. It is not proof of current native-tool availability, a permanent extension fix or a requirement to use desktop Computer Use first.
- Current capabilities must be verified from advertised tools and successful observations in each session. A preferred tool, an old tool name or a historical success must not be reported as a currently available or completed check.
