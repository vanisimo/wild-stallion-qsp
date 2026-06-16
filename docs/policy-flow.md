# Policy Event Flow

This document defines the expected order for tavern policy-driven events.
Keep event modules aligned with this flow before refactoring shared helpers.

## Event Order

1. Pick or receive the event girl and return location.
2. Print the intro scene.
3. Apply and print current policy reaction.
4. Print policy-based scene variation.
5. Build the player choice menu.
6. Apply the selected choice consequences.
7. Print choice consequences through `HallChoiceConsequencePrint`.
8. Save shared choice memory through `HallChoiceConsequencesApply`.
9. Offer follow-up policy talk.
10. Return to the original location.

## Current Event Modules

| Event | Start reaction | Scene variation | Choice consequences | Memory write |
| --- | --- | --- | --- | --- |
| `harassment` | `HallPolicyReaction` | `GirlPolicySceneVariationPrint` | `HallChoiceConsequencePrint` | `HallChoiceConsequencesApply` |
| `hall_lewd` | `HallPolicyReaction` | `GirlPolicySceneVariationPrint` | `HallChoiceConsequencePrint` | `HallChoiceConsequencesApply` |
| `hall_missing` | `HallPolicyReaction` | `GirlPolicySceneVariationPrint` | `HallChoiceConsequencePrint` | `HallChoiceConsequencesApply` |
| `kitchen` | `KitchenPolicyReaction` | `GirlPolicySceneVariationPrint` | `HallChoiceConsequencePrint` | `HallChoiceConsequencesApply` |

## Ownership Rules

- Event-specific `ApplyConsequences` locations change immediate scene stats only.
- `HallChoiceConsequencePrint` is the public compatibility entry for post-choice feedback.
- `HallChoiceConsequencesApply` owns shared memory and family-state updates.
- `GirlMemoryOfStefanRegister` should not be called directly from event-specific result handlers when `HallChoiceConsequencePrint` is used.
- `GirlPolicySceneVariationPrint` belongs before the player choice, never inside a debug-only block.

## Next Refactor Targets

- Normalize choice names across hall and kitchen events.
- Reduce duplicate result-handler structure in `hall_lewd`, `hall_missing`, and `kitchen`.
- Keep compatibility aliases in `modules/core/system/compatibility_aliases.qsps` until old call sites are gone.
