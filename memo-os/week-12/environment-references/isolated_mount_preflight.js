'use strict';
// Host-side single-source preflight predicate; this is not a renderer adapter or proof of a provider mount.
function mount(expected,received){return Boolean(received && received.mount_status==='PASS' && Array.isArray(received.mounted_reference_ids) && Array.isArray(received.mounted_reference_hashes) && received.mounted_reference_ids.length===1 && received.mounted_reference_hashes.length===1 && received.generation_intent_id===expected.generation_intent_id && received.mounted_reference_ids[0]===expected.id && received.mounted_reference_hashes[0]===expected.hash);}
module.exports={mount};
