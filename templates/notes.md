# Release notes for {{ project_name }} {{ release }}
## Statistics since {{ last_release }}
 - {{ num_commits }} commits
 - {{ stats }}

## Authors
{% for author in authors %}
 - {{ author }}
{% endfor %}

## Merge History
{% for merge in merges %}
{{ merge }}
{% endfor %}
