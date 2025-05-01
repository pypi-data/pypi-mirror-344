# CSS 选择器总结

以下是从项目中读取的 CSS 文件中提取的去重后的选择器列表：

```
html
code
.font-secondary
math
.hljs
input::placeholder
textarea::placeholder
.input-prose
.input-prose-sm
.markdown-prose
.markdown-prose-xs
.markdown a
.font-primary
.drag-region
.drag-region a, .drag-region button
.no-drag-region
li p
::-webkit-scrollbar-thumb
.dark ::-webkit-scrollbar-thumb
::-webkit-scrollbar
::-webkit-scrollbar-track
select
.shimmer
:global(.dark) .shimmer
.status-description
.katex-mathml
.scrollbar-hidden:active::-webkit-scrollbar-thumb, .scrollbar-hidden:focus::-webkit-scrollbar-thumb, .scrollbar-hidden:hover::-webkit-scrollbar-thumb
.scrollbar-hidden::-webkit-scrollbar-thumb
.scrollbar-hidden::-webkit-scrollbar-corner
.scrollbar-none::-webkit-scrollbar
.scrollbar-none::-webkit-scrollbar-corner
.scrollbar-none
input::-webkit-outer-spin-button, input::-webkit-inner-spin-button
input[type='number']
.katex-display
.katex-display::-webkit-scrollbar
.katex-display:active::-webkit-scrollbar-thumb, .katex-display:focus::-webkit-scrollbar-thumb, .katex-display:hover::-webkit-scrollbar-thumb
.katex-display::-webkit-scrollbar-thumb
.katex-display::-webkit-scrollbar-corner
.cm-editor
.cm-scroller:active::-webkit-scrollbar-thumb, .cm-scroller:focus::-webkit-scrollbar-thumb, .cm-scroller:hover::-webkit-scrollbar-thumb
.cm-scroller::-webkit-scrollbar-thumb
.cm-scroller::-webkit-scrollbar-corner
.cm-editor.cm-focused
.tippy-box[data-theme~='dark']
.password
.codespan
.svelte-flow
.svelte-flow__edge > path
.svelte-flow__edge.animated > path
.bg-gray-950-90
.ProseMirror
.ProseMirror:focus
.ProseMirror p.is-editor-empty:first-child::before
.ai-autocompletion::after
.tiptap > pre > code
.tiptap > pre
.tiptap p code
.hljs-comment, .hljs-quote
.hljs-variable, .hljs-template-variable, .hljs-attribute, .hljs-tag, .hljs-regexp, .hljs-link, .hljs-name, .hljs-selector-id, .hljs-selector-class
.hljs-number, .hljs-meta, .hljs-built_in, .hljs-builtin-name, .hljs-literal, .hljs-type, .hljs-params
.hljs-string, .hljs-symbol, .hljs-bullet
.hljs-title, .hljs-section
.hljs-keyword, .hljs-selector-tag
.hljs-emphasis
.hljs-strong
.language-javascript, [class*="language-"]
.dark .language-javascript, .dark [class*="language-"]
.sticky.top-8
.dark .sticky.top-8
.text-text-300
.dark .text-text-300
.save-code-button, .copy-code-button, .run-code-button
.dark .save-code-button, .dark .copy-code-button, .dark .run-code-button
.save-code-button:hover, .copy-code-button:hover
.dark .save-code-button:hover, .dark .copy-code-button:hover
.language-javascript::before, [class*="language-"]::before
.dakr .language-javascript::before, .dakr [class*="language-"]::before
.cm-content
.dark .cm-content
.cm-line .ͼb
.dark .cm-line .ͼb
.cm-line .ͼd
.dakr .cm-line .ͼd
.cm-line .ͼe
.dakr .cm-line .ͼe
.cm-line .ͼg
.dakr .cm-line .ͼg
.cm-comment
.cm-property
cm-tag
.cm-attribute
.cm-string
.cm-operator
span.ͼc
span.ͼl
span.ͼt
span.ͼr
span.ͼf
span.ͼm
span.ͼw
.cm-scroller::-webkit-scrollbar
.dark .cm-scroller::-webkit-scrollbar
.cm-scroller::-webkit-scrollbar-track
.dark .cm-scroller::-webkit-scrollbar-track
.cm-scroller::-webkit-scrollbar-thumb
.dark .cm-scroller::-webkit-scrollbar-thumb
.cm-gutters
.dark .cm-gutters
.cm-activeLine
.cm-gutterElement.cm-activeLineGutter
.dark .cm-gutterElement.cm-activeLineGutter
.cm-selectionBackground, .cm-content ::selection
.cm-line.cm-selected
.cm-content ::selection
.dark .cm-content ::selection
.cm-selectionMatch
.cm-selectionLayer > .cm-selectionBackground
#collapsed > .cm-scroller, #expanded > .cm-scroller
.cm-editor#collapsed
.code-expand-btn
.dark .code-expand-btn
.code-expand-btn:hover
.dark .code-expand-btn:hover
.code-expand-btn:active
.code-expand-btn::before
.code-expand-btn#expanded::before
.code-expand-btn::after
.code-expand-btn#expanded::after
.cm-editor#collapsed::after
.dark .cm-editor#collapsed::after
div.flex.items-center.gap-0\.5 button.flex.gap-1.items-center:not(.run-code-button)
.markdown-edit-btn
html.dark .markdown-edit-btn
.markdown-edit-btn:hover
html.dark .markdown-edit-btn:hover
#markdown-editor-modal
@media (prefers-color-scheme: dark) { #markdown-editor-modal
#markdown-editor-modal.active
.editor-container
@media (prefers-color-scheme: dark) { .editor-container
#markdown-editor-modal.active .editor-container
.editor-header
@media (prefers-color-scheme: dark) { .editor-header
.editor-title
@media (prefers-color-scheme: dark) { .editor-title
.close-btn
@media (prefers-color-scheme: dark) { .close-btn
.close-btn:hover
@media (prefers-color-scheme: dark) { .close-btn:hover
.editor-body
.editor-input, .preview-pane
.editor-input
@media (prefers-color-scheme: dark) { .editor-input
.preview-pane
@media (prefers-color-scheme: dark) { .preview-pane
.markdown-preview
@media (prefers-color-scheme: dark) { .markdown-preview
.editor-footer
@media (prefers-color-scheme: dark) { .editor-footer
.apply-btn
@media (prefers-color-scheme: dark) { .apply-btn
.apply-btn:hover
@media (prefers-color-scheme: dark) { .apply-btn:hover
.markdown-preview h1, .markdown-preview h2, .markdown-preview h3, .markdown-preview h4, .markdown-preview h5, .markdown-preview h6
@media (prefers-color-scheme: dark) { .markdown-preview h1, .markdown-preview h2, .markdown-preview h3, .markdown-preview h4, .markdown-preview h5, .markdown-preview h6
.markdown-preview h1
.markdown-preview h2
.markdown-preview h3
.markdown-preview h4
.markdown-preview h5
.markdown-preview h6
@media (prefers-color-scheme: dark) { .markdown-preview h1, .markdown-preview h2
@media (prefers-color-scheme: dark) { .markdown-preview h6
.markdown-preview p, .markdown-preview ul, .markdown-preview ol, .markdown-preview blockquote, .markdown-preview pre, .markdown-preview table
.markdown-preview ul, .markdown-preview ol
.markdown-preview code
@media (prefers-color-scheme: dark) { .markdown-preview code
.markdown-preview pre
@media (prefers-color-scheme: dark) { .markdown-preview pre
.markdown-preview pre code
.markdown-preview blockquote
@media (prefers-color-scheme: dark) { .markdown-preview blockquote
.markdown-preview img
.markdown-preview table
.markdown-preview table th, .markdown-preview table td
@media (prefers-color-scheme: dark) { .markdown-preview table th, .markdown-preview table td
.markdown-preview table th
.markdown-preview table tr
@media (prefers-color-scheme: dark) { .markdown-preview table tr
.markdown-preview table tr:nth-child(2n)
@media (prefers-color-scheme: dark) { .markdown-preview table tr:nth-child(2n)
*
@media (prefers-color-scheme: dark) { *
.hljs-comment, .hljs-quote
.hljs-doctag, .hljs-keyword, .hljs-formula
.hljs-section, .hljs-name, .hljs-selector-tag, .hljs-deletion, .hljs-subst
.hljs-literal
.hljs-string, .hljs-regexp, .hljs-addition, .hljs-attribute, .hljs-meta-string
.hljs-built_in, .hljs-class .hljs-title
.hljs-attr, .hljs-variable, .hljs-template-variable, .hljs-type, .hljs-selector-class, .hljs-selector-attr, .hljs-selector-pseudo, .hljs-number
.hljs-symbol, .hljs-bullet, .hljs-link, .hljs-meta, .hljs-selector-id, .hljs-title
.hljs-emphasis
.hljs-strong
.hljs-link
@media (prefers-color-scheme: dark) { .hljs
@media (prefers-color-scheme: dark) { .hljs-comment, .hljs-quote
@media (prefers-color-scheme: dark) { .hljs-doctag, .hljs-keyword, .hljs-formula
@media (prefers-color-scheme: dark) { .hljs-section, .hljs-name, .hljs-selector-tag, .hljs-deletion, .hljs-subst
@media (prefers-color-scheme: dark) { .hljs-literal
@media (prefers-color-scheme: dark) { .hljs-string, .hljs-regexp, .hljs-addition, .hljs-attribute, .hljs-meta-string
@media (prefers-color-scheme: dark) { .hljs-built_in, .hljs-class .hljs-title
@media (prefers-color-scheme: dark) { .hljs-attr, .hljs-variable, .hljs-template-variable, .hljs-type, .hljs-selector-class, .hljs-selector-attr, .hljs-selector-pseudo, .hljs-number
@media (prefers-color-scheme: dark) { .hljs-symbol, .hljs-bullet, .hljs-link, .hljs-meta, .hljs-selector-id, .hljs-title
@media (prefers-color-scheme: dark) { .hljs-emphasis
@media (prefers-color-scheme: dark) { .hljs-strong
@media (prefers-color-scheme: dark) { .hljs-link
#light-code-theme, #dark-code-theme
:root
.dark body
.dark *
.dark #nav
.dark .message.user
.dark .message.assistant
.dark input, .dark textarea, .dark select
.dark button
.dark button:hover
.dark input[type='checkbox']
.dark input[type='checkbox']:checked
.dark input[type='checkbox']:checked::before
.dark input[type='checkbox']:focus
.dark input[type='checkbox']:disabled
.dark input[type='checkbox']:disabled:checked::before
.blue
.blue *
.blue .app > *
.blue #nav, .blue .py-2\.5.my-auto.flex.flex-col.justify-between.h-screen
.blue .bg-white.dark\:bg-gray-800
.blue #chat-input
.blue .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
.blue .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900.shadow-3xl
.blue .base.enter.svelte-ug60r4
.blue .text-white.bg-gray-100.dark\:text-gray-800.dark\:bg-gray-600.disabled.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.blue .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.blue .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center:hover
.blue .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100.transition.rounded
.blue .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100.transition.rounded:hover
.blue .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
.blue .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
.blue .w-full.flex.justify-between.rounded-md.px-3.py-2.hover\:bg-gray-900.bg-gray-900.transition.whitespace-nowrap.text-ellipsis
.blue .hover\:bg-gray-900:hover
.blue .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
.blue #dropdownDots
.blue .flex.py-2\.5.px-3\.5.w-full.hover\:bg-gray-800.transition:hover
.blue .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.resize-none
.blue .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.svelte-1vx7r9s
.blue #chat-search > *
.blue .w-4.h-4
.blue .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center > *
.blue .scrollbar-hidden.relative.overflow-x-auto.whitespace-nowrap.svelte-3g4avz
.blue .message.svelte-1nauejd
.blue .svelte-1ee93ns
.blue .svelte-11kvm4p
html.dark .blue
html.dark .blue .bg-white.dark\:bg-gray-800
html.dark .blue .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
html.dark .blue .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900.shadow-3xl
html.dark .blue .text-white.bg-gray-100.dark\:text-gray-800.dark\:bg-gray-600.disabled.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
html.dark .blue .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center:hover
html.dark .blue .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
html.dark .blue .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
html.dark .blue .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
html.dark .blue .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.resize-none
html.dark .blue .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.svelte-1vx7r9s
.green
.green *
.green .app > *
.green #nav, .green .py-2\.5.my-auto.flex.flex-col.justify-between.h-screen
.green .bg-white.dark\:bg-gray-800
.green #chat-input
.green .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
.green .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900.shadow-3xl
.green .base.enter.svelte-ug60r4
.green .text-white.bg-gray-100.dark\:text-gray-800.dark\:bg-gray-600.disabled.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.green .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.green .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center:hover
.green .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100.transition.rounded
.green .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100.transition.rounded:hover
.green .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
.green .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
.green .w-full.flex.justify-between.rounded-md.px-3.py-2.hover\:bg-gray-900.bg-gray-900.transition.whitespace-nowrap.text-ellipsis
.green .hover\:bg-gray-900:hover
.green .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
.green #dropdownDots
.green .flex.py-2\.5.px-3\.5.w-full.hover\:bg-gray-800.transition:hover
.green .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.resize-none
.green .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.svelte-1vx7r9s
.green #chat-search > *
.green .w-4.h-4
.green .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center > *
.green .scrollbar-hidden.relative.overflow-x-auto.whitespace-nowrap.svelte-3g4avz
.green .message.svelte-1nauejd
.green .svelte-1ee93ns
.green .svelte-11kvm4p
html.dark .green
html.dark .green .bg-white.dark\:bg-gray-800
html.dark .green .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
html.dark .green .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900.shadow-3xl
html.dark .green .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center:hover
html.dark .green .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
html.dark .green .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
html.dark .green .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
html.dark .green .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.resize-none
html.dark .green .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.svelte-1vx7r9s
.her body
.her *
.her .app > *
.her #nav
.her .py-2\.5.my-auto.flex.flex-col.justify-between.h-screen
.her .bg-white.dark\:bg-gray-800
.her .w-4.h-4
.her #chat-input, .her #chat-input > *, .her #chat-search > *
.her #chat-input::placeholder
.her .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
.her button
.her button:hover
.her .text-white.bg-gray-100.dark\:text-gray-800.dark\:bg-gray-600.disabled
.her .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100
.her .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100:hover
.her .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100
.her .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100:hover
.her .w-full.flex.justify-between.rounded-md.px-3.py-2.hover\:bg-gray-900.bg-gray-900
.her .hover\:bg-gray-900:hover
.her .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
.her .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900
.her .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800, .her .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800
.her select.dark\:bg-gray-900
.her .message.user
.her .message.assistant
.her .message.svelte-1nauejd
.her .message.user .prose
.her .message.assistant .prose
.her .message.assistant code
.her .message.assistant pre
.her #dropdownDots
.her .flex.py-2\.5.px-3\.5.w-full.hover\:bg-gray-800.transition:hover
.her .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
.her .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
.her ::-webkit-scrollbar-thumb
.her ::-webkit-scrollbar-track
.her input[type='range']
.her input[type='checkbox']
.her input[type='checkbox']:checked
.her input[type='checkbox']:checked::before
.her input[type='checkbox']:focus
.her input[type='checkbox']:disabled
.her input[type='checkbox']:disabled:checked::before
.her .svelte-1ee93ns
.her .svelte-11kvm4p
.light body
.light *
.light #nav
.light .message.user
.light .message.assistant
.light input, .light textarea, .light select
.light button
.light button:hover
.light input[type='checkbox']
.light input[type='checkbox']:checked
.light input[type='checkbox']:checked::before
.light input[type='checkbox']:focus
.light input[type='checkbox']:disabled
.light input[type='checkbox']:disabled:checked::before
.oled-dark body
.oled-dark *
.oled-dark #nav
.oled-dark .message.user
.oled-dark .message.assistant
.oled-dark input, .oled-dark textarea, .oled-dark select
.oled-dark button
.oled-dark button:hover
.oled-dark input[type='checkbox']
.oled-dark input[type='checkbox']:checked
.oled-dark input[type='checkbox']:checked::before
.oled-dark input[type='checkbox']:focus
.oled-dark input[type='checkbox']:disabled
.oled-dark input[type='checkbox']:disabled:checked::before
.pink
.pink *
.pink .app > *
.pink #nav, .pink .py-2\.5.my-auto.flex.flex-col.justify-between.h-screen
.pink .bg-white.dark\:bg-gray-800
.pink #chat-input
.pink .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
.pink .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900.shadow-3xl
.pink .base.enter.svelte-ug60r4
.pink .text-white.bg-gray-100.dark\:text-gray-800.dark\:bg-gray-600.disabled.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.pink .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.pink .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center:hover
.pink .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100.transition.rounded
.pink .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100.transition.rounded:hover
.pink .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
.pink .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
.pink .w-full.flex.justify-between.rounded-md.px-3.py-2.hover\:bg-gray-900.bg-gray-900.transition.whitespace-nowrap.text-ellipsis
.pink .hover\:bg-gray-900:hover
.pink .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
.pink #dropdownDots
.pink .flex.py-2\.5.px-3\.5.w-full.hover\:bg-gray-800.transition:hover
.pink .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.resize-none
.pink .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.svelte-1vx7r9s
.pink #chat-search > *
.pink .w-4.h-4
.pink .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center > *
.pink .scrollbar-hidden.relative.overflow-x-auto.whitespace-nowrap.svelte-3g4avz
.pink .message.svelte-1nauejd
.pink .svelte-1ee93ns
.pink .svelte-11kvm4p
html.dark .pink
html.dark .pink .bg-white.dark\:bg-gray-800
html.dark .pink .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
html.dark .pink .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900.shadow-3xl
html.dark .pink .text-white.bg-gray-100.dark\:text-gray-800.dark\:bg-gray-600.disabled.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
html.dark .pink .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center:hover
html.dark .pink .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
html.dark .pink .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
html.dark .pink .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
html.dark .pink .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.resize-none
html.dark .pink .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.svelte-1vx7r9s
.rose-pine *
.rose-pine .app > *
.rose-pine #nav
.rose-pine .py-2\.5.my-auto.flex.flex-col.justify-between.h-screen
.rose-pine .bg-white.dark\:bg-gray-800
.rose-pine .w-4.h-4
.rose-pine #chat-input
.rose-pine .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
.rose-pine .text-white.bg-gray-100.dark\:text-gray-800.dark\:bg-gray-600.disabled.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.rose-pine .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.rose-pine .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center > *
.rose-pine .w-full.flex.justify-between.rounded-md.px-3.py-2.hover\:bg-gray-900.bg-gray-900.transition.whitespace-nowrap.text-ellipsis
.rose-pine .hover\:bg-gray-900:hover
.rose-pine .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
.rose-pine .scrollbar-hidden.relative.overflow-x-auto.whitespace-nowrap.svelte-3g4avz
.rose-pine .base.enter.svelte-ug60r4
.rose-pine .message.svelte-1nauejd
.rose-pine #dropdownDots
.rose-pine .flex.py-2\.5.px-3\.5.w-full.hover\:bg-gray-800.transition:hover
.rose-pine .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900.shadow-3xl
.rose-pine .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.resize-none
.rose-pine .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.svelte-1vx7r9s
.rose-pine .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
.rose-pine .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
.rose-pine .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100.transition.rounded
.rose-pine #chat-search > *
.rose-pine .svelte-1ee93ns
.rose-pine .svelte-11kvm4p
.rose-pine-dawn *
.rose-pine-dawn .app > *
.rose-pine-dawn #nav
.rose-pine-dawn .py-2\.5.my-auto.flex.flex-col.justify-between.h-screen
.rose-pine-dawn .bg-white.dark\:bg-gray-800
.rose-pine-dawn .w-4.h-4
.rose-pine-dawn #chat-input
.rose-pine-dawn .bg-gradient-to-t.from-white.dark\:from-gray-800.from-40\%.pb-2
.rose-pine-dawn .text-white.bg-gray-100.dark\:text-gray-800.dark\:bg-gray-600.disabled.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.rose-pine-dawn .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center
.rose-pine-dawn .bg-black.text-white.hover\:bg-gray-900.dark\:bg-white.dark\:text-black.dark\:hover\:bg-gray-100.transition.rounded-lg.p-1.mr-0\.5.w-7.h-7.self-center > *
.rose-pine-dawn .w-full.flex.justify-between.rounded-md.px-3.py-2.hover\:bg-gray-900.bg-gray-900.transition.whitespace-nowrap.text-ellipsis
.rose-pine-dawn .hover\:bg-gray-900:hover
.rose-pine-dawn .text-xs.text-gray-700.uppercase.bg-gray-50.dark\:bg-gray-700.dark\:text-gray-400
.rose-pine-dawn .scrollbar-hidden.relative.overflow-x-auto.whitespace-nowrap.svelte-3g4avz
.rose-pine-dawn .base.enter.svelte-ug60r4
.rose-pine-dawn .message.svelte-1nauejd
.rose-pine-dawn #dropdownDots
.rose-pine-dawn .flex.py-2\.5.px-3\.5.w-full.hover\:bg-gray-800.transition:hover
.rose-pine-dawn .m-auto.rounded-xl.max-w-full.w-\[40rem\].mx-2.bg-gray-50.dark\:bg-gray-900.shadow-3xl
.rose-pine-dawn .w-full.rounded.p-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.resize-none
.rose-pine-dawn .w-full.rounded.py-2.px-4.text-sm.dark\:text-gray-300.dark\:bg-gray-800.outline-none.svelte-1vx7r9s
.rose-pine-dawn .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.bg-gray-200.dark\:bg-gray-700
.rose-pine-dawn .px-2\.5.py-2\.5.min-w-fit.rounded-lg.flex-1.md\:flex-none.flex.text-right.transition.hover\:bg-gray-300.dark\:hover\:bg-gray-800:hover
.rose-pine-dawn .px-4.py-2.bg-emerald-600.hover\:bg-emerald-700.text-gray-100.transition.rounded
.rose-pine-dawn #chat-search > *
.rose-pine-dawn .svelte-1ee93ns
.rose-pine-dawn .svelte-11kvm4p
.system input[type='checkbox']
.system input[type='checkbox']:checked
.system input[type='checkbox']:checked::before
.system input[type='checkbox']:focus
.system input[type='checkbox']:disabled
.system input[type='checkbox']:disabled:checked::before
@media (prefers-color-scheme: dark) { .system input[type='checkbox']:checked
@media (prefers-color-scheme: dark) { .system input[type='checkbox']:checked::before
@media (prefers-color-scheme: dark) { .system input[type='checkbox']