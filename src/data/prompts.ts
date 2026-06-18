/** Starter prompts, grouped by the engine they exercise. Sourced from the example
 *  questions the agent already answers well (see README / the old Streamlit sidebar). */
export interface PromptGroup {
  label: string
  hint: string
  prompts: string[]
}

export const PROMPT_GROUPS: PromptGroup[] = [
  {
    label: 'Policies',
    hint: 'Company rules & guardrails',
    prompts: [
      'What is our refund policy?',
      'What discount can I give without approval?',
    ],
  },
  {
    label: 'Scripts',
    hint: 'How to say it',
    prompts: [
      'How should I open a cold call?',
      'Give me a line to handle a pricing objection.',
    ],
  },
  {
    label: 'Pipeline',
    hint: 'Live CRM data',
    prompts: [
      'Who owns the Acme Corp lead?',
      "What's the deal size for Acme Corp?",
      'What leads does Jane Smith own?',
    ],
  },
]
