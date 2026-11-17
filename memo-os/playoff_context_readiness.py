"""Audit analytics consumption in source copy and actual render requests.

This is a pure-data check, not a manuscript editor, Fact Lock certificate,
artwork review, or Director acknowledgement. A reference attached to a page
does not demonstrate that its copy or renderer consumed the referenced data.

``sports_source`` on the previs identifies the reconciled final source. Bound
pages carry ``analytics_consumption`` with the report/input hashes, a hash of
their actual draft_copy, and an ACCEPTED or NO_MATERIAL_CANDIDATE decision.
ACCEPTED selections also map packet JSON pointers to copy JSON pointers.
Render requests must mirror that receipt and the exact current publication copy.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import json
import re


COPY_MARKER = 'EXACT FULL PUBLICATION COPY'
EXACT_CLAIM = re.compile(
    r'\b(?:clinched?|eliminat(?:ed|es|ion|e))\b'
    r'|\bmathematically\s+(?:reachable|alive|out)\b'
    r'|\ball\s+(?:(?:twelve|\d+)\s+)?teams\b.{0,90}\b(?:route|path|alive)\b',
    re.IGNORECASE,
)
PERCENT = r'\d+(?:\.\d+)?\s*(?:%|percent\b|per\s+cent\b)'
PROBABILITY_CLAIM = re.compile(
    r'\b(?:playoff|postseason|qualification|championship)\s+(?:odds|probabilit\w*|chance)\b'
    r'|\b(?:odds|probabilit\w*|chance)\b.{0,60}'+PERCENT+
    r'|'+PERCENT+r'\s*(?:chance|probabilit\w*|playoff|postseason|odds)',
    re.IGNORECASE,
)
PROVISIONAL = re.compile(r'UNDECIDED|PROVISIONAL|PRE[_ -]?MNF|current.leads.hold', re.IGNORECASE)
PUBLICATION_DIRECTIVE = re.compile(
    r'\b(?:print(?:ed)?|caption|footnote|on[- ]page text|display(?:ed)? text|visible text|lettering)\b',
    re.IGNORECASE,
)


def digest(value):
    """Canonical JSON hash used by consumption and claim receipts."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def _hash(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def _time(value):
    if not isinstance(value, str):
        raise ValueError('timestamp is missing')
    value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if value.tzinfo is None:
        raise ValueError('timestamp lacks timezone')
    return value


def _strings(value, path=''):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, child in value.items():
            escaped = str(key).replace('~', '~0').replace('/', '~1')
            yield from _strings(child, path+'/'+escaped)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _strings(child, path+'/'+str(index))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        # Numeric leaves can still be forecasts when their structured key
        # supplies the meaning (for example playoff_odds/team_id = 0.9).
        yield path, str(value)


def _outside_copy_claims(text):
    """Flag claim-like instructions outside the exact-copy JSON for review.

    This bounded screen is not a semantic classifier. Recognizable standalone
    prohibitions remain instructions; other claim-like text needs inspection.
    """
    for fragment in re.split(r'[\n;]|(?<=[.!?])\s+', text):
        fragment = fragment.strip().strip(',\"\' ')
        if not (EXACT_CLAIM.search(fragment) or PROBABILITY_CLAIM.search(fragment)):
            continue
        if (re.match(r"^(?:do not|never|avoid|no|must not|don't)\b", fragment, re.IGNORECASE)
                and not re.search(r'\b(?:but|however|except)\b', fragment, re.IGNORECASE)):
            continue
        yield fragment


def _pointer(value, pointer):
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        raise ValueError('a nonempty JSON pointer is required')
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            if not token.isdigit():
                raise ValueError('invalid array pointer')
            value = value[int(token)]
        elif isinstance(value, dict):
            value = value[token]
        else:
            raise ValueError('pointer traverses a scalar')
    return value


def _display(value, style):
    if style == 'identity':
        return value
    if style == 'record':
        if not isinstance(value, dict):
            raise ValueError('record must be a mapping')
        parts = [value[k] for k in ('wins', 'losses', 'ties')]
        if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in parts):
            raise ValueError('invalid record')
        return '–'.join(str(x) for x in (parts if parts[2] else parts[:2]))
    if style not in ('fixed_2', 'integer') or isinstance(value, bool):
        raise ValueError('unsupported display format')
    number = Decimal(str(value))
    if not number.is_finite():
        raise ValueError('nonfinite number')
    if style == 'integer':
        if number != number.to_integral_value():
            raise ValueError('integer format would discard a fraction')
        return str(int(number))
    return format(number.quantize(Decimal('.01'), rounding=ROUND_HALF_UP), '.2f')


def _claim_accepted(receipts, page_id, path, text, claim_type, copy_hash, packet, verifier):
    """A bound receipt is necessary but cannot substitute for proof verification."""
    if not callable(verifier):
        return False
    for receipt in receipts:
        if not isinstance(receipt, dict):
            continue
        evidence = receipt.get('evidence')
        if (receipt.get('page_id') == page_id and receipt.get('copy_pointer') == path
                and receipt.get('claim_type') == claim_type
                and receipt.get('disposition') == 'ACCEPTED_FOR_EDITORIAL_REVIEW'
                and receipt.get('text_sha256') == hashlib.sha256(text.encode()).hexdigest()
                and receipt.get('copy_sha256') == copy_hash
                and receipt.get('report_sha256') == packet.get('report_sha256')
                and receipt.get('source_snapshot') == packet.get('source_snapshot')
                and isinstance(evidence, dict) and evidence
                and receipt.get('evidence_sha256') == digest(evidence)):
            try:
                return verifier(copy.deepcopy(receipt), packet=copy.deepcopy(packet),
                                page_id=page_id, copy_pointer=path, text=text) is True
            except (ValueError, TypeError, KeyError, ArithmeticError):
                return False
    return False


def audit_memo_readiness(packet, *, previs=None, render_requests=None, now=None,
                         max_age_seconds=86400, accepted_claims=None, claim_verifier=None):
    """Return source/copy/render HOLD reasons without changing any inputs.

    ``render_requests`` is a page-ID -> actual request JSON mapping, not a
    list of intended filenames. ``accepted_claims`` contains source-and-copy-
    bound evidence receipts. A caller-supplied ``claim_verifier`` must independently
    reproduce their proofs; receipt flags alone never clear a claim. Both are
    absent by default, and neither can override a held probabilistic forecast.
    A passing result only verifies this boundary, never artwork or release.
    """
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('timezone-aware review time required')
    if (isinstance(max_age_seconds, bool) or not isinstance(max_age_seconds, (int, float))
            or not 0 < max_age_seconds < float('inf')):
        raise ValueError('finite positive freshness SLO required')
    issues = []
    review_notes = []
    consumed = []
    compared_values = []

    def hold(code, detail, *, page_id=None, path=None, expected=None, observed=None):
        item = {'code': code, 'detail': detail}
        if page_id is not None:
            item['page_id'] = page_id
        if path is not None:
            item['path'] = path
        if expected is not None:
            item['expected'] = expected
        if observed is not None:
            item['observed'] = observed
        issues.append(item)

    if not isinstance(packet, dict):
        raise ValueError('packet must be a mapping')
    for key in ('report_sha256', 'source_snapshot'):
        if not _hash(packet.get(key)):
            hold('MISSING_SOURCE_HASH', 'A complete accepted-source hash is required.', path=key)
    try:
        age = (now-_time(packet.get('source_as_of'))).total_seconds()
        if age < 0 or age > max_age_seconds:
            hold('STALE_OR_FUTURE_ANALYTICS_SOURCE', 'Recheck the accepted source at actual consumption.',
                 expected={'max_age_seconds': max_age_seconds}, observed={'age_seconds': age})
    except (ValueError, TypeError):
        hold('INVALID_SOURCE_TIME', 'A timezone-qualified source observation is required.')

    bindings = packet.get('page_bindings', {})
    if not isinstance(bindings, dict) or not bindings:
        hold('MISSING_PAGE_BINDINGS', 'Explicit existing-page bindings are required.')
        bindings = {}
    week = packet.get('through_week')
    valid_week = isinstance(week, int) and not isinstance(week, bool) and week > 0
    prefix = f'W{week:02d}-' if valid_week else None
    if prefix is None:
        hold('INVALID_SOURCE_WEEK', 'The accepted cutoff week is required.')
    if not isinstance(previs, dict):
        hold('PREVIS_NOT_SUPPLIED', 'A candidate packet alone does not demonstrate production consumption.')
        previs = {}
    if previs.get('final_fact_lock') is not True:
        hold('PREVIS_NOT_FACT_LOCKED', 'The supplied issue still lacks its owning final Fact Lock.')
    revision = previs.get('creative_revision', {})
    sports_state = revision.get('sports_status', '') if isinstance(revision, dict) else ''
    if isinstance(sports_state, str) and PROVISIONAL.search(sports_state):
        hold('PROVISIONAL_SPORTS_STATE', 'The operative issue still describes provisional outcomes.',
             path='creative_revision/sports_status', observed=sports_state)
    sports_source = previs.get('sports_source')
    if not isinstance(sports_source, dict):
        hold('SOURCE_RECONCILIATION_NOT_WITNESSED',
             'An analytics attachment is not a reconciled sports_source receipt.')
    else:
        expected_source = {key: packet.get(key) for key in
                           ('league_id', 'season', 'through_week', 'source_snapshot',
                            'report_sha256', 'source_as_of')}
        expected_source['result_lock'] = 'FINAL'
        for key, expected in expected_source.items():
            if sports_source.get(key) != expected:
                hold('PREVIS_SOURCE_MISMATCH', 'Previs must identify the same accepted final source.',
                     path='sports_source/'+key, expected=expected, observed=sports_source.get(key))
    if previs.get('sports_snapshot_utc') != packet.get('source_as_of'):
        hold('PREVIS_SNAPSHOT_NOT_RECONCILED', 'The copy snapshot differs from its incoming analytics source.',
             expected=packet.get('source_as_of'), observed=previs.get('sports_snapshot_utc'))

    rows = previs.get('pages', [])
    if not isinstance(rows, list):
        rows = []
        hold('INVALID_PAGE_LIST', 'Previs pages must be a list.')
    pages = {}
    for page in rows:
        page_id = page.get('page_id') if isinstance(page, dict) else None
        if not isinstance(page_id, str) or page_id in pages:
            hold('INVALID_OR_DUPLICATE_PAGE', 'Each source page needs a unique identity.', page_id=page_id)
            continue
        pages[page_id] = page
        if prefix is None or not page_id.startswith(prefix):
            hold('PAGE_WEEK_MISMATCH', 'Page identity differs from the accepted cutoff.', page_id=page_id)
    for page_id in bindings:
        if page_id not in pages:
            hold('BOUND_PAGE_ABSENT', 'The bound page is absent from the actual issue.', page_id=page_id)
    if not isinstance(render_requests, dict):
        hold('RENDER_CONSUMPTION_NOT_WITNESSED', 'Supply actual render request JSON to verify consumption.')
        render_requests = {}
    receipts = accepted_claims if isinstance(accepted_claims, list) else []

    for page_id, page in pages.items():
        if page.get('include_in_recommended_issue') is False:
            if page_id in bindings:
                hold('BOUND_PAGE_OMITTED', 'Analytics cannot silently bind an omitted page.', page_id=page_id)
            continue
        copy = page.get('draft_copy')
        if not isinstance(copy, dict):
            hold('PUBLICATION_COPY_MISSING', 'Actual structured publication copy is required.', page_id=page_id)
            continue
        copy_hash = digest(copy)
        for path, text in _strings(copy):
            for claim_type, pattern in [('EXACT', EXACT_CLAIM), ('PROBABILISTIC', PROBABILITY_CLAIM)]:
                context = path.replace('_', ' ').replace('-', ' ').replace('/', ' ')
                if not (pattern.search(text) or (claim_type == 'PROBABILISTIC' and pattern.search(context))):
                    continue
                if claim_type == 'PROBABILISTIC':
                    hold('HELD_FORECAST_IN_VISIBLE_COPY', 'This consumer has no forecast approval mechanism; a packet flag or proof callback cannot release forecast copy.',
                         page_id=page_id, path=path, observed=text[:240])
                elif not _claim_accepted(receipts, page_id, path, text, claim_type, copy_hash, packet, claim_verifier):
                    hold('UNACCEPTED_'+claim_type+'_CLAIM',
                         'Retained claim needs acceptance bound to this copy and source; conditional wording is insufficient.',
                         page_id=page_id, path=path, observed=text[:240])
        mirrors = {'draft_copy_template': page.get('draft_copy_template')}
        brief = page.get('illustrated_page_brief')
        if isinstance(brief, dict):
            mirrors['illustrated_page_brief/publication_copy'] = brief.get('publication_copy')
            mirrors['illustrated_page_brief/exact_copy_template'] = brief.get('exact_copy_template')
            if brief.get('artist_prompt') != page.get('candidate_render_prompt'):
                hold('PREVIS_PROMPT_MIRROR_MISMATCH', 'Embedded artist prompts differ.', page_id=page_id)
        for path, value in mirrors.items():
            if value is not None and value != copy:
                hold('PREVIS_COPY_MIRROR_MISMATCH', 'Existing copy mirrors must match the current draft.',
                     page_id=page_id, path=path)

        # This existing consumer has a concrete current-standings contract.
        # Compare actual rows even when no consumption receipt has been written;
        # a new source hash cannot make an older printed table current.
        purpose = bindings.get(page_id, {}).get('purpose') if isinstance(bindings.get(page_id), dict) else None
        if purpose == 'official_standings':
            teams = packet.get('teams', {})
            by_name = {team.get('name'): team for team in teams.values() if isinstance(team, dict)}
            table = copy.get('rows')
            if not isinstance(table, list) or not table:
                hold('STANDINGS_TABLE_MISSING', 'The current-standings consumer needs actual table rows.', page_id=page_id)
            else:
                seen = set()
                for index, row in enumerate(table):
                    team = teams.get(str(row.get('team_id'))) if isinstance(row, dict) and 'team_id' in row else None
                    if team is None and isinstance(row, dict):
                        team = by_name.get(row.get('team'))
                    if not isinstance(team, dict):
                        hold('STANDINGS_TEAM_UNRESOLVED', 'A printed team cannot be mapped to the accepted source.',
                             page_id=page_id, path=f'/rows/{index}')
                        continue
                    if row.get('team') != team.get('name'):
                        hold('STANDINGS_DISPLAY_NAME_MISMATCH',
                             'An internal team ID cannot override a different printed team name.',
                             page_id=page_id, path=f'/rows/{index}/team',
                             expected=team.get('name'), observed=row.get('team'))
                    team_id = str(team.get('team_id'))
                    if team_id in seen:
                        hold('DUPLICATE_STANDINGS_TEAM', 'A printed standings team occurs more than once.', page_id=page_id)
                    seen.add(team_id)
                    try:
                        expected_fields = {
                            'record': _display({k: team[k] for k in ('wins', 'losses', 'ties')}, 'record'),
                            'points_for': _display(team['points_for'], 'fixed_2'),
                            'seed': team['provider_seed'],
                        }
                        for key, expected in expected_fields.items():
                            observed = row.get(key)
                            comparison = observed.replace('-', '–') if key == 'record' and isinstance(observed, str) else observed
                            if key == 'points_for' and observed is not None:
                                comparison = _display(observed, 'fixed_2')
                            source_field = 'provider_seed' if key == 'seed' else key
                            source_pointer = f'/teams/{team_id}' if key == 'record' else f'/teams/{team_id}/{source_field}'
                            compared_values.append({'page_id': page_id, 'source_pointer': source_pointer,
                                'copy_pointer': f'/rows/{index}/{key}', 'incoming': expected, 'copy_value': observed})
                            if comparison != expected:
                                hold('STANDINGS_VALUE_DIFFERS_FROM_SOURCE', 'The current standings row retains an older or different value.',
                                     page_id=page_id, path=f'/rows/{index}/{key}', expected=expected, observed=observed)
                    except (KeyError, TypeError, ValueError, InvalidOperation):
                        hold('INVALID_STANDINGS_VALUE', 'Printed standings cannot be reconciled to the accepted source.', page_id=page_id)
                if seen != {str(team.get('team_id')) for team in teams.values() if isinstance(team, dict)}:
                    hold('STANDINGS_COVERAGE_MISMATCH', 'The current table must cover each accepted team exactly once.', page_id=page_id)

        consumption = page.get('analytics_consumption')
        page_consumed = True
        if page_id in bindings:
            if not isinstance(consumption, dict):
                hold('PAGE_CONSUMPTION_NOT_WITNESSED',
                     'analytics_context alone is a reference; selection and copy reconciliation are still pending.', page_id=page_id)
                page_consumed = False
            else:
                for key, expected in [('report_sha256', packet.get('report_sha256')),
                                      ('source_snapshot', packet.get('source_snapshot')),
                                      ('copy_sha256', copy_hash)]:
                    if consumption.get(key) != expected:
                        hold('CONSUMPTION_HASH_MISMATCH', 'The consumption receipt is stale or belongs to different copy/source.',
                             page_id=page_id, path=key, expected=expected, observed=consumption.get(key))
                        page_consumed = False
                decision = consumption.get('decision')
                mappings = consumption.get('metric_bindings', [])
                if decision not in ('ACCEPTED', 'NO_MATERIAL_CANDIDATE'):
                    hold('EDITORIAL_SELECTION_PENDING', 'Record an explicit accepted selection or no-material-candidate decision.', page_id=page_id)
                    page_consumed = False
                if decision == 'ACCEPTED' and (not isinstance(mappings, list) or not mappings):
                    hold('METRIC_BINDINGS_MISSING', 'Accepted selections must map incoming values to actual copy fields.', page_id=page_id)
                    page_consumed = False
                for binding in mappings if isinstance(mappings, list) else []:
                    try:
                        if not isinstance(binding, dict) or not binding.get('source_pointer', '').startswith('/teams/'):
                            raise ValueError('team metric source pointer required')
                        expected = _display(_pointer(packet, binding['source_pointer']), binding.get('format', 'identity'))
                        observed = _pointer(copy, binding['copy_pointer'])
                        compared_values.append({'page_id': page_id, 'source_pointer': binding['source_pointer'],
                            'copy_pointer': binding['copy_pointer'], 'incoming': expected, 'copy_value': observed})
                        if observed != expected:
                            hold('COPY_VALUE_DIFFERS_FROM_SOURCE', 'Updated analytics and existing visible copy disagree.',
                                 page_id=page_id, path=binding['copy_pointer'], expected=expected, observed=observed)
                            page_consumed = False
                    except (KeyError, IndexError, TypeError, ValueError, InvalidOperation):
                        hold('INVALID_METRIC_BINDING', 'A source/copy pointer or display format cannot be resolved.', page_id=page_id)
                        page_consumed = False

        request = render_requests.get(page_id)
        if not isinstance(request, dict):
            hold('RENDER_REQUEST_MISSING', 'The actual included-page render request is missing.', page_id=page_id)
            continue
        if request.get('page_id') != page_id:
            hold('RENDER_PAGE_MISMATCH', 'Render request identity differs from its source page.', page_id=page_id)
            page_consumed = False
        if request.get('publication_copy') != copy:
            hold('RENDER_COPY_MISMATCH', 'Renderer still holds different publication copy.', page_id=page_id)
            page_consumed = False
        prompt = request.get('prompt')
        if page.get('candidate_render_prompt') is not None and prompt != page['candidate_render_prompt']:
            hold('RENDER_PROMPT_MISMATCH', 'Renderer and page prompt mirrors differ.', page_id=page_id)
            page_consumed = False
        try:
            if not isinstance(prompt, str) or prompt.count(COPY_MARKER) != 1:
                raise ValueError('one exact-copy marker required')
            before_copy, payload = prompt.split(COPY_MARKER, 1)
            payload = payload.lstrip()
            prompt_copy, copy_end = json.JSONDecoder().raw_decode(payload)
            if prompt_copy != copy:
                hold('PROMPT_PUBLICATION_COPY_MISMATCH', 'The exact copy embedded in the prompt is stale.', page_id=page_id)
                page_consumed = False
            for fragment in _outside_copy_claims(before_copy+'\n'+payload[copy_end:]):
                quantified_forecast = PROBABILITY_CLAIM.search(fragment) and re.search(PERCENT, fragment, re.IGNORECASE)
                if PUBLICATION_DIRECTIVE.search(fragment) or quantified_forecast:
                    hold('OUTSIDE_COPY_CLAIM_REVIEW_REQUIRED',
                         'An explicit publication directive or quantified forecast occurs outside the verified copy JSON; reconcile it before rendering.',
                         page_id=page_id, path='prompt/outside_exact_copy', observed=fragment[:240])
                    page_consumed = False
                else:
                    review_notes.append({'code': 'UNCLASSIFIED_PROMPT_CONTEXT', 'page_id': page_id,
                        'path': 'prompt/outside_exact_copy', 'observed': fragment[:240],
                        'detail': 'Context may be historical, prohibitory or figurative; this bounded screen does not classify it as a current publication claim.'})
        except (ValueError, TypeError, json.JSONDecodeError):
            hold('PROMPT_COPY_UNVERIFIABLE', 'Cannot verify the exact publication copy sent to the renderer.', page_id=page_id)
            page_consumed = False
        policy = request.get('sports_policy', {})
        if (not isinstance(policy, dict) or policy.get('official_winner_decided') is not True
                or PROVISIONAL.search(str(policy.get('source_capture_scope', '')))):
            hold('RENDER_SPORTS_STILL_PROVISIONAL', 'The operative render request has not consumed final sports state.', page_id=page_id)
            page_consumed = False
        if page_id in bindings:
            if not isinstance(consumption, dict) or request.get('analytics_consumption') != consumption:
                hold('RENDER_ANALYTICS_BINDING_MISSING', 'Render request must mirror the actual page consumption receipt.', page_id=page_id)
                page_consumed = False
            if page_consumed:
                consumed.append(page_id)

    return {
        'schema_version': 1, 'status': 'HOLD' if issues else 'SOURCE_AND_RENDER_INPUTS_VERIFIED',
        'scope': 'Final sports-copy source and render-input consistency only; existing provisional proof preparation is separate. No artwork or release approval.',
        'claim_screening_limit': 'Bounded text and key-context screening; passing does not certify every semantic claim or unrestricted prompt instruction.',
        'checked_at': now.isoformat(), 'report_sha256': packet.get('report_sha256'),
        'source_snapshot': packet.get('source_snapshot'), 'source_as_of': packet.get('source_as_of'),
        'freshness_slo_seconds': max_age_seconds,
        'copy_change_required': bool(issues), 'consumption_witnessed': not issues and bool(bindings),
        'consumed_page_ids': consumed, 'pending_page_ids': sorted(set(bindings)-set(consumed)),
        'compared_values': compared_values, 'issues': issues, 'review_notes': review_notes,
        'publication_authorized': False, 'canonical_fact_lock_certified': False,
        'artwork_reviewed': False, 'external_director_approval_claimed': False,
    }
