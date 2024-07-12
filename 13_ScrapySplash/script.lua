-- Página a usar: https://www.adamchoi.co.uk/overs/detailed

function main(splash, args)
    splash.private_mode_enabled = false

    assert(splash:go(args.url))
    assert(splash:wait(3))

    -- Frank usa simplemente el selector CSS 'label.btn.btn-sm.btn-primary'
    all_matches = splash:select_all("label.btn.btn-sm.btn-primary.ng-pristine.ng-untouched.ng-valid.ng-not-empty")
    all_matches[2]:mouse_click()  -- la indexación en Lua comienza en 1
    assert(splash:wait(3))
    splash:set_viewport_full()

    return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
    }
end
