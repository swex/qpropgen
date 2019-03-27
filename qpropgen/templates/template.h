// {{ autogenerated_disclaimer }}
{% set include_guard = header.replace('.', '_').upper() %}
#ifndef {{ include_guard }}
#define {{ include_guard }}

#include <QObject>

{%- for include in includes %}
#include <{{include}}>
{%- endfor %}

{%- if namespace %}
namespace {{namespace}} {
{%- endif %}

{%- for declaration in forward_declarations %}
class {{declaration}};
{%- endfor %}




class {{ className }} : public {{ baseClassName }} {
    Q_OBJECT
{% for property in properties %}
    Q_PROPERTY({{ property.type }} {{ property.name }} READ {{ property.name }}
    {%- if property.mutability == 'readwrite' %}
            WRITE {{ property.setterName }}
    {%- endif %}
    {%- if property.mutability == 'constant' %}
            CONSTANT
    {%- else %}
            NOTIFY {{ property.name}}Changed
    {%- endif %}
    )
    {%- if property.db|length > 0 %}
    Q_CLASSINFO("{{ property.name }}", "{% for option in property.db %}{{option if option is not none else "null"|string}}={{property.db[option]|string|lower}} {%- if not loop.last %} {% else %}"{% endif %}{% endfor %})
    {%- endif %}
{% endfor %}
public:
    explicit {{ className }}(QObject* parent = nullptr);

{% for property in properties %}
    {{ property.declaration_prefix }} {{ property.type }} {{ property.name }}() const {{- property.declaration_suffix }};
    {%- if property.mutability == 'readwrite' %}
    {{ property.declaration_prefix }} void {{property.setterName }}({{ property.argType }} value) {{- property.declaration_suffix }};
    {%- endif %}
{% endfor %}

signals:
{% for property in properties if property.mutability != 'constant' %}
    void {{property.name }}Changed({{ property.argType }} {{ property.name }});
{% endfor %}

{%- for group in properties|groupby('access') %}
{{ group.grouper }}:
    {%- for property in group.list %}
    {% if property.fk == True and baseClassName == 'QDjangoModel' %}{%else%}{{ property.type }} {{ property.varName }}{% if property.value is defined %} = {{ property.value }}{% endif %};
    {% endif %}
    {%- endfor %}
{%- endfor %}
};
{%- if namespace %}
} //namespace {{namespace}}
{%- endif %}
#endif // {{ include_guard }}

