#include <{{ header }}>

{{ class_name }}::{{ class_name }}(QObject* parent)
    : QObject(parent) {
}

{% for property in properties %}
{{ property.type }} {{ class_name }}::{{ property.name }}() const {
    return {{ property.var_name }};
}

void {{ class_name }}::{{ property.setter_name }}({{ property.arg_type }} value) {
    if ({{ property.var_name }} == value) {
        return;
    }
    {{ property.var_name }} = value;
    {{ property.name }}Changed(value);
}
{% endfor %}