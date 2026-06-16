# Policy Event Flow

This document defines the expected order for tavern policy-driven events.
Keep event modules aligned with this flow before refactoring shared helpers.

## Event Order

1. Pick or receive the event girl and return location.
2. Print the intro scene.
3. Apply and print current policy reaction.
4. Print policy-based scene variation through `PolicyEventSceneVariationPrint`.
5. Build the player choice menu.
6. Apply the selected choice consequences.
7. Print choice consequences through `PolicyEventChoiceConsequencePrint`.
8. Save shared choice memory through `HallChoiceConsequencesApply`.
9. Offer follow-up policy talk.
10. Return to the original location.

## Current Event Modules

| Event | Start reaction | Scene variation | Choice consequences | Memory write |
| --- | --- | --- | --- | --- |
| `harassment` | `HallPolicyReaction` | `PolicyEventSceneVariationPrint` | `PolicyEventChoiceConsequencePrint` | `HallChoiceConsequencesApply` |
| `hall_lewd` | `HallPolicyReaction` | `PolicyEventSceneVariationPrint` | `PolicyEventChoiceConsequencePrint` | `HallChoiceConsequencesApply` |
| `hall_missing` | `HallPolicyReaction` | `PolicyEventSceneVariationPrint` | `PolicyEventChoiceConsequencePrint` | `HallChoiceConsequencesApply` |
| `kitchen` | `KitchenPolicyReaction` | `PolicyEventSceneVariationPrint` | `PolicyEventChoiceConsequencePrint` | `HallChoiceConsequencesApply` |

## Choice Vocabulary

| Event | Choice | Meaning |
| --- | --- | --- |
| `harassment` | `protect_hard` | Direct protection by force or sharp intervention. |
| `harassment` | `warn_client` | Calm warning that sets a boundary. |
| `harassment` | `self_handle` | Let the girl handle the client herself. |
| `harassment` | `profit` | Let the situation continue for money or advantage. |
| `harassment` | `ignore` | Do not intervene. |
| `hall_lewd` | `stop` | Stop the scene. |
| `hall_lewd` | `watch` | Watch without intervening. |
| `hall_lewd` | `encourage` | Encourage the scene for attention or money. |
| `hall_missing` | `ignore` | Do not look for the girl. |
| `hall_missing` | `peek` | Quietly check what is happening. |
| `hall_missing` | `interrupt` | Interrupt the private scene. |
| `kitchen` | `stop` | Stop the customer conflict. |
| `kitchen` | `let_her` | Let the girl handle the kitchen situation herself. |
| `kitchen` | `client` | Keep the customer pleased for money or advantage. |

Choice names should be reused consistently by result handlers, `PolicyEventChoiceConsequencePrint`, `HallChoiceMemoryClassify`, and `GirlMemoryOfStefanClassifyChoice`.

## Ownership Rules

- Event-specific `ApplyConsequences` locations change immediate scene stats only.
- `PolicyEventChoiceConsequencePrint` is the owner entry for post-choice feedback.
- `HallChoiceConsequencePrint` is the compatibility entry behind that owner helper.
- `PolicyEventSceneVariationPrint` is the owner entry for pre-choice policy scene variation.
- `GirlPolicySceneVariationPrint` is the compatibility entry behind that owner helper.
- `HallChoiceConsequencesApply` owns shared memory and family-state updates.
- `GirlMemoryOfStefanRegister` should not be called directly from event-specific result handlers when `PolicyEventChoiceConsequencePrint` is used.
- `PolicyEventSceneVariationPrint` belongs before the player choice, never inside a debug-only block.

## Next Refactor Targets

- Normalize choice names across hall and kitchen events.
- Reduce duplicate result-handler structure in `hall_lewd`, `hall_missing`, and `kitchen`.
- Keep compatibility aliases in `modules/core/system/compatibility_aliases.qsps` until old call sites are gone.
