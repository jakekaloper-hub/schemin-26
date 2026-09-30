export const VERIFIED_COUNTERWEIGHT_BASELINE = Object.freeze({
  repository: 'jakekaloper-hub/bullpen',
  revision: 'fce34487cac4b3d7d18761f686a681cf2cf5ca1f',
  feature: 'Director Counterweight System',
});

/**
 * Consume a route produced by canonical Bullpen Core.
 *
 * Schemin does not copy the 18 Director counterweight registry. It accepts the
 * canonical route contract, preserves primary authority, and adds only
 * project-local roles supplied by the Schemin caller.
 */
export function adaptCanonicalBullpenRoute(route, {
  projectRoles = [],
  requireCounterweightPlan = true,
} = {}) {
  if (!route || typeof route !== 'object') {
    throw new TypeError('canonical Bullpen route must be an object');
  }
  if (!route.primary || typeof route.primary !== 'string') {
    throw new TypeError('canonical Bullpen route requires primary');
  }

  const plan = route.counterweight_plan;
  if (requireCounterweightPlan && (!plan || typeof plan !== 'object')) {
    throw new Error('canonical Bullpen route is missing counterweight_plan');
  }
  if (plan && plan.primary && plan.primary !== route.primary) {
    throw new Error('counterweight_plan primary must match route primary');
  }

  const secondary = Array.isArray(route.secondary) ? route.secondary : [];
  const activatedCounterweights = plan?.activated && Array.isArray(plan.counterweights)
    ? plan.counterweights
    : [];
  const canonicalParticipants = Array.isArray(route.participants)
    ? route.participants
    : [route.primary, ...secondary, ...activatedCounterweights];

  const cleanProjectRoles = Array.isArray(projectRoles)
    ? projectRoles.filter((role) => typeof role === 'string' && role.trim()).map((role) => role.trim())
    : [];

  const participants = [...new Set([
    route.primary,
    ...canonicalParticipants,
    ...activatedCounterweights,
    ...cleanProjectRoles,
  ])];

  return Object.freeze({
    source: VERIFIED_COUNTERWEIGHT_BASELINE.repository,
    verified_counterweight_baseline: VERIFIED_COUNTERWEIGHT_BASELINE.revision,
    primary: route.primary,
    secondary: [...secondary],
    counterweight_plan: plan || null,
    canonical_participants: [...new Set([route.primary, ...canonicalParticipants, ...activatedCounterweights])],
    schemin_project_roles: [...new Set(cleanProjectRoles)],
    participants,
    authority: Object.freeze({
      primary_preserved: true,
      counterweights_challenge_only: true,
      project_roles_do_not_create_directors: true,
      canonical_director_count: 18,
    }),
  });
}
