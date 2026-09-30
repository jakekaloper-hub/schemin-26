import test from 'node:test';
import assert from 'node:assert/strict';
import {
  VERIFIED_COUNTERWEIGHT_BASELINE,
  adaptCanonicalBullpenRoute,
} from '../src/counterweight-adapter.js';

test('inherits canonical counterweights without replacing primary authority', () => {
  const adapted = adaptCanonicalBullpenRoute({
    primary: 'the_architect',
    secondary: ['the_setup_man'],
    counterweight_plan: {
      primary: 'the_architect',
      activated: true,
      counterweights: ['the_setup_man','the_gm'],
      challenge_questions: ['What observed failure justifies this complexity?'],
    },
    participants: ['the_architect','the_setup_man','the_gm'],
  }, {
    projectRoles: ['Character Director','Memo OS Director'],
  });

  assert.equal(adapted.primary, 'the_architect');
  assert.equal(adapted.authority.primary_preserved, true);
  assert.equal(adapted.authority.counterweights_challenge_only, true);
  assert.equal(adapted.authority.project_roles_do_not_create_directors, true);
  assert.equal(adapted.authority.canonical_director_count, 18);
  assert.deepEqual(adapted.counterweight_plan.counterweights, ['the_setup_man','the_gm']);
  assert.ok(adapted.participants.includes('the_gm'));
  assert.ok(adapted.participants.includes('Character Director'));
  assert.equal(adapted.schemin_project_roles.includes('Character Director'), true);
});

test('fails closed when a canonical route omits the counterweight contract', () => {
  assert.throws(
    () => adaptCanonicalBullpenRoute({primary:'the_scout',secondary:[]}),
    /missing counterweight_plan/
  );
});

test('rejects a counterweight plan that changes primary ownership', () => {
  assert.throws(
    () => adaptCanonicalBullpenRoute({
      primary:'the_scout',
      counterweight_plan:{
        primary:'the_closer',
        activated:true,
        counterweights:['the_analyst'],
      },
    }),
    /primary must match/
  );
});

test('inactive counterweights do not become participants unless supplied by canonical route', () => {
  const adapted = adaptCanonicalBullpenRoute({
    primary:'the_gm',
    secondary:['the_commissioner'],
    counterweight_plan:{
      primary:'the_gm',
      activated:false,
      counterweights:[],
      challenge_questions:['What behavior would prove this wrong?'],
    },
  });

  assert.deepEqual(adapted.canonical_participants, ['the_gm','the_commissioner']);
  assert.deepEqual(adapted.schemin_project_roles, []);
});

test('records the standalone Bullpen revision that passed the counterweight promotion gate', () => {
  assert.equal(VERIFIED_COUNTERWEIGHT_BASELINE.repository, 'jakekaloper-hub/bullpen');
  assert.equal(VERIFIED_COUNTERWEIGHT_BASELINE.revision, 'fce34487cac4b3d7d18761f686a681cf2cf5ca1f');
});
