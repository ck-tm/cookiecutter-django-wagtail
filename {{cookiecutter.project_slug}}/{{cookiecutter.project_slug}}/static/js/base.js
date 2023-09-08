{%- if cookiecutter.frontend_pipeline == 'Webpack' %}
import '../scss/base.scss'
{%- endif %}

/* Project specific Javascript goes here. */

class CAPP {
  constructor() {
  }
}

export const APP = new CAPP()
