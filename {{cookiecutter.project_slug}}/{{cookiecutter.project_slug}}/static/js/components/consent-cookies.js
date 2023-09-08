export class ConsentCookies {
  init(options) {
    document.addEventListener('DOMContentLoaded', () => {
      this.showCookieBar(options)
    })
  }

  showCookieBar(options) {
    const defaults = {
      notification: document.querySelector(
        '#notification-container .is-consent'
      ),
      cookieGroups: [],
      cookieDecline: null, // set cookie_consent decline on client immediately
      beforeDeclined: null,
    }

    const opts = Object.assign(defaults, options)
    // console.log(opts)

    document
      .querySelector('.cc-cookie-accept')
      .addEventListener('click', (e) => {
        e.preventDefault()
        fetch(e.target.getAttribute('href'), { method: 'POST' }).then(() => {
          const scripts = document.querySelectorAll(
            "script[type='x/cookie_consent']"
          )
          opts.notification.classList.add('is-hidden')

          scripts.forEach((script) => {
            if (
              opts.cookieGroups.indexOf(script.getAttribute('data-varname')) !==
              -1
            ) {
              this.evalXCookieConsent(script)
            }
          })
        })
      })

    document
      .querySelector('.cc-cookie-decline')
      .addEventListener('click', (e) => {
        e.preventDefault()
        if (typeof opts.declined === 'function') {
          opts.declined()
        }
        fetch(e.target.getAttribute('href'), { method: 'POST' }).then(() => {
          opts.notification.classList.add('is-hidden')
          if (opts.cookieDecline) {
            document.cookie = opts.cookieDecline
          }
        })
      })
  }

  evalXCookieConsent(script) {
    const src = script.getAttribute('src')
    if (src) {
      const newScript = document.createElement('script')
      newScript.src = src
      document.getElementsByTagName('head')[0].appendChild(newScript)
    } else {
      eval(script.innerHTML)
    }

    script.remove()
  }
}
