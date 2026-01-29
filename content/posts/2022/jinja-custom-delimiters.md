---
date: "2022-02-18T10:00:00+05:30"
draft: false
title: "Using Custom Delimiters in Jinja Templates"
description:
  "How to use custom variable markers in Jinja templates to avoid conflicts with
  Apache Airflow or other template engines. Alternative approaches for nested
  templating scenarios."
tags:
  - "python"
  - "jinja"
  - "airflow"
  - "templates"
---

Apache Airflow uses Jinja templates for variable expansion and templating.
Whenever you write a DAG, you can use `{{ }}` blocks to expand variable names,
often using Airflow configurations or _macros_ to fill in the values. While that
is great, you get a problem when you have Jinja templates inside your code that
has nothing to do with Airflow.

At those times, you should probably note that Jinja supports _custom_ variable
start and stop markers.

## Standard Jinja Syntax

```python
template_string = """Select * from {{bigquery_project}}.{{bigquery_dataset}}.{{bigquery_table}}"""
template = jinja2.Template(template_string)
rendered_string = template.render(
   bigquery_project="my_gcp_project",
   bigquery_dataset="my_gcp_dataset",
   bigquery_table="my_gcp_table"
)
```

This uses the normal markers that Jinja uses, just like many other templating
languages. However, you might want to use other markers if you're using this
code block within the context of an Airflow DAG.

## Custom Delimiters

Then, you'd use:

```python
template_string = """Select * from [[bigquery_project]].[[bigquery_dataset]].[[bigquery_table]]"""
template = jinja2.Template(template_string, variable_start_string="[[", variable_end_string="]]")
rendered_string = template.render(
   bigquery_project="my_gcp_project",
   bigquery_dataset="my_gcp_dataset",
   bigquery_table="my_gcp_table"
)
```

If you'd like to know more about this, you should look at the
[official Jinja2 documentation on the Template class](https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Template).

{{< note >}} You can use these to override the need to implement your own hacks
for nested template variables. This will even help with Flask or Django
templates. Note that you probably shouldn't implement too much of your logic
within a template, but it is useful to know that this exists. {{< /note >}}

{{< warning >}} Another way of doing this is to use
[jinja2.Undefined](https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.DebugUndefined)
so that `Template.Render` ignores your undefined values, so that the values can
be filled in later.

While this _works_, you shouldn't use something that's implemented in order to
help you debug code, and you should instead use the provided APIs to do this.
{{< /warning >}}
