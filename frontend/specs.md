# Component Specs & Developer Handoff

This file lists the primary UI components, expected props, states and accessibility notes for implementation.

## Button
- Name: `Button` (variants: `primary`, `secondary`, `link`)
- Props: `{ size: 'small'|'medium'|'large', variant: 'primary'|'secondary'|'link', disabled: boolean, icon?: string, ariaLabel?: string }`
- States: `default`, `hover`, `active`, `disabled`
- Accessibility: `role='button'`, keyboard focus visible, `aria-disabled` when disabled.

## TextArea
- Name: `TextArea`
- Props: `{ rows?: number, placeholder?: string, value?: string, ariaLabel?: string, error?: string }`
- States: `empty`, `focused`, `error`, `disabled`
- Accessibility: label associated with textarea, announce line count via `aria-live` when changed.

## Input
- Name: `Input` (used for URL and filename)
- Props: `{ type?: 'text'|'url', placeholder?: string, value?: string, ariaLabel?: string, error?: string }`
- Accessibility: validate URL pattern and provide inline error messages with `aria-describedby` linking to error text.

## StepperProgress
- Props: `{ steps: string[], currentIndex: number, isCancellable?: boolean }`
- States: each step can be `pending|active|completed|failed`
- Accessibility: use `role='progressbar'` and `aria-valuemin/valuemax/valuenow` for overall progress; announce step changes with `aria-live`.

## SentimentChips / SentimentPie
- Chips: show label + percentage (aria-label=`Positive 75%`)
- Pie: SVG-based chart with `role='img'` and accessible `title` and `desc` elements.

## KeywordTagList
- Props: `{ items: {term: string, count: number}[] }`
- Interaction: click a tag to filter comment table; show tooltip with exact count on hover.

## CommentTable
- Props: `{ columns: string[], rows: object[], pageSize?: number }`
- Interaction: sortable columns, expandable row to show full context, row-level actions (copy, flag)
- Accessibility: table semantics, keyboard navigation, row focus state.

## Modals (Translate, Export)
- Props: `{ title: string, isOpen: boolean, onClose: ()=>void }`
- Accessibility: trap focus while open, restore focus to triggering element on close, provide `aria-modal='true'`.

## Banners
- Types: `info`, `warning`, `error`
- Props: `{ message: string, actionLabel?: string, action?: ()=>void }`

---

Use these specs with the `figma_components.csv` and `tokens.json` to import components and tokens into Figma and hand off to engineering.
