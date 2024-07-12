function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(2))

    -- Ejemplo usando buscador de Amazon
    -- NOTA: Splash sólo acepta selectores CSS!! (no XPath)
    input_box = assert(splash:select("#twotabsearchtextbox"))
    input_box:focus()
    input_box:send_text("books")  -- escribe "books" en la caja de texto
    assert(splash:wait(2))
    button = assert(splash:select("#nav-search-submit-button"))
    button:mouse_click()
    assert(splash:wait(5))

    return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
    }
end
