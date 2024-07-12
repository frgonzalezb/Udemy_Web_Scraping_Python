-- Página a usar: https://www.adamchoi.co.uk/overs/detailed

function main(splash, args)
    -- splash:user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    headers = {
        ["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    splash:set_custom_headers(headers)
    
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
