# -*- coding: utf-8 -*-
import yaml

p = '.github/workflows/test-dispatcher.yml'
s = open(p, encoding='utf-8').read()
old = 'run-name: "Test Dispatcher · ${{ github.sha }}"'
new = (
    'run-name: >-\n'
    '  Test Dispatcher · ${{ github.event.client_payload.source_repository || github.event.inputs.source_repository || github.repository }}\n'
    '  · ${{ github.event.client_payload.pr_number != \'\' && format(\'PR #{0}\', github.event.client_payload.pr_number)\n'
    '       || github.event.client_payload.branch || github.event.inputs.branch || \'\' }}\n'
    '  · ref ${{ github.event.client_payload.ref || github.event.inputs.ref || github.sha }}\n'
    '  · ${{ github.event.client_payload.trigger || github.event.inputs.trigger || github.event.action }}'
)
assert old in s, 'run-name anchor'
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
yaml.safe_load(s)
print('test-dispatcher: run-name expanded')
